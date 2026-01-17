"""
Task business logic service.
Handles CRUD operations with user isolation per FR-038, FR-050.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.task import Priority, Task
from src.schemas.task import TaskCreateRequest, TaskResponse, TaskUpdateRequest
from src.utils.errors import ForbiddenError, NotFoundError, ValidationError


async def create_task(
    task_data: TaskCreateRequest,
    user_id: UUID,
    session: AsyncSession,
) -> TaskResponse:
    """
    Create new task for authenticated user.

    Args:
        task_data: Task creation request with description
        user_id: ID of authenticated user (owner)
        session: Database session

    Returns:
        TaskResponse with created task data

    Raises:
        ValidationError: If description is empty or invalid
    """
    # Validate description
    if not task_data.description or not task_data.description.strip():
        raise ValidationError(
            message="Task description cannot be empty",
            code="INVALID_INPUT",
            details={"field": "description"},
        )

    # Create new task
    new_task = Task(
        user_id=user_id,
        description=task_data.description.strip(),
        completed=False,
        priority=task_data.priority,  # Priority validated by Pydantic enum per FR-019
        tags=task_data.tags,  # Tags array per FR-022
        due_date=task_data.due_date,  # Optional due date per FR-025
    )

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    return TaskResponse.model_validate(new_task)


async def get_tasks(
    user_id: UUID,
    session: AsyncSession,
    priority: Optional[Priority] = None,
    tags: Optional[List[str]] = None,
    search: Optional[str] = None,
    completed: Optional[bool] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = "desc",
) -> List[TaskResponse]:
    """
    Get all tasks for authenticated user with optional filtering and sorting.
    Enforces data isolation - only returns user's own tasks per FR-050.

    Args:
        user_id: ID of authenticated user
        session: Database session
        priority: Optional priority filter per FR-028
        tags: Optional tag filter (comma-separated list per FR-029)
        search: Optional text search in description per FR-026
        completed: Optional completion status filter per FR-027
        sort_by: Optional sort field (title/created/due_date/priority) per FR-032 to FR-035
        order: Sort order (asc/desc), defaults to desc

    Returns:
        List of TaskResponse objects
    """
    query = select(Task).where(Task.user_id == user_id)

    # Apply priority filter if provided per FR-028
    if priority is not None:
        query = query.where(Task.priority == priority)

    # Apply text search filter if provided per FR-026
    if search is not None and search.strip():
        query = query.where(Task.description.ilike(f"%{search.strip()}%"))

    # Apply completion status filter if provided per FR-027
    if completed is not None:
        query = query.where(Task.completed == completed)

    # Apply sorting per FR-032 to FR-035
    is_ascending = order and order.lower() == "asc"

    if sort_by == "title":
        # Sort by description (title) alphabetically per FR-032
        query = query.order_by(Task.description.asc() if is_ascending else Task.description.desc())
    elif sort_by == "created":
        # Sort by created_at newest first per FR-033
        query = query.order_by(Task.created_at.asc() if is_ascending else Task.created_at.desc())
    elif sort_by == "due_date":
        # Sort by due_date nearest first per FR-034
        # NULL values last in both ASC and DESC
        if is_ascending:
            query = query.order_by(Task.due_date.asc().nulls_last())
        else:
            query = query.order_by(Task.due_date.desc().nulls_last())
    elif sort_by == "priority":
        # Sort by priority High→Medium→Low per FR-035
        # Map: high=0, medium=1, low=2 for sorting
        # Use CASE statement for custom priority order
        from sqlalchemy import case
        priority_order = case(
            (Task.priority == Priority.HIGH, 0),
            (Task.priority == Priority.MEDIUM, 1),
            (Task.priority == Priority.LOW, 2),
            else_=3
        )
        query = query.order_by(priority_order.asc() if is_ascending else priority_order.desc())
    else:
        # Default: sort by created_at newest first
        query = query.order_by(Task.created_at.desc())

    result = await session.execute(query)
    tasks = result.scalars().all()

    # Apply tags filter if provided per FR-029 (client-side filtering)
    # Filter for tasks that have ANY of the specified tags
    if tags is not None and len(tags) > 0:
        tasks = [
            task for task in tasks
            if any(tag in task.tags for tag in tags)
        ]

    return [TaskResponse.model_validate(task) for task in tasks]


async def get_task_by_id(
    task_id: UUID,
    user_id: UUID,
    session: AsyncSession,
) -> TaskResponse:
    """
    Get single task by ID with ownership verification.

    Args:
        task_id: Task unique identifier
        user_id: ID of authenticated user
        session: Database session

    Returns:
        TaskResponse with task data

    Raises:
        NotFoundError: If task doesn't exist
        ForbiddenError: If task belongs to different user (FR-050)
    """
    result = await session.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise NotFoundError(
            message="Task not found",
            code="TASK_NOT_FOUND",
        )

    # Verify ownership per FR-050
    if task.user_id != user_id:
        raise ForbiddenError(
            message="You don't have permission to access this task",
            code="FORBIDDEN",
        )

    return TaskResponse.model_validate(task)


async def update_task(
    task_id: UUID,
    task_data: TaskUpdateRequest,
    user_id: UUID,
    session: AsyncSession,
) -> TaskResponse:
    """
    Update existing task with ownership verification.

    Args:
        task_id: Task unique identifier
        task_data: Task update request with optional fields
        user_id: ID of authenticated user
        session: Database session

    Returns:
        TaskResponse with updated task data

    Raises:
        NotFoundError: If task doesn't exist
        ForbiddenError: If task belongs to different user (FR-050)
        ValidationError: If update data is invalid
    """
    # Fetch task with ownership check
    result = await session.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise NotFoundError(
            message="Task not found",
            code="TASK_NOT_FOUND",
        )

    # Verify ownership per FR-050
    if task.user_id != user_id:
        raise ForbiddenError(
            message="You don't have permission to modify this task",
            code="FORBIDDEN",
        )

    # Update fields if provided
    if task_data.description is not None:
        if not task_data.description.strip():
            raise ValidationError(
                message="Task description cannot be empty",
                code="INVALID_INPUT",
                details={"field": "description"},
            )
        task.description = task_data.description.strip()

    if task_data.completed is not None:
        task.completed = task_data.completed

    if task_data.priority is not None:
        task.priority = task_data.priority  # Priority validated by Pydantic enum per FR-019

    if task_data.tags is not None:
        task.tags = task_data.tags  # Tags array per FR-023

    if task_data.due_date is not None:
        task.due_date = task_data.due_date  # Optional due date per FR-025

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return TaskResponse.model_validate(task)


async def delete_task(
    task_id: UUID,
    user_id: UUID,
    session: AsyncSession,
) -> None:
    """
    Delete task with ownership verification.

    Args:
        task_id: Task unique identifier
        user_id: ID of authenticated user
        session: Database session

    Raises:
        NotFoundError: If task doesn't exist
        ForbiddenError: If task belongs to different user (FR-050)
    """
    # Fetch task with ownership check
    result = await session.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise NotFoundError(
            message="Task not found",
            code="TASK_NOT_FOUND",
        )

    # Verify ownership per FR-050
    if task.user_id != user_id:
        raise ForbiddenError(
            message="You don't have permission to delete this task",
            code="FORBIDDEN",
        )

    await session.delete(task)
    await session.commit()


async def toggle_completion(
    task_id: UUID,
    user_id: UUID,
    session: AsyncSession,
) -> TaskResponse:
    """
    Toggle task completion status.

    Args:
        task_id: Task unique identifier
        user_id: ID of authenticated user
        session: Database session

    Returns:
        TaskResponse with updated completion status

    Raises:
        NotFoundError: If task doesn't exist
        ForbiddenError: If task belongs to different user (FR-050)
    """
    # Fetch task with ownership check
    result = await session.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise NotFoundError(
            message="Task not found",
            code="TASK_NOT_FOUND",
        )

    # Verify ownership per FR-050
    if task.user_id != user_id:
        raise ForbiddenError(
            message="You don't have permission to modify this task",
            code="FORBIDDEN",
        )

    # Toggle completion
    task.completed = not task.completed

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return TaskResponse.model_validate(task)
