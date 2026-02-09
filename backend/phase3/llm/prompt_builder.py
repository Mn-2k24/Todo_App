"""
Prompt Builder for Gemini AI Assistant

Constructs conversation prompts with:
- System instructions
- Conversation history
- User context (user_id, available tools)
- MCP tool descriptions
"""

from typing import Optional

from phase3.llm.system_prompts import get_system_instruction


class PromptBuilder:
    """
    Builds prompts for the Gemini AI assistant.

    Handles:
    - System instruction injection
    - Conversation history formatting
    - MCP tool documentation
    - Context window management (last N messages)
    """

    def __init__(
        self,
        system_instruction: Optional[str] = None,
        max_history_messages: int = 10,
    ):
        """
        Initialize prompt builder.

        Args:
            system_instruction: Custom system instruction (uses default if None)
            max_history_messages: Maximum number of conversation history messages to include
        """
        self.system_instruction = system_instruction or get_system_instruction()
        self.max_history_messages = max_history_messages

    def build_system_instruction_with_tools(
        self, user_id: str, available_tools: Optional[list[str]] = None
    ) -> str:
        """
        Build system instruction with user context and available tools.

        Args:
            user_id: Current user's UUID (for user isolation context)
            available_tools: List of available MCP tool names

        Returns:
            System instruction string with injected context
        """
        tools_list = available_tools or [
            "add_task",
            "list_tasks",
            "update_task",
            "complete_task",
            "delete_task",
        ]

        tools_description = self._get_tools_description(tools_list)

        return f"""{self.system_instruction}

CURRENT USER CONTEXT:
- User ID: {user_id}
- All operations are scoped to this user
- You can only access and modify tasks belonging to this user

{tools_description}

Remember: Always extract user_id={user_id} when calling tools."""

    def _get_tools_description(self, tools: list[str]) -> str:
        """
        Get detailed descriptions of available MCP tools.

        Args:
            tools: List of tool names

        Returns:
            Formatted tool descriptions
        """
        tool_docs = {
            "add_task": """
add_task: Create a new task
  Parameters:
    - user_id (required): User UUID
    - title (required): Task description (1-500 chars)
    - priority (optional): low | medium | high (default: medium)
    - due_date (optional): ISO 8601 date (YYYY-MM-DD)
    - tags (optional): Array of tag strings
  Example: add_task(user_id="uuid", title="Buy groceries", priority="high", due_date="2026-02-01", tags=["shopping"])
""",
            "list_tasks": """
list_tasks: Query tasks with optional filtering
  Parameters:
    - user_id (required): User UUID
    - status (optional): pending | completed | all (default: all)
    - priority (optional): low | medium | high
    - tag (optional): Filter by single tag
  Example: list_tasks(user_id="uuid", status="pending", priority="high")
""",
            "update_task": """
update_task: Modify an existing task
  Parameters:
    - user_id (required): User UUID
    - task_id (required): Task number from the numbered list (e.g., 1, 2, 3) - NEVER use UUID
    - title (optional): New task description
    - priority (optional): low | medium | high
    - due_date (optional): ISO 8601 date or null to clear
    - tags (optional): Array of tag strings
  Example: update_task(user_id="uuid", task_id=2, title="Buy groceries and cook dinner", priority="high")
  Note: When user says "update task 2", use task_id=2, NOT a UUID
""",
            "complete_task": """
complete_task: Mark a task as completed
  Parameters:
    - user_id (required): User UUID
    - task_id (required): Task number from the numbered list (e.g., 1, 2, 3) - NEVER use UUID
  Example: complete_task(user_id="uuid", task_id=2)
  Note: When user says "complete task 2", use task_id=2, NOT a UUID
""",
            "delete_task": """
delete_task: Delete a task permanently
  Parameters:
    - user_id (required): User UUID
    - task_id (required): Task number from the numbered list (e.g., 1, 2, 3) - NEVER use UUID
  Example: delete_task(user_id="uuid", task_id=2)
  Note: When user says "delete task 2", use task_id=2, NOT a UUID. NEVER ask user for UUID.
""",
        }

        descriptions = ["AVAILABLE TOOLS:"]
        for tool in tools:
            if tool in tool_docs:
                descriptions.append(tool_docs[tool])

        return "\n".join(descriptions)

    def build_conversation_messages(
        self,
        conversation_history: list[dict[str, str]],
        new_message: str,
    ) -> list[dict[str, str]]:
        """
        Build conversation messages with history and new user message.

        Args:
            conversation_history: Previous messages (role, content dicts)
            new_message: New user message to add

        Returns:
            List of message dicts with role and content, limited to max_history_messages

        Example:
            history = [
                {"role": "user", "content": "Show my tasks"},
                {"role": "assistant", "content": "You have 3 tasks..."}
            ]
            messages = builder.build_conversation_messages(history, "Add task: buy milk")
            # Returns: history + new message, keeping only last 10 messages
        """
        # Take only the last N messages to avoid context window overflow
        recent_history = conversation_history[-self.max_history_messages :]

        # Add new user message
        messages = recent_history + [{"role": "user", "content": new_message}]

        return messages

    def format_tool_call_result(
        self, tool_name: str, parameters: dict, result: dict
    ) -> str:
        """
        Format a tool call result for inclusion in conversation history.

        Args:
            tool_name: Name of the MCP tool called
            parameters: Parameters passed to the tool
            result: Result returned by the tool

        Returns:
            Formatted string describing the tool call and result

        Example:
            formatted = builder.format_tool_call_result(
                "add_task",
                {"user_id": "123", "title": "Buy groceries"},
                {"success": True, "task": {...}}
            )
            # Returns: "Called add_task(...) → Success: Task created"
        """
        # Format parameters (hide user_id for cleaner output)
        params_str = ", ".join(
            f"{k}={v}" for k, v in parameters.items() if k != "user_id"
        )

        # Format result
        if result.get("success"):
            if tool_name == "list_tasks":
                count = result.get("count", 0)
                result_str = f"Found {count} task(s)"
            elif tool_name == "add_task":
                task = result.get("task", {})
                result_str = f"Created task: {task.get('description', 'N/A')}"
            elif tool_name == "update_task":
                result_str = "Task updated successfully"
            elif tool_name == "complete_task":
                result_str = "Task marked as completed"
            elif tool_name == "delete_task":
                result_str = "Task deleted successfully"
            else:
                result_str = "Operation completed"
        else:
            error = result.get("error", "UNKNOWN")
            message = result.get("message", "An error occurred")
            result_str = f"Error: {error} - {message}"

        return f"[Tool Call] {tool_name}({params_str}) → {result_str}"

    def extract_user_intent(self, message: str) -> dict[str, any]:
        """
        Extract basic intent signals from user message.

        This is a simple heuristic-based extraction for common patterns.
        The LLM will do the full intent parsing.

        Args:
            message: User message text

        Returns:
            Dict with intent signals (action_keywords, urgency_keywords, etc.)

        Example:
            intent = builder.extract_user_intent("urgent: buy groceries tomorrow")
            # Returns: {"urgency": ["urgent"], "timeframe": ["tomorrow"], ...}
        """
        message_lower = message.lower()

        # Action keywords
        action_keywords = []
        if any(
            word in message_lower
            for word in ["add", "create", "new", "make", "remind"]
        ):
            action_keywords.append("create")
        if any(word in message_lower for word in ["show", "list", "display", "get"]):
            action_keywords.append("list")
        if any(
            word in message_lower for word in ["update", "change", "modify", "edit"]
        ):
            action_keywords.append("update")
        if any(
            word in message_lower
            for word in ["complete", "done", "finish", "mark as done"]
        ):
            action_keywords.append("complete")
        if any(word in message_lower for word in ["delete", "remove", "cancel"]):
            action_keywords.append("delete")

        # Urgency keywords
        urgency_keywords = []
        if any(word in message_lower for word in ["urgent", "asap", "important"]):
            urgency_keywords.append("high")
        if any(word in message_lower for word in ["sometime", "eventually", "later"]):
            urgency_keywords.append("low")

        # Timeframe keywords
        timeframe_keywords = []
        if any(
            word in message_lower
            for word in ["today", "now", "immediately", "right now"]
        ):
            timeframe_keywords.append("today")
        if "tomorrow" in message_lower:
            timeframe_keywords.append("tomorrow")
        if any(word in message_lower for word in ["next week", "this week"]):
            timeframe_keywords.append("week")

        return {
            "action_keywords": action_keywords,
            "urgency_keywords": urgency_keywords,
            "timeframe_keywords": timeframe_keywords,
            "message_length": len(message),
        }
