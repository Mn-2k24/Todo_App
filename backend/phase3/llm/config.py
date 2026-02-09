"""
Gemini LLM Configuration

Centralizes all configuration for Google Gemini Flash 2.5 integration:
- API key management
- Model selection
- Generation parameters (temperature, top_p, top_k, max_tokens)
- Safety settings
"""

from typing import Optional

from google.genai import types

# Use FastAPI settings system instead of reading env vars directly
from src.config import get_settings

# Model configuration
GEMINI_MODEL = "gemini-2.5-flash"  # Gemini Flash 2.5 (latest fast model)

# Generation parameters optimized for task management assistant
# These values balance creativity with determinism for reliable tool calling
GENERATION_CONFIG = types.GenerateContentConfig(
    temperature=0.3,  # Low temperature for more deterministic responses
    top_p=0.9,  # Nucleus sampling threshold
    top_k=40,  # Top-k sampling limit
    max_output_tokens=1024,  # Maximum response length
    candidate_count=1,  # Only generate one response candidate
)

# Safety settings - block medium and above harmful content
# This ensures the assistant stays professional and safe
SAFETY_SETTINGS = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
]


def get_gemini_api_key() -> str:
    """
    Retrieve Gemini API key from FastAPI settings.

    Returns:
        API key string

    Note:
        API key is loaded from .env file via FastAPI settings system.
        Get your API key from https://aistudio.google.com/apikey
    """
    settings = get_settings()
    return settings.gemini_api_key


def get_generation_config(
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None,
    max_output_tokens: Optional[int] = None,
) -> types.GenerateContentConfig:
    """
    Get generation config with optional overrides.

    Args:
        temperature: Override default temperature (0.0-2.0)
        top_p: Override default top_p (0.0-1.0)
        top_k: Override default top_k (1-100)
        max_output_tokens: Override default max tokens (1-8192)

    Returns:
        GenerateContentConfig with merged settings
    """
    return types.GenerateContentConfig(
        temperature=temperature if temperature is not None else 0.3,
        top_p=top_p if top_p is not None else 0.9,
        top_k=top_k if top_k is not None else 40,
        max_output_tokens=max_output_tokens if max_output_tokens is not None else 1024,
        candidate_count=1,
    )


# Error handling configuration
MAX_RETRIES = 3  # Maximum retry attempts for rate limit errors
RETRY_DELAY = 2.0  # Initial delay in seconds before retrying (exponential backoff)
REQUEST_TIMEOUT = 30.0  # Timeout for API requests in seconds

# Prompt injection detection patterns (simple keyword-based)
# These patterns help detect attempts to manipulate the system prompt
INJECTION_PATTERNS = [
    "ignore previous",
    "ignore all previous",
    "disregard previous",
    "forget previous",
    "ignore the above",
    "ignore your instructions",
    "new instructions",
    "you are now",
    "your new role",
    "system prompt",
    "ignore system",
    "override system",
]
