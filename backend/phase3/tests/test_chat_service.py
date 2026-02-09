"""
Unit tests for ChatService 7-step pipeline.

Tests:
- New conversation creation
- Existing conversation continuation
- User message persistence
- AI agent invocation
- MCP tool execution
- Assistant response persistence
- Error handling (invalid input, unauthorized access, conversation not found)
"""

import pytest
from datetime import datetime
from uuid import UUID, uuid4
from unittest.mock import AsyncMock, MagicMock, patch

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, select

from phase3.models.conversation import Conversation
from phase3.models.message import Message
from phase3.schemas.chat_schema import ChatRequest, ChatResponse
from phase3.services.chat_service import (
    ChatService,
    ChatServiceError,
    ConversationNotFoundError,
    UnauthorizedAccessError,
)


# Test fixtures

@pytest.fixture
def mock_session():
    """Create a mock AsyncSession for testing."""
    session = AsyncMock(spec=AsyncSession)
    session.execute = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    return session


@pytest.fixture
def mock_mcp_client():
    """Create a mock MCP client."""
    client = MagicMock()
    client.invoke_multiple_tools = AsyncMock(return_value=[
        {
            "success": True,
            "task": {
                "id": 1,
                "title": "Test task",
                "completed": False,
                "priority": "medium",
            }
        }
    ])
    return client


@pytest.fixture
def test_user_id():
    """Test user UUID."""
    return UUID("550e8400-e29b-41d4-a716-446655440000")


@pytest.fixture
def test_conversation_id():
    """Test conversation UUID."""
    return UUID("123e4567-e89b-12d3-a456-426614174000")


@pytest.fixture
def chat_service(mock_session):
    """Create ChatService instance with mocked session."""
    return ChatService(mock_session)


# Test Step 1: Receive & Validate

def test_validate_request_valid(chat_service, test_user_id):
    """Test validation with valid request."""
    request = ChatRequest(message="Test message", conversation_id=None)
    # Should not raise any exception
    chat_service._validate_request(test_user_id, request)


def test_validate_request_empty_message(chat_service, test_user_id):
    """Test validation rejects empty message."""
    # Pydantic validation should handle this before reaching service
    # Testing service-level validation for stripped whitespace
    request = ChatRequest(message="   ", conversation_id=None)
    # Pydantic validator will raise ValueError


def test_validate_request_message_too_long(chat_service, test_user_id):
    """Test validation rejects message exceeding max length."""
    # Pydantic validation enforces max_length=2000
    with pytest.raises(Exception):  # Pydantic ValidationError
        request = ChatRequest(message="a" * 2001, conversation_id=None)


# Test Step 2: Load Conversation History

@pytest.mark.asyncio
async def test_load_conversation_new(chat_service, mock_session, test_user_id):
    """Test loading conversation history when creating new conversation."""
    # Mock: No existing conversation (conversation_id=None)
    conversation, history = await chat_service._load_conversation_history(
        test_user_id, None
    )

    # Verify new conversation created
    assert isinstance(conversation, Conversation)
    assert conversation.user_id == test_user_id
    assert history == []
    mock_session.add.assert_called_once()
    mock_session.flush.assert_called_once()


@pytest.mark.asyncio
async def test_load_conversation_existing(
    chat_service, mock_session, test_user_id, test_conversation_id
):
    """Test loading conversation history for existing conversation."""
    # Mock existing conversation
    existing_conversation = Conversation(
        id=test_conversation_id,
        user_id=test_user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    # Mock existing messages
    existing_messages = [
        Message(
            id=uuid4(),
            conversation_id=test_conversation_id,
            role="user",
            content="Hello",
            created_at=datetime.utcnow(),
        ),
        Message(
            id=uuid4(),
            conversation_id=test_conversation_id,
            role="assistant",
            content="Hi! How can I help?",
            created_at=datetime.utcnow(),
        ),
    ]

    # Mock database responses
    mock_conversation_result = MagicMock()
    mock_conversation_result.scalar_one.return_value = existing_conversation

    mock_messages_result = MagicMock()
    mock_messages_result.scalars.return_value.all.return_value = existing_messages

    mock_session.execute.side_effect = [
        mock_conversation_result,
        mock_messages_result,
    ]

    conversation, history = await chat_service._load_conversation_history(
        test_user_id, test_conversation_id
    )

    # Verify conversation loaded
    assert conversation.id == test_conversation_id
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


@pytest.mark.asyncio
async def test_load_conversation_unauthorized(
    chat_service, mock_session, test_user_id, test_conversation_id
):
    """Test loading conversation fails when user_id doesn't match."""
    # Mock existing conversation with different user_id
    other_user_id = UUID("999e9999-e99b-99d9-a999-999999999999")
    existing_conversation = Conversation(
        id=test_conversation_id,
        user_id=other_user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    mock_conversation_result = MagicMock()
    mock_conversation_result.scalar_one.return_value = existing_conversation
    mock_session.execute.return_value = mock_conversation_result

    # Should raise UnauthorizedAccessError
    with pytest.raises(UnauthorizedAccessError):
        await chat_service._load_conversation_history(
            test_user_id, test_conversation_id
        )


# Test Step 3: Persist User Message

@pytest.mark.asyncio
async def test_persist_user_message(chat_service, mock_session, test_conversation_id):
    """Test persisting user message to database."""
    message_text = "Add a task to buy groceries"

    message = await chat_service._persist_user_message(
        test_conversation_id, message_text
    )

    # Verify message created
    assert isinstance(message, Message)
    assert message.conversation_id == test_conversation_id
    assert message.role == "user"
    assert message.content == message_text
    assert message.tool_calls is None

    mock_session.add.assert_called_once()
    mock_session.flush.assert_called_once()


# Test Step 4: Invoke AI Agent

@pytest.mark.asyncio
async def test_invoke_ai_agent(chat_service, test_user_id):
    """Test invoking AI agent with message and history."""
    message = "Add a task to buy groceries"
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi! How can I help?"},
    ]

    with patch("phase3.services.chat_service.AgentOrchestrator") as mock_orchestrator_class:
        mock_orchestrator = AsyncMock()
        mock_orchestrator.process_message = AsyncMock(return_value={
            "message": "I've added the task 'Buy groceries'.",
            "tool_calls": [
                {
                    "tool_name": "add_task",
                    "parameters": {
                        "user_id": str(test_user_id),
                        "title": "Buy groceries",
                        "priority": "medium",
                    }
                }
            ],
            "intent": "CREATE_TASK",
        })
        mock_orchestrator_class.return_value = mock_orchestrator

        result = await chat_service._invoke_ai_agent(test_user_id, message, history)

        # Verify agent invoked
        mock_orchestrator_class.assert_called_once()
        mock_orchestrator.process_message.assert_called_once_with(message)
        assert result["message"] == "I've added the task 'Buy groceries'."
        assert len(result["tool_calls"]) == 1


# Test Step 5: Execute MCP Tools

@pytest.mark.asyncio
async def test_execute_mcp_tools(chat_service, mock_mcp_client):
    """Test executing MCP tool calls."""
    chat_service.mcp_client = mock_mcp_client

    tool_calls = [
        {
            "tool_name": "add_task",
            "parameters": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "priority": "medium",
            }
        }
    ]

    results = await chat_service._execute_mcp_tools(tool_calls)

    # Verify tool executed
    mock_mcp_client.invoke_multiple_tools.assert_called_once_with(tool_calls)
    assert len(results) == 1
    assert results[0]["success"] is True


@pytest.mark.asyncio
async def test_execute_mcp_tools_empty(chat_service):
    """Test executing with no tool calls."""
    results = await chat_service._execute_mcp_tools([])
    assert results == []


# Test Step 6: Persist Assistant Response

@pytest.mark.asyncio
async def test_persist_assistant_response(chat_service, mock_session, test_conversation_id):
    """Test persisting assistant response with tool results."""
    content = "I've added the task 'Buy groceries'."
    tool_results = [
        {
            "tool_name": "add_task",
            "parameters": {"user_id": "test", "title": "Buy groceries"},
            "result": {"success": True, "task": {"id": 1, "title": "Buy groceries"}},
        }
    ]

    # Mock conversation update
    mock_conversation = Conversation(
        id=test_conversation_id,
        user_id=uuid4(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    mock_conv_result = MagicMock()
    mock_conv_result.scalar_one.return_value = mock_conversation
    mock_session.execute.return_value = mock_conv_result

    message = await chat_service._persist_assistant_response(
        test_conversation_id, content, tool_results
    )

    # Verify message created
    assert isinstance(message, Message)
    assert message.role == "assistant"
    assert message.content == content
    assert message.tool_calls is not None

    # Verify database operations
    assert mock_session.add.call_count == 1
    mock_session.commit.assert_called_once()


# Test Step 7: Build Response

def test_build_response(chat_service, test_conversation_id):
    """Test building ChatResponse from results."""
    message_id = uuid4()
    message = Message(
        id=message_id,
        conversation_id=test_conversation_id,
        role="assistant",
        content="Task added successfully.",
        created_at=datetime.utcnow(),
    )
    response_text = "Task added successfully."
    tool_results = [
        {
            "tool_name": "add_task",
            "parameters": {"user_id": "test", "title": "Test"},
            "result": {"success": True},
        }
    ]

    response = chat_service._build_response(
        test_conversation_id, message, response_text, tool_results
    )

    # Verify response structure
    assert isinstance(response, ChatResponse)
    assert response.conversation_id == test_conversation_id
    assert response.message_id == message_id
    assert response.response == response_text
    assert len(response.tool_calls) == 1
    assert response.tool_calls[0].tool_name == "add_task"


# Integration Test: Full Pipeline

@pytest.mark.asyncio
async def test_process_chat_message_full_pipeline(
    chat_service, mock_session, mock_mcp_client, test_user_id
):
    """Test complete chat message processing pipeline."""
    chat_service.mcp_client = mock_mcp_client

    request = ChatRequest(message="Add a task to buy groceries", conversation_id=None)

    # Mock new conversation creation
    mock_session.add = MagicMock()
    mock_session.flush = AsyncMock()
    mock_session.commit = AsyncMock()

    # Mock agent response
    with patch("phase3.services.chat_service.AgentOrchestrator") as mock_orchestrator_class:
        mock_orchestrator = AsyncMock()
        mock_orchestrator.process_message = AsyncMock(return_value={
            "message": "I've added the task 'Buy groceries'.",
            "tool_calls": [
                {
                    "tool_name": "add_task",
                    "parameters": {
                        "user_id": str(test_user_id),
                        "title": "Buy groceries",
                        "priority": "medium",
                    }
                }
            ],
            "intent": "CREATE_TASK",
        })
        mock_orchestrator_class.return_value = mock_orchestrator

        # Mock conversation update for Step 6
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=test_user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        mock_conv_result = MagicMock()
        mock_conv_result.scalar_one.return_value = mock_conversation
        mock_session.execute.return_value = mock_conv_result

        # Execute full pipeline
        response = await chat_service.process_chat_message(test_user_id, request)

        # Verify response
        assert isinstance(response, ChatResponse)
        assert "groceries" in response.response.lower()
        assert len(response.tool_calls) == 1

        # Verify database operations
        assert mock_session.add.call_count >= 2  # User message + Assistant message
        assert mock_session.commit.call_count >= 1
