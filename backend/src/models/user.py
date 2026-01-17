"""User model for authentication and task ownership."""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.task import Task


class User(SQLModel, table=True):
    """User entity managed by Better Auth.

    Attributes:
        id: Unique user identifier (UUID)
        email: User email address (unique, indexed)
        password_hash: Hashed password (bcrypt)
        created_at: Account creation timestamp

    Relationships:
        tasks: One-to-many relationship with Task
    """

    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    email: str = Field(
        unique=True,
        index=True,
        nullable=False,
        max_length=255,
        sa_column_kwargs={"unique": True},
    )
    name: str = Field(
        nullable=False,
        min_length=2,
        max_length=100,
        description="User's full name (2-100 characters)",
    )
    password_hash: str = Field(
        nullable=False,
        max_length=255,
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    tasks: List["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "created_at": "2026-01-09T12:00:00Z",
            }
        }


class UserPublic(SQLModel):
    """Public user data (excludes password_hash)."""

    id: UUID
    email: str
    name: str
    created_at: datetime


class UserCreate(SQLModel):
    """User creation request."""

    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=100)


class UserLogin(SQLModel):
    """User login request."""

    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=100)
