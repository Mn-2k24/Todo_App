"""
Conversation model for Phase III AI Chatbot.

Represents a multi-turn chat session between user and AI agent.
"""

from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Index

if TYPE_CHECKING:
    from .message import Message
    from ...src.models.user import User  # Phase II User model


class Conversation(SQLModel, table=True):
    """
    Conversation model - represents a chat session.

    Relationships:
    - Belongs to one User (Phase II model)
    - Has many Messages (Phase III model)

    Indexes:
    - Primary key: id (UUID)
    - Foreign key index: user_id
    - Composite index: (user_id, created_at) for listing user's conversations
    """

    __tablename__ = "conversations"

    # Primary key
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    # Foreign keys
    user_id: UUID = Field(foreign_key="users.id", index=True)

    # Attributes
    title: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    # Relationships
    # user: "User" = Relationship(back_populates="conversations")  # Uncomment when Phase II User model updated
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    # Table indexes
    __table_args__ = (
        Index("ix_conversations_user_created", "user_id", "created_at"),
    )


# Note: Phase II User model needs to be updated to include:
# conversations: list["Conversation"] = Relationship(back_populates="user")
