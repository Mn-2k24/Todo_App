"""
Message model for Phase III AI Chatbot.

Represents an individual message within a Conversation.
"""

from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Index

if TYPE_CHECKING:
    from .conversation import Conversation


class Message(SQLModel, table=True):
    """
    Message model - represents a single message in a conversation.

    Relationships:
    - Belongs to one Conversation (Phase III model)

    Indexes:
    - Primary key: id (UUID)
    - Foreign key index: conversation_id
    - Composite index: (conversation_id, created_at) for loading messages in order

    Constraints:
    - role must be one of: "user", "assistant"
    - content cannot be null or empty
    """

    __tablename__ = "messages"

    # Primary key
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    # Foreign keys
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)

    # Attributes
    role: str = Field(...)  # "user" | "assistant"
    content: str = Field(..., max_length=10000)  # Message text
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls executed
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")

    # Table indexes
    __table_args__ = (
        Index("ix_messages_conversation_created", "conversation_id", "created_at"),
    )


# tool_calls JSON Structure (when role="assistant"):
# [
#   {
#     "tool_name": "add_task",
#     "parameters": {
#       "user_id": "...",
#       "title": "...",
#       "priority": "..."
#     },
#     "result": {
#       "id": 42,
#       "title": "...",
#       "completed": false,
#       ...
#     }
#   }
# ]
