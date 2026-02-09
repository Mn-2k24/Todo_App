"""
MCP Task Management Tools

Implements 5 core task operations with user_id isolation:
- add_task
- list_tasks
- update_task
- complete_task
- delete_task
"""

from mcp_server.tools.task_tools import (
    handle_add_task,
    handle_complete_task,
    handle_delete_task,
    handle_list_tasks,
    handle_update_task,
)

__all__ = [
    "handle_add_task",
    "handle_list_tasks",
    "handle_update_task",
    "handle_complete_task",
    "handle_delete_task",
]
