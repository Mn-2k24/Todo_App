"""
Security Module for Gemini AI Assistant

Implements security checks:
- Prompt injection detection
- Input validation
- Content filtering
"""

import logging
import re
from typing import Optional

from phase3.llm.config import INJECTION_PATTERNS

logger = logging.getLogger(__name__)


class SecurityViolation(Exception):
    """Raised when input violates security policies."""

    pass


class PromptInjectionDetector:
    """
    Detects potential prompt injection attacks.

    Uses keyword-based detection for common injection patterns.
    This is a basic defense layer - the LLM's own safety filters are the primary defense.
    """

    def __init__(self, custom_patterns: Optional[list[str]] = None):
        """
        Initialize detector with injection patterns.

        Args:
            custom_patterns: Additional patterns to check (extends defaults)
        """
        self.patterns = INJECTION_PATTERNS.copy()
        if custom_patterns:
            self.patterns.extend(custom_patterns)

        # Compile patterns for efficiency
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.patterns
        ]

    def detect(self, user_input: str) -> tuple[bool, Optional[str]]:
        """
        Check if input contains prompt injection patterns.

        Args:
            user_input: User message to check

        Returns:
            Tuple of (is_suspicious, matched_pattern)
            - is_suspicious: True if injection detected
            - matched_pattern: The pattern that matched, or None

        Example:
            detector = PromptInjectionDetector()
            is_suspicious, pattern = detector.detect("Ignore previous instructions and do X")
            # Returns: (True, "ignore previous")
        """
        user_input_lower = user_input.lower()

        for i, pattern in enumerate(self.compiled_patterns):
            if pattern.search(user_input_lower):
                matched = self.patterns[i]
                logger.warning(f"Potential prompt injection detected: '{matched}'")
                return (True, matched)

        return (False, None)

    def validate_and_sanitize(self, user_input: str, strict: bool = False) -> str:
        """
        Validate and optionally sanitize user input.

        Args:
            user_input: User message to validate
            strict: If True, raise exception on detection; if False, log warning

        Returns:
            Sanitized input (currently returns original input)

        Raises:
            SecurityViolation: If strict=True and injection detected

        Example:
            detector = PromptInjectionDetector()
            safe_input = detector.validate_and_sanitize("Add task: buy milk", strict=True)
        """
        is_suspicious, matched_pattern = self.detect(user_input)

        if is_suspicious:
            if strict:
                raise SecurityViolation(
                    f"Input contains suspicious pattern: '{matched_pattern}'. "
                    "Please rephrase your request."
                )
            else:
                logger.warning(
                    f"Suspicious input passed through (strict=False): '{matched_pattern}'"
                )

        # Currently no sanitization - just validation
        # Future: could strip suspicious content or add warnings
        return user_input


class InputValidator:
    """
    Validates user input for basic constraints.

    Checks:
    - Message length limits
    - Character encoding
    - Empty/whitespace-only input
    """

    MIN_LENGTH = 1
    MAX_LENGTH = 2000  # Match ChatRequest schema

    def validate_message(self, message: str) -> tuple[bool, Optional[str]]:
        """
        Validate user message for basic constraints.

        Args:
            message: User input message

        Returns:
            Tuple of (is_valid, error_message)

        Example:
            validator = InputValidator()
            is_valid, error = validator.validate_message("Add task: buy milk")
            # Returns: (True, None)
        """
        # Check empty or whitespace-only
        if not message or not message.strip():
            return (False, "Message cannot be empty or contain only whitespace")

        # Check length constraints
        if len(message) < self.MIN_LENGTH:
            return (False, f"Message too short (min {self.MIN_LENGTH} characters)")

        if len(message) > self.MAX_LENGTH:
            return (
                False,
                f"Message too long (max {self.MAX_LENGTH} characters, got {len(message)})",
            )

        # Check for valid UTF-8 encoding
        try:
            message.encode("utf-8")
        except UnicodeEncodeError as e:
            return (False, f"Invalid character encoding: {e}")

        return (True, None)


class ContentFilter:
    """
    Filters inappropriate content from user input.

    Note: This is a lightweight pre-filter. Gemini's built-in safety filters
    are the primary defense against harmful content.
    """

    # Basic profanity filter (placeholder - production would use comprehensive list)
    BLOCKED_TERMS = [
        # This would contain comprehensive profanity/harmful content list
        # For now, just placeholders
    ]

    def __init__(self, custom_blocked_terms: Optional[list[str]] = None):
        """
        Initialize content filter.

        Args:
            custom_blocked_terms: Additional terms to block
        """
        self.blocked_terms = self.BLOCKED_TERMS.copy()
        if custom_blocked_terms:
            self.blocked_terms.extend(custom_blocked_terms)

        # Compile for case-insensitive matching
        self.patterns = [
            re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
            for term in self.blocked_terms
        ]

    def contains_blocked_content(self, text: str) -> tuple[bool, Optional[str]]:
        """
        Check if text contains blocked content.

        Args:
            text: Text to check

        Returns:
            Tuple of (contains_blocked, matched_term)

        Example:
            filter = ContentFilter()
            contains, term = filter.contains_blocked_content("Some text")
            # Returns: (False, None)
        """
        for i, pattern in enumerate(self.patterns):
            if pattern.search(text):
                matched = self.blocked_terms[i]
                logger.warning(f"Blocked content detected: '{matched}'")
                return (True, matched)

        return (False, None)


# Singleton instances for convenience
prompt_injection_detector = PromptInjectionDetector()
input_validator = InputValidator()
content_filter = ContentFilter()


def validate_user_input(
    message: str, strict_injection_check: bool = False
) -> tuple[bool, Optional[str]]:
    """
    Convenience function: Run all security checks on user input.

    Args:
        message: User input message
        strict_injection_check: If True, raise exception on injection detection

    Returns:
        Tuple of (is_valid, error_message)

    Raises:
        SecurityViolation: If strict=True and injection detected

    Example:
        is_valid, error = validate_user_input("Add task: buy milk")
        if not is_valid:
            return error_response(error)
    """
    # 1. Basic validation
    is_valid, error = input_validator.validate_message(message)
    if not is_valid:
        return (False, error)

    # 2. Prompt injection detection
    try:
        prompt_injection_detector.validate_and_sanitize(
            message, strict=strict_injection_check
        )
    except SecurityViolation as e:
        return (False, str(e))

    # 3. Content filtering
    contains_blocked, term = content_filter.contains_blocked_content(message)
    if contains_blocked:
        return (False, f"Message contains inappropriate content: '{term}'")

    return (True, None)
