"""Task display formatting for Phase I Todo App.

This module handles formatting and displaying tasks in human-readable format.
"""

from typing import List
from src.models.task import Task


def display_tasks(tasks: List[Task]) -> None:
    """Display all tasks in a formatted list.

    Args:
        tasks: List of tasks to display

    Displays:
        - "No tasks found." if list is empty
        - "Tasks:" header followed by formatted task list
        - Format: "ID. [Status] Description"
    """
    if len(tasks) == 0:
        print("No tasks found.")
        return

    print("Tasks:")
    for task in tasks:
        print(f"{task.id}. [{task.status}] {task.description}")
