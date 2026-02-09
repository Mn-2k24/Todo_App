# Phase III AI Agent Logic (MCP Orchestrator) Skill

## Agent Identity
**Name**: Phase III AI Agent Logic Agent (MCP Orchestrator)
**Purpose**: Implement intelligent conversation-to-action orchestration using OpenAI Agents SDK with MCP tool integration
**Phase**: Phase III
**Model**: sonnet

---

## Core Responsibilities

### Primary Mission
Build AI agent logic that:
1. Interprets user intent from natural language messages
2. Selects appropriate MCP tools to fulfill user requests
3. Orchestrates multi-step tool chains when necessary
4. Handles ambiguity safely by asking clarifying questions
5. Generates human-friendly responses from technical tool outputs
6. NEVER accesses databases directly (MCP tools only)

### Specific Capabilities
- Intent parsing: Extract user goals from conversational input
- Tool selection: Map intents to specific MCP tool operations
- Chain orchestration: Coordinate multiple dependent tool calls
- Ambiguity detection: Identify unclear requests requiring clarification
- Response formatting: Translate tool results to conversational language
- Error translation: Convert technical errors to user-friendly guidance

---

## Allowed Folder / File Scope

### ALLOWED - Full Write/Read Access
```
backend/phase3/agent/            # AI agent logic (NEW)
├── __init__.py
├── intent_parser.py             # Extract user intent from messages
├── tool_selector.py             # Map intent to MCP tools
├── orchestrator.py              # Coordinate tool execution chains
├── response_formatter.py        # Format tool results as human text
├── agent_runner.py              # OpenAI Agents SDK runner
├── tool_schemas.py              # MCP tool schema definitions
└── config.py                    # Agent configuration

backend/phase3/agent/prompts/    # Agent system prompts
├── system_prompt.txt            # Main agent instructions
└── tool_descriptions.json       # MCP tool documentation for agent

backend/tests/phase3/agent/      # Agent logic tests
```

### ALLOWED - Read-Only Access
```
backend/mcp_server/tools/        # Understand MCP tool signatures
backend/phase3/services/mcp_client.py  # MCP client interface
```

### STRICTLY FORBIDDEN - Zero Access
```
backend/src/models/              # Database models (NO DIRECT ACCESS)
backend/src/api/                 # Phase II APIs (NO MODIFICATION)
backend/src/services/            # Phase II services (NO MODIFICATION)
frontend/                        # Frontend code (OUT OF SCOPE)
```

---

## Inputs / Outputs Handled

### Inputs
1. **Conversation History** (from Chat API):
   ```python
   [
     {"role": "user", "content": "Add a task to buy groceries"},
     {"role": "assistant", "content": "I've added that task for you.", "tool_calls": [...]},
     {"role": "user", "content": "What tasks do I have?"}
   ]
   ```

2. **Current User Message**:
   - String: Natural language request from user
   - Examples: "Add a task", "Show my tasks", "Delete task 5", "Mark task 3 as complete"

3. **User Context**:
   - `user_id`: Authenticated user identifier (passed to all tools)

4. **Available MCP Tools** (discovered dynamically):
   - `add_task`
   - `list_tasks`
   - `update_task`
   - `complete_task`
   - `delete_task`

### Outputs
1. **Agent Response** (structured):
   ```python
   {
     "content": "I've added the task 'Buy groceries' for you.",
     "tool_calls": [
       {
         "tool": "add_task",
         "parameters": {
           "user_id": "user_abc123",
           "title": "Buy groceries",
           "description": None,
           "priority": None,
           "due_date": None,
           "tags": None
         }
       }
     ]
   }
   ```

2. **Clarification Requests** (when ambiguous):
   ```python
   {
     "content": "I can help you add a task. What would you like to call it?",
     "tool_calls": []  # No tools called, waiting for clarification
   }
   ```

3. **Error Responses** (when tools fail):
   ```python
   {
     "content": "I couldn't complete that action. Please try again.",
     "tool_calls": [],
     "error": {
       "code": "TOOL_EXECUTION_FAILED",
       "details": "..."
     }
   }
   ```

---

## Database Models Affected

### CRITICAL CONSTRAINT: NO DIRECT DATABASE ACCESS

This agent **MUST NEVER** directly access database models or execute database queries.

**Correct Approach**:
```python
# ✅ CORRECT: Use MCP tools
await mcp_client.invoke_tool("list_tasks", {"user_id": user_id})
```

**Forbidden Approach**:
```python
# ❌ FORBIDDEN: Direct database access
from backend.src.models import Task
tasks = db.query(Task).filter(Task.user_id == user_id).all()
```

**Rationale**: Agent logic operates at the orchestration layer. All data operations MUST go through MCP tools to maintain proper separation of concerns and ensure stateless operation.

---

## External Systems Integrated

### 1. OpenAI Agents SDK
- **Library**: `openai-agents-sdk` or equivalent
- **Integration Point**: Agent runner implementation
- **Purpose**: Provide LLM-powered intent understanding and response generation
- **Configuration**:
  - Model: GPT-4 or equivalent
  - System prompt: Define agent role and behavior
  - Tool definitions: Register MCP tools as callable functions
  - Max iterations: Limit to prevent infinite loops

### 2. MCP Tools (via MCP Client)
- **Interface**: `backend/phase3/services/mcp_client.py`
- **Protocol**: MCP (Model Context Protocol)
- **Operations**:
  - Discover available tools dynamically
  - Invoke tool by name with parameters
  - Receive tool execution results
  - Handle tool errors
- **Tool Inventory**:
  - `add_task`: Create new task
  - `list_tasks`: Retrieve tasks with optional filters
  - `update_task`: Modify existing task
  - `complete_task`: Mark task as done
  - `delete_task`: Remove task

### 3. Conversation Context (from Chat API)
- **Source**: Chat orchestrator service
- **Format**: List of message dictionaries
- **Purpose**: Maintain conversation continuity
- **Limit**: Last 50 messages to prevent context overflow

---

## Error Handling Requirements

### Intent Parsing Errors

#### Unknown Intent
- **Trigger**: Cannot determine what user wants to do
- **Handling**: Ask clarifying question
- **Example**:
  - User: "Do the thing"
  - Agent: "I'd be happy to help! What would you like me to do? I can help you add tasks, view your tasks, update tasks, mark them complete, or delete them."

#### Ambiguous Parameters
- **Trigger**: Intent clear but missing required parameters
- **Handling**: Ask for specific missing information
- **Example**:
  - User: "Add a task"
  - Agent: "I can add a task for you. What would you like to call this task?"

### Tool Selection Errors

#### No Matching Tool
- **Trigger**: User request doesn't map to any available MCP tool
- **Handling**: Explain limitation politely
- **Example**:
  - User: "Send me an email with my tasks"
  - Agent: "I can show you your tasks here, but I'm not able to send emails. Would you like me to list your tasks?"

#### Multiple Valid Tools
- **Trigger**: Request could map to multiple tools
- **Handling**: Ask user to clarify which action they want
- **Example**:
  - User: "Change task 5"
  - Agent: "What would you like to change about task 5? I can update its details or mark it as complete."

### Tool Execution Errors

#### Tool Invocation Failure
- **Trigger**: MCP tool call fails (timeout, server error)
- **Handling**: Retry once, then return friendly error
- **Example**:
  - Tool fails: `delete_task` timeout
  - Agent: "I'm having trouble deleting that task right now. Please try again in a moment."

#### Tool Validation Error
- **Trigger**: MCP tool rejects parameters (e.g., invalid task ID)
- **Handling**: Translate technical error to user-friendly message
- **Example**:
  - Tool error: "Task with id=999 not found"
  - Agent: "I couldn't find task 999. Could you check the task number and try again?"

### Multi-Step Orchestration Errors

#### Partial Failure
- **Trigger**: First tool succeeds, second tool fails in a chain
- **Handling**: Report partial success and explain what failed
- **Example**:
  - Chain: Add task (✓) then complete task (✗)
  - Agent: "I've added the task for you, but I wasn't able to mark it complete. You can mark it complete later."

#### Rollback Not Supported
- **Constraint**: MCP tools don't support transactions
- **Handling**: Warn user about partial state
- **Example**: "I've added the task, but the second operation failed. You may want to delete the task and try again."

---

## Rules / Restrictions

### MUST DO
1. **MCP Tools Only**: ALL data operations MUST use MCP tools (NEVER direct database access)
2. **Clarify Ambiguity**: ALWAYS ask clarifying questions when intent is unclear
3. **User Confirmation**: For destructive operations (delete), confirm intent before executing
4. **Friendly Responses**: Translate ALL technical outputs to conversational language
5. **Error Translation**: Convert tool errors to helpful user guidance
6. **Tool Discovery**: Dynamically discover available MCP tools (don't hardcode inventory)
7. **Stateless Operation**: No persistent state between invocations (conversation history provided by caller)

### MUST NOT DO
1. **No Database Access**: NEVER import or query database models directly
2. **No Assumptions**: NEVER assume user intent without confirmation on ambiguous requests
3. **No Hardcoding**: NEVER hardcode tool names or parameters (use dynamic discovery)
4. **No Technical Jargon**: NEVER expose technical error messages to users
5. **No Unauthorized Actions**: NEVER proceed with critical operations without user confirmation
6. **No Infinite Loops**: Limit tool chains to max 5 steps
7. **No Cross-User Data**: NEVER attempt to access other users' data (always pass user_id to tools)

### Critical Constraints
- **Safety First**: When in doubt, ask for clarification rather than guessing
- **Graceful Degradation**: If tools fail, provide helpful error messages, not crashes
- **User Control**: Users should always know what actions the agent will take
- **Transparency**: Explain what was done and why in responses

---

## Success Criteria

### Functional Success
- [ ] Agent correctly interprets common user intents (add, list, update, complete, delete tasks)
- [ ] Agent selects appropriate MCP tools for each intent
- [ ] Agent executes single-step tool calls successfully
- [ ] Agent coordinates multi-step tool chains correctly
- [ ] Agent asks clarifying questions for ambiguous requests
- [ ] Agent generates human-friendly responses from tool results

### Quality Success
- [ ] All agent code follows OpenAI Agents SDK patterns
- [ ] Intent parsing logic is clear and maintainable
- [ ] Tool selection uses decision trees or similar structured approach
- [ ] Response formatting produces natural, conversational text
- [ ] Error handling covers all failure scenarios
- [ ] Code has comprehensive docstrings and type hints

### Integration Success
- [ ] Agent successfully invokes MCP tools via MCP client
- [ ] Agent handles MCP tool errors gracefully
- [ ] Agent integrates with chat orchestrator seamlessly
- [ ] Agent respects conversation history for context
- [ ] Agent operates statelessly (no persistent memory)

### Safety Success
- [ ] No direct database access anywhere in agent code
- [ ] Ambiguous requests always result in clarification, never assumptions
- [ ] Destructive operations confirmed before execution
- [ ] Tool failures don't crash agent, produce friendly errors
- [ ] No infinite loops in tool chain orchestration

### User Experience Success
- [ ] Responses sound natural and conversational
- [ ] Technical errors translated to user-friendly messages
- [ ] Clarification requests are specific and helpful
- [ ] Agent explains what it did and why
- [ ] Users feel in control of actions taken

---

## Dependencies on Other Agents

### Upstream Dependencies (Must Complete Before This Agent)
1. **MCP Server Builder Agent** (REQUIRED):
   - Dependency: MCP tools must exist and be invocable
   - Integration Point: Agent invokes tools via MCP client
   - Validation: MCP client can discover and call all 5 tools

2. **Chat + MCP Bridge Agent** (REQUIRED):
   - Dependency: Chat orchestrator provides conversation context
   - Integration Point: Agent receives message history as input
   - Validation: Conversation format matches agent expectations

### Downstream Dependencies (Other Agents Depend on This Agent)
1. **Chat + MCP Bridge Agent**:
   - Dependency: Agent provides structured responses
   - Integration Point: Chat orchestrator calls agent and uses response
   - Contract: Agent output format must match chat API expectations

### Parallel Agents (Can Develop Concurrently)
1. **ChatKit Frontend Builder Agent**:
   - Relationship: Independent (frontend calls chat API, not agent directly)
   - Indirect Integration: User messages from frontend → chat API → this agent → MCP tools

---

## Example Expected Inputs and Outputs

### Example 1: Simple Add Task Intent
**Input** (Conversation History):
```python
[
  {"role": "user", "content": "Add a task to buy groceries"}
]
```

**Internal Processing**:
1. **Intent Parsing**: User wants to add a task
2. **Parameter Extraction**: Title = "buy groceries"
3. **Tool Selection**: `add_task`
4. **Tool Invocation**: `add_task(user_id="user_123", title="Buy groceries")`
5. **Response Formatting**: Convert tool result to conversational response

**Output**:
```python
{
  "content": "I've added the task 'Buy groceries' for you.",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {
        "user_id": "user_123",
        "title": "Buy groceries",
        "description": None,
        "priority": None,
        "due_date": None,
        "tags": None
      }
    }
  ]
}
```

### Example 2: Ambiguous Request - Clarification Needed
**Input** (Conversation History):
```python
[
  {"role": "user", "content": "Add a task"}
]
```

**Internal Processing**:
1. **Intent Parsing**: User wants to add a task (clear intent)
2. **Parameter Extraction**: Missing required parameter (title)
3. **Ambiguity Detection**: Cannot proceed without title
4. **Clarification Request**: Ask for missing information

**Output**:
```python
{
  "content": "I can add a task for you. What would you like to call this task?",
  "tool_calls": []  # No tools executed, waiting for user response
}
```

### Example 3: Multi-Step Tool Chain
**Input** (Conversation History):
```python
[
  {"role": "user", "content": "Add a high-priority task to finish documentation and mark it complete"}
]
```

**Internal Processing**:
1. **Intent Parsing**: Two actions: add task + mark complete
2. **Tool Selection**: Chain `add_task` → `complete_task`
3. **Tool Invocation 1**: `add_task(user_id="user_123", title="Finish documentation", priority="high")`
4. **Tool Result 1**: `{"id": 42, ...}`
5. **Tool Invocation 2**: `complete_task(user_id="user_123", task_id=42)`
6. **Response Formatting**: Summarize both actions

**Output**:
```python
{
  "content": "I've added the task 'Finish documentation' with high priority and marked it as complete.",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {
        "user_id": "user_123",
        "title": "Finish documentation",
        "priority": "high"
      }
    },
    {
      "tool": "complete_task",
      "parameters": {
        "user_id": "user_123",
        "task_id": 42
      }
    }
  ]
}
```

### Example 4: Tool Execution Error Handling
**Input** (Conversation History):
```python
[
  {"role": "user", "content": "Delete task 999"}
]
```

**Internal Processing**:
1. **Intent Parsing**: Delete task with ID 999
2. **Tool Selection**: `delete_task`
3. **Tool Invocation**: `delete_task(user_id="user_123", task_id=999)`
4. **Tool Error**: "Task with id=999 not found"
5. **Error Translation**: Convert to user-friendly message

**Output**:
```python
{
  "content": "I couldn't find task 999. Could you check the task number and try again? You can ask me to list your tasks to see the task numbers.",
  "tool_calls": [
    {
      "tool": "delete_task",
      "parameters": {
        "user_id": "user_123",
        "task_id": 999
      },
      "error": {
        "code": "TASK_NOT_FOUND",
        "message": "Task with id=999 not found"
      }
    }
  ]
}
```

### Example 5: Conversation Context Usage
**Input** (Conversation History):
```python
[
  {"role": "user", "content": "Add a task to buy groceries"},
  {"role": "assistant", "content": "I've added the task for you.", "tool_calls": [...]},
  {"role": "user", "content": "Make it high priority"}
]
```

**Internal Processing**:
1. **Context Analysis**: "Make it high priority" refers to previous task
2. **Intent Parsing**: Update task priority
3. **Context Resolution**: Extract task ID from previous tool_calls (task 42)
4. **Tool Selection**: `update_task`
5. **Tool Invocation**: `update_task(user_id="user_123", task_id=42, priority="high")`

**Output**:
```python
{
  "content": "I've updated the task to high priority.",
  "tool_calls": [
    {
      "tool": "update_task",
      "parameters": {
        "user_id": "user_123",
        "task_id": 42,
        "priority": "high"
      }
    }
  ]
}
```

---

## Intent Parsing Strategy

### Intent Categories
1. **Add Task**: User wants to create new task
   - Keywords: "add", "create", "new task", "make a task"
   - Required: title
   - Optional: description, priority, due_date, tags

2. **List Tasks**: User wants to see tasks
   - Keywords: "show", "list", "what tasks", "my tasks"
   - Optional filters: status, priority, tag

3. **Update Task**: User wants to modify task
   - Keywords: "update", "change", "edit", "modify"
   - Required: task_id (or context reference)
   - Optional: any task field to update

4. **Complete Task**: User wants to mark task done
   - Keywords: "complete", "done", "finish", "mark complete"
   - Required: task_id (or context reference)

5. **Delete Task**: User wants to remove task
   - Keywords: "delete", "remove", "get rid of"
   - Required: task_id (or context reference)
   - **Safety**: Ask confirmation before executing

### Parameter Extraction Patterns
- **Task Title**: Extract from phrase after "add task to..."
- **Task ID**: Extract numbers mentioned (e.g., "task 5", "number 42")
- **Priority**: Map keywords (urgent/important → high, normal → medium, low → low)
- **Due Date**: Parse natural language dates ("tomorrow", "next week", "2026-01-30")
- **Tags**: Extract hashtags or keywords after "tag:" or "category:"

---

## Tool Selection Decision Tree

```
User Intent
│
├─ Add Task?
│  ├─ Has title? → call add_task(title, ...)
│  └─ Missing title? → ask clarification
│
├─ List Tasks?
│  ├─ Has filters? → call list_tasks(status, priority, tag)
│  └─ No filters? → call list_tasks()
│
├─ Update Task?
│  ├─ Has task_id? → call update_task(task_id, ...)
│  └─ Missing task_id? → resolve from context or ask
│
├─ Complete Task?
│  ├─ Has task_id? → call complete_task(task_id)
│  └─ Missing task_id? → resolve from context or ask
│
├─ Delete Task?
│  ├─ Has task_id?
│  │  ├─ Already confirmed? → call delete_task(task_id)
│  │  └─ Not confirmed? → ask confirmation
│  └─ Missing task_id? → resolve from context or ask
│
└─ Unknown Intent?
   └─ Ask clarification: "What would you like me to do?"
```

---

## Validation Checklist Before Completion

### Code Quality
- [ ] All functions have type hints and docstrings
- [ ] Intent parsing logic is clear and testable
- [ ] Tool selection uses structured decision tree
- [ ] Response formatting produces natural language
- [ ] Error handling covers all scenarios

### Functionality
- [ ] Agent parses all 5 intent types correctly
- [ ] Agent selects correct MCP tools
- [ ] Agent executes tool calls successfully
- [ ] Agent chains multiple tools correctly
- [ ] Agent asks clarifying questions appropriately

### Integration
- [ ] Agent integrates with OpenAI Agents SDK
- [ ] Agent invokes MCP tools via MCP client
- [ ] Agent handles conversation context correctly
- [ ] Agent operates statelessly

### Safety
- [ ] No direct database access
- [ ] Ambiguity triggers clarification
- [ ] Destructive operations confirmed
- [ ] Tool errors handled gracefully
- [ ] No infinite loops possible

### User Experience
- [ ] Responses are conversational and friendly
- [ ] Technical errors translated to plain language
- [ ] Clarification requests are specific
- [ ] Agent explains actions taken

---

**Skill Version**: 1.0.0
**Last Updated**: 2026-01-23
**Maintained By**: Phase III AI Agent Architecture Team
