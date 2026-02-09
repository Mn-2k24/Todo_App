"""
Integration tests for Phase III Chat API endpoint.

Tests:
- POST /api/{user_id}/chat with valid authentication
- JWT authentication (valid, missing, invalid, expired)
- User ID validation (path vs JWT mismatch)
- Error responses (400, 401, 403, 404, 500)
- Multi-turn conversations
- Tool execution results in response
"""

import pytest
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient
from jose import jwt

from src.main import app
from src.config import get_settings

settings = get_settings()


# Test fixtures

@pytest.fixture
def test_user_id():
    """Test user UUID."""
    return UUID("550e8400-e29b-41d4-a716-446655440000")


@pytest.fixture
def test_user_id_str(test_user_id):
    """Test user ID as string."""
    return str(test_user_id)


@pytest.fixture
def valid_jwt_token(test_user_id_str):
    """Generate a valid JWT token for testing."""
    payload = {
        "sub": test_user_id_str,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token


@pytest.fixture
def expired_jwt_token(test_user_id_str):
    """Generate an expired JWT token for testing."""
    payload = {
        "sub": test_user_id_str,
        "exp": datetime.utcnow() - timedelta(hours=1),
        "iat": datetime.utcnow() - timedelta(hours=2),
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token


@pytest.fixture
def different_user_jwt_token():
    """Generate JWT token for a different user."""
    different_user_id = "999e9999-e99b-99d9-a999-999999999999"
    payload = {
        "sub": different_user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token


@pytest.fixture
def client():
    """Create TestClient for FastAPI app."""
    return TestClient(app)


# Test 200: Successful chat message processing

@pytest.mark.asyncio
async def test_chat_endpoint_success(client, test_user_id_str, valid_jwt_token):
    """Test successful chat message processing."""
    # Mock the entire chat service pipeline
    with patch("phase3.routers.chat.get_chat_service") as mock_get_service:
        mock_service = AsyncMock()
        mock_service.process_chat_message = AsyncMock(return_value={
            "conversation_id": uuid4(),
            "message_id": uuid4(),
            "response": "I've added the task 'Buy groceries'.",
            "tool_calls": [
                {
                    "tool_name": "add_task",
                    "parameters": {
                        "user_id": test_user_id_str,
                        "title": "Buy groceries",
                        "priority": "medium",
                    },
                    "result": {
                        "success": True,
                        "task": {"id": 1, "title": "Buy groceries", "completed": False},
                    },
                }
            ],
            "created_at": datetime.utcnow(),
        })
        mock_get_service.return_value = mock_service

        response = client.post(
            f"/api/{test_user_id_str}/chat",
            json={"message": "Add a task to buy groceries", "conversation_id": None},
            headers={"Authorization": f"Bearer {valid_jwt_token}"},
        )

        # Verify success response
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert "message_id" in data
        assert "response" in data
        assert "groceries" in data["response"].lower()
        assert "tool_calls" in data
        assert len(data["tool_calls"]) == 1


# Test 401: Authentication errors

def test_chat_endpoint_missing_token(client, test_user_id_str):
    """Test request without JWT token returns 401."""
    response = client.post(
        f"/api/{test_user_id_str}/chat",
        json={"message": "Test message"},
    )

    assert response.status_code == 401
    assert "not authenticated" in response.json()["detail"].lower() or response.json()["detail"] == "Not authenticated"


def test_chat_endpoint_invalid_token(client, test_user_id_str):
    """Test request with invalid JWT token returns 401."""
    response = client.post(
        f"/api/{test_user_id_str}/chat",
        json={"message": "Test message"},
        headers={"Authorization": "Bearer invalid.token.here"},
    )

    assert response.status_code == 401


def test_chat_endpoint_expired_token(client, test_user_id_str, expired_jwt_token):
    """Test request with expired JWT token returns 401."""
    response = client.post(
        f"/api/{test_user_id_str}/chat",
        json={"message": "Test message"},
        headers={"Authorization": f"Bearer {expired_jwt_token}"},
    )

    assert response.status_code == 401


# Test 403: User ID mismatch (authorization)

def test_chat_endpoint_user_id_mismatch(
    client, test_user_id_str, different_user_jwt_token
):
    """Test request with path user_id != JWT user_id returns 403."""
    response = client.post(
        f"/api/{test_user_id_str}/chat",
        json={"message": "Test message"},
        headers={"Authorization": f"Bearer {different_user_jwt_token}"},
    )

    assert response.status_code == 403
    detail = response.json()["detail"]
    assert "forbidden" in detail["code"].lower() or "access denied" in detail["error"].lower()


# Test 400: Invalid input

def test_chat_endpoint_empty_message(client, test_user_id_str, valid_jwt_token):
    """Test request with empty message returns 400."""
    response = client.post(
        f"/api/{test_user_id_str}/chat",
        json={"message": ""},
        headers={"Authorization": f"Bearer {valid_jwt_token}"},
    )

    # Pydantic validation error (422) or service validation error (400)
    assert response.status_code in [400, 422]


def test_chat_endpoint_message_too_long(client, test_user_id_str, valid_jwt_token):
    """Test request with message exceeding max length returns 400."""
    response = client.post(
        f"/api/{test_user_id_str}/chat",
        json={"message": "a" * 2001},
        headers={"Authorization": f"Bearer {valid_jwt_token}"},
    )

    # Pydantic validation error (422) or service validation error (400)
    assert response.status_code in [400, 422]


def test_chat_endpoint_invalid_conversation_id(
    client, test_user_id_str, valid_jwt_token
):
    """Test request with invalid conversation_id format returns 400."""
    response = client.post(
        f"/api/{test_user_id_str}/chat",
        json={"message": "Test", "conversation_id": "not-a-uuid"},
        headers={"Authorization": f"Bearer {valid_jwt_token}"},
    )

    # Pydantic validation error
    assert response.status_code == 422


# Test 404: Conversation not found

@pytest.mark.asyncio
async def test_chat_endpoint_conversation_not_found(
    client, test_user_id_str, valid_jwt_token
):
    """Test request with non-existent conversation_id returns 404."""
    nonexistent_conversation_id = str(uuid4())

    with patch("phase3.routers.chat.get_chat_service") as mock_get_service:
        from phase3.services.chat_service import ConversationNotFoundError

        mock_service = AsyncMock()
        mock_service.process_chat_message = AsyncMock(
            side_effect=ConversationNotFoundError("Conversation not found")
        )
        mock_get_service.return_value = mock_service

        response = client.post(
            f"/api/{test_user_id_str}/chat",
            json={
                "message": "Test",
                "conversation_id": nonexistent_conversation_id,
            },
            headers={"Authorization": f"Bearer {valid_jwt_token}"},
        )

        assert response.status_code == 404
        detail = response.json()["detail"]
        assert "not_found" in detail["code"].lower()


# Test multi-turn conversation

@pytest.mark.asyncio
async def test_chat_endpoint_multi_turn_conversation(
    client, test_user_id_str, valid_jwt_token
):
    """Test multi-turn conversation with same conversation_id."""
    conversation_id = uuid4()

    with patch("phase3.routers.chat.get_chat_service") as mock_get_service:
        mock_service = AsyncMock()

        # First turn
        mock_service.process_chat_message = AsyncMock(return_value={
            "conversation_id": conversation_id,
            "message_id": uuid4(),
            "response": "I've added the task 'Buy groceries'.",
            "tool_calls": [
                {
                    "tool_name": "add_task",
                    "parameters": {"user_id": test_user_id_str, "title": "Buy groceries"},
                    "result": {"success": True, "task": {"id": 1}},
                }
            ],
            "created_at": datetime.utcnow(),
        })
        mock_get_service.return_value = mock_service

        response1 = client.post(
            f"/api/{test_user_id_str}/chat",
            json={"message": "Add a task to buy groceries"},
            headers={"Authorization": f"Bearer {valid_jwt_token}"},
        )

        assert response1.status_code == 200
        data1 = response1.json()
        returned_conversation_id = data1["conversation_id"]

        # Second turn (continue conversation)
        mock_service.process_chat_message = AsyncMock(return_value={
            "conversation_id": conversation_id,
            "message_id": uuid4(),
            "response": "Here are your pending tasks: 1. Buy groceries (medium priority)",
            "tool_calls": [
                {
                    "tool_name": "list_tasks",
                    "parameters": {"user_id": test_user_id_str, "status": "pending"},
                    "result": {
                        "success": True,
                        "tasks": [{"id": 1, "title": "Buy groceries", "priority": "medium"}],
                    },
                }
            ],
            "created_at": datetime.utcnow(),
        })

        response2 = client.post(
            f"/api/{test_user_id_str}/chat",
            json={
                "message": "Show me my pending tasks",
                "conversation_id": returned_conversation_id,
            },
            headers={"Authorization": f"Bearer {valid_jwt_token}"},
        )

        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["conversation_id"] == returned_conversation_id
        assert "pending tasks" in data2["response"].lower()


# Test tool execution in response

@pytest.mark.asyncio
async def test_chat_endpoint_tool_calls_in_response(
    client, test_user_id_str, valid_jwt_token
):
    """Test that tool calls and results are included in response."""
    with patch("phase3.routers.chat.get_chat_service") as mock_get_service:
        mock_service = AsyncMock()
        mock_service.process_chat_message = AsyncMock(return_value={
            "conversation_id": uuid4(),
            "message_id": uuid4(),
            "response": "Task updated successfully.",
            "tool_calls": [
                {
                    "tool_name": "update_task",
                    "parameters": {
                        "user_id": test_user_id_str,
                        "task_id": 1,
                        "priority": "high",
                    },
                    "result": {
                        "success": True,
                        "task": {"id": 1, "priority": "high"},
                    },
                }
            ],
            "created_at": datetime.utcnow(),
        })
        mock_get_service.return_value = mock_service

        response = client.post(
            f"/api/{test_user_id_str}/chat",
            json={"message": "Set task 1 to high priority"},
            headers={"Authorization": f"Bearer {valid_jwt_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["tool_calls"]) == 1
        assert data["tool_calls"][0]["tool_name"] == "update_task"
        assert data["tool_calls"][0]["parameters"]["priority"] == "high"
        assert data["tool_calls"][0]["result"]["success"] is True


# Test error handling

@pytest.mark.asyncio
async def test_chat_endpoint_internal_error(client, test_user_id_str, valid_jwt_token):
    """Test internal server error handling (500)."""
    with patch("phase3.routers.chat.get_chat_service") as mock_get_service:
        mock_service = AsyncMock()
        mock_service.process_chat_message = AsyncMock(
            side_effect=Exception("Unexpected database error")
        )
        mock_get_service.return_value = mock_service

        response = client.post(
            f"/api/{test_user_id_str}/chat",
            json={"message": "Test message"},
            headers={"Authorization": f"Bearer {valid_jwt_token}"},
        )

        assert response.status_code == 500
        detail = response.json()["detail"]
        assert "internal_error" in detail["code"].lower()
