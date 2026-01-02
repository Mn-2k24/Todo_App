"""Task model for Phase I Todo App.

This module defines the Task entity with id, description, and status attributes.
"""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique sequential identifier (immutable after creation)
        description: Task text, 1-200 characters after trimming (mutable)
        status: Either "Complete" or "Incomplete" (mutable)
    """
    id: int
    description: str
    status: str  # "Complete" or "Incomplete"
