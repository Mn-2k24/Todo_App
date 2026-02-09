"""
Unit Tests for MCP Task Tools

Tests all 5 MCP tools with mocked database to verify:
- Correct behavior with valid inputs
- Error handling for invalid inputs
- User data isolation enforcement
- JSON response formatting
"""

import json
from datetime import date, datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest

from mcp_server.tools.task_tools import (
    ErrorCode,
    format_error_response,
    format_task_response,
    handle_add_task,
    handle_complete_task,
    handle_delete_task,
    handle_list_tasks,
    handle_update_task,
)
from src.models.task import Priority, Task


# Test fixtures

@pytest.fixture
def mock_user_id():
    """Fixed user_id for testing."""
    return uuid4()


@pytest.fixture
def mock_task_id():
    """Fixed task_id for testing."""
    return uuid4()


@pytest.fixture
def mock_task(mock_user_id, mock_task_id):
    """Create a mock Task instance."""
    return Task(
        id=mock_task_id,
        user_id=mock_user_id,
        description="Test task",
        completed=False,
        priority=Priority.MEDIUM,
        tags=["test"],
        due_date=date(2026, 2, 1),
        created_at=datetime(2026, 1, 27, 10, 0, 0),
        updated_at=datetime(2026, 1, 27, 10, 0, 0),
    )


# Helper function tests

def test_format_task_response(mock_task):
    """Test task formatting to JSON-serializable dict."""
    result = format_task_response(mock_task)

    assert result["id"] == str(mock_task.id)
    assert result["user_id"] == str(mock_task.user_id)
    assert result["description"] == "Test task"
    assert result["completed"] is False
    assert result["priority"] == "medium"
    assert result["tags"] == ["test"]
    assert result["due_date"] == "2026-02-01"
    assert "created_at" in result
    assert "updated_at" in result


def test_format_error_response():
    """Test error response formatting."""
    result = format_error_response(
        ErrorCode.INVALID_INPUT, "Test error", "Details here"
    )
    data = json.loads(result)

    assert data["error"] == ErrorCode.INVALID_INPUT
    assert data["message"] == "Test error"
    assert data["details"] == "Details here"


def test_format_error_response_no_details():
    """Test error response without details."""
    result = format_error_response(ErrorCode.TASK_NOT_FOUND, "Not found")
    data = json.loads(result)

    assert data["error"] == ErrorCode.TASK_NOT_FOUND
    assert data["message"] == "Not found"
    assert "details" not in data


# add_task tests

@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_add_task_success(mock_session_factory, mock_user_id):
    """Test successful task creation."""
    # Mock database session
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    # Prepare arguments
    arguments = {
        "user_id": str(mock_user_id),
        "title": "Buy groceries",
        "priority": "high",
        "due_date": "2026-02-01",
        "tags": ["shopping"],
    }

    # Call handler
    result = await handle_add_task(arguments)

    # Verify response
    assert len(result) == 1
    response_text = result[0].text
    data = json.loads(response_text)

    assert data["success"] is True
    assert data["message"] == "Task created successfully"
    assert "task" in data
    assert data["task"]["description"] == "Buy groceries"
    assert data["task"]["priority"] == "high"

    # Verify database operations
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_add_task_invalid_user_id(mock_session_factory):
    """Test add_task with invalid user_id."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    arguments = {"user_id": "invalid-uuid", "title": "Test"}

    result = await handle_add_task(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["error"] == ErrorCode.INVALID_INPUT
    assert "Invalid user_id" in data["message"]


@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_add_task_empty_title(mock_session_factory, mock_user_id):
    """Test add_task with empty title."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    arguments = {"user_id": str(mock_user_id), "title": "   "}

    result = await handle_add_task(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["error"] == ErrorCode.INVALID_INPUT
    assert "required" in data["message"].lower()


@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_add_task_invalid_due_date(mock_session_factory, mock_user_id):
    """Test add_task with invalid date format."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    arguments = {
        "user_id": str(mock_user_id),
        "title": "Test",
        "due_date": "not-a-date",
    }

    result = await handle_add_task(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["error"] == ErrorCode.INVALID_INPUT
    assert "due_date" in data["message"].lower()


# list_tasks tests

@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_list_tasks_success(mock_session_factory, mock_user_id, mock_task):
    """Test successful task listing."""
    # Mock database session and query results
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_task]
    mock_session.execute = AsyncMock(return_value=mock_result)

    arguments = {"user_id": str(mock_user_id)}

    result = await handle_list_tasks(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["success"] is True
    assert data["count"] == 1
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["description"] == "Test task"


@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_list_tasks_with_filters(mock_session_factory, mock_user_id, mock_task):
    """Test list_tasks with status and priority filters."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_task]
    mock_session.execute = AsyncMock(return_value=mock_result)

    arguments = {
        "user_id": str(mock_user_id),
        "status": "pending",
        "priority": "medium",
    }

    result = await handle_list_tasks(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["success"] is True
    assert data["filters"]["status"] == "pending"
    assert data["filters"]["priority"] == "medium"


@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_list_tasks_empty(mock_session_factory, mock_user_id):
    """Test list_tasks returns empty array when no tasks found."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute = AsyncMock(return_value=mock_result)

    arguments = {"user_id": str(mock_user_id)}

    result = await handle_list_tasks(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["success"] is True
    assert data["count"] == 0
    assert data["tasks"] == []


# update_task tests

@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_update_task_success(
    mock_session_factory, mock_user_id, mock_task_id, mock_task
):
    """Test successful task update."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_task
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    arguments = {
        "user_id": str(mock_user_id),
        "task_id": str(mock_task_id),
        "title": "Updated task",
        "priority": "high",
    }

    result = await handle_update_task(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["success"] is True
    assert data["message"] == "Task updated successfully"
    assert mock_task.description == "Updated task"
    assert mock_task.priority == Priority.HIGH


@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_update_task_not_found(mock_session_factory, mock_user_id, mock_task_id):
    """Test update_task when task doesn't exist or unauthorized."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    arguments = {
        "user_id": str(mock_user_id),
        "task_id": str(mock_task_id),
        "title": "Updated",
    }

    result = await handle_update_task(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["error"] == ErrorCode.TASK_NOT_FOUND


@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_update_task_clear_due_date(
    mock_session_factory, mock_user_id, mock_task_id, mock_task
):
    """Test clearing due_date by passing null."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_task
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    arguments = {
        "user_id": str(mock_user_id),
        "task_id": str(mock_task_id),
        "due_date": None,
    }

    result = await handle_update_task(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["success"] is True
    assert mock_task.due_date is None


# complete_task tests

@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_complete_task_success(
    mock_session_factory, mock_user_id, mock_task_id, mock_task
):
    """Test successful task completion."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_task
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    arguments = {"user_id": str(mock_user_id), "task_id": str(mock_task_id)}

    result = await handle_complete_task(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["success"] is True
    assert data["message"] == "Task completed successfully"
    assert mock_task.completed is True


@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_complete_task_not_found(
    mock_session_factory, mock_user_id, mock_task_id
):
    """Test complete_task when task doesn't exist."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    arguments = {"user_id": str(mock_user_id), "task_id": str(mock_task_id)}

    result = await handle_complete_task(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["error"] == ErrorCode.TASK_NOT_FOUND


# delete_task tests

@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_delete_task_success(
    mock_session_factory, mock_user_id, mock_task_id, mock_task
):
    """Test successful task deletion."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_task
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    arguments = {"user_id": str(mock_user_id), "task_id": str(mock_task_id)}

    result = await handle_delete_task(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["success"] is True
    assert data["message"] == "Task deleted successfully"
    assert data["task_id"] == str(mock_task_id)
    mock_session.delete.assert_called_once_with(mock_task)


@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_delete_task_not_found(mock_session_factory, mock_user_id, mock_task_id):
    """Test delete_task when task doesn't exist."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    arguments = {"user_id": str(mock_user_id), "task_id": str(mock_task_id)}

    result = await handle_delete_task(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["error"] == ErrorCode.TASK_NOT_FOUND


# User isolation tests

@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_user_isolation_list_tasks(mock_session_factory):
    """Test that list_tasks only returns tasks for the authenticated user."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    user1_id = uuid4()
    user2_id = uuid4()

    # User 1 has 2 tasks, User 2 has 1 task
    user1_task1 = Task(
        id=uuid4(),
        user_id=user1_id,
        description="User 1 Task 1",
        completed=False,
        priority=Priority.MEDIUM,
        tags=[],
    )
    user1_task2 = Task(
        id=uuid4(),
        user_id=user1_id,
        description="User 1 Task 2",
        completed=False,
        priority=Priority.MEDIUM,
        tags=[],
    )

    # Mock returns only user1's tasks (user_id filter enforced)
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [user1_task1, user1_task2]
    mock_session.execute = AsyncMock(return_value=mock_result)

    arguments = {"user_id": str(user1_id)}

    result = await handle_list_tasks(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["success"] is True
    assert data["count"] == 2
    # Verify all tasks belong to user1
    for task in data["tasks"]:
        assert task["user_id"] == str(user1_id)


@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_user_isolation_update_task_unauthorized(mock_session_factory):
    """Test that users cannot update tasks they don't own."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    user1_id = uuid4()
    user2_id = uuid4()
    task_id = uuid4()

    # Database query with user_id filter returns None (task owned by different user)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    # User 2 tries to update User 1's task
    arguments = {
        "user_id": str(user2_id),
        "task_id": str(task_id),
        "title": "Unauthorized update",
    }

    result = await handle_update_task(arguments)

    response_text = result[0].text
    data = json.loads(response_text)

    assert data["error"] == ErrorCode.TASK_NOT_FOUND
    assert "unauthorized" in data["message"].lower()
