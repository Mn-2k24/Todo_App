"""Task model for todo items."""

from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from sqlmodel import Column, Field, JSON, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.user import User


class Priority(str, Enum):
    """Task priority levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task(SQLModel, table=True):
    """Task entity owned by a user.

    Attributes:
        id: Unique task identifier (UUID)
        user_id: Foreign key to User (indexed)
        description: Task description (required, max 500 chars)
        completed: Completion status (default False)
        priority: Priority level (High/Medium/Low, default Medium)
        tags: List of tag strings (default empty array)
        due_date: Optional due date (date only, no time)
        created_at: Task creation timestamp (indexed)
        updated_at: Last update timestamp

    Relationships:
        user: Many-to-one relationship with User
    """

    __tablename__ = "tasks"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
    )
    description: str = Field(
        nullable=False,
        max_length=500,
        min_length=1,
    )
    completed: bool = Field(
        default=False,
        nullable=False,
    )
    priority: Priority = Field(
        default=Priority.MEDIUM,
        nullable=False,
    )
    tags: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON),
    )
    due_date: Optional[date] = Field(
        default=None,
        nullable=True,
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )

    # Relationships
    user: "User" = Relationship(back_populates="tasks")

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "660e8400-e29b-41d4-a716-446655440000",
                "description": "Complete project documentation",
                "completed": False,
                "priority": "medium",
                "tags": ["work", "documentation"],
                "due_date": "2026-01-15",
                "created_at": "2026-01-09T12:00:00Z",
                "updated_at": "2026-01-09T12:00:00Z",
            }
        }


class TaskPublic(SQLModel):
    """Public task data."""

    id: UUID
    user_id: UUID
    description: str
    completed: bool
    priority: Priority
    tags: List[str]
    due_date: Optional[date]
    created_at: datetime
    updated_at: datetime


class TaskCreate(SQLModel):
    """Task creation request."""

    description: str = Field(min_length=1, max_length=500)
    priority: Priority = Field(default=Priority.MEDIUM)
    tags: List[str] = Field(default_factory=list)
    due_date: Optional[date] = None


class TaskUpdate(SQLModel):
    """Task update request (all fields optional)."""

    description: Optional[str] = Field(default=None, min_length=1, max_length=500)
    completed: Optional[bool] = None
    priority: Optional[Priority] = None
    tags: Optional[List[str]] = None
    due_date: Optional[date] = None
