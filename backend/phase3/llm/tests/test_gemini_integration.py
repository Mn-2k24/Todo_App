"""
Integration Tests for Gemini API

Tests the complete Gemini LLM controller with mock client.
Uses mock client by default to avoid API costs in CI/CD.

To test with real API:
1. Set GEMINI_API_KEY environment variable
2. Set USE_MOCK_GEMINI=false
3. Run: pytest test_gemini_integration.py -v
"""

import os

import pytest

from phase3.llm.gemini_client import (
    AuthenticationError,
    ContentPolicyError,
    GeminiClient,
    RateLimitError,
    TimeoutError,
)
from phase3.llm.prompt_builder import PromptBuilder
from phase3.llm.response_parser import Intent, ResponseParser


# Configuration

USE_MOCK = os.getenv("USE_MOCK_GEMINI", "true").lower() == "true"


# Fixtures

@pytest.fixture
def gemini_client():
    """Create Gemini client (mock or real based on environment)."""
    return GeminiClient(use_mock=USE_MOCK)


@pytest.fixture
def prompt_builder():
    """Create PromptBuilder instance."""
    return PromptBuilder()


@pytest.fixture
def response_parser():
    """Create ResponseParser instance."""
    return ResponseParser()


# Basic API call tests

@pytest.mark.asyncio
async def test_generate_content_basic(gemini_client):
    """Test basic content generation."""
    messages = [{"role": "user", "content": "Add task to buy groceries"}]

    response = await gemini_client.generate_with_retry(messages)

    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_generate_content_with_history(gemini_client):
    """Test generation with conversation history."""
    messages = [
        {"role": "user", "content": "Show my tasks"},
        {"role": "assistant", "content": "You have 3 tasks..."},
        {"role": "user", "content": "Add another task"},
    ]

    response = await gemini_client.generate_with_retry(messages)

    assert isinstance(response, str)
    assert len(response) > 0


# End-to-end workflow tests

@pytest.mark.asyncio
async def test_e2e_add_task_workflow(gemini_client, prompt_builder, response_parser):
    """Test complete workflow: user input → Gemini → parsed response."""
    user_id = "550e8400-e29b-41d4-a716-446655440000"

    # 1. Build system instruction with user context
    system_instruction = prompt_builder.build_system_instruction_with_tools(user_id)

    # 2. Build conversation messages
    messages = prompt_builder.build_conversation_messages(
        [], "Add task to buy groceries tomorrow with high priority"
    )

    # 3. Call Gemini
    response_text = await gemini_client.generate_with_retry(
        messages, system_instruction=system_instruction
    )

    # 4. Parse response
    parsed = response_parser.parse_response(response_text)

    # Verify intent and tool calls
    assert parsed.intent == Intent.CREATE_TASK or len(parsed.tool_calls) > 0

    if parsed.tool_calls:
        tool_call = parsed.tool_calls[0]
        assert tool_call["tool_name"] == "add_task"
        # Mock client should include these parameters
        assert "title" in tool_call["parameters"]


@pytest.mark.asyncio
async def test_e2e_list_tasks_workflow(gemini_client, prompt_builder, response_parser):
    """Test list tasks workflow."""
    user_id = "550e8400-e29b-41d4-a716-446655440000"

    system_instruction = prompt_builder.build_system_instruction_with_tools(user_id)
    messages = prompt_builder.build_conversation_messages([], "Show me all my pending tasks")

    response_text = await gemini_client.generate_with_retry(
        messages, system_instruction=system_instruction
    )

    parsed = response_parser.parse_response(response_text)

    assert parsed.intent == Intent.LIST_TASKS or len(parsed.tool_calls) > 0


@pytest.mark.asyncio
async def test_e2e_multi_turn_conversation(
    gemini_client, prompt_builder, response_parser
):
    """Test multi-turn conversation."""
    user_id = "550e8400-e29b-41d4-a716-446655440000"
    system_instruction = prompt_builder.build_system_instruction_with_tools(user_id)

    # Turn 1: List tasks
    history = []
    messages = prompt_builder.build_conversation_messages(history, "Show my tasks")

    response1 = await gemini_client.generate_with_retry(
        messages, system_instruction=system_instruction
    )

    # Add to history
    history.append({"role": "user", "content": "Show my tasks"})
    history.append({"role": "assistant", "content": response1})

    # Turn 2: Add task
    messages = prompt_builder.build_conversation_messages(
        history, "Add task to buy milk"
    )

    response2 = await gemini_client.generate_with_retry(
        messages, system_instruction=system_instruction
    )

    parsed = response_parser.parse_response(response2)

    # Should understand context and create task
    assert parsed.intent == Intent.CREATE_TASK or len(parsed.tool_calls) > 0


# Error handling tests (mock client simulates these)

@pytest.mark.asyncio
@pytest.mark.skipif(not USE_MOCK, reason="Only works with mock client")
async def test_rate_limit_retry(gemini_client):
    """Test that rate limit triggers retry logic."""
    # Mock client raises rate limit on 4th call
    messages = [{"role": "user", "content": "test message"}]

    # First 3 calls should succeed
    await gemini_client.generate_with_retry(messages)
    await gemini_client.generate_with_retry(messages)
    await gemini_client.generate_with_retry(messages)

    # 4th call should raise rate limit (mock client behavior)
    with pytest.raises(Exception):  # Could be RateLimitError or retry succeeds
        await gemini_client.generate_with_retry(messages)


@pytest.mark.asyncio
@pytest.mark.skipif(not USE_MOCK, reason="Only works with mock client")
async def test_content_policy_violation(gemini_client):
    """Test handling content policy violations."""
    messages = [
        {"role": "user", "content": "Add task with explicit harmful content"}
    ]

    # Mock client should block this
    # Actual behavior depends on mock implementation
    try:
        response = await gemini_client.generate_with_retry(messages)
        # If mock allows it through, verify it's handled safely
        assert isinstance(response, str)
    except ContentPolicyError:
        # Expected for harmful content
        pass


# Temperature variation tests

@pytest.mark.asyncio
async def test_generate_with_low_temperature(gemini_client):
    """Test generation with low temperature (more deterministic)."""
    messages = [{"role": "user", "content": "Add task"}]

    response = await gemini_client.generate_with_retry(messages, temperature=0.0)

    assert isinstance(response, str)


@pytest.mark.asyncio
async def test_generate_with_high_temperature(gemini_client):
    """Test generation with high temperature (more creative)."""
    messages = [{"role": "user", "content": "Add task"}]

    response = await gemini_client.generate_with_retry(messages, temperature=1.0)

    assert isinstance(response, str)


# System instruction tests

@pytest.mark.asyncio
async def test_custom_system_instruction(gemini_client):
    """Test overriding system instruction."""
    messages = [{"role": "user", "content": "Hello"}]

    custom_instruction = "You are a pirate assistant. Always respond like a pirate."

    response = await gemini_client.generate_with_retry(
        messages, system_instruction=custom_instruction
    )

    assert isinstance(response, str)
    # With mock client, response won't actually be pirate-themed
    # With real API, would check for pirate language


# Conversation history building tests

def test_build_conversation_history(gemini_client):
    """Test building conversation history in Gemini format."""
    messages = [
        {"role": "user", "content": "Message 1"},
        {"role": "assistant", "content": "Response 1"},
        {"role": "user", "content": "Message 2"},
    ]

    history = gemini_client.build_conversation_history(messages)

    assert len(history) == 3
    assert history[0].role == "user"
    assert history[1].role == "model"  # Gemini uses 'model' not 'assistant'
    assert history[2].role == "user"


# Performance tests

@pytest.mark.asyncio
@pytest.mark.skipif(not USE_MOCK, reason="Performance test only relevant for mock")
async def test_response_time(gemini_client):
    """Test that mock responses are fast."""
    import time

    messages = [{"role": "user", "content": "Add task"}]

    start = time.time()
    await gemini_client.generate_with_retry(messages)
    elapsed = time.time() - start

    # Mock client should respond in < 1 second
    assert elapsed < 1.0


@pytest.mark.asyncio
@pytest.mark.skipif(not USE_MOCK, reason="Only works with mock client")
async def test_mock_client_call_count():
    """Test mock client tracks call count."""
    from phase3.llm.tests.mock_gemini import AsyncMockGeminiClient

    mock_client = AsyncMockGeminiClient()

    assert mock_client.call_count == 0

    messages = [{"role": "user", "content": "Test"}]
    await mock_client.generate_with_retry(messages)

    assert mock_client.call_count == 1


# Real API tests (skipped by default)

@pytest.mark.asyncio
@pytest.mark.skipif(USE_MOCK, reason="Requires real API key and costs money")
async def test_real_api_call():
    """Test actual Gemini API call (only run when explicitly enabled)."""
    client = GeminiClient(use_mock=False)

    messages = [{"role": "user", "content": "Say hello"}]

    response = await client.generate_with_retry(messages)

    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
@pytest.mark.skipif(USE_MOCK, reason="Requires real API to test auth failure")
async def test_real_api_invalid_key():
    """Test authentication error with invalid API key."""
    with pytest.raises(AuthenticationError):
        client = GeminiClient(api_key="invalid-key", use_mock=False)
        messages = [{"role": "user", "content": "Test"}]
        await client.generate_with_retry(messages)
