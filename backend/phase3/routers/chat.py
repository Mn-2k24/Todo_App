"""
Phase III Chat API router.

Implements POST /api/{user_id}/chat endpoint that:
1. Authenticates user via JWT token (Authorization header or httpOnly cookie)
2. Validates user_id in path matches JWT user_id (prevents impersonation)
3. Processes natural language message through AI agent
4. Executes MCP tool calls for task management
5. Persists conversation history
6. Returns assistant response with tool execution results

Security:
- JWT authentication required (401 if missing/invalid)
- User isolation enforced (403 if path user_id != JWT user_id)
- All tool calls automatically scoped to authenticated user_id

Architecture:
- Stateless: Each request loads conversation history from database
- 7-step pipeline: Validate → Load → Persist User → Invoke Agent → Execute Tools → Persist Assistant → Return
- Database-backed conversation persistence (supports multi-turn)
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.auth.dependencies import get_current_user_id
from phase3.schemas.chat_schema import ChatRequest, ChatResponse, ErrorResponse
from phase3.services.chat_service import (
    ChatService,
    get_chat_service,
    ChatServiceError,
    ConversationNotFoundError,
    UnauthorizedAccessError,
)

router = APIRouter(prefix="/api", tags=["chat"])


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Process chat message",
    description="Process natural language message through AI agent and execute task management operations",
    responses={
        200: {
            "description": "Message processed successfully",
            "model": ChatResponse,
        },
        400: {
            "description": "Invalid input (empty message, invalid conversation_id)",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "error": "Validation failed",
                        "code": "INVALID_INPUT",
                        "details": "Message cannot be empty",
                        "message": "Please provide a valid message",
                    }
                }
            },
        },
        401: {
            "description": "Not authenticated (missing or invalid JWT token)",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "error": "Not authenticated",
                        "code": "UNAUTHORIZED",
                        "details": "JWT token missing or invalid",
                        "message": "Please log in to continue",
                    }
                }
            },
        },
        403: {
            "description": "Forbidden (user_id in path does not match JWT user_id)",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "error": "Access denied",
                        "code": "FORBIDDEN",
                        "details": "User ID mismatch: path user_id does not match authenticated user",
                        "message": "You can only access your own conversations",
                    }
                }
            },
        },
        404: {
            "description": "Conversation not found",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "error": "Conversation not found",
                        "code": "NOT_FOUND",
                        "details": "No conversation exists with the given ID",
                        "message": "The conversation you're looking for doesn't exist",
                    }
                }
            },
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "error": "Internal server error",
                        "code": "INTERNAL_ERROR",
                        "details": "An unexpected error occurred while processing your request",
                        "message": "Please try again later",
                    }
                }
            },
        },
    },
)
async def chat(
    user_id: UUID,
    request: ChatRequest,
    authenticated_user_id: UUID = Depends(get_current_user_id),
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """Process chat message through AI agent and execute task operations.

    This endpoint implements Phase III chat functionality:
    1. Validates JWT authentication (get_current_user_id dependency)
    2. Validates user_id in path matches JWT user_id (prevents impersonation)
    3. Invokes ChatService 7-step pipeline:
       - Step 1: Validate request (message length, conversation_id format)
       - Step 2: Load conversation history (or create new conversation)
       - Step 3: Persist user message to database
       - Step 4: Invoke AI agent (intent recognition, entity extraction, tool selection)
       - Step 5: Execute MCP tool calls (add_task, list_tasks, etc.)
       - Step 6: Persist assistant response with tool results
       - Step 7: Return response to client
    4. Returns assistant response with natural language + tool execution results

    Args:
        user_id: User ID from path parameter (must match JWT user_id)
        request: ChatRequest with message and optional conversation_id
        authenticated_user_id: User ID extracted from JWT token (injected by dependency)
        chat_service: ChatService instance (injected by dependency)

    Returns:
        ChatResponse: Assistant response with conversation_id, message_id, response text, tool_calls, timestamp

    Raises:
        HTTPException 400: Invalid input (Pydantic validation or ChatServiceError)
        HTTPException 401: Not authenticated (handled by get_current_user_id dependency)
        HTTPException 403: User ID mismatch (path user_id != JWT user_id)
        HTTPException 404: Conversation not found (ConversationNotFoundError)
        HTTPException 500: Internal server error (unexpected exceptions)

    Example:
        POST /api/550e8400-e29b-41d4-a716-446655440000/chat
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        Content-Type: application/json

        {
            "message": "Add a task to buy groceries tomorrow",
            "conversation_id": null
        }

        Response 200:
        {
            "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
            "message_id": "123e4567-e89b-12d3-a456-426614174001",
            "response": "I've added the task 'Buy groceries' with due date tomorrow.",
            "tool_calls": [
                {
                    "tool_name": "add_task",
                    "parameters": {
                        "user_id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Buy groceries",
                        "due_date": "2026-01-28T23:59:59Z",
                        "priority": "medium"
                    },
                    "result": {
                        "success": true,
                        "task": {
                            "id": 42,
                            "title": "Buy groceries",
                            "completed": false,
                            "priority": "medium",
                            "due_date": "2026-01-28T23:59:59Z"
                        }
                    }
                }
            ],
            "created_at": "2026-01-27T10:30:00Z"
        }
    """
    # Validate user_id in path matches authenticated user_id from JWT
    # This prevents users from impersonating other users by changing the path parameter
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse(
                error="Access denied",
                code="FORBIDDEN",
                details=f"User ID mismatch: path user_id={user_id}, JWT user_id={authenticated_user_id}",
                message="You can only access your own conversations",
            ).model_dump(),
        )

    try:
        # Invoke ChatService to process message through 7-step pipeline
        response = await chat_service.process_chat_message(user_id, request)
        return response

    except ConversationNotFoundError as e:
        # Conversation ID provided but doesn't exist in database
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(
                error="Conversation not found",
                code="NOT_FOUND",
                details=str(e),
                message="The conversation you're looking for doesn't exist",
            ).model_dump(),
        )

    except UnauthorizedAccessError as e:
        # User tried to access another user's conversation
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse(
                error="Access denied",
                code="FORBIDDEN",
                details=str(e),
                message="You don't have permission to access this conversation",
            ).model_dump(),
        )

    except ChatServiceError as e:
        # Other chat service errors (validation, etc.)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(
                error="Bad request",
                code="INVALID_INPUT",
                details=str(e),
                message="There was a problem processing your request",
            ).model_dump(),
        )

    except Exception as e:
        # Unexpected errors (database, network, etc.)
        # Log the error in production
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="Internal server error",
                code="INTERNAL_ERROR",
                details=f"Unexpected error: {str(e)}",
                message="An unexpected error occurred. Please try again later.",
            ).model_dump(),
        )
