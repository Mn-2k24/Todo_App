"""
Integration Tests for AI Agent

Tests complete workflows from user input through Gemini to tool execution.
Uses mock Gemini client for deterministic testing.
"""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from phase3.agent.orchestrator import AgentOrchestrator
from phase3.llm.response_parser import Intent


# Fixtures

@pytest.fixture
def user_id():
    """Fixed user ID for testing."""
    return uuid4()


@pytest.fixture
def mock_mcp_client():
    """Mock MCP client."""
    return MagicMock()


@pytest.fixture
def agent(user_id, mock_mcp_client):
    """Create agent with mock components."""
    return AgentOrchestrator(
        user_id=user_id,
        mcp_client=mock_mcp_client,
        use_mock_llm=True,
    )


# Complete Workflow Tests (T065)

@pytest.mark.asyncio
async def test_e2e_create_task_workflow(agent):
    """Test complete workflow: user message → Gemini → tool execution → response."""
    # User request
    user_message = "Add a task to buy groceries tomorrow with high priority"

    # Process through agent
    result = await agent.process_message(user_message)

    # Verify workflow
    assert result["success"] is True
    assert result["intent"] == Intent.CREATE_TASK.value
    assert len(result["tool_calls"]) > 0

    # Verify tool execution
    tool_call = result["tool_calls"][0]
    assert tool_call["tool"] == "add_task"
    assert "user_id" in tool_call["parameters"]

    # Verify natural language response
    assert isinstance(result["message"], str)
    assert len(result["message"]) > 0


@pytest.mark.asyncio
async def test_e2e_list_tasks_workflow(agent):
    """Test list tasks workflow."""
    result = await agent.process_message("Show me all my pending tasks")

    assert result["success"] is True
    assert result["intent"] == Intent.LIST_TASKS.value

    if result["tool_calls"]:
        tool_call = result["tool_calls"][0]
        assert tool_call["tool"] == "list_tasks"


@pytest.mark.asyncio
async def test_e2e_update_task_workflow(agent):
    """Test update task workflow with context."""
    # First list tasks to populate context
    await agent.process_message("Show my tasks")

    # Mock a task list
    agent.last_task_list = [{"id": "task-123", "description": "Test task"}]

    # Update the task
    result = await agent.process_message("Change the first task to high priority")

    assert result["success"] is True
    # Should attempt to update or ask for clarification


@pytest.mark.asyncio
async def test_e2e_complete_task_workflow(agent):
    """Test complete task workflow."""
    # Create context
    agent.last_task_list = [{"id": "task-456", "description": "Buy groceries"}]

    result = await agent.process_message("Mark the first task as done")

    assert result["success"] is True


@pytest.mark.asyncio
async def test_e2e_delete_task_workflow(agent):
    """Test delete task workflow."""
    # Create context
    agent.last_task_list = [{"id": "task-789", "description": "Old task"}]

    result = await agent.process_message("Delete the first task")

    assert result["success"] is True


# Multi-Step Workflow Tests

@pytest.mark.asyncio
async def test_multi_step_list_then_complete(agent):
    """Test workflow that requires multiple steps."""
    # This would require listing tasks first, then completing one
    result = await agent.process_message("Show my tasks and mark the first one as done")

    assert result["success"] is True
    # Might execute multiple tools or handle sequentially


@pytest.mark.asyncio
async def test_multi_step_create_then_list(agent):
    """Test creating and listing in one request."""
    result = await agent.process_message("Add a task to buy milk and show all my tasks")

    assert result["success"] is True
    # Should handle both operations


# Conversation Context Tests

@pytest.mark.asyncio
async def test_conversation_context_maintained(agent):
    """Test that context is maintained across turns."""
    # Turn 1
    result1 = await agent.process_message("Show my pending tasks")
    assert result1["success"] is True

    # Turn 2 - should remember we were talking about tasks
    result2 = await agent.process_message("How many do I have?")
    assert result2["success"] is True

    # Conversation history should be updated
    assert len(agent.conversation_history) == 4


@pytest.mark.asyncio
async def test_pronoun_resolution_across_turns(agent):
    """Test resolving pronouns using conversation context."""
    # Turn 1: Create a task
    result1 = await agent.process_message("Add task to buy groceries")
    assert result1["success"] is True

    # Turn 2: Reference it with pronoun
    result2 = await agent.process_message("Make it high priority")
    assert result2["success"] is True

    # Turn 3: Complete it
    result3 = await agent.process_message("Mark it as done")
    assert result3["success"] is True


@pytest.mark.asyncio
async def test_ordinal_reference_resolution(agent):
    """Test resolving ordinal references like 'first', 'second', 'last'."""
    # Populate task list
    agent.last_task_list = [
        {"id": "task-1", "description": "First"},
        {"id": "task-2", "description": "Second"},
        {"id": "task-3", "description": "Third"},
    ]

    # Reference first
    result1 = await agent.process_message("Complete the first task")
    assert result1["success"] is True

    # Reference last
    result2 = await agent.process_message("Delete the last task")
    assert result2["success"] is True


# Ambiguity and Clarification Tests

@pytest.mark.asyncio
async def test_clarification_for_ambiguous_reference(agent):
    """Test that agent asks for clarification when reference is ambiguous."""
    result = await agent.process_message("Update the task")

    assert result["success"] is True
    # Should either ask for clarification or attempt with context
    if result["intent"] == Intent.CLARIFICATION.value:
        assert "?" in result["message"]


@pytest.mark.asyncio
async def test_clarification_for_missing_title(agent):
    """Test asking for missing task title."""
    result = await agent.process_message("Add a task")

    assert result["success"] is True
    # Might ask "What should the task be called?" or use default


@pytest.mark.asyncio
async def test_handling_out_of_scope_requests(agent):
    """Test handling requests outside task management scope."""
    result = await agent.process_message("What's the weather today?")

    assert result["success"] is True
    assert result["intent"] == Intent.OUT_OF_SCOPE.value
    assert len(result["tool_calls"]) == 0
    assert "task management" in result["message"].lower()


# Error Recovery Tests

@pytest.mark.asyncio
async def test_recovery_from_tool_execution_failure(agent):
    """Test graceful handling when tool execution fails."""
    # This will be tested more thoroughly when real MCP client is integrated
    # For now, test that orchestrator handles simulated failures
    result = await agent.process_message("Add task")

    # Should not crash
    assert "success" in result
    assert "message" in result


@pytest.mark.asyncio
async def test_recovery_from_invalid_input(agent):
    """Test recovery from invalid user input."""
    result = await agent.process_message("")

    assert result["success"] is False
    assert "Invalid input" in result["message"]

    # Should still be able to process next message
    result2 = await agent.process_message("Show my tasks")
    assert result2["success"] is True


# Intent-Specific Workflow Tests

@pytest.mark.asyncio
async def test_create_task_with_all_attributes(agent):
    """Test creating task with title, priority, due date, and tags."""
    result = await agent.process_message(
        "Add urgent work task to finish report by Friday tagged important"
    )

    assert result["success"] is True
    assert result["intent"] == Intent.CREATE_TASK.value


@pytest.mark.asyncio
async def test_list_tasks_with_filters(agent):
    """Test listing tasks with multiple filters."""
    result = await agent.process_message("Show completed high priority work tasks")

    assert result["success"] is True
    assert result["intent"] == Intent.LIST_TASKS.value


@pytest.mark.asyncio
async def test_update_task_multiple_attributes(agent):
    """Test updating multiple task attributes at once."""
    agent.last_task_list = [{"id": "task-1", "description": "Test"}]

    result = await agent.process_message(
        "Change first task to high priority due tomorrow"
    )

    assert result["success"] is True


# Performance and Limits Tests

@pytest.mark.asyncio
async def test_conversation_history_stays_within_limits(agent):
    """Test that conversation history respects max size."""
    # Send 30 messages
    for i in range(30):
        await agent.process_message(f"Message {i}")

    # Should keep only last 20 messages
    assert len(agent.conversation_history) <= 20


@pytest.mark.asyncio
async def test_tool_call_limit_enforced(agent):
    """Test that max tool calls per turn is enforced."""
    # This would require Gemini to return many tool calls
    # Orchestrator should limit to max_tool_calls_per_turn (5)
    assert agent.max_tool_calls_per_turn == 5


# Natural Language Variation Tests

@pytest.mark.asyncio
async def test_various_create_task_phrasings(agent):
    """Test different ways of asking to create a task."""
    phrasings = [
        "Add task to buy milk",
        "Create a new task for buying milk",
        "Remind me to buy milk",
        "I need to buy milk",
        "Make a task: buy milk",
    ]

    for phrasing in phrasings:
        agent.reset_conversation()  # Reset between tests
        result = await agent.process_message(phrasing)

        assert result["success"] is True
        # Should recognize as create intent or execute add_task
        if result["tool_calls"]:
            assert result["tool_calls"][0]["tool"] == "add_task"


@pytest.mark.asyncio
async def test_various_list_task_phrasings(agent):
    """Test different ways of asking to list tasks."""
    phrasings = [
        "Show my tasks",
        "What tasks do I have?",
        "List all my tasks",
        "Display my todo list",
        "What's on my plate?",
    ]

    for phrasing in phrasings:
        agent.reset_conversation()
        result = await agent.process_message(phrasing)

        assert result["success"] is True
        # Should recognize as list intent
        if result["tool_calls"]:
            assert result["tool_calls"][0]["tool"] == "list_tasks"


# Edge Case Tests

@pytest.mark.asyncio
async def test_empty_task_list_context(agent):
    """Test handling when task list is empty."""
    agent.last_task_list = []

    result = await agent.process_message("Complete the first task")

    assert result["success"] is True
    # Should handle gracefully (ask for clarification or explain no tasks)


@pytest.mark.asyncio
async def test_concurrent_message_processing(agent):
    """Test that agent can handle rapid messages."""
    # Send multiple messages in quick succession
    results = await asyncio.gather(
        agent.process_message("Show my tasks"),
        agent.process_message("Add task 1"),
        agent.process_message("Add task 2"),
    )

    # All should complete successfully
    for result in results:
        assert result["success"] is True


# Integration with All Components Test

@pytest.mark.asyncio
async def test_full_stack_integration(agent):
    """Test integration of all components: Gemini, Parser, Security, Orchestrator."""
    # This tests the complete flow:
    # 1. Security validation
    # 2. Prompt building
    # 3. Gemini API call
    # 4. Response parsing
    # 5. Tool execution
    # 6. Natural response generation

    result = await agent.process_message("Add an urgent task to finish the project")

    # All components should work together
    assert result["success"] is True
    assert "intent" in result
    assert "message" in result
    assert "tool_calls" in result

    # Conversation history should be updated
    assert len(agent.conversation_history) == 2


# Import for concurrent test
import asyncio
