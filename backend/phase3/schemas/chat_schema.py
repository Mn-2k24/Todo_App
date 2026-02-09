"""
Pydantic schemas for Phase III Chat API.

Request and response models for POST /api/{user_id}/chat endpoint.
"""

from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ToolCall(BaseModel):
    """
    Represents a single MCP tool call executed by the AI agent.
    """
    tool_name: str = Field(..., description="Name of the MCP tool called")
    parameters: dict = Field(..., description="Parameters passed to the tool")
    result: dict = Field(..., description="Result returned by the tool")


class ChatRequest(BaseModel):
    """
    Request schema for POST /api/{user_id}/chat endpoint.

    Fields:
    - message: User's natural language message (required, 1-2000 chars)
    - conversation_id: Optional UUID to continue existing conversation
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's natural language message"
    )
    conversation_id: Optional[UUID] = Field(
        default=None,
        description="Optional conversation ID to continue existing conversation"
    )

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        """Validate message is not just whitespace."""
        if not v.strip():
            raise ValueError("Message cannot be empty or only whitespace")
        return v.strip()


class ChatResponse(BaseModel):
    """
    Response schema for POST /api/{user_id}/chat endpoint.

    Fields:
    - conversation_id: UUID of the conversation (new or existing)
    - message_id: UUID of the assistant's response message
    - response: Assistant's natural language response
    - tool_calls: List of MCP tools executed (with parameters and results)
    - created_at: Timestamp of the assistant's response
    """
    conversation_id: UUID = Field(..., description="UUID of the conversation")
    message_id: UUID = Field(..., description="UUID of the assistant's message")
    response: str = Field(..., description="Assistant's natural language response")
    tool_calls: list[ToolCall] = Field(
        default_factory=list,
        description="List of MCP tools executed by the agent"
    )
    created_at: datetime = Field(..., description="Timestamp of the response")

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                "message_id": "123e4567-e89b-12d3-a456-426614174001",
                "response": "I've added the task 'Buy groceries' for tomorrow.",
                "tool_calls": [
                    {
                        "tool_name": "add_task",
                        "parameters": {
                            "user_id": "user_123",
                            "title": "Buy groceries",
                            "due_date": "2026-01-24T23:59:59Z"
                        },
                        "result": {
                            "id": 42,
                            "title": "Buy groceries",
                            "completed": False
                        }
                    }
                ],
                "created_at": "2026-01-23T10:30:00Z"
            }
        }


class ErrorResponse(BaseModel):
    """
    Error response schema for all API errors.

    Fields:
    - error: Human-readable error message
    - code: Error code (e.g., INVALID_INPUT, UNAUTHORIZED, INTERNAL_ERROR)
    - details: Optional additional details for debugging
    - message: Optional user-friendly message
    """
    error: str = Field(..., description="Human-readable error message")
    code: str = Field(..., description="Error code")
    details: Optional[str] = Field(default=None, description="Additional error details")
    message: Optional[str] = Field(default=None, description="User-friendly message")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Validation failed",
                "code": "INVALID_INPUT",
                "details": "Message text is required",
                "message": "Please provide a valid message"
            }
        }
