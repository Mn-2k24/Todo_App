# Feature Specification: Phase III - AI Chatbot with MCP Server

**Feature Branch**: `004-phase-iii-chatbot`
**Created**: 2026-01-23
**Status**: Draft
**Input**: User description: "Extend the Todo Full-Stack Web Application with AI chatbot functionality using MCP server, OpenAI Agents SDK, and ChatKit frontend"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Task Management (Priority: P1)

Users can create, update, and manage tasks through conversational AI instead of clicking through forms.

**Why this priority**: This is the core value proposition - enabling users to manage tasks using natural language commands, which provides a fundamentally better UX than traditional form-based interaction.

**Independent Test**: Can be fully tested by sending chat messages like "Add a task to buy groceries tomorrow" and verifying the task appears in the task list. Delivers immediate value as a complete feature.

**Acceptance Scenarios**:

1. **Given** user is authenticated and on the chat page, **When** user types "Add a task to buy groceries tomorrow with high priority", **Then** system creates a new task with title "Buy groceries", due date set to tomorrow, priority "high", and confirms creation in chat
2. **Given** user has existing tasks, **When** user types "Show me all my high priority tasks", **Then** system displays a filtered list of high priority tasks in the chat response
3. **Given** user has a task with ID 5, **When** user types "Mark task 5 as complete", **Then** system marks the task as completed and confirms the action
4. **Given** user types "Delete the grocery task", **When** system finds multiple tasks matching "grocery", **Then** system asks for clarification before proceeding

---

### User Story 2 - Multi-Turn Conversation Context (Priority: P1)

Users can have multi-turn conversations where the AI remembers previous context within the session.

**Why this priority**: Essential for natural conversation flow - users shouldn't have to repeat information or provide full context in every message.

**Independent Test**: Start a conversation, reference a task created in message 1 using pronouns or partial information in message 3. System should resolve the reference correctly using conversation history.

**Acceptance Scenarios**:

1. **Given** user asked "What are my tasks?" in message 1, **When** user follows up with "Mark the first one as done" in message 2, **Then** system uses conversation history to identify which task to mark complete
2. **Given** user created a task for "Buy groceries" in message 1, **When** user says "Add high priority to that task" in message 2, **Then** system updates the grocery task with high priority
3. **Given** user has a 5-message conversation about project tasks, **When** user says "Show me everything we discussed", **Then** system can summarize the conversation history

---

### User Story 3 - Persistent Conversation History (Priority: P2)

Users can return to previous conversations and continue where they left off, with full history preserved.

**Why this priority**: Improves long-term usability by allowing users to maintain context across sessions, though not critical for initial MVP functionality.

**Independent Test**: Create a conversation, log out, log back in, and verify the conversation appears in history and can be resumed with context intact.

**Acceptance Scenarios**:

1. **Given** user created tasks via chat yesterday, **When** user opens the chat page today, **Then** user sees the previous conversation and can reference tasks created in that conversation
2. **Given** user has multiple conversations, **When** user selects a specific conversation from history, **Then** system loads that conversation's full message history
3. **Given** user is in a conversation from last week, **When** user types "What did we discuss about the project?", **Then** system can reference messages from that specific conversation

---

### User Story 4 - Error Recovery and Clarification (Priority: P2)

When the AI cannot determine user intent or encounters errors, it asks for clarification instead of guessing or failing silently.

**Why this priority**: Critical for user trust and data integrity, but depends on the core functionality being in place first.

**Independent Test**: Send ambiguous commands like "update the task" without specifying which task. System should ask "Which task would you like to update?" with available options.

**Acceptance Scenarios**:

1. **Given** user has 3 tasks titled "Project", **When** user types "Delete the project task", **Then** system lists the 3 matching tasks and asks which one to delete
2. **Given** user types an unclear command like "make it tomorrow", **When** system cannot determine which task to update, **Then** system asks "Which task would you like to reschedule?"
3. **Given** user attempts to complete a non-existent task, **When** the task ID doesn't exist, **Then** system responds with "I couldn't find task #X. Would you like to see your current tasks?"

---

### User Story 5 - Task Creation with All Metadata (Priority: P2)

Users can specify all task attributes (title, description, priority, due date, tags) in a single natural language command.

**Why this priority**: Enhances UX but not required for MVP - users can create basic tasks first and add metadata separately.

**Independent Test**: Send message "Create a high priority task to finish the report by Friday, tagged as work and urgent, with description 'Complete Q4 financial analysis'". Verify all attributes are correctly extracted and saved.

**Acceptance Scenarios**:

1. **Given** user types "Add a task to call John tomorrow at 3pm, high priority, tagged as follow-up", **When** system processes the command, **Then** task is created with title "Call John", due date tomorrow 3pm, priority "high", tags ["follow-up"]
2. **Given** user omits priority in command, **When** creating a task, **Then** system creates task with default priority or asks "What priority should this task have?"
3. **Given** user provides relative date like "next Monday", **When** creating a task, **Then** system correctly converts to absolute date

---

### User Story 6 - Bulk Operations via Natural Language (Priority: P3)

Users can perform bulk actions on multiple tasks using natural language filters.

**Why this priority**: Power-user feature that provides significant efficiency gains but not essential for core functionality.

**Independent Test**: Create 5 tasks with tag "shopping", then send "Complete all shopping tasks". Verify all 5 tasks are marked complete with a single command.

**Acceptance Scenarios**:

1. **Given** user has 10 tasks tagged "meeting", **When** user types "Delete all meeting tasks", **Then** system confirms and deletes all 10 tasks
2. **Given** user has overdue tasks, **When** user types "Show me all overdue tasks and mark them as high priority", **Then** system updates all overdue tasks to high priority
3. **Given** user has completed tasks from last month, **When** user types "Archive all completed tasks from December", **Then** system archives matching tasks

---

### User Story 7 - Mobile-Responsive Chat Interface (Priority: P3)

Chat interface adapts seamlessly to mobile devices with touch-optimized interactions.

**Why this priority**: Important for accessibility but can be implemented after core desktop experience is solid.

**Independent Test**: Open chat page on mobile device, send messages, scroll through history, and verify all interactions work smoothly on small screens.

**Acceptance Scenarios**:

1. **Given** user accesses chat on mobile device, **When** typing a message, **Then** keyboard doesn't obscure the input field and messages
2. **Given** user has long conversation history on mobile, **When** scrolling through messages, **Then** performance remains smooth and responsive
3. **Given** user receives long AI responses on mobile, **When** viewing the message, **Then** text wraps correctly and remains readable

---

### Edge Cases

- What happens when user sends a message while the AI is still processing the previous message?
- How does system handle database connection failures during MCP tool execution?
- What happens when OpenAI API rate limit is exceeded?
- How does system handle user_id mismatch between JWT token and conversation owner?
- What happens when user requests to update a task that was deleted by another session?
- How does system handle malformed natural language that doesn't map to any intent?
- What happens when conversation history exceeds context window limits?
- How does system handle concurrent updates to the same task from chat and web UI?
- What happens when MCP server is unreachable or down?
- How does system handle messages containing PII or sensitive data?

## Requirements *(mandatory)*

### Functional Requirements

**MCP Server Requirements**:

- **FR-001**: System MUST implement a standalone MCP server at `backend/mcp_server/` that registers 5 task management tools
- **FR-002**: System MUST expose `add_task` tool accepting user_id, title, description, priority, due_date, tags as parameters
- **FR-003**: System MUST expose `list_tasks` tool accepting user_id and optional filters (status, priority, tag)
- **FR-004**: System MUST expose `update_task` tool accepting user_id, task_id, and optional updates to title, description, priority, due_date, tags
- **FR-005**: System MUST expose `complete_task` tool accepting user_id and task_id
- **FR-006**: System MUST expose `delete_task` tool accepting user_id and task_id
- **FR-007**: All MCP tools MUST be stateless and read current state from Neon PostgreSQL database
- **FR-008**: All MCP tools MUST filter data by user_id to enforce user data isolation
- **FR-009**: MCP server MUST start independently without Phase II backend running
- **FR-010**: MCP server MUST use Official MCP SDK for tool registration and protocol handling

**Chat API Requirements**:

- **FR-011**: System MUST implement POST `/api/{user_id}/chat` endpoint in `backend/phase3/`
- **FR-012**: Chat endpoint MUST accept message text and optional conversation_id
- **FR-013**: Chat endpoint MUST create new conversation if conversation_id not provided
- **FR-014**: Chat endpoint MUST load existing conversation history when conversation_id provided
- **FR-015**: Chat endpoint MUST persist user message to database before AI processing
- **FR-016**: Chat endpoint MUST invoke OpenAI Agents SDK with conversation history and available MCP tools
- **FR-017**: Chat endpoint MUST execute selected MCP tools via MCP client
- **FR-018**: Chat endpoint MUST persist assistant response to database after AI processing
- **FR-019**: Chat endpoint MUST return conversation_id, message_id, assistant response, and tool calls executed
- **FR-020**: Chat endpoint MUST enforce JWT authentication and verify user_id matches token

**AI Agent Behavior Requirements**:

- **FR-021**: Agent MUST parse natural language to identify user intent (create, read, update, delete, list)
- **FR-022**: Agent MUST select appropriate MCP tool(s) based on identified intent
- **FR-023**: Agent MUST extract entities from natural language (task title, priority, dates, tags)
- **FR-024**: Agent MUST handle ambiguous requests by asking clarifying questions
- **FR-025**: Agent MUST use conversation history to resolve pronouns and references
- **FR-026**: Agent MUST chain multiple MCP tool calls when required (e.g., list then update)
- **FR-027**: Agent MUST provide natural language confirmation after successful operations
- **FR-028**: Agent MUST explain errors in user-friendly language without exposing system details
- **FR-029**: Agent MUST NEVER access database directly, only through MCP tools
- **FR-030**: Agent MUST handle partial matches by presenting options to user

**Database Requirements**:

- **FR-031**: System MUST create Conversation model with id, user_id, title, created_at, updated_at
- **FR-032**: System MUST create Message model with id, conversation_id, role (user/assistant), content, tool_calls, created_at
- **FR-033**: System MUST maintain foreign key relationship between Message.conversation_id and Conversation.id
- **FR-034**: System MUST maintain foreign key relationship between Conversation.user_id and User.id
- **FR-035**: System MUST use existing Task model from Phase II without modification
- **FR-036**: All database queries MUST filter by user_id for data isolation
- **FR-037**: System MUST use database transactions for multi-step operations (persist user message + invoke agent + persist assistant message)

**Frontend Requirements**:

- **FR-038**: System MUST implement protected `/chat` route accessible only to authenticated users
- **FR-039**: System MUST implement MessageList component displaying conversation history
- **FR-040**: System MUST implement MessageInput component for user message entry
- **FR-041**: System MUST implement LoadingIndicator shown during AI processing
- **FR-042**: System MUST implement ErrorDisplay for API and network errors
- **FR-043**: System MUST implement EmptyState for new conversations
- **FR-044**: System MUST use OpenAI ChatKit framework for chat UI components
- **FR-045**: System MUST configure domain allowlist via NEXT_PUBLIC_OPENAI_DOMAIN_KEY
- **FR-046**: Frontend MUST display tool calls executed by the agent (transparent AI actions)
- **FR-047**: Frontend MUST handle streaming responses if OpenAI Agents SDK supports it
- **FR-048**: Frontend MUST preserve scroll position when new messages arrive

**Error Handling Requirements**:

- **FR-049**: System MUST implement three-tier error handling (validation 400, business logic 404/403, system 500)
- **FR-050**: System MUST return user-friendly error messages without exposing stack traces or database details

### Key Entities

- **Conversation**: Represents a multi-turn chat session between user and AI agent. Contains user_id (owner), title (optional), timestamps. One-to-many relationship with Messages.
- **Message**: Individual message within a Conversation. Contains role (user or assistant), content (message text), tool_calls (JSON array of MCP tools executed), conversation_id (foreign key), timestamp.
- **Task**: Existing entity from Phase II. Represents a user's todo item with title, description, completed status, priority, due_date, tags, user_id, timestamps. Used by MCP tools.
- **User**: Existing entity from Phase II. Represents authenticated user. Referenced by Conversation.user_id and Task.user_id.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create tasks via chat with 100% accuracy for simple commands (e.g., "Add task to buy milk")
- **SC-002**: Users can list, update, complete, and delete tasks via natural language with >90% intent recognition accuracy
- **SC-003**: System handles 50 concurrent chat requests without response time exceeding 3 seconds (95th percentile)
- **SC-004**: MCP server starts independently and registers all 5 tools within 5 seconds
- **SC-005**: Chat endpoint returns response within 2 seconds for 90% of requests (excluding OpenAI API latency)
- **SC-006**: All MCP tool calls enforce user data isolation with 100% accuracy (zero cross-user data leaks)
- **SC-007**: Conversation history persists correctly for 100% of messages (zero data loss)
- **SC-008**: Frontend chat interface renders correctly on desktop (Chrome, Firefox, Safari) and mobile (iOS Safari, Chrome Android)
- **SC-009**: Agent asks clarifying questions when confidence < 70% instead of guessing or failing
- **SC-010**: System handles OpenAI API errors gracefully with user-friendly fallback messages (no crashes)
- **SC-011**: All error messages are user-friendly and actionable (no stack traces or technical jargon exposed)
- **SC-012**: Phase II functionality remains 100% intact (zero regression) - all existing tests pass

---

## MCP Tools Specification

### Tool 1: add_task

**Description**: Creates a new task for the authenticated user.

**Parameters**:
```python
{
  "user_id": str,           # Required: Owner of the task
  "title": str,             # Required: Task title (1-200 chars)
  "description": str | None, # Optional: Detailed description
  "priority": str | None,    # Optional: "low" | "medium" | "high"
  "due_date": str | None,    # Optional: ISO 8601 datetime
  "tags": list[str] | None   # Optional: Array of tag strings
}
```

**Returns** (Success):
```python
{
  "id": int,
  "title": str,
  "description": str | None,
  "completed": bool,
  "priority": str | None,
  "due_date": str | None,
  "tags": list[str],
  "user_id": str,
  "created_at": str,
  "updated_at": str
}
```

**Returns** (Error):
```python
{
  "error": str,
  "code": "INVALID_INPUT" | "INTERNAL_ERROR",
  "details": str
}
```

**Example**:
```python
# Input
{
  "user_id": "user_123",
  "title": "Buy groceries",
  "priority": "high",
  "due_date": "2026-01-25T17:00:00Z",
  "tags": ["shopping", "urgent"]
}

# Output
{
  "id": 42,
  "title": "Buy groceries",
  "description": None,
  "completed": False,
  "priority": "high",
  "due_date": "2026-01-25T17:00:00Z",
  "tags": ["shopping", "urgent"],
  "user_id": "user_123",
  "created_at": "2026-01-23T10:30:00Z",
  "updated_at": "2026-01-23T10:30:00Z"
}
```

---

### Tool 2: list_tasks

**Description**: Retrieves tasks for the authenticated user with optional filtering.

**Parameters**:
```python
{
  "user_id": str,         # Required: Owner of tasks
  "status": str | None,   # Optional: "complete" | "incomplete"
  "priority": str | None, # Optional: "low" | "medium" | "high"
  "tag": str | None       # Optional: Filter by single tag
}
```

**Returns** (Success):
```python
[
  {
    "id": int,
    "title": str,
    "description": str | None,
    "completed": bool,
    "priority": str | None,
    "due_date": str | None,
    "tags": list[str],
    "user_id": str,
    "created_at": str,
    "updated_at": str
  },
  ...
]
```

**Returns** (Error):
```python
{
  "error": str,
  "code": "INVALID_INPUT" | "INTERNAL_ERROR",
  "details": str
}
```

**Example**:
```python
# Input
{
  "user_id": "user_123",
  "status": "incomplete",
  "priority": "high"
}

# Output
[
  {
    "id": 42,
    "title": "Buy groceries",
    "description": None,
    "completed": False,
    "priority": "high",
    "due_date": "2026-01-25T17:00:00Z",
    "tags": ["shopping", "urgent"],
    "user_id": "user_123",
    "created_at": "2026-01-23T10:30:00Z",
    "updated_at": "2026-01-23T10:30:00Z"
  }
]
```

---

### Tool 3: update_task

**Description**: Updates an existing task's attributes.

**Parameters**:
```python
{
  "user_id": str,           # Required: Owner of the task
  "task_id": int,           # Required: Task to update
  "title": str | None,      # Optional: New title
  "description": str | None, # Optional: New description
  "priority": str | None,    # Optional: New priority
  "due_date": str | None,    # Optional: New due date
  "tags": list[str] | None   # Optional: New tags (replaces existing)
}
```

**Returns** (Success):
```python
{
  "id": int,
  "title": str,
  "description": str | None,
  "completed": bool,
  "priority": str | None,
  "due_date": str | None,
  "tags": list[str],
  "user_id": str,
  "created_at": str,
  "updated_at": str
}
```

**Returns** (Error):
```python
{
  "error": str,
  "code": "TASK_NOT_FOUND" | "UNAUTHORIZED" | "INVALID_INPUT" | "INTERNAL_ERROR",
  "details": str,
  "task_id": int,
  "user_id": str
}
```

**Example**:
```python
# Input
{
  "user_id": "user_123",
  "task_id": 42,
  "priority": "low",
  "tags": ["shopping"]
}

# Output
{
  "id": 42,
  "title": "Buy groceries",
  "description": None,
  "completed": False,
  "priority": "low",  # Updated
  "due_date": "2026-01-25T17:00:00Z",
  "tags": ["shopping"],  # Updated
  "user_id": "user_123",
  "created_at": "2026-01-23T10:30:00Z",
  "updated_at": "2026-01-23T11:00:00Z"  # Updated
}
```

---

### Tool 4: complete_task

**Description**: Marks a task as completed (idempotent operation).

**Parameters**:
```python
{
  "user_id": str,  # Required: Owner of the task
  "task_id": int   # Required: Task to complete
}
```

**Returns** (Success):
```python
{
  "id": int,
  "title": str,
  "description": str | None,
  "completed": bool,  # True
  "priority": str | None,
  "due_date": str | None,
  "tags": list[str],
  "user_id": str,
  "created_at": str,
  "updated_at": str
}
```

**Returns** (Error):
```python
{
  "error": str,
  "code": "TASK_NOT_FOUND" | "UNAUTHORIZED" | "INTERNAL_ERROR",
  "details": str,
  "task_id": int,
  "user_id": str
}
```

**Example**:
```python
# Input
{
  "user_id": "user_123",
  "task_id": 42
}

# Output
{
  "id": 42,
  "title": "Buy groceries",
  "description": None,
  "completed": True,  # Marked complete
  "priority": "low",
  "due_date": "2026-01-25T17:00:00Z",
  "tags": ["shopping"],
  "user_id": "user_123",
  "created_at": "2026-01-23T10:30:00Z",
  "updated_at": "2026-01-23T12:00:00Z"  # Updated
}
```

---

### Tool 5: delete_task

**Description**: Permanently deletes a task.

**Parameters**:
```python
{
  "user_id": str,  # Required: Owner of the task
  "task_id": int   # Required: Task to delete
}
```

**Returns** (Success):
```python
{
  "message": str,  # "Task deleted successfully"
  "task_id": int
}
```

**Returns** (Error):
```python
{
  "error": str,
  "code": "TASK_NOT_FOUND" | "UNAUTHORIZED" | "INTERNAL_ERROR",
  "details": str,
  "task_id": int,
  "user_id": str
}
```

**Example**:
```python
# Input
{
  "user_id": "user_123",
  "task_id": 42
}

# Output
{
  "message": "Task deleted successfully",
  "task_id": 42
}
```

---

## AI Agent Behavior Specification

### Natural Language Intent Mapping

| User Input Example | Identified Intent | Selected MCP Tool(s) | Entity Extraction |
|--------------------|-------------------|----------------------|-------------------|
| "Add a task to buy milk" | CREATE_TASK | add_task | title: "Buy milk" |
| "Create high priority task to call John tomorrow" | CREATE_TASK | add_task | title: "Call John", priority: "high", due_date: tomorrow |
| "Show me all my tasks" | LIST_TASKS | list_tasks | filters: none |
| "What are my high priority tasks?" | LIST_TASKS | list_tasks | filters: priority="high" |
| "Mark task 5 as done" | COMPLETE_TASK | complete_task | task_id: 5 |
| "Complete the grocery task" | COMPLETE_TASK | list_tasks → complete_task | search: "grocery" (chained) |
| "Delete task 10" | DELETE_TASK | delete_task | task_id: 10 |
| "Remove the meeting task" | DELETE_TASK | list_tasks → delete_task | search: "meeting" (chained) |
| "Update task 3 to medium priority" | UPDATE_TASK | update_task | task_id: 3, priority: "medium" |
| "Change the due date to Friday" | UPDATE_TASK | update_task (context-dependent) | due_date: next Friday (needs context) |
| "Add urgent tag to that task" | UPDATE_TASK | update_task (context-dependent) | tags: ["urgent"] (needs context from history) |

### Tool Chaining Examples

**Scenario 1: Ambiguous Task Reference**
```
User: "Complete the project task"
Agent: [Calls list_tasks with search filter "project"]
        [Finds 3 matching tasks]
        "I found 3 tasks related to 'project':
         1. Project planning (ID: 5)
         2. Project review (ID: 12)
         3. Project submission (ID: 18)
         Which one would you like to complete?"
User: "The first one"
Agent: [Calls complete_task with task_id=5]
        "I've marked 'Project planning' as complete."
```

**Scenario 2: Context-Dependent Update**
```
User: "Show my tasks"
Agent: [Calls list_tasks]
        "You have 5 tasks:
         1. Buy groceries (ID: 42)
         2. Call dentist (ID: 43)
         ..."
User: "Set the first one to high priority"
Agent: [Uses conversation history to resolve "first one" = task ID 42]
        [Calls update_task with task_id=42, priority="high"]
        "I've updated 'Buy groceries' to high priority."
```

**Scenario 3: Multi-Step Operation**
```
User: "Create a task to finish report by Friday, then show me all my tasks for this week"
Agent: [Calls add_task with title="Finish report", due_date=next Friday]
        [Calls list_tasks with filter due_date range this week]
        "I've created the task 'Finish report' due Friday. Here are all your tasks for this week:
         1. Finish report (ID: 50, due Friday)
         2. Team meeting (ID: 48, due Wednesday)
         ..."
```

### Ambiguity Handling

**Strategy**: When confidence in intent or entity extraction is < 70%, agent MUST ask clarifying questions instead of guessing.

**Examples**:
- Ambiguous reference: "Delete the task" → "Which task would you like to delete? Please provide the task ID or title."
- Missing required entity: "Create a task" → "What should the task be titled?"
- Multiple matches: "Complete the meeting task" (when 3 tasks contain "meeting") → Present all matches with IDs and ask user to specify
- Unclear intent: "What about Friday?" → "I'm not sure what you'd like to do. Are you trying to create a task, update a due date, or list tasks for Friday?"

### Context Resolution

Agent uses conversation history to resolve:
- **Pronouns**: "Update that task" (references task from previous message)
- **Relative references**: "The first one", "The last task I created"
- **Implicit entities**: "Change it to high priority" (uses last mentioned task)
- **Time references**: "Tomorrow", "next week", "Friday" (converts to absolute dates)

**History Window**: Agent receives last 10 messages (5 user + 5 assistant) as context for each new message.

---

## Chat API Specification

### Endpoint: POST `/api/{user_id}/chat`

**Route**: `backend/phase3/routers/chat.py`

**Authentication**: JWT Bearer token required. `user_id` in path must match user_id in JWT payload.

**Request Body**:
```json
{
  "message": "string (required, 1-2000 chars)",
  "conversation_id": "string (optional, UUID format)"
}
```

**Response** (Success - 200):
```json
{
  "conversation_id": "string (UUID)",
  "message_id": "string (UUID)",
  "response": "string (assistant message content)",
  "tool_calls": [
    {
      "tool_name": "string",
      "parameters": {},
      "result": {}
    }
  ],
  "created_at": "string (ISO 8601)"
}
```

**Response** (Error - 400):
```json
{
  "error": "Validation failed",
  "code": "INVALID_INPUT",
  "details": "Message text is required"
}
```

**Response** (Error - 401):
```json
{
  "error": "Unauthorized",
  "code": "UNAUTHORIZED",
  "details": "Invalid or missing authentication token"
}
```

**Response** (Error - 403):
```json
{
  "error": "Forbidden",
  "code": "FORBIDDEN",
  "details": "User ID in path does not match authenticated user"
}
```

**Response** (Error - 404):
```json
{
  "error": "Conversation not found",
  "code": "CONVERSATION_NOT_FOUND",
  "details": "Conversation ID abc-123 does not exist or does not belong to user"
}
```

**Response** (Error - 500):
```json
{
  "error": "An internal error occurred",
  "code": "INTERNAL_ERROR",
  "message": "Please try again or contact support"
}
```

### 7-Step Processing Pipeline

**Step 1: Receive & Validate**
- Extract user_id from path and JWT token
- Validate user_id match between path and JWT
- Validate message text (required, 1-2000 chars)
- Validate conversation_id format if provided (UUID)

**Step 2: Load Conversation History**
- If conversation_id provided: Load existing conversation and verify ownership (conversation.user_id == user_id)
- If conversation_id not provided: Create new Conversation record with user_id
- Load last 10 messages from conversation for context

**Step 3: Persist User Message**
- Create Message record with role="user", content=message_text, conversation_id
- Commit to database before AI processing (ensures no data loss on failure)

**Step 4: Invoke OpenAI Agent**
- Initialize OpenAI Agents SDK client
- Provide agent with:
  - Conversation history (last 10 messages)
  - User's new message
  - Available MCP tools (5 task management tools)
  - System instructions (defined in `backend/phase3/agent/prompts.py`)
- Agent performs intent recognition, entity extraction, tool selection

**Step 5: Execute MCP Tools**
- For each tool call selected by agent:
  - Invoke MCP client to call tool on MCP server
  - Pass user_id and extracted parameters
  - Capture tool result (success or error)
  - Aggregate all tool results

**Step 6: Persist Assistant Response**
- Create Message record with:
  - role="assistant"
  - content=agent's natural language response
  - tool_calls=JSON array of tools executed and results
  - conversation_id
- Commit to database

**Step 7: Return Response**
- Return conversation_id, message_id, response text, tool_calls to frontend
- Include HTTP 200 status for success
- Frontend displays assistant message and tool calls

### Error Handling Within Pipeline

- **Step 1 failure**: Return 400/401/403 immediately (validation/auth errors)
- **Step 2 failure**: Return 404 if conversation not found, 500 for database errors
- **Step 3 failure**: Return 500 (critical - user message must be persisted)
- **Step 4 failure**: Catch OpenAI API errors, return 500 with user-friendly message, persist error state
- **Step 5 failure**: If MCP tool fails, agent includes error in response ("I couldn't complete that task because..."), persist assistant message with error
- **Step 6 failure**: Return 500 (critical - response must be persisted)
- **Step 7 failure**: Return 500 (unlikely - JSON serialization)

**Rollback Strategy**: If Steps 4-7 fail after Step 3 (user message persisted), the user message remains in database but no assistant response is saved. User can retry and conversation history will include their original message.

---

## Database Models

### Model 1: Conversation

**Location**: `backend/phase3/models/conversation.py`

**Schema**:
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str | None = Field(default=None, max_length=200)  # Optional: derived from first message
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(back_populates="conversation", cascade_delete=True)
```

**Indexes**:
- Primary key: `id`
- Foreign key index: `user_id`
- Composite index: `(user_id, created_at)` for listing conversations by user

**Constraints**:
- `user_id` must reference existing User
- Cascade delete: When Conversation deleted, all associated Messages deleted

---

### Model 2: Message

**Location**: `backend/phase3/models/message.py`

**Schema**:
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: str = Field(...)  # "user" | "assistant"
    content: str = Field(..., max_length=10000)  # Message text
    tool_calls: str | None = Field(default=None)  # JSON string of tool calls executed
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
```

**Indexes**:
- Primary key: `id`
- Foreign key index: `conversation_id`
- Composite index: `(conversation_id, created_at)` for loading conversation history in order

**Constraints**:
- `conversation_id` must reference existing Conversation
- `role` must be one of: "user", "assistant"
- `content` cannot be null or empty

**tool_calls JSON Structure** (when role="assistant"):
```json
[
  {
    "tool_name": "add_task",
    "parameters": {
      "user_id": "user_123",
      "title": "Buy groceries",
      "priority": "high"
    },
    "result": {
      "id": 42,
      "title": "Buy groceries",
      "completed": false,
      ...
    }
  }
]
```

---

### Model 3: Task (Existing - No Modification)

**Location**: `backend/src/models/task.py` (Phase II - READ ONLY)

**Schema** (Reference Only):
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(primary_key=True)
    title: str = Field(..., max_length=200)
    description: str | None = Field(default=None)
    completed: bool = Field(default=False)
    priority: str | None = Field(default=None)  # "low" | "medium" | "high"
    due_date: datetime | None = Field(default=None)
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Usage in Phase III**: MCP tools read/write to this table. NO schema changes allowed.

---

## Conversation Flow Examples

### Example 1: Simple Task Creation

```
User: "Add a task to buy groceries tomorrow"

[Backend Processing]
1. Receive message, create/load conversation
2. Persist user message to database
3. Invoke OpenAI Agent with conversation history + message
4. Agent identifies intent: CREATE_TASK
5. Agent extracts entities: title="Buy groceries", due_date=tomorrow
6. Agent selects MCP tool: add_task
7. Execute MCP tool via MCP client:
   add_task(user_id="user_123", title="Buy groceries", due_date="2026-01-24T23:59:59Z")
8. MCP tool returns: {"id": 42, "title": "Buy groceries", ...}
9. Agent generates response: "I've added the task 'Buy groceries' for tomorrow."
10. Persist assistant message with tool_calls to database
11. Return response to frontend

[Frontend Display]
Assistant: "I've added the task 'Buy groceries' for tomorrow."
Tool calls: [add_task(title="Buy groceries", due_date="2026-01-24")]
```

---

### Example 2: Context-Dependent Multi-Turn Conversation

```
User (Message 1): "Show me my tasks"

[Processing]
1-2. Create conversation, persist user message
3-6. Agent identifies LIST_TASKS intent, calls list_tasks(user_id="user_123")
7. MCP returns: [{"id": 42, "title": "Buy groceries"}, {"id": 43, "title": "Call dentist"}]
8. Agent response: "You have 2 tasks: 1. Buy groceries (ID: 42), 2. Call dentist (ID: 43)"
9-11. Persist and return

[Frontend Display]
Assistant: "You have 2 tasks:
  1. Buy groceries (ID: 42)
  2. Call dentist (ID: 43)"

---

User (Message 2): "Mark the first one as done"

[Processing - with conversation history]
1. Load conversation with 2 previous messages (user's "Show me my tasks" + assistant's response)
2. Persist new user message
3-5. Agent uses conversation history to resolve "the first one" = task ID 42
6. Agent selects MCP tool: complete_task
7. Execute: complete_task(user_id="user_123", task_id=42)
8. MCP returns: {"id": 42, "title": "Buy groceries", "completed": True}
9. Agent response: "I've marked 'Buy groceries' as complete."
10-11. Persist and return

[Frontend Display]
Assistant: "I've marked 'Buy groceries' as complete."
Tool calls: [complete_task(task_id=42)]
```

---

### Example 3: Ambiguity Handling with Clarification

```
User: "Delete the meeting task"

[Processing]
1-2. Create/load conversation, persist user message
3-5. Agent extracts intent: DELETE_TASK, entity: "meeting"
6. Agent searches for tasks matching "meeting" via list_tasks
7. MCP returns 3 tasks:
   - {"id": 10, "title": "Team meeting"}
   - {"id": 15, "title": "Client meeting prep"}
   - {"id": 20, "title": "Meeting notes review"}
8. Agent detects ambiguity (multiple matches), generates clarification request
9-11. Persist and return

[Frontend Display]
Assistant: "I found 3 tasks related to 'meeting':
  1. Team meeting (ID: 10)
  2. Client meeting prep (ID: 15)
  3. Meeting notes review (ID: 20)
Which one would you like to delete?"

---

User: "The second one"

[Processing - with history]
1-2. Load conversation history, persist user message
3-5. Agent uses context to resolve "second one" = task ID 15
6. Agent selects delete_task
7. Execute: delete_task(user_id="user_123", task_id=15)
8. MCP returns: {"message": "Task deleted successfully", "task_id": 15}
9. Agent response: "I've deleted 'Client meeting prep'."
10-11. Persist and return

[Frontend Display]
Assistant: "I've deleted 'Client meeting prep'."
Tool calls: [delete_task(task_id=15)]
```

---

### Example 4: Error Handling - Task Not Found

```
User: "Complete task 999"

[Processing]
1-2. Create/load conversation, persist user message
3-6. Agent identifies COMPLETE_TASK intent, extracts task_id=999, selects complete_task
7. Execute: complete_task(user_id="user_123", task_id=999)
8. MCP returns error: {"error": "Task not found", "code": "TASK_NOT_FOUND", "task_id": 999}
9. Agent translates error to user-friendly message: "I couldn't find task #999. Would you like to see your current tasks?"
10-11. Persist assistant message with error, return

[Frontend Display]
Assistant: "I couldn't find task #999. Would you like to see your current tasks?"
Tool calls: [complete_task(task_id=999) - FAILED]
Error: TASK_NOT_FOUND
```

---

## Frontend ChatKit Specification

### Protected Route: `/chat`

**Location**: `frontend/src/app/chat/page.tsx`

**Authentication**: Requires authenticated user session via Better Auth. Redirects to `/login` if not authenticated.

**Route Structure**:
```typescript
// frontend/src/app/chat/page.tsx
export default function ChatPage() {
  const { user, isLoading } = useAuth();

  if (isLoading) return <LoadingSpinner />;
  if (!user) redirect('/login');

  return (
    <div className="h-screen flex flex-col">
      <ChatHeader user={user} />
      <ChatInterface user={user} />
    </div>
  );
}
```

---

### Components Specification

#### Component 1: MessageList

**Purpose**: Display conversation history with user and assistant messages.

**Location**: `frontend/src/components/chat/MessageList.tsx`

**Props**:
```typescript
interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  tool_calls?: ToolCall[];
  created_at: string;
}

interface ToolCall {
  tool_name: string;
  parameters: Record<string, any>;
  result: Record<string, any> | null;
}
```

**Rendering Rules**:
- User messages: Right-aligned, blue background
- Assistant messages: Left-aligned, gray background
- Tool calls: Display below assistant message in collapsed accordion (expandable)
- Timestamps: Show relative time (e.g., "2 minutes ago")
- Auto-scroll to bottom when new message arrives
- Preserve scroll position when user is scrolled up viewing history

**Example**:
```tsx
<MessageList messages={conversationMessages} isLoading={isSending} />
```

---

#### Component 2: MessageInput

**Purpose**: Input field for user to type and send messages.

**Location**: `frontend/src/components/chat/MessageInput.tsx`

**Props**:
```typescript
interface MessageInputProps {
  onSend: (message: string) => Promise<void>;
  disabled: boolean;
}
```

**Behavior**:
- Multiline textarea (auto-expands up to 5 lines)
- Send on Enter (Shift+Enter for newline)
- Disable input while message is being processed
- Clear input after successful send
- Show character count (max 2000 chars)
- Prevent empty message submission

**Example**:
```tsx
<MessageInput onSend={handleSendMessage} disabled={isSending} />
```

---

#### Component 3: LoadingIndicator

**Purpose**: Show visual feedback while AI is processing request.

**Location**: `frontend/src/components/chat/LoadingIndicator.tsx`

**Props**:
```typescript
interface LoadingIndicatorProps {
  message?: string;
}
```

**Display**:
- Animated typing indicator (three bouncing dots)
- Optional message: "AI is thinking..." or "Processing your request..."
- Shown at bottom of message list while waiting for response

**Example**:
```tsx
{isSending && <LoadingIndicator message="AI is thinking..." />}
```

---

#### Component 4: ErrorDisplay

**Purpose**: Display user-friendly error messages for API and network failures.

**Location**: `frontend/src/components/chat/ErrorDisplay.tsx`

**Props**:
```typescript
interface ErrorDisplayProps {
  error: string | null;
  onDismiss: () => void;
}
```

**Error Types**:
- Network errors: "Unable to connect. Please check your internet connection."
- API errors: Display error message from backend response
- Timeout errors: "Request timed out. Please try again."
- Generic fallback: "Something went wrong. Please try again."

**Behavior**:
- Display as dismissible toast notification at top of chat
- Auto-dismiss after 5 seconds
- User can manually dismiss by clicking close button

**Example**:
```tsx
<ErrorDisplay error={errorMessage} onDismiss={() => setErrorMessage(null)} />
```

---

#### Component 5: EmptyState

**Purpose**: Display helpful message when conversation is empty (no messages yet).

**Location**: `frontend/src/components/chat/EmptyState.tsx`

**Content**:
- Welcome message: "Hi! I'm your AI task assistant."
- Example prompts:
  - "Add a task to buy groceries tomorrow"
  - "Show me all my high priority tasks"
  - "Mark task #5 as complete"
- Instructions: "Type a message below to get started"

**Example**:
```tsx
{messages.length === 0 && <EmptyState />}
```

---

### OpenAI ChatKit Integration

**Installation**:
```bash
npm install @openai/chatkit
```

**Configuration** (`frontend/src/lib/chatkit-config.ts`):
```typescript
import { ChatKitConfig } from '@openai/chatkit';

export const chatKitConfig: ChatKitConfig = {
  domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY!,
  apiEndpoint: `/api/${userId}/chat`,
  theme: {
    primaryColor: '#3b82f6',
    backgroundColor: '#ffffff',
    messageBackgroundColor: '#f3f4f6'
  }
};
```

**Environment Variables**:
```env
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_domain_key_here
```

**Domain Allowlist Setup**:
1. Register domain at OpenAI ChatKit dashboard
2. Obtain domain key
3. Add to `.env.local` as `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`
4. Configure in ChatKit client

---

### API Integration

**API Client** (`frontend/src/lib/api/chat.ts`):
```typescript
export async function sendChatMessage(
  userId: string,
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  const response = await fetch(`/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getAuthToken()}`
    },
    body: JSON.stringify({ message, conversation_id: conversationId })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.details || 'Failed to send message');
  }

  return response.json();
}
```

**State Management** (React hooks):
```typescript
const [messages, setMessages] = useState<Message[]>([]);
const [isSending, setIsSending] = useState(false);
const [error, setError] = useState<string | null>(null);

const handleSendMessage = async (text: string) => {
  setIsSending(true);
  setError(null);

  try {
    const response = await sendChatMessage(user.id, text, conversationId);
    setMessages(prev => [
      ...prev,
      { role: 'user', content: text, created_at: new Date().toISOString() },
      {
        role: 'assistant',
        content: response.response,
        tool_calls: response.tool_calls,
        created_at: response.created_at
      }
    ]);
  } catch (err) {
    setError(err.message);
  } finally {
    setIsSending(false);
  }
};
```

---

## Agent Skills Reference

All Phase III agents are defined as Claude Skills in `.claude/skills/`:

1. **MCP Server Builder Skill**: `.claude/skills/mcp-server-builder-skill.md`
   - Responsible for implementing the standalone MCP server
   - Defines MCP tool signatures and implementations
   - Enforces stateless architecture and user data isolation

2. **Chat + MCP Bridge Skill**: `.claude/skills/chat-mcp-bridge-skill.md`
   - Responsible for implementing the POST `/api/{user_id}/chat` endpoint
   - Defines 7-step processing pipeline
   - Manages conversation persistence and MCP tool orchestration

3. **AI Agent Logic Skill (MCP Orchestrator)**: `.claude/skills/phase3-mcp-orchestrator-skill.md`
   - Responsible for intent recognition and tool selection
   - Defines natural language mapping and ambiguity handling
   - Enforces "MCP tools only" constraint (no direct database access)

4. **ChatKit Frontend Builder Skill**: `.claude/skills/chatkit-frontend-builder-skill.md`
   - Responsible for implementing chat UI components
   - Defines ChatKit integration and domain allowlist configuration
   - Enforces authentication and protected route requirements

**Usage**: Reference these skills when implementing each agent's responsibilities. Each skill includes detailed examples, success criteria, and constraints.

---

## Rules & Restrictions

### Phase II Protection (CRITICAL)

**MUST NOT Modify**:
- ANY file in `backend/src/api/`
- ANY file in `backend/src/services/`
- ANY file in `backend/src/schemas/`
- ANY file in `backend/src/models/` (read-only imports allowed)
- ANY file in `frontend/src/app/` except `/chat`
- ANY file in `frontend/src/components/` except `/chat`
- ANY existing database migrations
- ANY existing tests for Phase II functionality

**MUST Verify**: Before merging Phase III to main:
- All Phase II tests pass without modification
- Phase II frontend pages (/, /dashboard, /login, /register) work unchanged
- Phase II API endpoints function identically
- No Phase II dependencies were altered

**Enforcement**: Use `git diff` to verify zero changes to Phase II code paths.

---

### Stateless Architecture Requirements

**MCP Server**:
- ZERO in-memory state (no global variables, no caches, no session storage)
- ALL state persisted in Neon PostgreSQL database
- MCP server MUST be horizontally scalable (multiple instances can run concurrently)
- Each tool call reads current state from database before processing

**Chat API**:
- NO session state on backend
- Authentication state from JWT only (stateless auth)
- Conversation history loaded from database per request
- Each request is independent and self-contained

---

### Security Requirements

**Authentication**:
- ALL Phase III endpoints require JWT Bearer token
- User ID in URL path MUST match user ID in JWT payload
- Tokens validated on every request (no caching)

**Authorization**:
- ALL database queries MUST filter by user_id
- Users can ONLY access their own conversations, messages, and tasks
- Cross-user data access MUST return 403 Forbidden

**Data Validation**:
- Input validation on all parameters (type, length, format)
- SQL injection prevention via ORM (SQLModel)
- XSS prevention via proper output encoding
- No sensitive data in error messages or logs visible to users

**Secrets Management**:
- NO hardcoded API keys or database URLs
- ALL secrets in environment variables (.env file)
- .env MUST be in .gitignore
- Production secrets managed via deployment platform (e.g., Vercel, Render)

---

### Error Handling Standards

**Three-Tier Strategy**:

1. **Validation Errors (400-level)**:
   - Trigger: Invalid user input
   - Response: Specific error message with field name
   - Example: `{"error": "Validation failed", "code": "INVALID_INPUT", "details": "Field 'title' is required"}`

2. **Business Logic Errors (404, 403)**:
   - Trigger: Resource not found, unauthorized access
   - Response: Clear error message without exposing internal details
   - Example: `{"error": "Task not found", "code": "TASK_NOT_FOUND", "task_id": 42}`

3. **System Errors (500)**:
   - Trigger: Database failures, API errors, unexpected exceptions
   - Response: Generic user-facing message
   - Example: `{"error": "An internal error occurred", "code": "INTERNAL_ERROR"}`
   - Internal: Log full error with stack trace for debugging

**Logging**:
- Log ALL errors with full context (user_id, request_id, stack trace)
- Use structured logging (JSON format preferred)
- Include correlation IDs for tracing requests across services

---

## Testing & Validation

### Unit Tests Required

**Backend (pytest)**:
- MCP tool unit tests (test each tool independently with mocked database)
- Chat API endpoint tests (test 7-step pipeline with mocked dependencies)
- Agent logic tests (test intent recognition with sample inputs)
- Database model tests (test CRUD operations and relationships)

**Frontend (Jest + React Testing Library)**:
- Component tests for MessageList, MessageInput, LoadingIndicator, ErrorDisplay, EmptyState
- API client tests (test fetch calls with mocked responses)
- Authentication flow tests (test redirect logic)

**Test Coverage Target**: >80% for Phase III code

---

### Integration Tests Required

**End-to-End Scenarios**:
1. User sends message → task created → appears in Phase II dashboard
2. User creates task via Phase II dashboard → asks AI about it → AI can see and reference it
3. User has multi-turn conversation → refreshes page → conversation persists
4. User attempts to access another user's conversation → receives 403 error
5. MCP server down → chat returns user-friendly error message

**Tools**: Playwright or Cypress for E2E tests

---

### Manual Testing Checklist

Before marking Phase III complete, manually verify:

- [ ] MCP server starts independently with `python backend/mcp_server/main.py`
- [ ] All 5 MCP tools registered and discoverable
- [ ] Chat page loads for authenticated users
- [ ] Chat page redirects to login for unauthenticated users
- [ ] Simple task creation works: "Add task to buy milk"
- [ ] Task listing works: "Show me all my tasks"
- [ ] Task completion works: "Mark task 5 as done"
- [ ] Task deletion works: "Delete task 10"
- [ ] Task update works: "Update task 3 to high priority"
- [ ] Multi-turn context works: "Show tasks" → "Mark first one done"
- [ ] Ambiguity handling works: "Delete the meeting task" with multiple matches asks for clarification
- [ ] Error handling works: Attempting to complete non-existent task shows friendly error
- [ ] Conversation persists across page refreshes
- [ ] User data isolation: Cannot access other users' conversations
- [ ] Phase II dashboard shows tasks created via chat
- [ ] Phase II task updates reflect in chat when asked
- [ ] Mobile responsiveness: Chat works on phone screen
- [ ] Network error handling: Disconnect internet and verify error message

---

## Deliverables

### Code Deliverables

1. **MCP Server** (`backend/mcp_server/`):
   - `main.py` - MCP server entry point
   - `tools/task_tools.py` - 5 MCP tool implementations
   - `config.py` - Database and environment configuration
   - `requirements.txt` - Python dependencies
   - `README.md` - Startup instructions and tool reference

2. **Chat API** (`backend/phase3/`):
   - `routers/chat.py` - POST `/api/{user_id}/chat` endpoint
   - `services/chat_service.py` - 7-step pipeline logic
   - `models/conversation.py` - Conversation model
   - `models/message.py` - Message model
   - `schemas/chat_schema.py` - Request/response Pydantic schemas
   - `agent/prompts.py` - System instructions for OpenAI agent
   - `agent/orchestrator.py` - Intent recognition and tool selection logic

3. **Frontend Chat UI** (`frontend/src/`):
   - `app/chat/page.tsx` - Protected chat route
   - `components/chat/MessageList.tsx`
   - `components/chat/MessageInput.tsx`
   - `components/chat/LoadingIndicator.tsx`
   - `components/chat/ErrorDisplay.tsx`
   - `components/chat/EmptyState.tsx`
   - `lib/chatkit-config.ts` - OpenAI ChatKit configuration
   - `lib/api/chat.ts` - API client for chat endpoint

4. **Database Migrations**:
   - Migration for `conversations` table
   - Migration for `messages` table

5. **Tests**:
   - `backend/phase3/tests/test_mcp_tools.py`
   - `backend/phase3/tests/test_chat_api.py`
   - `backend/phase3/tests/test_agent_logic.py`
   - `frontend/src/components/chat/__tests__/`
   - E2E test suite

6. **Documentation**:
   - `backend/mcp_server/README.md` - MCP server setup and usage
   - `docs/phase-iii/ARCHITECTURE.md` - System architecture diagram and flow
   - `docs/phase-iii/API_REFERENCE.md` - Chat API documentation
   - `docs/phase-iii/DEPLOYMENT.md` - Deployment instructions
   - Updated root README.md with Phase III overview

---

### Configuration Files

1. **Environment Variables**:
   ```env
   # Backend (.env)
   DATABASE_URL=postgresql://user:pass@host:5432/db
   OPENAI_API_KEY=sk-...
   JWT_SECRET=...

   # Frontend (.env.local)
   NEXT_PUBLIC_OPENAI_DOMAIN_KEY=domain_key_here
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

2. **MCP Server Config**: Domain allowlist, port configuration, logging level

3. **Agent Config**: System prompt, conversation history window size, confidence threshold

---

### Success Validation

Phase III is considered complete when:

1. All functional requirements (FR-001 through FR-050) are implemented and tested
2. All success criteria (SC-001 through SC-012) are met
3. All unit tests pass with >80% coverage
4. All integration tests pass
5. Manual testing checklist 100% complete
6. Phase II functionality verified unchanged (zero regression)
7. Code review completed by at least one other developer
8. Documentation complete and reviewed
9. Deployment guide tested on staging environment
10. Security review completed (authentication, authorization, data isolation)

---

## Final Enforcement Notes

**This specification is the contract for Phase III implementation. Any deviation from these requirements MUST be documented and approved before implementation.**

**Key Invariants**:
- Phase II code remains untouched
- All agents follow their skill definitions exactly
- Stateless architecture is non-negotiable
- User data isolation is security-critical
- Three-tier error handling is mandatory

**Before Starting Implementation**:
1. Read all 4 agent skills in `.claude/skills/`
2. Review Phase III Constitution in `.specify/memory/phase-iii-constitution.md`
3. Set up local MCP server development environment
4. Configure OpenAI API key and ChatKit domain key
5. Verify Phase II is working correctly on main branch

**During Implementation**:
- Follow agent boundaries strictly (no cross-agent code)
- Test each component independently before integration
- Commit frequently with descriptive messages
- Run Phase II tests after every change to verify no regression
- Update documentation as you implement

**Before Merging to Main**:
- Run full test suite (unit + integration + E2E)
- Verify all deliverables are complete
- Validate success criteria are met
- Perform manual testing checklist
- Get code review approval
- Update CHANGELOG with Phase III changes

---

**Specification Version**: 1.0.0
**Last Updated**: 2026-01-23
**Next Phase**: Phase IV (Advanced Features - Not Yet Defined)