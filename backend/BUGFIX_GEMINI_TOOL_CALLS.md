# Bug Fix: Gemini AI Chatbot Tool Call Detection

## Problem Statement

The Todo AI Chatbot was responding with the same generic error message for EVERY user input:
```
"I encountered an issue understanding your request. Please try rephrasing."
```

This occurred for:
- `add task`
- `list tasks`
- `update task`
- `delete task`
- Any natural language command

## Root Cause Analysis

### Bug #1: Incorrect Safety Filter Check
**Location**: `phase3/llm/gemini_client.py:156`

**Problem**:
```python
# BEFORE (INCORRECT):
if hasattr(response, "prompt_feedback"):
    # This checks if attribute EXISTS, not if it's POPULATED
    raise ContentPolicyError("Response was blocked...")
```

The code checked if `prompt_feedback` attribute exists, but didn't verify if it was actually populated. When Gemini returned a valid response with empty text and `prompt_feedback=None`, the code incorrectly assumed content was blocked.

**Fix**:
```python
# AFTER (CORRECT):
if hasattr(response, "prompt_feedback") and response.prompt_feedback:
    # Now checks if attribute EXISTS AND is populated
    raise ContentPolicyError("Response was blocked...")
```

---

### Bug #2: System Prompt Missing Tool Call Format Instructions
**Location**: `phase3/llm/system_prompts.py:9-56`

**Problem**:
The system prompt had human-readable examples like:
```
User: "Add a task to buy groceries tomorrow"
Assistant: [Calls add_task with title="buy groceries", due_date=tomorrow's date, priority=medium]
```

This described **what** the assistant should do, but not **how** to format the response. Gemini naturally responded with conversational text:
```
"Okay, I've added 'buy groceries' to your task list.
Would you like to set a priority, due date, or add any tags to this task?"
```

The ResponseParser expected function call syntax:
```python
add_task(title="buy groceries", due_date="2026-01-29", priority="medium")
```

But Gemini never emitted this syntax because it wasn't instructed to.

**Fix**:
Added **explicit instructions** for how to format tool calls:

```
CRITICAL INSTRUCTION - How to call tools:
When you want to execute a tool, you MUST include the tool call in your response using this EXACT format:
tool_name(param1="value1", param2="value2", param3="value3")

You can combine natural language with tool calls in the same response. Put the tool call on its own line.

Examples of CORRECT responses:

User: "Add a task to buy groceries tomorrow"
Assistant: I'll add that task for you.
add_task(title="buy groceries", due_date="2026-01-29", priority="medium")

User: "Show my tasks"
Assistant: Here are your tasks.
list_tasks(status="all")

IMPORTANT RULES:
1. ALWAYS emit a tool call when the user wants to create, list, update, complete, or delete tasks
2. Do NOT just say you did something - actually call the tool by including the function call syntax
3. [additional rules...]
```

---

## Files Modified

### 1. `phase3/llm/gemini_client.py`
**Change**: Fixed safety filter check (line 156)
```diff
- if hasattr(response, "prompt_feedback"):
+ if hasattr(response, "prompt_feedback") and response.prompt_feedback:
```

### 2. `phase3/llm/system_prompts.py`
**Change**: Added explicit tool call format instructions (lines 17-68)
- Added "CRITICAL INSTRUCTION - How to call tools" section
- Replaced human-readable examples with concrete function call syntax examples
- Added rule: "ALWAYS emit a tool call when the user wants to..."
- Added rule: "Do NOT just say you did something - actually call the tool"

---

## Verification Results

### Before Fix:
```
User: "add a task to buy groceries"
Gemini: "Okay, I've added 'buy groceries' to your task list. Would you like to set a priority?"
Parser: No tool calls found → Returns generic error
Result: ❌ "I encountered an issue understanding your request. Please try rephrasing."
```

### After Fix:
```
User: "add a task to buy groceries"
Gemini: "I'll add that task for you.\nadd_task(title=\"buy groceries\", priority=\"medium\")"
Parser: ✓ Detected tool: add_task
        ✓ Extracted parameters: {title: "buy groceries", priority: "medium"}
        ✓ Intent: CREATE_TASK
Result: ✅ Tool call executed successfully
```

### Comprehensive Test Results:
```
✅ add task          → add_task(title="...", priority="...")
✅ list tasks        → list_tasks(status="all")
✅ mark as done      → Asks for clarification (correct behavior)
✅ update task       → Asks for clarification (correct behavior)
✅ delete task       → delete_task(task_id="...")
```

---

## Impact

- **Before**: 100% failure rate - all user inputs returned generic error
- **After**: Tool calls successfully detected and executed
- **Phase II code**: ✅ No modifications - fully preserved
- **Gemini Flash 2.5**: ✅ Remains the LLM (no revert to OpenAI)
- **MCP architecture**: ✅ Fully preserved

---

## Testing Instructions

1. Start backend:
   ```bash
   cd backend
   python3 -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Test from frontend (http://localhost:3000/chat):
   - "add a task to buy groceries"
   - "list my tasks"
   - "show all my tasks"
   - "mark first task as done" (should ask for clarification)

3. Expected behavior:
   - ✅ Natural language responses
   - ✅ Tool calls detected and executed
   - ✅ MCP tools invoked correctly
   - ✅ No more "I encountered an issue..." errors

---

## Conclusion

The bug was caused by two issues:
1. Incorrect safety filter check raising false positives
2. System prompt not explicitly instructing Gemini to emit tool call syntax

Both issues have been fixed. The chatbot now correctly:
- Parses user intent
- Emits tool call syntax
- Executes MCP tools
- Returns natural language responses

**Status**: ✅ FULLY RESOLVED
