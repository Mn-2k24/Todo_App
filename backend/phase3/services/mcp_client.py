"""
MCP Client Wrapper

Provides interface to invoke MCP server tools.
Handles tool invocation, response parsing, and error handling.

Note: This client directly imports and calls MCP tools rather than using
stdio/HTTP transport. This is simpler for a monolithic deployment and
avoids the complexity of running a separate MCP server process.
"""

import json
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

logger = logging.getLogger(__name__)


class MCPClientError(Exception):
    """Base exception for MCP client errors."""

    pass


class MCPToolNotFoundError(MCPClientError):
    """Raised when requested tool doesn't exist."""

    pass


class MCPToolExecutionError(MCPClientError):
    """Raised when tool execution fails."""

    pass


class MCPClient:
    """
    Client for invoking MCP server tools.

    This implementation directly imports and calls the MCP tool handlers
    rather than using a separate process with stdio transport.
    """

    def __init__(self):
        """Initialize MCP client."""
        # Import tool handlers
        from mcp_server.tools.task_tools import (
            handle_add_task,
            handle_complete_task,
            handle_delete_task,
            handle_list_tasks,
            handle_update_task,
        )

        # Map tool names to handlers
        self._tool_handlers = {
            "add_task": handle_add_task,
            "list_tasks": handle_list_tasks,
            "update_task": handle_update_task,
            "complete_task": handle_complete_task,
            "delete_task": handle_delete_task,
        }

        logger.info(f"MCP Client initialized with {len(self._tool_handlers)} tools")

    async def invoke_tool(
        self, tool_name: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Invoke an MCP tool with given parameters.

        Args:
            tool_name: Name of the tool to invoke
            parameters: Tool parameters (must include user_id)

        Returns:
            Tool result as dict (parsed from JSON response)

        Raises:
            MCPToolNotFoundError: If tool doesn't exist
            MCPToolExecutionError: If tool execution fails
            MCPClientError: For other client errors

        Example:
            result = await client.invoke_tool(
                "add_task",
                {"user_id": "123", "title": "Buy milk", "priority": "high"}
            )
        """
        # Validate tool exists
        if tool_name not in self._tool_handlers:
            available = ", ".join(self._tool_handlers.keys())
            raise MCPToolNotFoundError(
                f"Tool '{tool_name}' not found. Available tools: {available}"
            )

        # Validate user_id is present (security critical)
        if "user_id" not in parameters:
            raise MCPClientError(
                f"Missing required parameter 'user_id' for tool '{tool_name}'"
            )

        # Get tool handler
        handler = self._tool_handlers[tool_name]

        try:
            logger.info(f"Invoking MCP tool: {tool_name} with params: {parameters}")

            # Call the tool handler
            result_contents = await handler(parameters)

            # Parse result from MCP TextContent format
            if result_contents and len(result_contents) > 0:
                result_text = result_contents[0].text
                result_dict = json.loads(result_text)
                logger.info(
                    f"MCP tool {tool_name} executed successfully: {result_dict.get('success', False)}"
                )
                return result_dict
            else:
                raise MCPToolExecutionError(
                    f"Tool '{tool_name}' returned no content"
                )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse tool result as JSON: {e}")
            raise MCPToolExecutionError(
                f"Tool '{tool_name}' returned invalid JSON: {e}"
            ) from e
        except Exception as e:
            logger.error(f"Tool execution failed for {tool_name}: {e}", exc_info=True)
            raise MCPToolExecutionError(
                f"Tool '{tool_name}' execution failed: {str(e)}"
            ) from e

    async def invoke_multiple_tools(
        self, tool_calls: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Invoke multiple tools sequentially.

        Args:
            tool_calls: List of dicts with 'tool_name' and 'parameters' keys

        Returns:
            List of tool results in same order

        Example:
            results = await client.invoke_multiple_tools([
                {"tool_name": "list_tasks", "parameters": {"user_id": "123"}},
                {"tool_name": "add_task", "parameters": {"user_id": "123", "title": "New task"}}
            ])
        """
        results = []

        for tool_call in tool_calls:
            tool_name = tool_call.get("tool_name")
            parameters = tool_call.get("parameters", {})

            if not tool_name:
                results.append({
                    "success": False,
                    "error": "INVALID_TOOL_CALL",
                    "message": "Missing tool_name in tool call",
                })
                continue

            try:
                result = await self.invoke_tool(tool_name, parameters)
                results.append(result)
            except MCPClientError as e:
                logger.error(f"Tool {tool_name} failed: {e}")
                results.append({
                    "success": False,
                    "error": "TOOL_EXECUTION_ERROR",
                    "message": str(e),
                })

        return results

    def get_available_tools(self) -> List[str]:
        """
        Get list of available tool names.

        Returns:
            List of tool names
        """
        return list(self._tool_handlers.keys())

    def validate_parameters(
        self, tool_name: str, parameters: Dict[str, Any]
    ) -> tuple[bool, Optional[str]]:
        """
        Validate parameters for a tool.

        Args:
            tool_name: Name of the tool
            parameters: Parameters to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check tool exists
        if tool_name not in self._tool_handlers:
            return (False, f"Tool '{tool_name}' not found")

        # Check user_id is present
        if "user_id" not in parameters:
            return (False, "Missing required parameter: user_id")

        # Tool-specific validation
        if tool_name == "add_task":
            if "title" not in parameters:
                return (False, "Missing required parameter: title")
            if len(parameters.get("title", "")) > 500:
                return (False, "Title must be max 500 characters")

        elif tool_name in ["update_task", "complete_task", "delete_task"]:
            if "task_id" not in parameters:
                return (False, "Missing required parameter: task_id")

        # Validate user_id format (should be valid UUID string)
        try:
            UUID(parameters["user_id"])
        except (ValueError, AttributeError):
            return (False, "user_id must be a valid UUID")

        return (True, None)


# Singleton instance for convenience
_mcp_client_instance: Optional[MCPClient] = None


def get_mcp_client() -> MCPClient:
    """
    Get singleton MCP client instance.

    Returns:
        MCPClient instance
    """
    global _mcp_client_instance
    if _mcp_client_instance is None:
        _mcp_client_instance = MCPClient()
    return _mcp_client_instance
