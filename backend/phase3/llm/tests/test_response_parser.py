"""
Unit Tests for Response Parser

Tests parsing Gemini responses to extract intents and tool calls.
"""

import pytest

from phase3.llm.response_parser import Intent, ResponseParser


# Fixtures

@pytest.fixture
def parser():
    """Create ResponseParser instance."""
    return ResponseParser()


# Tool call extraction tests

def test_parse_response_add_task(parser):
    """Test parsing add_task tool call."""
    response_text = (
        "I'll add that task for you. "
        "add_task(user_id='123', title='Buy groceries', priority='high')"
    )

    parsed = parser.parse_response(response_text)

    assert parsed.intent == Intent.CREATE_TASK
    assert len(parsed.tool_calls) == 1
    assert parsed.tool_calls[0]["tool_name"] == "add_task"
    assert parsed.tool_calls[0]["parameters"]["title"] == "Buy groceries"
    assert parsed.tool_calls[0]["parameters"]["priority"] == "high"


def test_parse_response_list_tasks(parser):
    """Test parsing list_tasks tool call."""
    response_text = "Here are your tasks. list_tasks(user_id='123', status='pending')"

    parsed = parser.parse_response(response_text)

    assert parsed.intent == Intent.LIST_TASKS
    assert len(parsed.tool_calls) == 1
    assert parsed.tool_calls[0]["tool_name"] == "list_tasks"
    assert parsed.tool_calls[0]["parameters"]["status"] == "pending"


def test_parse_response_update_task(parser):
    """Test parsing update_task tool call."""
    response_text = (
        "Updating the task. "
        "update_task(user_id='123', task_id='456', title='New title', priority='low')"
    )

    parsed = parser.parse_response(response_text)

    assert parsed.intent == Intent.UPDATE_TASK
    assert len(parsed.tool_calls) == 1
    assert parsed.tool_calls[0]["parameters"]["task_id"] == "456"
    assert parsed.tool_calls[0]["parameters"]["title"] == "New title"


def test_parse_response_complete_task(parser):
    """Test parsing complete_task tool call."""
    response_text = "Marking as done. complete_task(user_id='123', task_id='456')"

    parsed = parser.parse_response(response_text)

    assert parsed.intent == Intent.COMPLETE_TASK
    assert len(parsed.tool_calls) == 1
    assert parsed.tool_calls[0]["parameters"]["task_id"] == "456"


def test_parse_response_delete_task(parser):
    """Test parsing delete_task tool call."""
    response_text = "Deleting task. delete_task(user_id='123', task_id='456')"

    parsed = parser.parse_response(response_text)

    assert parsed.intent == Intent.DELETE_TASK
    assert len(parsed.tool_calls) == 1


# JSON format tests

def test_parse_response_json_format(parser):
    """Test parsing JSON-formatted response."""
    response_text = """
    Here's what I'll do:
    ```json
    {
        "intent": "CREATE_TASK",
        "tool_calls": [
            {
                "tool_name": "add_task",
                "parameters": {
                    "user_id": "123",
                    "title": "Buy milk"
                }
            }
        ],
        "response": "Adding task to buy milk"
    }
    ```
    """

    parsed = parser.parse_response(response_text)

    assert parsed.intent == Intent.CREATE_TASK
    assert len(parsed.tool_calls) == 1
    assert parsed.tool_calls[0]["tool_name"] == "add_task"


# Clarification detection tests

def test_parse_response_clarification_which(parser):
    """Test detecting clarification requests with 'which'."""
    response_text = "Which task did you want to update?"

    parsed = parser.parse_response(response_text)

    assert parsed.intent == Intent.CLARIFICATION
    assert parsed.requires_clarification is True
    assert len(parsed.tool_calls) == 0


def test_parse_response_clarification_question(parser):
    """Test detecting clarification requests with questions."""
    response_text = "Can you specify which task you mean?"

    parsed = parser.parse_response(response_text)

    assert parsed.intent == Intent.CLARIFICATION
    assert parsed.requires_clarification is True


# Out of scope detection tests

def test_parse_response_out_of_scope(parser):
    """Test detecting out-of-scope responses."""
    response_text = (
        "I'm a task management assistant and can only help with "
        "creating, viewing, and managing tasks."
    )

    parsed = parser.parse_response(response_text)

    assert parsed.intent == Intent.OUT_OF_SCOPE
    assert len(parsed.tool_calls) == 0


# Natural response extraction tests

def test_extract_natural_response(parser):
    """Test extracting natural language part of response."""
    response_text = (
        "Sure, I'll add that for you! "
        "add_task(user_id='123', title='Buy groceries') "
        "The task has been created."
    )

    parsed = parser.parse_response(response_text)

    # Natural response should exclude the tool call
    assert "add_task(" not in parsed.natural_response
    assert parsed.natural_response.strip()  # Should have some text


# Multiple tool calls tests

def test_parse_response_multiple_tool_calls(parser):
    """Test parsing response with multiple tool calls."""
    response_text = (
        "I'll list your tasks and then add a new one. "
        "list_tasks(user_id='123') "
        "add_task(user_id='123', title='New task')"
    )

    parsed = parser.parse_response(response_text)

    assert len(parsed.tool_calls) == 2
    assert parsed.tool_calls[0]["tool_name"] == "list_tasks"
    assert parsed.tool_calls[1]["tool_name"] == "add_task"


# Parameter parsing tests

def test_parse_parameters_key_value(parser):
    """Test parsing key=value parameters."""
    params_str = "user_id='123', title='Buy milk', priority='high'"
    params = parser._parse_parameters(params_str)

    assert params["user_id"] == "123"
    assert params["title"] == "Buy milk"
    assert params["priority"] == "high"


def test_parse_parameters_with_arrays(parser):
    """Test parsing parameters with array values."""
    params_str = "user_id='123', tags=['work', 'urgent']"
    params = parser._parse_parameters(params_str)

    assert params["user_id"] == "123"
    assert isinstance(params["tags"], list)
    assert "work" in params["tags"]
    assert "urgent" in params["tags"]


def test_parse_parameters_empty(parser):
    """Test parsing empty parameters."""
    params = parser._parse_parameters("")

    assert params is None or params == {}


# Edge cases

def test_parse_response_no_tool_calls(parser):
    """Test parsing response with no tool calls."""
    response_text = "I understand. Let me help you with that."

    parsed = parser.parse_response(response_text)

    assert len(parsed.tool_calls) == 0
    assert parsed.natural_response == response_text


def test_parse_response_malformed_tool_call(parser):
    """Test handling malformed tool calls."""
    response_text = "add_task(this is not valid syntax)"

    parsed = parser.parse_response(response_text)

    # Should not crash, might have empty tool calls
    assert isinstance(parsed.tool_calls, list)


def test_parse_response_unknown_tool(parser):
    """Test ignoring unknown tool names."""
    response_text = "unknown_tool(param='value')"

    parsed = parser.parse_response(response_text)

    # Should ignore unknown tools
    assert len(parsed.tool_calls) == 0


def test_parse_response_confidence_scores(parser):
    """Test confidence scores for different response types."""
    # Tool call response should have high confidence
    tool_response = "add_task(user_id='123', title='Test')"
    parsed_tool = parser.parse_response(tool_response)
    assert parsed_tool.confidence >= 0.8

    # Unknown response should have lower confidence
    unknown_response = "I'm not sure what you mean"
    parsed_unknown = parser.parse_response(unknown_response)
    assert parsed_unknown.confidence < 0.8


def test_parse_response_empty(parser):
    """Test parsing empty response."""
    parsed = parser.parse_response("")

    assert parsed.intent == Intent.UNKNOWN
    assert len(parsed.tool_calls) == 0
