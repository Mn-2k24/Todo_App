"""
MCP Server for Todo App Task Management

This package provides a Model Context Protocol (MCP) server that exposes
5 task management operations as tools for AI agents:

- add_task: Create new tasks
- list_tasks: Query tasks with filtering
- update_task: Modify task properties
- complete_task: Mark tasks as completed
- delete_task: Remove tasks

All operations enforce strict user_id isolation for data security.
"""

__version__ = "1.0.0"
