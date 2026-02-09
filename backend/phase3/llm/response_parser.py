"""
Response Parser for Gemini AI Assistant

Parses Gemini's text responses to extract:
- User intent (CREATE_TASK, LIST_TASKS, UPDATE_TASK, etc.)
- Tool calls with parameters
- Natural language responses
- Confidence scores
"""

import json
import re
from typing import Optional
from enum import Enum


class Intent(str, Enum):
    """
    User intent categories for task management operations.
    """

    CREATE_TASK = "CREATE_TASK"
    LIST_TASKS = "LIST_TASKS"
    UPDATE_TASK = "UPDATE_TASK"
    COMPLETE_TASK = "COMPLETE_TASK"
    DELETE_TASK = "DELETE_TASK"
    CLARIFICATION = "CLARIFICATION"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    UNKNOWN = "UNKNOWN"


class ParsedResponse:
    """
    Structured representation of a parsed Gemini response.
    """

    def __init__(
        self,
        intent: Intent,
        tool_calls: list[dict],
        natural_response: str,
        confidence: float = 1.0,
        requires_clarification: bool = False,
    ):
        """
        Initialize parsed response.

        Args:
            intent: Detected user intent
            tool_calls: List of tool call dicts (tool_name, parameters)
            natural_response: Natural language response text
            confidence: Confidence score (0.0-1.0)
            requires_clarification: Whether user input is ambiguous
        """
        self.intent = intent
        self.tool_calls = tool_calls
        self.natural_response = natural_response
        self.confidence = confidence
        self.requires_clarification = requires_clarification


class ResponseParser:
    """
    Parses Gemini's text responses to extract structured information.

    Handles multiple response formats:
    1. Tool call syntax: add_task(...)
    2. JSON format: {"tool": "add_task", "params": {...}}
    3. Natural language with embedded actions
    """

    # Regex patterns for tool call extraction
    TOOL_CALL_PATTERN = re.compile(
        r"(\w+)\((.*?)\)",
        re.DOTALL,
    )

    # JSON pattern for structured responses
    JSON_PATTERN = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL)

    def parse_response(self, response_text: str) -> ParsedResponse:
        """
        Parse Gemini's response text into structured format.

        Args:
            response_text: Raw text response from Gemini

        Returns:
            ParsedResponse with intent, tool calls, and natural response

        Example:
            parser = ResponseParser()
            parsed = parser.parse_response("I'll add that task. add_task(user_id='123', title='Buy milk')")
            # Returns ParsedResponse with intent=CREATE_TASK and tool_calls=[{...}]
        """
        # Try to extract JSON if present
        json_match = self.JSON_PATTERN.search(response_text)
        if json_match:
            try:
                json_data = json.loads(json_match.group(1))
                return self._parse_json_response(json_data, response_text)
            except json.JSONDecodeError:
                pass  # Fall through to other parsing methods

        # Try to extract tool calls
        tool_calls = self._extract_tool_calls(response_text)
        if tool_calls:
            intent = self._infer_intent_from_tools(tool_calls)
            natural_response = self._extract_natural_response(response_text, tool_calls)
            return ParsedResponse(
                intent=intent,
                tool_calls=tool_calls,
                natural_response=natural_response,
                confidence=0.9,
            )

        # Check for clarification requests
        if self._is_clarification_request(response_text):
            return ParsedResponse(
                intent=Intent.CLARIFICATION,
                tool_calls=[],
                natural_response=response_text,
                confidence=1.0,
                requires_clarification=True,
            )

        # Check for out-of-scope responses
        if self._is_out_of_scope(response_text):
            return ParsedResponse(
                intent=Intent.OUT_OF_SCOPE,
                tool_calls=[],
                natural_response=response_text,
                confidence=1.0,
            )

        # Default: unknown intent, no tool calls
        return ParsedResponse(
            intent=Intent.UNKNOWN,
            tool_calls=[],
            natural_response=response_text,
            confidence=0.5,
        )

    def _extract_tool_calls(self, text: str) -> list[dict]:
        """
        Extract tool calls from response text.

        Args:
            text: Response text potentially containing tool calls

        Returns:
            List of dicts with tool_name and parameters

        Example:
            text = "add_task(user_id='123', title='Buy milk', priority='high')"
            calls = parser._extract_tool_calls(text)
            # Returns: [{"tool_name": "add_task", "parameters": {...}}]
        """
        tool_calls = []

        for match in self.TOOL_CALL_PATTERN.finditer(text):
            tool_name = match.group(1)
            params_str = match.group(2)

            # Only process known tool names
            if tool_name not in [
                "add_task",
                "list_tasks",
                "update_task",
                "complete_task",
                "delete_task",
            ]:
                continue

            # Parse parameters
            parameters = self._parse_parameters(params_str)
            if parameters:
                tool_calls.append({"tool_name": tool_name, "parameters": parameters})

        return tool_calls

    def _parse_parameters(self, params_str: str) -> Optional[dict]:
        """
        Parse parameter string into dict.

        Handles multiple formats:
        - Key-value pairs: user_id='123', title='Buy milk'
        - JSON-like: {"user_id": "123", "title": "Buy milk"}

        Args:
            params_str: Parameter string

        Returns:
            Dict of parameters or None if parsing fails
        """
        # Try JSON format first
        try:
            return json.loads(params_str)
        except (json.JSONDecodeError, TypeError):
            pass

        # Try key=value format
        params = {}
        # Match key='value' or key="value" or key=value
        param_pattern = re.compile(r"(\w+)\s*=\s*['\"]?([^'\"=,]+)['\"]?")

        for match in param_pattern.finditer(params_str):
            key = match.group(1)
            value = match.group(2).strip()

            # Try to parse value as JSON array for tags
            if value.startswith("[") and value.endswith("]"):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    pass

            params[key] = value

        return params if params else None

    def _parse_json_response(self, json_data: dict, full_text: str) -> ParsedResponse:
        """
        Parse structured JSON response.

        Args:
            json_data: Parsed JSON object
            full_text: Full response text

        Returns:
            ParsedResponse
        """
        intent_str = json_data.get("intent", "UNKNOWN")
        intent = Intent[intent_str] if intent_str in Intent.__members__ else Intent.UNKNOWN

        tool_calls = json_data.get("tool_calls", [])
        natural_response = json_data.get("response", full_text)
        confidence = json_data.get("confidence", 1.0)

        return ParsedResponse(
            intent=intent,
            tool_calls=tool_calls,
            natural_response=natural_response,
            confidence=confidence,
        )

    def _infer_intent_from_tools(self, tool_calls: list[dict]) -> Intent:
        """
        Infer user intent from extracted tool calls.

        Args:
            tool_calls: List of tool call dicts

        Returns:
            Inferred Intent enum
        """
        if not tool_calls:
            return Intent.UNKNOWN

        # Use the first tool call to determine intent
        tool_name = tool_calls[0]["tool_name"]

        intent_map = {
            "add_task": Intent.CREATE_TASK,
            "list_tasks": Intent.LIST_TASKS,
            "update_task": Intent.UPDATE_TASK,
            "complete_task": Intent.COMPLETE_TASK,
            "delete_task": Intent.DELETE_TASK,
        }

        return intent_map.get(tool_name, Intent.UNKNOWN)

    def _extract_natural_response(
        self, full_text: str, tool_calls: list[dict]
    ) -> str:
        """
        Extract natural language response by removing tool call syntax.

        Args:
            full_text: Full response text
            tool_calls: Extracted tool calls

        Returns:
            Natural language response without tool syntax
        """
        cleaned_text = full_text

        # Remove tool call patterns
        for tool_call in tool_calls:
            tool_name = tool_call["tool_name"]
            # Remove the tool call pattern
            cleaned_text = re.sub(
                rf"{tool_name}\([^)]*\)", "", cleaned_text, flags=re.DOTALL
            )

        # Remove JSON code blocks
        cleaned_text = self.JSON_PATTERN.sub("", cleaned_text)

        # Clean up extra whitespace
        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

        return cleaned_text or "Processing your request..."

    def _is_clarification_request(self, text: str) -> bool:
        """
        Check if response is asking for clarification.

        Args:
            text: Response text

        Returns:
            True if response is requesting clarification
        """
        clarification_patterns = [
            r"which (one|task)",
            r"can you (specify|clarify|provide more)",
            r"need more information",
            r"could you (tell me|specify)",
            r"\?",  # Contains question mark
        ]

        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in clarification_patterns)

    def _is_out_of_scope(self, text: str) -> bool:
        """
        Check if response indicates out-of-scope request.

        Args:
            text: Response text

        Returns:
            True if response is declining out-of-scope request
        """
        out_of_scope_patterns = [
            r"can only help with",
            r"outside my scope",
            r"not able to",
            r"task management assistant",
        ]

        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in out_of_scope_patterns)
