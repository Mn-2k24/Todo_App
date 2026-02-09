"""
MCP Server Main Entry Point for Todo App Task Management

This MCP server exposes 5 task management operations as tools:
- add_task: Create new tasks
- list_tasks: Query tasks with filtering
- update_task: Modify task properties
- complete_task: Mark tasks as completed
- delete_task: Remove tasks

All operations enforce strict user_id isolation - users can only access their own data.
"""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from mcp_server.config import get_database_session
from mcp_server.tools.task_tools import (
    handle_add_task,
    handle_complete_task,
    handle_delete_task,
    handle_list_tasks,
    handle_update_task,
)


@asynccontextmanager
async def server_lifespan(_server: Server) -> AsyncIterator[dict[str, Any]]:
    """
    Manage server lifecycle - initialize database connection on startup,
    clean up on shutdown.
    """
    # Database session will be created per-request via dependency injection
    # This lifespan context is available for shared resources if needed
    print("MCP Server starting up...")
    try:
        yield {}
    finally:
        print("MCP Server shutting down...")


# Initialize MCP server with lifespan management
server = Server("todo-mcp-server", lifespan=server_lifespan)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    Register all 5 task management MCP tools.
    Each tool enforces user_id isolation at the database query level.
    """
    return [
        types.Tool(
            name="add_task",
            description="Create a new task for the authenticated user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "UUID of the user creating the task",
                        "format": "uuid",
                    },
                    "title": {
                        "type": "string",
                        "description": "Task title (1-200 characters)",
                        "minLength": 1,
                        "maxLength": 200,
                    },
                    "description": {
                        "type": "string",
                        "description": "Task description (optional, max 2000 characters)",
                        "maxLength": 2000,
                    },
                    "priority": {
                        "type": "string",
                        "description": "Task priority level",
                        "enum": ["low", "medium", "high"],
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Due date in ISO 8601 format (optional)",
                        "format": "date-time",
                    },
                    "tags": {
                        "type": "array",
                        "description": "List of tags (optional)",
                        "items": {"type": "string"},
                    },
                },
                "required": ["user_id", "title"],
            },
        ),
        types.Tool(
            name="list_tasks",
            description="List tasks for the authenticated user with optional filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "UUID of the user querying tasks",
                        "format": "uuid",
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by completion status (optional)",
                        "enum": ["pending", "completed", "all"],
                    },
                    "priority": {
                        "type": "string",
                        "description": "Filter by priority (optional)",
                        "enum": ["low", "medium", "high"],
                    },
                    "tag": {
                        "type": "string",
                        "description": "Filter by tag (optional)",
                    },
                },
                "required": ["user_id"],
            },
        ),
        types.Tool(
            name="update_task",
            description="Update an existing task (user can only update their own tasks)",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "UUID of the user updating the task",
                        "format": "uuid",
                    },
                    "task_id": {
                        "type": "string",
                        "description": "UUID of the task to update",
                        "format": "uuid",
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (optional)",
                        "minLength": 1,
                        "maxLength": 200,
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description (optional)",
                        "maxLength": 2000,
                    },
                    "priority": {
                        "type": "string",
                        "description": "New priority level (optional)",
                        "enum": ["low", "medium", "high"],
                    },
                    "due_date": {
                        "type": "string",
                        "description": "New due date in ISO 8601 format (optional)",
                        "format": "date-time",
                    },
                    "tags": {
                        "type": "array",
                        "description": "New list of tags (optional)",
                        "items": {"type": "string"},
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
        types.Tool(
            name="complete_task",
            description="Mark a task as completed (user can only complete their own tasks)",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "UUID of the user completing the task",
                        "format": "uuid",
                    },
                    "task_id": {
                        "type": "string",
                        "description": "UUID of the task to complete",
                        "format": "uuid",
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
        types.Tool(
            name="delete_task",
            description="Delete a task (user can only delete their own tasks)",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "UUID of the user deleting the task",
                        "format": "uuid",
                    },
                    "task_id": {
                        "type": "string",
                        "description": "UUID of the task to delete",
                        "format": "uuid",
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any]
) -> list[types.TextContent]:
    """
    Route tool calls to appropriate handlers.
    All handlers enforce user_id isolation and return structured responses.
    """
    try:
        if name == "add_task":
            return await handle_add_task(arguments)
        elif name == "list_tasks":
            return await handle_list_tasks(arguments)
        elif name == "update_task":
            return await handle_update_task(arguments)
        elif name == "complete_task":
            return await handle_complete_task(arguments)
        elif name == "delete_task":
            return await handle_delete_task(arguments)
        else:
            return [
                types.TextContent(
                    type="text",
                    text=f'{{"error": "UNKNOWN_TOOL", "message": "Tool {name} not found"}}',
                )
            ]
    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f'{{"error": "INTERNAL_ERROR", "message": "{str(e)}"}}',
            )
        ]


async def run():
    """
    Run the MCP server with stdio transport.
    This allows the server to communicate via standard input/output.
    """
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="todo-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    """Entry point for MCP server."""
    asyncio.run(run())


if __name__ == "__main__":
    main()
