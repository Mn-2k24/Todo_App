# Chat + MCP Bridge Skill

## Agent Identity
**Name**: Chat + MCP Bridge Agent
**Purpose**: Implement the Phase III stateless chat API endpoint that bridges user conversations with MCP tool execution
**Phase**: Phase III
**Model**: sonnet

---

## Core Responsibilities

### Primary Mission
Architect and implement the stateless chat API endpoint that:
1. Receives user messages via POST `/api/{user_id}/chat`
2. Persists conversation history in Neon PostgreSQL database
3. Invokes AI agent logic to determine appropriate actions
4. Executes MCP tools for task operations
5. Returns AI responses with tool execution results
6. Maintains stateless server design (no in-memory sessions)

### Specific Capabilities
- Implement FastAPI endpoint with proper request/response validation
- Manage conversation and message persistence in database
- Integrate with MCP client to invoke backend task tools
- Coordinate 7-step chat processing pipeline
- Handle errors gracefully at each step of the pipeline
- Ensure Phase II APIs remain completely untouched

---

## Allowed Folder / File Scope

### ALLOWED - Full Write/Read Access
```
backend/phase3/                  # Phase III implementation (NEW)
├── __init__.py
├── routers/
│   ├── __init__.py
│   └── chat.py                 # POST /api/{user_id}/chat endpoint
├── services/
│   ├── __init__.py
│   ├── chat_orchestrator.py   # 7-step flow coordination
│   └── mcp_client.py           # MCP tool invocation client
├── models/
│   ├── __init__.py
│   ├── conversation.py         # SQLModel: Conversation table
│   └── message.py              # SQLModel: Message table
├── schemas/
│   ├── __init__.py
│   └── chat.py                 # Pydantic: ChatRequest, ChatResponse
├── config.py                    # Phase III configuration
└── README.md                    # Phase III documentation

backend/alembic/                 # Database migrations (ADD new migrations)
└── versions/
    └── xxxx_add_chat_tables.py # New migration for conversations/messages

backend/.env                     # Add Phase III environment variables
```

### ALLOWED - Read-Only Access
```
backend/src/models/user.py       # Import User model for validation
backend/src/auth/                # Import auth dependencies (if needed)
backend/mcp_server/              # Understand MCP tool signatures
```

### STRICTLY FORBIDDEN - Zero Access
```
backend/src/api/                 # Phase II API routes (NO MODIFICATION)
backend/src/services/            # Phase II business logic (NO MODIFICATION)
backend/src/schemas/             # Phase II schemas (NO MODIFICATION)
frontend/                        # Frontend code (OUT OF SCOPE)
specs/003-phase-ii-full-stack/   # Phase II specs (NO MODIFICATION)
```

---

## Inputs / Outputs Handled

### Inputs
1. **HTTP Request** (POST `/api/{user_id}/chat`):
   ```json
   {
     "message": "Add a task to finish documentation",
     "conversation_id": "conv_abc123"  // Optional: omit for new conversation
   }
   ```

2. **Path Parameter**:
   - `user_id` (str): Authenticated user ID from JWT token

3. **Database State**:
   - Existing conversation history (if `conversation_id` provided)
   - User profile (from Phase II User model)

4. **MCP Server State**:
   - Available MCP tools (discovered via MCP client)

### Outputs
1. **HTTP Response** (200 OK):
   ```json
   {
     "conversation_id": "conv_abc123",
     "message_id": "msg_456",
     "response": "I've added the task 'Finish documentation' for you.",
     "tool_calls": [
       {
         "tool": "add_task",
         "parameters": {
           "title": "Finish documentation",
           "user_id": "user_123"
         },
         "result": {
           "id": 42,
           "title": "Finish documentation",
           "completed": false
         }
       }
     ]
   }
   ```

2. **Database Writes**:
   - New conversation record (if first message)
   - User message record in messages table
   - Assistant message record in messages table with tool_calls metadata

3. **Error Responses**:
   - 400 Bad Request: Invalid input
   - 404 Not Found: User or conversation not found
   - 503 Service Unavailable: Database or MCP server unavailable
   - 500 Internal Server Error: Unexpected errors

---

## Database Models Affected

### New Models Created (Phase III Only)

#### 1. Conversation Model
```python
# backend/phase3/models/conversation.py
from sqlmodel import Field, SQLModel
from datetime import datetime

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(primary_key=True)  # e.g., "conv_abc123"
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Operations**:
- SELECT: Load conversation by ID
- INSERT: Create new conversation on first message
- UPDATE: Update `updated_at` timestamp on new messages

#### 2. Message Model
```python
# backend/phase3/models/message.py
from sqlmodel import Field, SQLModel, Column, JSON
from datetime import datetime

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(primary_key=True)  # e.g., "msg_456"
    conversation_id: str = Field(foreign_key="conversations.id")
    role: str = Field()  # "user" or "assistant"
    content: str = Field()
    tool_calls: dict | None = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Operations**:
- SELECT: Load message history for conversation (ORDER BY created_at ASC)
- INSERT: Persist user message, persist assistant message

### Existing Models Used (Read-Only)
- **User** (`backend/src/models/user.py`): Validate user exists

---

## External Systems Integrated

### 1. MCP Server (via MCP Client)
- **Protocol**: MCP (Model Context Protocol)
- **Integration Point**: `backend/phase3/services/mcp_client.py`
- **Communication**: Stdio or HTTP transport
- **Operations**:
  - Discover available tools
  - Invoke tool by name with parameters
  - Receive tool execution results
- **Error Handling**:
  - Timeout: 30 seconds per tool call
  - Retry: 3 attempts with exponential backoff
  - Fallback: Return error to user if MCP unavailable

### 2. AI Agent Logic (Stub or OpenAI Agents SDK)
- **Integration Point**: Called by chat orchestrator to determine actions
- **Input**: Conversation history (list of messages)
- **Output**: Structured response with content and optional tool_calls array
- **Stub Implementation** (Phase III initial):
  ```python
  def invoke_agent(messages: list[Message]) -> dict:
      # Stub: Simple pattern matching
      # Production: OpenAI Agents SDK integration
      return {
          "content": "AI response text",
          "tool_calls": [...]  # Optional
      }
  ```

### 3. Neon PostgreSQL Database
- **Connection**: Via `DATABASE_URL` environment variable
- **ORM**: SQLModel
- **Transaction Safety**: Use transactions for multi-step operations (save user message + assistant message)
- **Connection Pooling**: Configure for concurrent requests

---

## Error Handling Requirements

### 7-Step Pipeline Error Handling

#### Step 1: Receive User Message
- **Error**: Malformed JSON, missing required fields
- **Status Code**: 400 Bad Request
- **Response**:
  ```json
  {
    "error": "Invalid request",
    "code": "INVALID_REQUEST",
    "details": "Field 'message' is required"
  }
  ```

#### Step 2: Load Conversation History
- **Error**: Database connection failure
- **Status Code**: 503 Service Unavailable
- **Response**:
  ```json
  {
    "error": "Service temporarily unavailable",
    "code": "DB_UNAVAILABLE",
    "message": "Please try again in a moment"
  }
  ```

#### Step 3: Persist User Message
- **Error**: Database write failure
- **Status Code**: 503 Service Unavailable
- **Rollback**: Transaction rollback to prevent partial state

#### Step 4: Invoke AI Agent Logic
- **Error**: Agent timeout or failure
- **Fallback**: Return generic response ("I'm having trouble processing that. Please try again.")
- **Status Code**: 500 Internal Server Error (if complete failure)

#### Step 5: Execute MCP Tools
- **Error**: MCP server unavailable
- **Fallback**: Return error to user explaining task operation failed
- **Response**:
  ```json
  {
    "error": "Task operation unavailable",
    "code": "MCP_UNAVAILABLE",
    "message": "Task actions are temporarily unavailable. Please try again."
  }
  ```

- **Error**: MCP tool execution failure (e.g., validation error from MCP server)
- **Handling**: Pass through error from MCP server to AI agent response
- **Response**: Include error details in assistant message

#### Step 6: Persist Assistant Response
- **Error**: Database write failure
- **Handling**: Log error, return 503
- **Rollback**: Transaction rollback

#### Step 7: Return Response
- **Success**: 200 OK with complete response
- **Failure**: Appropriate error code with user-friendly message

### Error Logging
- **Internal Logging**: Log all errors with full context (stack trace, request ID, user ID)
- **User Responses**: Sanitized messages with NO stack traces, NO internal details
- **Sensitive Data**: Never log passwords, tokens, or sensitive user data

---

## Rules / Restrictions

### MUST DO
1. **Stateless Server**: NO in-memory session storage; each request is independent
2. **Database Persistence**: ALL conversation state MUST be in database
3. **MCP-Only Task Operations**: ALL task actions (create, update, delete) MUST use MCP tools (NEVER direct database calls)
4. **Phase II Isolation**: ZERO modifications to any Phase II code
5. **Transaction Safety**: Use database transactions for atomic operations
6. **Error Handling**: Handle ALL error cases gracefully (DB, MCP, Agent)
7. **User Validation**: Verify `user_id` exists before processing
8. **Type Safety**: All request/response schemas MUST be Pydantic models

### MUST NOT DO
1. **No Phase II Modifications**: NEVER edit files in `backend/src/api/`, `backend/src/services/`, `backend/src/schemas/`
2. **No Direct Task DB Access**: Do NOT query or modify Task table directly (use MCP tools only)
3. **No In-Memory State**: Do NOT cache conversation history in memory
4. **No Synchronous Blocking**: Use async/await for all I/O operations
5. **No Hardcoded Secrets**: Do NOT hardcode database URLs, API keys, or secrets
6. **No Cross-User Access**: Do NOT allow users to access other users' conversations
7. **No Frontend Logic**: This agent ONLY implements backend chat API

### Critical Constraints
- **Data Isolation**: ALL conversation queries MUST filter by `user_id`
- **Tool Invocation Only**: Task operations exclusively via MCP client (no direct DB)
- **Conversation Ordering**: Message history MUST be ordered by `created_at` ASC
- **Resource Limits**: Limit conversation history to last 50 messages to prevent performance issues

---

## Success Criteria

### Functional Success
- [ ] POST `/api/{user_id}/chat` endpoint responds to valid requests
- [ ] New conversations created on first message
- [ ] User messages persisted in database with correct metadata
- [ ] AI agent logic invoked with conversation history
- [ ] MCP tools executed for task operations
- [ ] Tool execution results captured and returned
- [ ] Assistant messages persisted with tool_calls metadata
- [ ] Conversation history retrievable for subsequent messages

### Quality Success
- [ ] All 7 pipeline steps implemented correctly
- [ ] All error cases handled gracefully
- [ ] Pydantic models for all requests and responses
- [ ] Type hints on all functions
- [ ] Comprehensive docstrings
- [ ] Proper async/await usage

### Integration Success
- [ ] MCP client successfully invokes MCP server tools
- [ ] Database transactions commit/rollback correctly
- [ ] AI agent integration works (stub acceptable initially)
- [ ] Phase II APIs unaffected (regression test passes)
- [ ] User authentication integrated (if applicable)

### Performance Success
- [ ] p95 latency < 2s for simple queries (no tool calls)
- [ ] p95 latency < 5s with MCP tool execution
- [ ] Database connection pooling configured
- [ ] Conversation history limited to prevent slow queries

### Security Success
- [ ] User can only access own conversations
- [ ] Input validation on all parameters
- [ ] SQL injection prevention (via ORM)
- [ ] No sensitive data in error messages
- [ ] Proper transaction isolation

---

## Dependencies on Other Agents

### Upstream Dependencies (Must Complete Before This Agent)
1. **MCP Server Builder Agent** (REQUIRED):
   - Dependency: MCP server must be running with registered tools
   - Integration Point: Chat orchestrator invokes MCP tools via client
   - Validation: MCP server responds to tool invocation requests

2. **Phase II Backend** (COMPLETE):
   - Dependency: User model exists in `backend/src/models/user.py`
   - Reason: Validate user exists before processing chat
   - Validation: Can import and query User model

### Downstream Dependencies (Other Agents Depend on This Agent)
1. **AI Agent Logic Agent**:
   - Dependency: Chat API provides structured conversation context
   - Integration Point: Agent logic receives message history from chat orchestrator
   - Contract: Message format must match what agent expects

2. **ChatKit Frontend Builder Agent**:
   - Dependency: Chat API endpoint must exist and respond correctly
   - Integration Point: Frontend calls POST `/api/{user_id}/chat`
   - Contract: Request/response format must match frontend expectations

### Parallel Agents (Can Develop Concurrently)
- None (this agent is on the critical path)

---

## Example Expected Inputs and Outputs

### Example 1: First Message in New Conversation
**Input** (HTTP Request):
```http
POST /api/user_abc123/chat
Content-Type: application/json

{
  "message": "Add a task to buy groceries"
}
```

**Internal Processing**:
1. Validate user `user_abc123` exists
2. Create new conversation `conv_xyz789`
3. Persist user message: "Add a task to buy groceries"
4. Invoke AI agent → determines need to call `add_task` tool
5. Execute MCP tool: `add_task(user_id="user_abc123", title="Buy groceries")`
6. MCP returns: `{"id": 42, "title": "Buy groceries", ...}`
7. Persist assistant message with tool_calls metadata

**Output** (HTTP Response):
```json
{
  "conversation_id": "conv_xyz789",
  "message_id": "msg_001",
  "response": "I've added the task 'Buy groceries' for you.",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {
        "user_id": "user_abc123",
        "title": "Buy groceries",
        "description": null,
        "priority": null,
        "due_date": null,
        "tags": null
      },
      "result": {
        "id": 42,
        "title": "Buy groceries",
        "completed": false,
        "user_id": "user_abc123"
      }
    }
  ]
}
```

### Example 2: Subsequent Message in Existing Conversation
**Input** (HTTP Request):
```http
POST /api/user_abc123/chat
Content-Type: application/json

{
  "message": "Show me all my tasks",
  "conversation_id": "conv_xyz789"
}
```

**Internal Processing**:
1. Load conversation `conv_xyz789` for user `user_abc123`
2. Load message history (previous messages)
3. Persist user message: "Show me all my tasks"
4. Invoke AI agent with full conversation history
5. Execute MCP tool: `list_tasks(user_id="user_abc123")`
6. MCP returns: `[{task1}, {task2}, ...]`
7. Persist assistant message

**Output** (HTTP Response):
```json
{
  "conversation_id": "conv_xyz789",
  "message_id": "msg_002",
  "response": "You have 2 tasks: 1) Buy groceries 2) Finish documentation",
  "tool_calls": [
    {
      "tool": "list_tasks",
      "parameters": {
        "user_id": "user_abc123"
      },
      "result": [
        {"id": 42, "title": "Buy groceries", "completed": false},
        {"id": 43, "title": "Finish documentation", "completed": false}
      ]
    }
  ]
}
```

### Example 3: Error Handling - MCP Unavailable
**Input** (HTTP Request):
```http
POST /api/user_abc123/chat
Content-Type: application/json

{
  "message": "Delete task 42"
}
```

**Internal Processing**:
1. Validate user, create/load conversation
2. Persist user message
3. Invoke AI agent → determines need to call `delete_task` tool
4. Attempt MCP tool execution → MCP server unavailable (timeout)
5. Fallback: Return error response

**Output** (HTTP Response):
```json
{
  "conversation_id": "conv_xyz789",
  "message_id": "msg_003",
  "response": "I'm sorry, but I'm unable to perform task operations right now. Please try again in a moment.",
  "error": {
    "code": "MCP_UNAVAILABLE",
    "message": "Task service temporarily unavailable"
  }
}
```

---

## 7-Step Pipeline Implementation Details

### Step 1: Receive User Message
```python
@router.post("/api/{user_id}/chat")
async def chat(
    user_id: str,
    request: ChatRequest,
    db: Session = Depends(get_db)
) -> ChatResponse:
    # Validate request schema (Pydantic handles)
    # Extract message and optional conversation_id
    pass
```

### Step 2: Load Conversation History
```python
# If conversation_id provided
conversation = db.query(Conversation).filter(
    Conversation.id == request.conversation_id,
    Conversation.user_id == user_id
).first()

# If not found, create new conversation
if not conversation:
    conversation = Conversation(id=generate_id(), user_id=user_id)
    db.add(conversation)
    db.commit()

# Load message history
messages = db.query(Message).filter(
    Message.conversation_id == conversation.id
).order_by(Message.created_at.asc()).all()
```

### Step 3: Persist User Message
```python
user_message = Message(
    id=generate_message_id(),
    conversation_id=conversation.id,
    role="user",
    content=request.message,
    tool_calls=None
)
db.add(user_message)
db.commit()
```

### Step 4: Invoke AI Agent Logic
```python
# Prepare conversation context
context = [{"role": m.role, "content": m.content} for m in messages]
context.append({"role": "user", "content": request.message})

# Invoke agent (stub or OpenAI Agents SDK)
agent_response = await invoke_agent(context)
# Returns: {"content": "...", "tool_calls": [...]}
```

### Step 5: Execute MCP Tools
```python
tool_results = []
for tool_call in agent_response.get("tool_calls", []):
    result = await mcp_client.invoke_tool(
        tool_name=tool_call["tool"],
        parameters=tool_call["parameters"]
    )
    tool_results.append({
        "tool": tool_call["tool"],
        "parameters": tool_call["parameters"],
        "result": result
    })
```

### Step 6: Persist Assistant Response
```python
assistant_message = Message(
    id=generate_message_id(),
    conversation_id=conversation.id,
    role="assistant",
    content=agent_response["content"],
    tool_calls=tool_results if tool_results else None
)
db.add(assistant_message)
db.commit()
```

### Step 7: Return Response
```python
return ChatResponse(
    conversation_id=conversation.id,
    message_id=assistant_message.id,
    response=agent_response["content"],
    tool_calls=tool_results
)
```

---

## Validation Checklist Before Completion

### Code Quality
- [ ] All functions have type hints and docstrings
- [ ] Pydantic models for all requests and responses
- [ ] Proper async/await usage
- [ ] Error handling at each pipeline step
- [ ] No hardcoded values

### Functionality
- [ ] Endpoint responds to valid requests
- [ ] Conversations created and loaded correctly
- [ ] Messages persisted in correct order
- [ ] MCP tools invoked successfully
- [ ] Tool results captured and returned

### Integration
- [ ] MCP client connects to MCP server
- [ ] Database transactions work correctly
- [ ] User validation works
- [ ] Phase II code untouched (verify with git diff)

### Performance
- [ ] Database queries optimized
- [ ] Connection pooling configured
- [ ] Conversation history limited
- [ ] Timeout protection on MCP calls

### Security
- [ ] User can only access own conversations
- [ ] Input validation on all parameters
- [ ] No SQL injection vulnerabilities
- [ ] No sensitive data in errors

---

**Skill Version**: 1.0.0
**Last Updated**: 2026-01-23
**Maintained By**: Phase III Chat Architecture Team
