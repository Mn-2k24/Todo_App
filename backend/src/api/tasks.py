"""
Task API endpoints.
Implements REST contract per contracts/tasks.yaml.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.database import get_session
from src.models.task import Priority
from src.models.user import User
from src.schemas.task import (
    TaskCreateRequest,
    TaskResponse,
    TaskToggleResponse,
    TaskUpdateRequest,
)
from src.services import task_service

router = APIRouter()


@router.get(
    "",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all tasks",
    description="Retrieve all tasks for the authenticated user with optional filtering. Returns tasks ordered by creation date (newest first).",
)
async def get_tasks(
    priority: Optional[Priority] = Query(None, description="Filter by priority (high/medium/low) per FR-028"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated list per FR-029)"),
    search: Optional[str] = Query(None, description="Search tasks by description text per FR-026"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by completion status (completed/incomplete) per FR-027"),
    sort_by: Optional[str] = Query(None, description="Sort by field (title/created/due_date/priority) per FR-032 to FR-035"),
    order: Optional[str] = Query("desc", description="Sort order (asc/desc), defaults to desc"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[TaskResponse]:
    """
    Get all tasks for authenticated user with optional filtering.
    Enforces data isolation - only returns user's own tasks.

    Args:
        priority: Optional priority filter (high/medium/low)
        tags: Optional tag filter (comma-separated list)
        search: Optional text search in description (FR-026)
        status_filter: Optional status filter (completed/incomplete) (FR-027)

    Returns:
        200: List of tasks
        401: Unauthorized (invalid/missing token)
    """
    # Parse comma-separated tags string into list
    tags_list = [tag.strip() for tag in tags.split(",")] if tags else None

    # Parse status filter to boolean
    completed_filter: Optional[bool] = None
    if status_filter:
        if status_filter.lower() == "completed":
            completed_filter = True
        elif status_filter.lower() == "incomplete":
            completed_filter = False

    return await task_service.get_tasks(
        user_id=current_user.id,
        session=session,
        priority=priority,
        tags=tags_list,
        search=search,
        completed=completed_filter,
        sort_by=sort_by,
        order=order,
    )


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create task",
    description="Create a new task for the authenticated user.",
)
async def create_task(
    task_data: TaskCreateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Create new task for authenticated user.

    Args:
        task_data: Task creation request with description

    Returns:
        201: Created task
        400: Invalid input (empty description)
        401: Unauthorized (invalid/missing token)
    """
    return await task_service.create_task(
        task_data=task_data,
        user_id=current_user.id,
        session=session,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get task by ID",
    description="Retrieve a single task by its unique identifier. User must own the task.",
)
async def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Get single task by ID with ownership verification.

    Args:
        task_id: Task unique identifier

    Returns:
        200: Task data
        401: Unauthorized (invalid/missing token)
        403: Forbidden (task belongs to different user)
        404: Task not found
    """
    return await task_service.get_task_by_id(
        task_id=task_id,
        user_id=current_user.id,
        session=session,
    )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update task",
    description="Update an existing task. User must own the task. All fields are optional.",
)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Update existing task with ownership verification.

    Args:
        task_id: Task unique identifier
        task_data: Task update request with optional fields

    Returns:
        200: Updated task
        400: Invalid input (empty description)
        401: Unauthorized (invalid/missing token)
        403: Forbidden (task belongs to different user)
        404: Task not found
    """
    return await task_service.update_task(
        task_id=task_id,
        task_data=task_data,
        user_id=current_user.id,
        session=session,
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete an existing task. User must own the task.",
)
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Delete task with ownership verification.

    Args:
        task_id: Task unique identifier

    Returns:
        204: Task deleted successfully
        401: Unauthorized (invalid/missing token)
        403: Forbidden (task belongs to different user)
        404: Task not found
    """
    await task_service.delete_task(
        task_id=task_id,
        user_id=current_user.id,
        session=session,
    )


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Toggle task completion",
    description="Toggle the completion status of a task. User must own the task.",
)
async def toggle_completion(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Toggle task completion status.

    Args:
        task_id: Task unique identifier

    Returns:
        200: Updated task with new completion status
        401: Unauthorized (invalid/missing token)
        403: Forbidden (task belongs to different user)
        404: Task not found
    """
    return await task_service.toggle_completion(
        task_id=task_id,
        user_id=current_user.id,
        session=session,
    )
