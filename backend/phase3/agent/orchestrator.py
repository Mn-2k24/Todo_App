"""
AI Agent Orchestrator

Central coordinator that:
- Parses user intent using Gemini LLM
- Extracts entities (task titles, priorities, dates, tags)
- Selects and executes MCP tools
- Manages conversation context
- Handles multi-step operations and ambiguity
"""

import asyncio
import json
import logging
from datetime import date, datetime, timedelta
from typing import Any, Optional
from uuid import UUID

from phase3.llm.gemini_client import (
    GeminiClient,
    GeminiError,
    RateLimitError,
    AuthenticationError,
    ContentPolicyError,
)
from phase3.llm.prompt_builder import PromptBuilder
from phase3.llm.response_parser import Intent, ParsedResponse, ResponseParser
from phase3.llm.security import validate_user_input

logger = logging.getLogger(__name__)


class OrchestratorError(Exception):
    """Base exception for orchestrator errors."""

    pass


class ToolExecutionError(OrchestratorError):
    """Raised when MCP tool execution fails."""

    pass


class AgentOrchestrator:
    """
    AI Agent that orchestrates task management operations.

    Coordinates between:
    - Gemini LLM (intent parsing, entity extraction)
    - MCP Server (task operations)
    - Conversation history (context resolution)
    """

    def __init__(
        self,
        user_id: UUID,
        mcp_client: Any,  # MCP client for tool calls
        use_mock_llm: bool = False,
    ):
        """
        Initialize agent orchestrator.

        Args:
            user_id: Current user's UUID (for user isolation)
            mcp_client: MCP client for executing tool calls
            use_mock_llm: If True, use mock Gemini client for testing
        """
        self.user_id = str(user_id)
        self.mcp_client = mcp_client

        # Initialize LLM components
        self.gemini_client = GeminiClient(use_mock=use_mock_llm)
        self.prompt_builder = PromptBuilder(max_history_messages=10)
        self.response_parser = ResponseParser()

        # Conversation state
        self.conversation_history: list[dict[str, str]] = []
        self.last_task_list: list[dict] = []  # Cache for "the first task" references
        self.task_index_map: dict[int, str] = {}  # Maps 1-based index -> task_id UUID

        # Configuration
        self.confidence_threshold = 0.7  # Minimum confidence to execute without clarification
        self.max_tool_calls_per_turn = 5  # Prevent infinite loops

    async def process_message(self, user_message: str) -> dict[str, Any]:
        """
        Process a user message and execute appropriate actions.

        Args:
            user_message: User's natural language input

        Returns:
            Response dict with:
            - success: bool
            - message: str (natural language response)
            - tool_calls: list (executed tool calls)
            - intent: str (detected intent)

        Raises:
            OrchestratorError: If processing fails
        """
        try:
            # 1. Validate input
            is_valid, error = validate_user_input(user_message, strict_injection_check=False)
            if not is_valid:
                return {
                    "success": False,
                    "message": f"Invalid input: {error}",
                    "tool_calls": [],
                    "intent": Intent.UNKNOWN.value,
                }

            # 2. Build system instruction with user context
            system_instruction = self.prompt_builder.build_system_instruction_with_tools(
                user_id=self.user_id
            )

            # 3. Build conversation messages
            messages = self.prompt_builder.build_conversation_messages(
                self.conversation_history, user_message
            )

            # 4. Call Gemini to parse intent and generate response
            logger.info(f"Processing message for user {self.user_id}: {user_message[:50]}...")
            response_text = await self.gemini_client.generate_with_retry(
                messages, system_instruction=system_instruction
            )

            # 5. Parse Gemini's response
            parsed = self.response_parser.parse_response(response_text)
            logger.info(f"Detected intent: {parsed.intent}, confidence: {parsed.confidence}")

            # 6. Handle based on intent
            if parsed.requires_clarification:
                # Gemini is asking for clarification - return without tool execution
                result = {
                    "success": True,
                    "message": parsed.natural_response,
                    "tool_calls": [],
                    "intent": Intent.CLARIFICATION.value,
                }
            elif parsed.intent == Intent.OUT_OF_SCOPE:
                # Request is outside task management scope
                result = {
                    "success": True,
                    "message": parsed.natural_response,
                    "tool_calls": [],
                    "intent": Intent.OUT_OF_SCOPE.value,
                }
            elif parsed.tool_calls:
                # Execute tool calls
                result = await self._execute_tool_calls(parsed)
            else:
                # No tool calls detected - return natural response
                result = {
                    "success": True,
                    "message": parsed.natural_response,
                    "tool_calls": [],
                    "intent": parsed.intent.value,
                }

            # 7. Update conversation history
            self._update_conversation_history(user_message, result["message"])

            return result

        except RateLimitError as e:
            logger.error(f"Rate limit error: {e}")
            return {
                "success": False,
                "message": "I'm currently unavailable due to API quota limits. The free tier has a limit of 20 requests per day. Please try again later or contact support to upgrade.",
                "tool_calls": [],
                "intent": Intent.UNKNOWN.value,
            }
        except AuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            return {
                "success": False,
                "message": "Chatbot is currently unavailable due to an API authentication issue. The API key may be invalid, expired, or reported as leaked. Please contact support.",
                "tool_calls": [],
                "intent": Intent.UNKNOWN.value,
            }
        except ContentPolicyError as e:
            logger.error(f"Content policy error: {e}")
            return {
                "success": False,
                "message": "Your message violates content policy. Please rephrase your request.",
                "tool_calls": [],
                "intent": Intent.UNKNOWN.value,
            }
        except GeminiError as e:
            logger.error(f"Gemini error during processing: {e}")
            return {
                "success": False,
                "message": "I encountered an issue understanding your request. Please try rephrasing.",
                "tool_calls": [],
                "intent": Intent.UNKNOWN.value,
            }
        except Exception as e:
            logger.error(f"Unexpected error during processing: {e}", exc_info=True)
            return {
                "success": False,
                "message": "An unexpected error occurred. Please try again.",
                "tool_calls": [],
                "intent": Intent.UNKNOWN.value,
            }

    async def _execute_tool_calls(self, parsed: ParsedResponse) -> dict[str, Any]:
        """
        Execute MCP tool calls from parsed response.

        Args:
            parsed: ParsedResponse with tool calls

        Returns:
            Result dict with success, message, and executed tool calls
        """
        executed_calls = []
        tool_results = []

        # Limit number of tool calls to prevent abuse
        tool_calls = parsed.tool_calls[: self.max_tool_calls_per_turn]

        for tool_call in tool_calls:
            tool_name = tool_call["tool_name"]
            parameters = tool_call["parameters"]

            # Ensure user_id is injected (security critical)
            parameters["user_id"] = self.user_id

            # Auto-fetch task list if needed for index resolution
            # NOTE: If user deletes tasks from Phase II UI while chat is active,
            # the index map may become stale. Consider invalidating map on errors.
            if tool_name in ["delete_task", "update_task", "complete_task"]:
                if "task_id" in parameters and not self.task_index_map:
                    logger.info("Index map empty, fetching task list first")
                    try:
                        list_result = await self._call_mcp_tool("list_tasks", {"user_id": self.user_id, "status": "all"})
                        if list_result.get("success"):
                            self.last_task_list = list_result.get("tasks", [])
                            self.task_index_map = {
                                i + 1: task["id"] for i, task in enumerate(self.last_task_list)
                            }
                            logger.info(f"Auto-built task index map with {len(self.task_index_map)} entries: {list(self.task_index_map.keys())}")
                    except Exception as e:
                        logger.warning(f"Failed to auto-fetch task list: {e}")

            # Resolve context references (e.g., "the first task", numeric indexes, task names)
            parameters = await self._resolve_context_references(tool_name, parameters)

            # Validate task_id is UUID format (not integer index)
            if "task_id" in parameters and isinstance(parameters["task_id"], int):
                logger.error(f"ERROR: task_id is still an integer ({parameters['task_id']}) - resolution failed!")
                error_result = {
                    "success": False,
                    "error": "RESOLUTION_ERROR",
                    "message": f"Could not resolve task index {parameters['task_id']} to UUID. Please list tasks first.",
                }
                executed_calls.append({
                    "tool_name": tool_name,
                    "parameters": parameters,
                    "result": error_result,
                })
                tool_results.append(error_result)
                continue

            # Execute the tool call
            try:
                logger.info(f"Executing tool: {tool_name} with params: {parameters}")
                result = await self._call_mcp_tool(tool_name, parameters)

                executed_calls.append({
                    "tool_name": tool_name,
                    "parameters": parameters,
                    "result": result,
                })
                tool_results.append(result)

                # Cache task list for context resolution and build index map
                if tool_name == "list_tasks" and result.get("success"):
                    self.last_task_list = result.get("tasks", [])
                    # Build 1-based index -> task_id mapping for user-friendly references
                    self.task_index_map = {
                        i + 1: task["id"] for i, task in enumerate(self.last_task_list)
                    }
                    logger.info(f"Built task index map with {len(self.task_index_map)} entries")

            except Exception as e:
                logger.error(f"Tool execution failed: {tool_name} - {e}")
                error_result = {
                    "success": False,
                    "error": "TOOL_EXECUTION_ERROR",
                    "message": str(e),
                }
                executed_calls.append({
                    "tool_name": tool_name,
                    "parameters": parameters,
                    "result": error_result,
                })
                tool_results.append(error_result)

        # Generate natural language response
        natural_response = self._generate_natural_response(
            parsed, executed_calls, tool_results
        )

        # Log summary for debugging
        logger.info(f"Tool execution summary: {len(executed_calls)} tools, all_succeeded={all(r.get('success', False) for r in tool_results)}")
        for call in executed_calls:
            logger.info(f"  - {call['tool_name']}: success={call['result'].get('success', False)}")

        return {
            "success": True,
            "message": natural_response,
            "tool_calls": executed_calls,
            "intent": parsed.intent.value,
        }

    async def _call_mcp_tool(self, tool_name: str, parameters: dict) -> dict:
        """
        Call MCP tool via MCP client.

        Args:
            tool_name: Name of the MCP tool
            parameters: Tool parameters

        Returns:
            Tool result dict

        Raises:
            ToolExecutionError: If tool call fails
        """
        # Call the REAL MCP client (connected to actual database)
        try:
            result = await self.mcp_client.invoke_tool(tool_name, parameters)
            logger.info(f"MCP tool {tool_name} returned: success={result.get('success')}")
            return result
        except Exception as e:
            logger.error(f"MCP tool call failed: {tool_name} - {e}")
            raise ToolExecutionError(f"Tool {tool_name} failed: {str(e)}") from e

    async def _resolve_context_references(self, tool_name: str, parameters: dict) -> dict:
        """
        Resolve context references like "the first task", "that one", numeric indexes, task names, etc.

        Args:
            tool_name: Name of the tool being called
            parameters: Tool parameters potentially containing references

        Returns:
            Parameters with resolved references
        """
        # Check if task_id is a context reference
        if "task_id" in parameters:
            task_id = parameters["task_id"]

            # Handle numeric indexes (1, 2, 3, etc.) - PRIORITY CHECK
            if isinstance(task_id, (int, str)):
                try:
                    # Try to parse as integer index
                    index = int(task_id)
                    if index in self.task_index_map:
                        resolved_id = self.task_index_map[index]
                        logger.info(f"Resolved task index {index} to ID {resolved_id}")
                        parameters["task_id"] = resolved_id
                        return parameters
                    else:
                        logger.warning(f"Task index {index} not in map (size: {len(self.task_index_map)})")
                except (ValueError, TypeError):
                    pass  # Not a numeric index, try other resolution methods

            # Handle task name matching (e.g., "delete reading task")
            if isinstance(task_id, str) and len(task_id) > 1:
                task_id_lower = task_id.lower()

                # Try to find task by partial name match
                for task in self.last_task_list:
                    task_desc = task.get("description", "").lower()
                    # Check if the task_id string appears in the task description
                    if task_id_lower in task_desc or task_desc in task_id_lower:
                        logger.info(f"Resolved task name '{task_id}' to ID {task['id']} ('{task['description']}')")
                        parameters["task_id"] = task["id"]
                        return parameters

            # Handle ordinal references like "first", "second", "last"
            if isinstance(task_id, str):
                if "first" in task_id.lower() and self.last_task_list:
                    parameters["task_id"] = self.last_task_list[0]["id"]
                    logger.info(f"Resolved 'first' to ID {self.last_task_list[0]['id']}")
                elif "second" in task_id.lower() and len(self.last_task_list) > 1:
                    parameters["task_id"] = self.last_task_list[1]["id"]
                    logger.info(f"Resolved 'second' to ID {self.last_task_list[1]['id']}")
                elif "last" in task_id.lower() and self.last_task_list:
                    parameters["task_id"] = self.last_task_list[-1]["id"]
                    logger.info(f"Resolved 'last' to ID {self.last_task_list[-1]['id']}")

        return parameters

    def _get_task_name_from_call(self, executed_call: dict) -> str:
        """
        Extract task name from an executed tool call for user-friendly messages.

        Args:
            executed_call: Executed call dict with tool, parameters, result

        Returns:
            Task description/name, or empty string if not found
        """
        # Get the task_id from parameters (already resolved to UUID)
        task_id = executed_call.get("parameters", {}).get("task_id")
        if not task_id:
            return ""

        # Find the task in our cached list
        for task in self.last_task_list:
            if task.get("id") == task_id:
                return task.get("description", "")

        return ""

    def _format_task_for_user(self, task: dict) -> str:
        """
        Format a single task in human-friendly format.

        Args:
            task: Task dict from MCP tool result

        Returns:
            Formatted task string (e.g., "⏳ Buy groceries (Due: Jan 28)")
        """
        # Extract task fields
        description = task.get("description", "Untitled")
        completed = task.get("completed", False)
        priority = task.get("priority", "medium")
        due_date_str = task.get("due_date")

        # Status emoji
        status_emoji = "✅" if completed else "⏳"

        # Build task line
        task_line = f"{status_emoji} {description}"

        # Add due date if present
        if due_date_str:
            try:
                # Parse ISO date and format as "Jan 28, 2024"
                if "T" in due_date_str:
                    due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
                else:
                    due_date = datetime.fromisoformat(due_date_str)
                formatted_date = due_date.strftime("%b %d, %Y")
                task_line += f" (Due: {formatted_date})"
            except:
                pass  # Skip invalid dates

        # Add priority indicator for high priority tasks
        if priority == "high" and not completed:
            task_line += " 🔥"

        return task_line

    def _generate_natural_response(
        self, parsed: ParsedResponse, executed_calls: list[dict], tool_results: list[dict]
    ) -> str:
        """
        Generate natural language response based on tool execution results.

        IMPORTANT: Tool results are the single source of truth.
        This method MUST derive responses from actual tool data, not from
        Gemini's pre-execution predictions.

        Args:
            parsed: Original parsed response from Gemini
            executed_calls: List of executed tool calls
            tool_results: List of tool results

        Returns:
            Natural language response string
        """
        # Check if all tools succeeded
        all_succeeded = all(result.get("success", False) for result in tool_results)

        if not all_succeeded:
            # Find first failure and provide detailed error
            for i, result in enumerate(tool_results):
                if not result.get("success"):
                    error_message = result.get("message", "Unknown error")
                    error_code = result.get("error", "")

                    # Provide user-friendly error messages
                    if "not found" in error_message.lower() or "unauthorized" in error_message.lower():
                        return f"❌ I couldn't find that task. It may have been already deleted or the task number is invalid. Please list your tasks to see current tasks."
                    elif "invalid" in error_message.lower():
                        return f"❌ Invalid input: {error_message}"
                    else:
                        return f"❌ I encountered an issue: {error_message}"

        # Generate response based on tool type and ACTUAL tool results
        # Tool results = source of truth, NOT Gemini's pre-execution response
        if executed_calls:
            tool_name = executed_calls[0]["tool_name"]
            tool_result = tool_results[0]

            if tool_name == "add_task" and tool_result.get("success"):
                task = tool_result.get("task", {})
                title = task.get("description", "task")
                return f"✅ I've added the task '{title}' successfully."

            elif tool_name == "list_tasks" and tool_result.get("success"):
                # CRITICAL: Use actual task count from tool result, not Gemini's guess
                tasks = tool_result.get("tasks", [])
                count = len(tasks)  # Always derive count from actual tasks array

                if count == 0:
                    return "You don't have any tasks yet. Would you like to add one?"
                else:
                    # Format tasks in human-friendly way
                    response_lines = []

                    if count == 1:
                        response_lines.append("Here's your task:")
                    else:
                        response_lines.append(f"Here are your {count} tasks:")

                    # Format each task (limit to first 20 for readability)
                    for i, task in enumerate(tasks[:20], 1):
                        task_line = f"{i}. {self._format_task_for_user(task)}"
                        response_lines.append(task_line)

                    if count > 20:
                        response_lines.append(f"\n...and {count - 20} more tasks.")

                    response_lines.append("\nWhat would you like to do next?")

                    return "\n".join(response_lines)

            elif tool_name == "complete_task" and tool_result.get("success"):
                # Try to get task name from parameters and index map
                task_name = self._get_task_name_from_call(executed_calls[0])
                if task_name:
                    return f"✅ Task '{task_name}' marked as completed!"
                return "✅ Task marked as completed!"

            elif tool_name == "update_task" and tool_result.get("success"):
                task_name = self._get_task_name_from_call(executed_calls[0])
                if task_name:
                    return f"✅ Task '{task_name}' updated successfully."
                return "✅ Task updated successfully."

            elif tool_name == "delete_task" and tool_result.get("success"):
                task_name = self._get_task_name_from_call(executed_calls[0])
                if task_name:
                    return f"✅ Task '{task_name}' deleted successfully."
                return "✅ Task deleted successfully."

        # Fallback: use Gemini's natural response only if no specific tool handling above
        if parsed.natural_response and parsed.natural_response.strip():
            return parsed.natural_response

        return "I've processed your request."

    def _update_conversation_history(self, user_message: str, assistant_message: str):
        """
        Update conversation history with new messages.

        Args:
            user_message: User's message
            assistant_message: Assistant's response
        """
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})

        # Keep only last 20 messages (10 turns) to avoid context overflow
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

    def reset_conversation(self):
        """Reset conversation history and cached state."""
        self.conversation_history = []
        self.last_task_list = []
        self.task_index_map = {}
        logger.info(f"Reset conversation for user {self.user_id}")

    def get_conversation_summary(self) -> dict[str, Any]:
        """
        Get summary of current conversation state.

        Returns:
            Dict with conversation stats and cached state
        """
        return {
            "user_id": self.user_id,
            "message_count": len(self.conversation_history),
            "cached_tasks": len(self.last_task_list),
            "last_messages": self.conversation_history[-4:] if self.conversation_history else [],
        }
