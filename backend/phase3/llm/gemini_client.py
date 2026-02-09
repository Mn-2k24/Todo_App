"""
Gemini API Client Wrapper

Handles all interactions with Google Gemini Flash 2.5 API:
- Client initialization and configuration
- Request/response handling
- Error handling and retries
- Rate limit management
"""

import asyncio
import logging
from typing import Optional

from google import genai
from google.api_core import exceptions as google_exceptions
from google.genai import types

from phase3.llm.config import (
    GEMINI_MODEL,
    MAX_RETRIES,
    REQUEST_TIMEOUT,
    RETRY_DELAY,
    SAFETY_SETTINGS,
    get_gemini_api_key,
    get_generation_config,
)
from phase3.llm.system_prompts import get_system_instruction

logger = logging.getLogger(__name__)


class GeminiError(Exception):
    """Base exception for Gemini client errors."""

    pass


class RateLimitError(GeminiError):
    """Raised when API rate limit is exceeded."""

    pass


class ContentPolicyError(GeminiError):
    """Raised when content violates safety policies."""

    pass


class AuthenticationError(GeminiError):
    """Raised when API key is invalid or expired."""

    pass


class TimeoutError(GeminiError):
    """Raised when request times out."""

    pass


class GeminiClient:
    """
    Wrapper for Google Gemini API client.

    Handles API initialization, request execution, error handling, and retries.
    Configured specifically for task management assistant use case.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = GEMINI_MODEL,
        use_mock: bool = False,
    ):
        """
        Initialize Gemini client.

        Args:
            api_key: Gemini API key (uses environment variable if not provided)
            model: Model name to use (default: gemini-2.0-flash-001)
            use_mock: If True, use mock client for testing (default: False)

        Raises:
            ValueError: If API key is missing
            AuthenticationError: If API key is invalid
        """
        if use_mock:
            # For testing - import mock client dynamically to avoid circular imports
            from phase3.llm.tests.mock_gemini import MockGeminiClient

            self._client = MockGeminiClient()
            self.model = model
            logger.info("Initialized MockGeminiClient for testing")
        else:
            try:
                api_key = api_key or get_gemini_api_key()
                self._client = genai.Client(api_key=api_key)
                self.model = model
                logger.info(f"Initialized Gemini client with model: {model}")
            except ValueError as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                raise

    async def generate_content(
        self,
        conversation_history: list[types.Content],
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None,
        max_retries: int = MAX_RETRIES,
    ) -> str:
        """
        Generate content using Gemini API with conversation history.

        Args:
            conversation_history: List of Content objects (user/assistant messages)
            system_instruction: Override default system instruction
            temperature: Override default temperature
            max_retries: Maximum retry attempts for rate limits

        Returns:
            Generated text response

        Raises:
            RateLimitError: If rate limit exceeded after retries
            ContentPolicyError: If content violates safety policies
            AuthenticationError: If API authentication fails
            TimeoutError: If request times out
            GeminiError: For other API errors
        """
        system_inst = system_instruction or get_system_instruction()

        # Build generation config with safety settings
        config = get_generation_config(temperature=temperature)
        config.safety_settings = SAFETY_SETTINGS
        config.system_instruction = system_inst

        retry_count = 0
        last_error = None

        while retry_count <= max_retries:
            try:
                # Execute API call with timeout
                response = await asyncio.wait_for(
                    self._call_api(conversation_history, config),
                    timeout=REQUEST_TIMEOUT,
                )

                # Extract text from response
                if response.text:
                    logger.info(f"Generated response: {len(response.text)} characters")
                    return response.text
                else:
                    # Check if response was blocked by safety filters
                    if hasattr(response, "prompt_feedback") and response.prompt_feedback:
                        logger.warning(
                            f"Content blocked by safety filters: {response.prompt_feedback}"
                        )
                        raise ContentPolicyError(
                            "Response was blocked due to safety policy violations"
                        )
                    raise GeminiError("No text in response")

            except asyncio.TimeoutError:
                logger.error(f"Request timed out after {REQUEST_TIMEOUT}s")
                raise TimeoutError(
                    f"Request timed out after {REQUEST_TIMEOUT} seconds"
                )

            except google_exceptions.ResourceExhausted as e:
                # Rate limit error (429) - retry with exponential backoff
                retry_count += 1
                last_error = e
                if retry_count <= max_retries:
                    delay = RETRY_DELAY * (2 ** (retry_count - 1))  # Exponential backoff
                    logger.warning(
                        f"Rate limit hit (429). Retrying in {delay}s (attempt {retry_count}/{max_retries})"
                    )
                    await asyncio.sleep(delay)
                    continue
                else:
                    logger.error(
                        f"Rate limit exceeded after {max_retries} retries: {e}"
                    )
                    raise RateLimitError(
                        f"API rate limit exceeded. Please try again later."
                    ) from e

            except google_exceptions.InvalidArgument as e:
                # Bad request (400) - likely content policy violation
                logger.error(f"Content policy violation (400): {e}")
                raise ContentPolicyError(
                    "Request violates content policy. Please rephrase your input."
                ) from e

            except (
                google_exceptions.Unauthenticated,
                google_exceptions.PermissionDenied,
            ) as e:
                # Authentication error (401/403)
                logger.critical(f"Authentication failed (401/403): {e}")
                raise AuthenticationError(
                    "API authentication failed. Check your API key."
                ) from e

            except Exception as e:
                # Catch-all for other errors including ClientError
                error_str = str(e)
                logger.error(f"Unexpected error during API call: {type(e).__name__}: {e}")

                # Check if it's a rate limit error (429) from ClientError
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
                    raise RateLimitError(
                        "API quota exceeded. You've reached the free tier limit. Please try again later or upgrade your plan."
                    ) from e

                # Check if it's an authentication error
                if "401" in error_str or "403" in error_str or "UNAUTHENTICATED" in error_str or "PERMISSION_DENIED" in error_str:
                    raise AuthenticationError(
                        "API authentication failed. Check your API key."
                    ) from e

                # Generic error
                raise GeminiError(f"API error: {str(e)}") from e

        # Should never reach here, but just in case
        raise RateLimitError(
            f"Failed after {max_retries} retries: {last_error}"
        )

    async def _call_api(
        self, conversation_history: list[types.Content], config: types.GenerateContentConfig
    ) -> types.GenerateContentResponse:
        """
        Internal method to call Gemini API.

        Args:
            conversation_history: List of Content objects
            config: Generation configuration

        Returns:
            API response object
        """
        # Use sync API but run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self._client.models.generate_content(
                model=self.model,
                contents=conversation_history,
                config=config,
            ),
        )
        return response

    def build_conversation_history(
        self, messages: list[dict[str, str]]
    ) -> list[types.Content]:
        """
        Build conversation history in Gemini format.

        Args:
            messages: List of dicts with 'role' (user|assistant) and 'content' keys

        Returns:
            List of Content objects for Gemini API

        Example:
            messages = [
                {"role": "user", "content": "Add task: buy groceries"},
                {"role": "assistant", "content": "Task added successfully"}
            ]
        """
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role, parts=[types.Part.from_text(text=msg["content"])]
                )
            )
        return contents

    async def generate_with_retry(
        self,
        messages: list[dict[str, str]],
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Convenience method: Generate content from message list with automatic retry.

        Args:
            messages: List of message dicts (role, content)
            system_instruction: Optional system instruction override
            temperature: Optional temperature override

        Returns:
            Generated text response

        Raises:
            Same exceptions as generate_content()
        """
        conversation_history = self.build_conversation_history(messages)
        return await self.generate_content(
            conversation_history=conversation_history,
            system_instruction=system_instruction,
            temperature=temperature,
        )
