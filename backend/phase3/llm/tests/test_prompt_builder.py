"""
Unit Tests for Prompt Builder

Tests prompt construction, system instruction injection, and conversation history formatting.
"""

import pytest

from phase3.llm.prompt_builder import PromptBuilder


# Fixtures

@pytest.fixture
def prompt_builder():
    """Create PromptBuilder instance."""
    return PromptBuilder()


@pytest.fixture
def user_id():
    """Fixed user ID for testing."""
    return "550e8400-e29b-41d4-a716-446655440000"


# System instruction tests

def test_build_system_instruction_with_tools(prompt_builder, user_id):
    """Test building system instruction with user context and tools."""
    instruction = prompt_builder.build_system_instruction_with_tools(
        user_id=user_id, available_tools=["add_task", "list_tasks"]
    )

    # Verify user ID is included
    assert user_id in instruction

    # Verify tools are documented
    assert "add_task" in instruction
    assert "list_tasks" in instruction

    # Verify system instruction is included
    assert "task management assistant" in instruction.lower()


def test_build_system_instruction_default_tools(prompt_builder, user_id):
    """Test building system instruction with default tools."""
    instruction = prompt_builder.build_system_instruction_with_tools(user_id=user_id)

    # Verify all 5 default tools are included
    assert "add_task" in instruction
    assert "list_tasks" in instruction
    assert "update_task" in instruction
    assert "complete_task" in instruction
    assert "delete_task" in instruction


# Conversation history tests

def test_build_conversation_messages_empty_history(prompt_builder):
    """Test building messages with empty history."""
    messages = prompt_builder.build_conversation_messages([], "Add task: buy milk")

    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Add task: buy milk"


def test_build_conversation_messages_with_history(prompt_builder):
    """Test building messages with existing history."""
    history = [
        {"role": "user", "content": "Show my tasks"},
        {"role": "assistant", "content": "You have 3 tasks..."},
    ]

    messages = prompt_builder.build_conversation_messages(history, "Add new task")

    assert len(messages) == 3
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"
    assert messages[2]["role"] == "user"
    assert messages[2]["content"] == "Add new task"


def test_build_conversation_messages_respects_max_history(prompt_builder):
    """Test that conversation history is limited to max_history_messages."""
    # Create 15 messages (> default max of 10)
    history = [
        {"role": "user" if i % 2 == 0 else "assistant", "content": f"Message {i}"}
        for i in range(15)
    ]

    messages = prompt_builder.build_conversation_messages(history, "New message")

    # Should have 10 (max history) + 1 (new message) = 11
    assert len(messages) <= 11


# Tool call result formatting tests

def test_format_tool_call_result_add_task_success(prompt_builder):
    """Test formatting successful add_task result."""
    result = prompt_builder.format_tool_call_result(
        tool_name="add_task",
        parameters={"user_id": "123", "title": "Buy groceries"},
        result={
            "success": True,
            "task": {"id": "456", "description": "Buy groceries"},
        },
    )

    assert "[Tool Call]" in result
    assert "add_task" in result
    assert "Buy groceries" in result
    assert "user_id" not in result  # Should be hidden


def test_format_tool_call_result_list_tasks_success(prompt_builder):
    """Test formatting successful list_tasks result."""
    result = prompt_builder.format_tool_call_result(
        tool_name="list_tasks",
        parameters={"user_id": "123", "status": "pending"},
        result={"success": True, "count": 5, "tasks": []},
    )

    assert "[Tool Call]" in result
    assert "list_tasks" in result
    assert "5 task(s)" in result


def test_format_tool_call_result_error(prompt_builder):
    """Test formatting error result."""
    result = prompt_builder.format_tool_call_result(
        tool_name="delete_task",
        parameters={"user_id": "123", "task_id": "456"},
        result={
            "success": False,
            "error": "TASK_NOT_FOUND",
            "message": "Task not found",
        },
    )

    assert "[Tool Call]" in result
    assert "delete_task" in result
    assert "Error" in result
    assert "TASK_NOT_FOUND" in result


# Intent extraction tests

def test_extract_user_intent_create(prompt_builder):
    """Test extracting CREATE_TASK intent."""
    intent = prompt_builder.extract_user_intent("Add task to buy groceries tomorrow")

    assert "create" in intent["action_keywords"]
    assert "tomorrow" in intent["timeframe_keywords"]


def test_extract_user_intent_list(prompt_builder):
    """Test extracting LIST_TASKS intent."""
    intent = prompt_builder.extract_user_intent("Show me all my tasks")

    assert "list" in intent["action_keywords"]


def test_extract_user_intent_high_urgency(prompt_builder):
    """Test detecting high urgency keywords."""
    intent = prompt_builder.extract_user_intent("Urgent: add important task")

    assert "high" in intent["urgency_keywords"]


def test_extract_user_intent_low_urgency(prompt_builder):
    """Test detecting low urgency keywords."""
    intent = prompt_builder.extract_user_intent("Sometime later, add task")

    assert "low" in intent["urgency_keywords"]


def test_extract_user_intent_multiple_actions(prompt_builder):
    """Test detecting multiple action keywords."""
    intent = prompt_builder.extract_user_intent("Show tasks and add new one")

    assert "list" in intent["action_keywords"]
    assert "create" in intent["action_keywords"]


# Custom max_history tests

def test_custom_max_history():
    """Test creating builder with custom max_history."""
    builder = PromptBuilder(max_history_messages=5)

    history = [{"role": "user", "content": f"Message {i}"} for i in range(10)]
    messages = builder.build_conversation_messages(history, "New")

    # Should have 5 (custom max) + 1 (new) = 6
    assert len(messages) == 6


# Edge cases

def test_build_conversation_messages_none_history(prompt_builder):
    """Test handling None history."""
    messages = prompt_builder.build_conversation_messages([], "Test")
    assert len(messages) == 1


def test_format_tool_call_result_missing_keys(prompt_builder):
    """Test formatting result with missing keys."""
    result = prompt_builder.format_tool_call_result(
        tool_name="add_task",
        parameters={},
        result={},  # Empty result
    )

    assert "[Tool Call]" in result
    assert "add_task" in result


def test_extract_user_intent_empty_message(prompt_builder):
    """Test extracting intent from empty message."""
    intent = prompt_builder.extract_user_intent("")

    assert intent["action_keywords"] == []
    assert intent["urgency_keywords"] == []
    assert intent["message_length"] == 0
