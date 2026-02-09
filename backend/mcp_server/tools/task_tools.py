"""
MCP Task Management Tools

All tools enforce strict user_id isolation - users can only access their own tasks.
Each tool returns JSON-formatted responses for easy parsing by the AI agent.
"""

import json
from datetime import date, datetime
from typing import Any
from uuid import UUID

import mcp.types as types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mcp_server.config import AsyncSessionLocal
from src.models.task import Priority, Task


# Error codes for consistent error handling
class ErrorCode:
    """Standard error codes for MCP tool responses."""

    TASK_NOT_FOUND = "TASK_NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_INPUT = "INVALID_INPUT"
    INTERNAL_ERROR = "INTERNAL_ERROR"


def format_task_response(task: Task) -> dict[str, Any]:
    """
    Format a Task model instance as a JSON-serializable dict.

    Args:
        task: SQLModel Task instance

    Returns:
        Dictionary with task data suitable for JSON serialization
    """
    return {
        "id": str(task.id),
        "user_id": str(task.user_id),
        "description": task.description,
        "completed": task.completed,
        "priority": task.priority.value,
        "tags": task.tags,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }


def format_error_response(code: str, message: str, details: str = "") -> str:
    """
    Format an error response as JSON.

    Args:
        code: Error code constant
        message: Human-readable error message
        details: Optional additional details

    Returns:
        JSON string with error information
    """
    error_obj = {"error": code, "message": message}
    if details:
        error_obj["details"] = details
    return json.dumps(error_obj)


async def handle_add_task(arguments: dict[str, Any]) -> list[types.TextContent]:
    """
    Create a new task for the authenticated user.

    Args:
        arguments: {
            "user_id": str (UUID),
            "title": str (1-200 chars),
            "description": str (optional, max 2000 chars),
            "priority": str (low|medium|high, optional),
            "due_date": str (ISO 8601 date, optional),
            "tags": list[str] (optional)
        }

    Returns:
        JSON response with created task data or error

    Note: MCP "title" maps to Task "description" field in Phase II schema
    """
    async with AsyncSessionLocal() as session:
        try:
            # Validate and parse user_id
            try:
                user_id = UUID(arguments["user_id"])
            except (KeyError, ValueError) as e:
                return [
                    types.TextContent(
                        type="text",
                        text=format_error_response(
                            ErrorCode.INVALID_INPUT,
                            "Invalid user_id",
                            str(e),
                        ),
                    )
                ]

            # Extract and validate title (maps to description in Task model)
            title = arguments.get("title", "").strip()
            if not title or len(title) > 500:
                return [
                    types.TextContent(
                        type="text",
                        text=format_error_response(
                            ErrorCode.INVALID_INPUT,
                            "Title is required and must be 1-500 characters",
                        ),
                    )
                ]

            # Parse optional fields
            priority_str = arguments.get("priority", "medium").lower()
            try:
                priority = Priority(priority_str)
            except ValueError:
                priority = Priority.MEDIUM

            due_date_val = None
            if due_date_str := arguments.get("due_date"):
                try:
                    # Parse ISO 8601 date or datetime, extract date part
                    if "T" in due_date_str:
                        due_date_val = datetime.fromisoformat(
                            due_date_str.replace("Z", "+00:00")
                        ).date()
                    else:
                        due_date_val = date.fromisoformat(due_date_str)
                except ValueError:
                    return [
                        types.TextContent(
                            type="text",
                            text=format_error_response(
                                ErrorCode.INVALID_INPUT,
                                "Invalid due_date format. Use ISO 8601 (YYYY-MM-DD)",
                            ),
                        )
                    ]

            tags = arguments.get("tags", [])
            if not isinstance(tags, list):
                tags = []

            # Create new task with user_id isolation
            new_task = Task(
                user_id=user_id,
                description=title,
                priority=priority,
                due_date=due_date_val,
                tags=tags,
                completed=False,
            )

            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)

            # Return success response
            response_data = {
                "success": True,
                "task": format_task_response(new_task),
                "message": "Task created successfully",
            }

            return [types.TextContent(type="text", text=json.dumps(response_data))]

        except Exception as e:
            await session.rollback()
            return [
                types.TextContent(
                    type="text",
                    text=format_error_response(
                        ErrorCode.INTERNAL_ERROR,
                        "Failed to create task",
                        str(e),
                    ),
                )
            ]


async def handle_list_tasks(arguments: dict[str, Any]) -> list[types.TextContent]:
    """
    List tasks for the authenticated user with optional filtering.

    Args:
        arguments: {
            "user_id": str (UUID),
            "status": str (pending|completed|all, optional),
            "priority": str (low|medium|high, optional),
            "tag": str (optional)
        }

    Returns:
        JSON response with array of tasks or error

    User isolation: Only returns tasks where task.user_id == arguments.user_id
    """
    async with AsyncSessionLocal() as session:
        try:
            # Validate user_id
            try:
                user_id = UUID(arguments["user_id"])
            except (KeyError, ValueError) as e:
                return [
                    types.TextContent(
                        type="text",
                        text=format_error_response(
                            ErrorCode.INVALID_INPUT,
                            "Invalid user_id",
                            str(e),
                        ),
                    )
                ]

            # Build query with user_id isolation (CRITICAL: prevents cross-user access)
            query = select(Task).where(Task.user_id == user_id)

            # Apply status filter
            status = arguments.get("status", "all").lower()
            if status == "pending":
                query = query.where(Task.completed == False)  # noqa: E712
            elif status == "completed":
                query = query.where(Task.completed == True)  # noqa: E712

            # Apply priority filter
            if priority_str := arguments.get("priority"):
                try:
                    priority = Priority(priority_str.lower())
                    query = query.where(Task.priority == priority)
                except ValueError:
                    pass  # Ignore invalid priority, don't filter

            # Apply tag filter
            if tag := arguments.get("tag"):
                # PostgreSQL JSON array contains check
                query = query.where(Task.tags.contains([tag]))

            # Order by created_at descending (newest first)
            query = query.order_by(Task.created_at.desc())

            # Execute query
            result = await session.execute(query)
            tasks = result.scalars().all()

            # Format response
            response_data = {
                "success": True,
                "tasks": [format_task_response(task) for task in tasks],
                "count": len(tasks),
                "filters": {
                    "status": status,
                    "priority": arguments.get("priority"),
                    "tag": arguments.get("tag"),
                },
            }

            return [types.TextContent(type="text", text=json.dumps(response_data))]

        except Exception as e:
            return [
                types.TextContent(
                    type="text",
                    text=format_error_response(
                        ErrorCode.INTERNAL_ERROR,
                        "Failed to list tasks",
                        str(e),
                    ),
                )
            ]


async def handle_update_task(arguments: dict[str, Any]) -> list[types.TextContent]:
    """
    Update an existing task (user can only update their own tasks).

    Args:
        arguments: {
            "user_id": str (UUID),
            "task_id": str (UUID),
            "title": str (optional, 1-500 chars),
            "description": str (optional, ignored - Phase II only has one field),
            "priority": str (optional, low|medium|high),
            "due_date": str (optional, ISO 8601 date),
            "tags": list[str] (optional)
        }

    Returns:
        JSON response with updated task data or error

    User isolation: Only updates task if task.user_id == arguments.user_id
    """
    async with AsyncSessionLocal() as session:
        try:
            # Validate IDs
            try:
                user_id = UUID(arguments["user_id"])
                task_id = UUID(arguments["task_id"])
            except (KeyError, ValueError) as e:
                return [
                    types.TextContent(
                        type="text",
                        text=format_error_response(
                            ErrorCode.INVALID_INPUT,
                            "Invalid user_id or task_id",
                            str(e),
                        ),
                    )
                ]

            # Fetch task with user_id isolation (CRITICAL: prevents unauthorized updates)
            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()

            if not task:
                return [
                    types.TextContent(
                        type="text",
                        text=format_error_response(
                            ErrorCode.TASK_NOT_FOUND,
                            f"Task {task_id} not found or unauthorized",
                        ),
                    )
                ]

            # Update fields if provided
            if title := arguments.get("title"):
                title = title.strip()
                if len(title) > 500:
                    return [
                        types.TextContent(
                            type="text",
                            text=format_error_response(
                                ErrorCode.INVALID_INPUT,
                                "Title must be max 500 characters",
                            ),
                        )
                    ]
                task.description = title

            if priority_str := arguments.get("priority"):
                try:
                    task.priority = Priority(priority_str.lower())
                except ValueError:
                    pass  # Ignore invalid priority

            if "due_date" in arguments:
                due_date_str = arguments["due_date"]
                if due_date_str:
                    try:
                        if "T" in due_date_str:
                            task.due_date = datetime.fromisoformat(
                                due_date_str.replace("Z", "+00:00")
                            ).date()
                        else:
                            task.due_date = date.fromisoformat(due_date_str)
                    except ValueError:
                        return [
                            types.TextContent(
                                type="text",
                                text=format_error_response(
                                    ErrorCode.INVALID_INPUT,
                                    "Invalid due_date format",
                                ),
                            )
                        ]
                else:
                    task.due_date = None

            if "tags" in arguments:
                tags = arguments["tags"]
                if isinstance(tags, list):
                    task.tags = tags

            # Update timestamp
            task.updated_at = datetime.utcnow()

            await session.commit()
            await session.refresh(task)

            # Return success response
            response_data = {
                "success": True,
                "task": format_task_response(task),
                "message": "Task updated successfully",
            }

            return [types.TextContent(type="text", text=json.dumps(response_data))]

        except Exception as e:
            await session.rollback()
            return [
                types.TextContent(
                    type="text",
                    text=format_error_response(
                        ErrorCode.INTERNAL_ERROR,
                        "Failed to update task",
                        str(e),
                    ),
                )
            ]


async def handle_complete_task(arguments: dict[str, Any]) -> list[types.TextContent]:
    """
    Mark a task as completed (user can only complete their own tasks).

    Args:
        arguments: {
            "user_id": str (UUID),
            "task_id": str (UUID)
        }

    Returns:
        JSON response with updated task data or error

    User isolation: Only completes task if task.user_id == arguments.user_id
    """
    async with AsyncSessionLocal() as session:
        try:
            # Validate IDs
            try:
                user_id = UUID(arguments["user_id"])
                task_id = UUID(arguments["task_id"])
            except (KeyError, ValueError) as e:
                return [
                    types.TextContent(
                        type="text",
                        text=format_error_response(
                            ErrorCode.INVALID_INPUT,
                            "Invalid user_id or task_id",
                            str(e),
                        ),
                    )
                ]

            # Fetch task with user_id isolation
            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()

            if not task:
                return [
                    types.TextContent(
                        type="text",
                        text=format_error_response(
                            ErrorCode.TASK_NOT_FOUND,
                            f"Task {task_id} not found or unauthorized",
                        ),
                    )
                ]

            # Mark as completed
            task.completed = True
            task.updated_at = datetime.utcnow()

            await session.commit()
            await session.refresh(task)

            # Return success response
            response_data = {
                "success": True,
                "task": format_task_response(task),
                "message": "Task completed successfully",
            }

            return [types.TextContent(type="text", text=json.dumps(response_data))]

        except Exception as e:
            await session.rollback()
            return [
                types.TextContent(
                    type="text",
                    text=format_error_response(
                        ErrorCode.INTERNAL_ERROR,
                        "Failed to complete task",
                        str(e),
                    ),
                )
            ]


async def handle_delete_task(arguments: dict[str, Any]) -> list[types.TextContent]:
    """
    Delete a task (user can only delete their own tasks).

    Args:
        arguments: {
            "user_id": str (UUID),
            "task_id": str (UUID)
        }

    Returns:
        JSON response with success status or error

    User isolation: Only deletes task if task.user_id == arguments.user_id
    """
    async with AsyncSessionLocal() as session:
        try:
            # Validate IDs
            try:
                user_id = UUID(arguments["user_id"])
                task_id = UUID(arguments["task_id"])
            except (KeyError, ValueError) as e:
                return [
                    types.TextContent(
                        type="text",
                        text=format_error_response(
                            ErrorCode.INVALID_INPUT,
                            "Invalid user_id or task_id",
                            str(e),
                        ),
                    )
                ]

            # Fetch task with user_id isolation
            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()

            if not task:
                return [
                    types.TextContent(
                        type="text",
                        text=format_error_response(
                            ErrorCode.TASK_NOT_FOUND,
                            f"Task {task_id} not found or unauthorized",
                        ),
                    )
                ]

            # Delete the task
            await session.delete(task)
            await session.commit()

            # Return success response
            response_data = {
                "success": True,
                "task_id": str(task_id),
                "message": "Task deleted successfully",
            }

            return [types.TextContent(type="text", text=json.dumps(response_data))]

        except Exception as e:
            await session.rollback()
            return [
                types.TextContent(
                    type="text",
                    text=format_error_response(
                        ErrorCode.INTERNAL_ERROR,
                        "Failed to delete task",
                        str(e),
                    ),
                )
            ]
