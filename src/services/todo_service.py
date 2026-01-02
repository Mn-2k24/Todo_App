"""Todo service for Phase I Todo App.

This module contains all business logic for CRUD operations on tasks.
Manages global in-memory task storage and ID assignment.
"""

from typing import List, Optional
from src.models.task import Task


# Global state: In-memory task storage
tasks: List[Task] = []

# Global state: Next available task ID (monotonically increasing)
next_task_id: int = 1


def add_task(description: str) -> Optional[Task]:
    """Create and store a new task with the provided description.

    Args:
        description: Task description text (will be trimmed)

    Returns:
        Task: Created task object if successful
        None: If description is empty after trimming

    Side effects:
        - Appends task to global tasks list
        - Increments global next_task_id counter
    """
    global next_task_id

    # Trim whitespace
    description = description.strip()

    # Validate: description must not be empty
    if len(description) == 0:
        return None

    # Create task with auto-assigned ID and "Incomplete" status
    task = Task(id=next_task_id, description=description, status="Incomplete")

    # Append to global task list
    tasks.append(task)

    # Increment ID counter
    next_task_id += 1

    return task


def get_all_tasks() -> List[Task]:
    """Retrieve all tasks from in-memory storage.

    Returns:
        List[Task]: All tasks (ordered by creation/ID)
    """
    return tasks


def get_task_by_id(task_id: int) -> Optional[Task]:
    """Find and return a task by its ID.

    Args:
        task_id: Task ID to search for

    Returns:
        Task: Task object if found
        None: If no task with given ID exists
    """
    for task in tasks:
        if task.id == task_id:
            return task
    return None


def update_task(task_id: int, new_description: str) -> bool:
    """Update the description of an existing task.

    Args:
        task_id: ID of task to update
        new_description: New description text (will be trimmed)

    Returns:
        bool: True if update successful, False if task not found or description invalid

    Preserves:
        - Task ID (immutable)
        - Task status (unchanged during update)
    """
    # Find task
    task = get_task_by_id(task_id)
    if task is None:
        return False

    # Trim and validate new description
    new_description = new_description.strip()
    if len(new_description) == 0:
        return False

    # Update description (ID and status preserved)
    task.description = new_description
    return True


def delete_task(task_id: int) -> bool:
    """Delete a task by its ID.

    Args:
        task_id: ID of task to delete

    Returns:
        bool: True if deletion successful, False if task not found

    Note:
        Deleted IDs are not reused (gap in sequence preserved)
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    tasks.remove(task)
    return True


def mark_task(task_id: int) -> Optional[str]:
    """Toggle task completion status.

    Args:
        task_id: ID of task to mark

    Returns:
        str: New status ("Complete" or "Incomplete") if successful
        None: If task not found

    Preserves:
        - Task ID (immutable)
        - Task description (unchanged during status toggle)
    """
    task = get_task_by_id(task_id)
    if task is None:
        return None

    # Toggle status
    if task.status == "Incomplete":
        task.status = "Complete"
    else:
        task.status = "Incomplete"

    return task.status
