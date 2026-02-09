"""
Integration Tests for MCP Server

Tests the MCP server as a whole:
- Server startup and initialization
- Tool registration
- Tool execution via MCP protocol
- Server lifecycle management
"""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from mcp_server.main import handle_call_tool, handle_list_tools, server


# Server initialization tests

@pytest.mark.asyncio
async def test_server_initialization():
    """Test MCP server initializes correctly."""
    assert server is not None
    assert server._server_name == "todo-mcp-server"


@pytest.mark.asyncio
async def test_list_tools_returns_all_tools():
    """Test server registers all 5 task management tools."""
    tools = await handle_list_tools()

    assert len(tools) == 5

    tool_names = [tool.name for tool in tools]
    assert "add_task" in tool_names
    assert "list_tasks" in tool_names
    assert "update_task" in tool_names
    assert "complete_task" in tool_names
    assert "delete_task" in tool_names


@pytest.mark.asyncio
async def test_tool_schemas_are_valid():
    """Test all tools have valid JSON schemas."""
    tools = await handle_list_tools()

    for tool in tools:
        # Verify tool has required fields
        assert tool.name
        assert tool.description
        assert tool.inputSchema

        # Verify schema structure
        schema = tool.inputSchema
        assert schema["type"] == "object"
        assert "properties" in schema
        assert "required" in schema

        # All tools must require user_id
        assert "user_id" in schema["required"]
        assert "user_id" in schema["properties"]


@pytest.mark.asyncio
async def test_add_task_tool_schema():
    """Test add_task tool has correct schema."""
    tools = await handle_list_tools()
    add_task = next(t for t in tools if t.name == "add_task")

    schema = add_task.inputSchema
    props = schema["properties"]

    # Required fields
    assert "user_id" in schema["required"]
    assert "title" in schema["required"]

    # Optional fields
    assert "description" in props
    assert "priority" in props
    assert "due_date" in props
    assert "tags" in props

    # Priority enum
    assert props["priority"]["enum"] == ["low", "medium", "high"]


# Tool execution tests

@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_handle_call_tool_add_task(mock_session_factory):
    """Test calling add_task via handle_call_tool."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    user_id = uuid4()
    arguments = {
        "user_id": str(user_id),
        "title": "Integration test task",
        "priority": "high",
    }

    result = await handle_call_tool("add_task", arguments)

    assert len(result) == 1
    response_text = result[0].text
    data = json.loads(response_text)

    assert data["success"] is True
    assert data["task"]["description"] == "Integration test task"


@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_handle_call_tool_list_tasks(mock_session_factory):
    """Test calling list_tasks via handle_call_tool."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute = AsyncMock(return_value=mock_result)

    user_id = uuid4()
    arguments = {"user_id": str(user_id)}

    result = await handle_call_tool("list_tasks", arguments)

    assert len(result) == 1
    response_text = result[0].text
    data = json.loads(response_text)

    assert data["success"] is True
    assert data["count"] == 0


@pytest.mark.asyncio
async def test_handle_call_tool_unknown_tool():
    """Test calling unknown tool returns error."""
    result = await handle_call_tool("unknown_tool", {})

    assert len(result) == 1
    response_text = result[0].text
    data = json.loads(response_text)

    assert data["error"] == "UNKNOWN_TOOL"
    assert "unknown_tool" in data["message"]


@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.handle_add_task")
async def test_handle_call_tool_exception_handling(mock_add_task):
    """Test handle_call_tool catches and formats exceptions."""
    # Simulate handler raising exception
    mock_add_task.side_effect = Exception("Database connection failed")

    user_id = uuid4()
    arguments = {"user_id": str(user_id), "title": "Test"}

    result = await handle_call_tool("add_task", arguments)

    assert len(result) == 1
    response_text = result[0].text
    data = json.loads(response_text)

    assert data["error"] == "INTERNAL_ERROR"
    assert "Database connection failed" in data["message"]


# Server lifecycle tests

@pytest.mark.asyncio
async def test_server_lifespan_context():
    """Test server lifespan context manager."""
    from mcp_server.main import server_lifespan

    # Test lifespan startup and shutdown
    async with server_lifespan(server) as context:
        assert context == {}  # Empty context for now


@pytest.mark.asyncio
async def test_server_can_start_independently():
    """
    Test MCP server can start without Phase II backend.

    This verifies the independence requirement - MCP server should be
    startable and testable without the full application stack.
    """
    # This test verifies the server structure, not actual runtime
    # In production, use: python3 -m mcp_server.main

    # Verify main entry point exists
    from mcp_server.main import main

    assert callable(main)

    # Verify run function exists
    from mcp_server.main import run

    assert callable(run)

    # Verify server is configured
    assert server is not None
    assert server._server_name == "todo-mcp-server"


# Performance tests

@pytest.mark.asyncio
async def test_server_startup_time():
    """Test server startup completes within 5 seconds."""
    from time import time

    start = time()

    # Simulate server initialization
    tools = await handle_list_tools()

    elapsed = time() - start

    assert elapsed < 5.0, f"Server startup took {elapsed}s, expected < 5s"
    assert len(tools) == 5


@pytest.mark.asyncio
async def test_tool_registration_time():
    """Test all 5 tools register quickly."""
    from time import time

    start = time()

    # Register tools
    tools = await handle_list_tools()

    elapsed = time() - start

    assert len(tools) == 5
    assert (
        elapsed < 0.1
    ), f"Tool registration took {elapsed}s, expected < 0.1s"


# End-to-end workflow tests

@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_e2e_task_workflow(mock_session_factory):
    """
    Test complete task workflow: create → list → update → complete → delete.
    """
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    user_id = uuid4()
    task_id = uuid4()

    # 1. Create task
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    result = await handle_call_tool(
        "add_task", {"user_id": str(user_id), "title": "E2E test task"}
    )
    data = json.loads(result[0].text)
    assert data["success"] is True

    # 2. List tasks
    from src.models.task import Priority, Task

    mock_task = Task(
        id=task_id,
        user_id=user_id,
        description="E2E test task",
        completed=False,
        priority=Priority.MEDIUM,
        tags=[],
    )

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_task]
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await handle_call_tool("list_tasks", {"user_id": str(user_id)})
    data = json.loads(result[0].text)
    assert data["success"] is True
    assert data["count"] >= 1

    # 3. Update task
    mock_result.scalar_one_or_none.return_value = mock_task
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await handle_call_tool(
        "update_task",
        {
            "user_id": str(user_id),
            "task_id": str(task_id),
            "title": "Updated E2E task",
            "priority": "high",
        },
    )
    data = json.loads(result[0].text)
    assert data["success"] is True

    # 4. Complete task
    result = await handle_call_tool(
        "complete_task", {"user_id": str(user_id), "task_id": str(task_id)}
    )
    data = json.loads(result[0].text)
    assert data["success"] is True

    # 5. Delete task
    mock_session.delete = AsyncMock()

    result = await handle_call_tool(
        "delete_task", {"user_id": str(user_id), "task_id": str(task_id)}
    )
    data = json.loads(result[0].text)
    assert data["success"] is True


# User isolation integration tests

@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_user_isolation_across_all_tools(mock_session_factory):
    """
    Test user_id isolation is enforced across all 5 tools.

    Verifies that User A cannot access User B's tasks through any tool.
    """
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    user_a_id = uuid4()
    user_b_id = uuid4()
    task_id = uuid4()

    # Create task as User A
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    result = await handle_call_tool(
        "add_task", {"user_id": str(user_a_id), "title": "User A task"}
    )
    data = json.loads(result[0].text)
    assert data["success"] is True

    # User B tries to list - should not see User A's task
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []  # Empty for User B
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await handle_call_tool("list_tasks", {"user_id": str(user_b_id)})
    data = json.loads(result[0].text)
    assert data["success"] is True
    assert data["count"] == 0  # User B sees no tasks

    # User B tries to update User A's task - should fail
    mock_result.scalar_one_or_none.return_value = None  # Task not found for User B
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await handle_call_tool(
        "update_task",
        {"user_id": str(user_b_id), "task_id": str(task_id), "title": "Hacked"},
    )
    data = json.loads(result[0].text)
    assert data["error"] == "TASK_NOT_FOUND"

    # User B tries to complete User A's task - should fail
    result = await handle_call_tool(
        "complete_task", {"user_id": str(user_b_id), "task_id": str(task_id)}
    )
    data = json.loads(result[0].text)
    assert data["error"] == "TASK_NOT_FOUND"

    # User B tries to delete User A's task - should fail
    result = await handle_call_tool(
        "delete_task", {"user_id": str(user_b_id), "task_id": str(task_id)}
    )
    data = json.loads(result[0].text)
    assert data["error"] == "TASK_NOT_FOUND"


# Concurrent request handling tests

@pytest.mark.asyncio
@patch("mcp_server.tools.task_tools.AsyncSessionLocal")
async def test_concurrent_tool_calls(mock_session_factory):
    """Test server can handle multiple concurrent tool calls."""
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute = AsyncMock(return_value=mock_result)

    user_id = uuid4()

    # Create 10 concurrent list_tasks calls
    tasks = [
        handle_call_tool("list_tasks", {"user_id": str(user_id)}) for _ in range(10)
    ]

    # Execute concurrently
    results = await asyncio.gather(*tasks)

    # All should succeed
    assert len(results) == 10
    for result in results:
        data = json.loads(result[0].text)
        assert data["success"] is True
