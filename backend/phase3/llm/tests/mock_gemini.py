"""
Mock Gemini Client for Testing

Provides deterministic responses for unit and integration tests.
Simulates Gemini API behavior without making actual API calls.
"""

import asyncio
from typing import Optional

from google.genai import types


class MockGenerateContentResponse:
    """
    Mock response object that mimics google.genai response structure.
    """

    def __init__(self, text: str, blocked: bool = False):
        """
        Initialize mock response.

        Args:
            text: Response text
            blocked: Whether response was blocked by safety filters
        """
        self.text = text if not blocked else ""
        self._blocked = blocked

        if blocked:
            self.prompt_feedback = {
                "block_reason": "SAFETY",
                "safety_ratings": [{"category": "HARM_CATEGORY_HATE_SPEECH", "probability": "HIGH"}],
            }


class MockModels:
    """Mock models service with generate_content method."""

    def __init__(self, parent):
        self._parent = parent

    def generate_content(
        self,
        model: str,
        contents: list[types.Content],
        config: types.GenerateContentConfig,
    ) -> MockGenerateContentResponse:
        """
        Mock generate_content that returns keyword-based responses.

        Args:
            model: Model name (ignored in mock)
            contents: Conversation history
            config: Generation config (ignored in mock)

        Returns:
            MockGenerateContentResponse with deterministic text
        """
        # Get the last user message
        last_message = ""
        for content in reversed(contents):
            if content.role == "user":
                last_message = content.parts[0].text.lower()
                break

        # Keyword-based response logic
        response_text = self._parent._generate_mock_response(last_message)

        # Check if content should be blocked
        blocked = self._parent._should_block_content(last_message)

        return MockGenerateContentResponse(response_text, blocked=blocked)


class MockGeminiClient:
    """
    Mock Gemini client for deterministic testing.

    Provides keyword-based responses that simulate tool calling behavior.
    """

    def __init__(self):
        """Initialize mock client."""
        self.models = MockModels(self)
        self.call_count = 0
        self.last_request = None

    def _generate_mock_response(self, user_message: str) -> str:
        """
        Generate mock response based on keywords in user message.

        Args:
            user_message: User's message text (lowercased)

        Returns:
            Mock response text with simulated tool calls
        """
        self.call_count += 1
        self.last_request = user_message

        # Simulate rate limit on 4th call
        if self.call_count == 4:
            from google.api_core import exceptions as google_exceptions

            raise google_exceptions.ResourceExhausted("Rate limit exceeded")

        # Create task patterns
        if any(
            keyword in user_message
            for keyword in ["add", "create", "new task", "remind me"]
        ):
            # Extract task title
            title = self._extract_task_title(user_message)
            priority = self._extract_priority(user_message)
            return (
                f"I'll add that task for you. "
                f"add_task(user_id='mock-user', title='{title}', priority='{priority}')"
            )

        # List tasks patterns
        if any(
            keyword in user_message for keyword in ["show", "list", "display", "what"]
        ):
            status_filter = "pending" if "pending" in user_message else "all"
            return (
                f"Here are your tasks. "
                f"list_tasks(user_id='mock-user', status='{status_filter}')"
            )

        # Update task patterns
        if any(keyword in user_message for keyword in ["update", "change", "modify"]):
            return (
                f"I'll update that task. "
                f"update_task(user_id='mock-user', task_id='mock-task-id', "
                f"title='Updated task', priority='high')"
            )

        # Complete task patterns
        if any(
            keyword in user_message for keyword in ["complete", "done", "finish", "mark"]
        ):
            return (
                f"Marking the task as completed. "
                f"complete_task(user_id='mock-user', task_id='mock-task-id')"
            )

        # Delete task patterns
        if any(keyword in user_message for keyword in ["delete", "remove", "cancel"]):
            return (
                f"Are you sure you want to delete this task? "
                f"delete_task(user_id='mock-user', task_id='mock-task-id')"
            )

        # Clarification patterns
        if "which" in user_message or "?" in user_message:
            return "Could you please clarify which task you're referring to?"

        # Out of scope patterns
        if any(
            keyword in user_message
            for keyword in ["weather", "joke", "story", "game"]
        ):
            return (
                "I'm a task management assistant and can only help with "
                "creating, viewing, updating, completing, and deleting tasks."
            )

        # Default response
        return "I can help you manage your tasks. What would you like to do?"

    def _extract_task_title(self, message: str) -> str:
        """
        Extract task title from user message.

        Args:
            message: User message (lowercased)

        Returns:
            Extracted title or default
        """
        # Simple heuristic: take text after action keywords
        for keyword in ["add", "create", "remind me to", "new task"]:
            if keyword in message:
                parts = message.split(keyword, 1)
                if len(parts) > 1:
                    title = parts[1].strip()
                    # Remove "task:" prefix if present
                    title = title.replace("task:", "").strip()
                    # Remove "to" prefix if present
                    if title.startswith("to "):
                        title = title[3:].strip()
                    return title if title else "Untitled task"

        return "Untitled task"

    def _extract_priority(self, message: str) -> str:
        """
        Extract priority from user message.

        Args:
            message: User message (lowercased)

        Returns:
            Priority level (low/medium/high)
        """
        if any(
            keyword in message for keyword in ["urgent", "important", "asap", "high"]
        ):
            return "high"
        if any(keyword in message for keyword in ["low", "sometime", "eventually"]):
            return "low"
        return "medium"

    def _should_block_content(self, message: str) -> bool:
        """
        Simulate safety filter blocking.

        Args:
            message: User message (lowercased)

        Returns:
            True if content should be blocked
        """
        # Simulate blocking for obviously harmful content
        blocked_keywords = ["violence", "hate", "explicit", "harmful"]
        return any(keyword in message for keyword in blocked_keywords)

    def reset_call_count(self):
        """Reset call counter for testing."""
        self.call_count = 0
        self.last_request = None


# Async wrapper for MockGeminiClient to match real client interface
class AsyncMockGeminiClient:
    """
    Async wrapper for mock Gemini client.

    Provides the same async interface as the real GeminiClient.
    """

    def __init__(self):
        """Initialize async mock client."""
        self._sync_client = MockGeminiClient()

    async def generate_content(
        self,
        conversation_history: list[types.Content],
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None,
        max_retries: int = 3,
    ) -> str:
        """
        Mock async generate_content.

        Args:
            conversation_history: List of Content objects
            system_instruction: System instruction (ignored in mock)
            temperature: Temperature (ignored in mock)
            max_retries: Max retries (used for rate limit simulation)

        Returns:
            Generated text response
        """
        # Simulate small async delay
        await asyncio.sleep(0.01)

        # Call sync mock
        response = self._sync_client.models.generate_content(
            model="mock-model",
            contents=conversation_history,
            config=types.GenerateContentConfig(),
        )

        return response.text

    def build_conversation_history(
        self, messages: list[dict[str, str]]
    ) -> list[types.Content]:
        """
        Build conversation history (same as real client).

        Args:
            messages: List of message dicts

        Returns:
            List of Content objects
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
        Mock generate with retry (same as real client).

        Args:
            messages: List of message dicts
            system_instruction: System instruction (ignored)
            temperature: Temperature (ignored)

        Returns:
            Generated text response
        """
        conversation_history = self.build_conversation_history(messages)
        return await self.generate_content(conversation_history)

    def reset_call_count(self):
        """Reset call counter for testing."""
        self._sync_client.reset_call_count()

    @property
    def call_count(self) -> int:
        """Get number of API calls made."""
        return self._sync_client.call_count

    @property
    def last_request(self) -> Optional[str]:
        """Get last request message."""
        return self._sync_client.last_request
