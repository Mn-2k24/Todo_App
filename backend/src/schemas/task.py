"""
Task request and response schemas for API contracts.
Per contracts/tasks.yaml specifications.
"""

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field
from sqlmodel import SQLModel

from src.models.task import Priority


class TaskCreateRequest(SQLModel):
    """Task creation request schema."""

    description: str = Field(
        min_length=1,
        max_length=500,
        description="Task description (1-500 characters)",
    )
    priority: Priority = Field(
        default=Priority.MEDIUM,
        description="Task priority (high/medium/low, defaults to medium per FR-021)",
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Task tags (default empty array per FR-022)",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="Task due date (optional ISO 8601 date per FR-025)",
    )


class TaskUpdateRequest(SQLModel):
    """Task update request schema - all fields optional."""

    description: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
        description="Updated task description (1-500 characters)",
    )
    completed: Optional[bool] = Field(
        default=None,
        description="Completion status",
    )
    priority: Optional[Priority] = Field(
        default=None,
        description="Task priority (high/medium/low)",
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="Task tags (optional array of strings)",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="Task due date (optional ISO 8601 date)",
    )


class TaskResponse(SQLModel):
    """Task response schema - returned from API."""

    id: UUID = Field(description="Task unique identifier")
    user_id: UUID = Field(description="Owner user ID")
    description: str = Field(description="Task description")
    completed: bool = Field(description="Completion status")
    priority: Priority = Field(description="Task priority (high/medium/low)")
    tags: List[str] = Field(default_factory=list, description="Task tags")
    due_date: Optional[date] = Field(default=None, description="Due date (ISO 8601)")
    created_at: datetime = Field(description="Creation timestamp (ISO 8601)")
    updated_at: datetime = Field(description="Last update timestamp (ISO 8601)")

    class Config:
        """Pydantic configuration."""

        from_attributes = True  # Allow ORM mode for SQLModel compatibility


class TaskToggleResponse(SQLModel):
    """Response for task completion toggle."""

    id: UUID = Field(description="Task unique identifier")
    completed: bool = Field(description="New completion status")
