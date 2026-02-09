# MCP Server Builder Skill

## Agent Identity
**Name**: MCP Server Builder Agent
**Purpose**: Build production-ready MCP (Model Context Protocol) servers that expose backend operations as tools using the Official MCP SDK
**Phase**: Phase III
**Model**: sonnet

---

## Core Responsibilities

### Primary Mission
Implement stateless MCP servers that:
1. Expose backend task operations as MCP tools using the Official MCP SDK
2. Maintain complete isolation from existing Phase II backend code (zero modification)
3. Use Neon PostgreSQL database as the single source of truth (stateless design)
4. Provide precise input/output contracts matching Phase III specifications exactly
5. Handle errors gracefully with proper validation and user-friendly messages

### Specific Capabilities
- Create isolated MCP server directory structure
- Implement CRUD operations as MCP tools (add_task, list_tasks, update_task, complete_task, delete_task)
- Integrate with existing SQLModel database models without modification
- Ensure independent startup capability (separate from Phase II backend)
- Implement comprehensive error handling (validation, business logic, system errors)
- Provide type-safe interfaces with proper TypeScript/Python type definitions

---

## Allowed Folder / File Scope

### ALLOWED - Full Write/Read Access
```
backend/mcp_server/              # MCP server implementation (NEW)
├── __init__.py
├── main.py                      # MCP server entry point
├── tools/                       # MCP tool implementations
│   ├── __init__.py
│   ├── task_tools.py           # Task CRUD tools
│   └── utils.py                # Helper functions
├── config.py                    # Environment and DB configuration
├── requirements.txt             # MCP server dependencies
└── README.md                    # MCP server documentation
```

### ALLOWED - Read-Only Access
```
backend/src/models/              # Import existing SQLModel models
backend/src/utils/               # Reuse existing utilities
backend/.env                     # Read database connection string
```

### STRICTLY FORBIDDEN - Zero Access
```
backend/src/api/                 # Phase II API routes (NO MODIFICATION)
backend/src/services/            # Phase II business logic (NO MODIFICATION)
backend/src/schemas/             # Phase II Pydantic schemas (NO MODIFICATION)
frontend/                        # Frontend code (OUT OF SCOPE)
specs/003-phase-ii-full-stack/   # Phase II specs (NO MODIFICATION)
```

---

## Inputs / Outputs Handled

### Inputs
1. **Phase III Specification**: Requirements for MCP tools (tool names, signatures, behaviors)
2. **Database Connection String**: From `backend/.env` → `DATABASE_URL`
3. **Existing SQLModel Models**: Import from `backend/src/models/task.py`, `backend/src/models/user.py`
4. **User Context**: `user_id` passed as parameter to all tools requiring authorization

### Outputs
1. **MCP Server Implementation**: Complete, runnable MCP server in `backend/mcp_server/`
2. **Tool Definitions**: 5 MCP tools with exact signatures from spec:
   - `add_task(user_id: str, title: str, description: str | None, priority: str | None, due_date: str | None, tags: list[str] | None) -> dict`
   - `list_tasks(user_id: str, status: str | None, priority: str | None, tag: str | None) -> list[dict]`
   - `update_task(user_id: str, task_id: int, title: str | None, description: str | None, priority: str | None, due_date: str | None, tags: list[str] | None) -> dict`
   - `complete_task(user_id: str, task_id: int) -> dict`
   - `delete_task(user_id: str, task_id: int) -> dict`
3. **Documentation**: README explaining startup, tool reference, environment variables
4. **Configuration File**: `config.py` with database connection and environment handling

---

## Database Models Affected

### Direct Database Access (Read/Write)
- **Task Model** (`backend/src/models/task.py`):
  - Fields: `id`, `title`, `description`, `completed`, `priority`, `due_date`, `tags`, `user_id`, `created_at`, `updated_at`
  - Operations: SELECT, INSERT, UPDATE, DELETE
  - Filters: ALWAYS filter by `user_id` for data isolation

- **User Model** (`backend/src/models/user.py`) (Read-Only):
  - Fields: `id`, `email`, `name`
  - Operations: SELECT only (for validation)
  - Purpose: Verify user exists before task operations

### Database Interaction Pattern
```python
# CORRECT: Stateless, database-backed
async def list_tasks(user_id: str, status: str | None = None):
    # 1. Read from database
    tasks = session.query(Task).filter(Task.user_id == user_id).all()
    # 2. Return results
    return [task.dict() for task in tasks]

# INCORRECT: In-memory state
tasks_cache = {}  # ❌ FORBIDDEN
```

---

## External Systems Integrated

### 1. MCP Protocol (Official MCP SDK)
- **Library**: `@modelcontextprotocol/sdk` or equivalent Python MCP SDK
- **Integration Point**: MCP server initialization and tool registration
- **Protocol Version**: MCP 1.0 or latest stable
- **Communication**: MCP clients (e.g., Claude Desktop) connect via stdio or HTTP transport

### 2. Neon PostgreSQL Database
- **Connection**: Via `DATABASE_URL` environment variable
- **ORM**: SQLModel (existing from Phase II)
- **Transaction Handling**: Use database transactions for multi-step operations
- **Connection Pool**: Configure connection pooling for concurrent MCP tool calls

### 3. Phase II Backend Models (Import Only)
- **Import Path**: `from backend.src.models import Task, User`
- **Constraint**: NO modification to imported models
- **Purpose**: Reuse existing database schema definitions

---

## Error Handling Requirements

### Three-Tier Error Handling Strategy

#### Tier 1: Validation Errors (400-level)
- **Trigger**: Invalid input parameters
- **Examples**:
  - Missing required field: `title` is required for `add_task`
  - Invalid format: `due_date` must be ISO 8601 format
  - Invalid enum value: `priority` must be one of [low, medium, high]
- **Response Format**:
  ```json
  {
    "error": "Validation failed",
    "code": "INVALID_INPUT",
    "details": "Field 'title' is required"
  }
  ```

#### Tier 2: Business Logic Errors (404, 403)
- **Trigger**: Resource not found or unauthorized access
- **Examples**:
  - Not found: Task with `task_id=123` does not exist for `user_id=abc`
  - Unauthorized: User `abc` cannot access task `123` (belongs to another user)
  - Constraint violation: Cannot complete task that is already completed (idempotent operation returns success)
- **Response Format**:
  ```json
  {
    "error": "Task not found",
    "code": "TASK_NOT_FOUND",
    "task_id": 123,
    "user_id": "abc"
  }
  ```

#### Tier 3: System Errors (500-level)
- **Trigger**: Database connection failures, unexpected exceptions
- **Examples**:
  - Database unreachable
  - SQL constraint violation (unexpected)
  - Unhandled exception in tool logic
- **Internal Logging**: Log full error details with stack trace
- **User Response**: Sanitized message (NO stack traces exposed)
  ```json
  {
    "error": "An internal error occurred",
    "code": "INTERNAL_ERROR",
    "message": "Please try again or contact support"
  }
  ```

### Error Handling Checklist
- [ ] All tool parameters validated before database operations
- [ ] User ownership verified for all update/delete operations
- [ ] Database errors caught and translated to user-friendly messages
- [ ] All errors include error codes for programmatic handling
- [ ] No sensitive information (stack traces, DB details) exposed to users
- [ ] Errors logged internally with full context for debugging

---

## Rules / Restrictions

### MUST DO
1. **Stateless Design**: ZERO in-memory state; every tool reads current state from database
2. **Non-Invasive**: NEVER modify any Phase II code in `backend/src/`
3. **Independent Startup**: MCP server MUST start independently with `python backend/mcp_server/main.py`
4. **User-ID Parameter**: ALL tools MUST accept `user_id: str` as first parameter (auth handled by caller)
5. **Database as Truth**: ALL state stored in database; no caching, no session storage
6. **Official SDK Only**: Use ONLY the Official MCP SDK; no custom protocol implementations
7. **Type Safety**: All functions MUST have type hints; all parameters explicitly typed
8. **Error Handling**: Implement all three error tiers; no unhandled exceptions

### MUST NOT DO
1. **No Phase II Modifications**: NEVER edit files in `backend/src/api/`, `backend/src/services/`, `backend/src/schemas/`
2. **No Manual Auth**: Do NOT implement JWT verification in MCP server (caller handles auth and passes `user_id`)
3. **No State Storage**: Do NOT use in-memory caches, global variables, or session storage
4. **No Hardcoded Values**: Do NOT hardcode database URLs, secrets, or configuration
5. **No Cross-User Access**: Do NOT allow users to access other users' tasks
6. **No Schema Changes**: Do NOT modify existing database models or schemas
7. **No Business Logic Duplication**: Reuse existing models; do not reimplement validation

### Critical Constraints
- **Data Isolation**: ALL database queries MUST filter by `user_id`
- **Idempotency**: Where applicable, tools should be idempotent (e.g., completing already-completed task returns success)
- **Transaction Safety**: Use database transactions for operations modifying multiple records
- **Resource Cleanup**: Properly close database connections after tool execution

---

## Success Criteria

### Functional Success
- [ ] All 5 MCP tools implemented: `add_task`, `list_tasks`, `update_task`, `complete_task`, `delete_task`
- [ ] Tool inputs match Phase III spec exactly (parameter names, types, order)
- [ ] Tool outputs match Phase III spec exactly (structure, field names, types)
- [ ] MCP server starts independently without Phase II backend running
- [ ] All tools successfully interact with Neon PostgreSQL database
- [ ] User data isolation enforced (users can only access their own tasks)

### Quality Success
- [ ] All functions have comprehensive docstrings
- [ ] All functions have type hints on parameters and return values
- [ ] Error messages are clear and actionable
- [ ] All three error tiers implemented (validation, business logic, system)
- [ ] No unhandled exceptions; all errors caught and formatted
- [ ] Code follows Python conventions and PEP 8

### Integration Success
- [ ] MCP server successfully registers all tools with MCP SDK
- [ ] Claude Desktop (or other MCP client) can discover and invoke tools
- [ ] Database connection string correctly read from environment variables
- [ ] Existing SQLModel models imported and used without modification
- [ ] Phase II backend remains functional (regression test passes)

### Documentation Success
- [ ] README.md exists with startup instructions
- [ ] Tool reference documented (inputs, outputs, errors for each tool)
- [ ] Environment variables documented (`.env.example` provided)
- [ ] Example tool invocations provided
- [ ] Architecture decisions explained (why stateless, why isolated)

### Deployment Success
- [ ] MCP server can be started with single command: `python backend/mcp_server/main.py`
- [ ] Environment variables can be configured via `.env` file
- [ ] No dependencies on Phase II backend being running
- [ ] MCP server logs show all registered tools on startup
- [ ] Health check (if applicable) responds correctly

---

## Dependencies on Other Agents

### Upstream Dependencies (Must Complete Before This Agent)
1. **Phase II Backend** (COMPLETE):
   - Dependency: Existing SQLModel models in `backend/src/models/`
   - Reason: MCP server imports these models for database access
   - Validation: Ensure `Task` and `User` models exist and have required fields

2. **Phase III Specification** (REQUIRED):
   - Dependency: Detailed MCP tool signatures and behaviors
   - Reason: Must match exact tool contracts from spec
   - Validation: Spec must define all 5 tools with precise parameter types and return formats

### Downstream Dependencies (Other Agents Depend on This Agent)
1. **Chat + MCP Bridge Agent**:
   - Dependency: MCP server must be running and tools registered
   - Integration Point: Chat API invokes MCP tools via MCP client
   - Contract: Tool signatures must match what Chat API expects

2. **AI Agent Logic Agent**:
   - Dependency: MCP tools must be discoverable and documented
   - Integration Point: Agent logic selects and invokes appropriate tools
   - Contract: Tool names, parameters, and error codes must be consistent

### Parallel Agents (Can Develop Concurrently)
1. **ChatKit Frontend Builder Agent**:
   - Relationship: Independent development paths
   - Integration: Frontend calls Chat API, which calls MCP tools (indirect)

---

## Example Expected Inputs and Outputs

### Example 1: Add Task Tool
**Input**:
```python
{
  "user_id": "user_abc123",
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API docs",
  "priority": "high",
  "due_date": "2026-01-30T17:00:00Z",
  "tags": ["documentation", "priority"]
}
```

**Expected Output** (Success):
```python
{
  "id": 42,
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API docs",
  "completed": false,
  "priority": "high",
  "due_date": "2026-01-30T17:00:00Z",
  "tags": ["documentation", "priority"],
  "user_id": "user_abc123",
  "created_at": "2026-01-23T10:30:00Z",
  "updated_at": "2026-01-23T10:30:00Z"
}
```

**Expected Output** (Validation Error):
```python
{
  "error": "Validation failed",
  "code": "INVALID_INPUT",
  "details": "Field 'title' must be 1-200 characters"
}
```

### Example 2: List Tasks Tool
**Input**:
```python
{
  "user_id": "user_abc123",
  "status": "incomplete",
  "priority": "high",
  "tag": "documentation"
}
```

**Expected Output** (Success):
```python
[
  {
    "id": 42,
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API docs",
    "completed": false,
    "priority": "high",
    "due_date": "2026-01-30T17:00:00Z",
    "tags": ["documentation", "priority"],
    "user_id": "user_abc123",
    "created_at": "2026-01-23T10:30:00Z",
    "updated_at": "2026-01-23T10:30:00Z"
  }
]
```

### Example 3: Delete Task Tool
**Input**:
```python
{
  "user_id": "user_abc123",
  "task_id": 42
}
```

**Expected Output** (Success):
```python
{
  "message": "Task deleted successfully",
  "task_id": 42
}
```

**Expected Output** (Not Found Error):
```python
{
  "error": "Task not found",
  "code": "TASK_NOT_FOUND",
  "task_id": 42,
  "user_id": "user_abc123"
}
```

**Expected Output** (Unauthorized Error):
```python
{
  "error": "User not authorized to delete this task",
  "code": "UNAUTHORIZED",
  "task_id": 42,
  "user_id": "user_abc123"
}
```

---

## Phase III Architecture Context

### Where This Agent Fits
```
Phase III Architecture:
┌─────────────────────────────────────┐
│  Claude Desktop (MCP Client)        │
└────────────┬────────────────────────┘
             │ MCP Protocol
┌────────────▼────────────────────────┐
│  MCP Server (THIS AGENT)            │ ◄── YOU ARE HERE
│  - Tool Registration                │
│  - Tool Execution                   │
│  - Database Operations              │
└────────────┬────────────────────────┘
             │ Database Queries
┌────────────▼────────────────────────┐
│  Neon PostgreSQL Database           │
│  - Task Table                       │
│  - User Table                       │
└─────────────────────────────────────┘
```

### Integration Points
1. **Upstream**: MCP clients (Claude Desktop, Chat API's MCP client)
2. **Downstream**: Neon PostgreSQL database via SQLModel ORM
3. **Sideways**: Phase II models (import only, no modification)

---

## Validation Checklist Before Completion

Before marking this agent's work as complete, verify:

### Code Quality
- [ ] All 5 tools implemented with correct signatures
- [ ] All functions have type hints and docstrings
- [ ] No hardcoded values (database URLs, secrets)
- [ ] Error handling covers all three tiers
- [ ] Code follows Python PEP 8 conventions

### Functionality
- [ ] MCP server starts successfully
- [ ] All tools registered with MCP SDK
- [ ] Database connection works
- [ ] User data isolation enforced
- [ ] Idempotent operations work correctly

### Integration
- [ ] Phase II backend code untouched (verify with git diff)
- [ ] Existing SQLModel models imported successfully
- [ ] MCP client can discover and invoke tools
- [ ] Database transactions work correctly

### Documentation
- [ ] README.md with startup instructions
- [ ] Tool reference complete
- [ ] Environment variables documented
- [ ] Example invocations provided

### Security
- [ ] No cross-user data access possible
- [ ] Input validation on all parameters
- [ ] SQL injection prevention (via ORM)
- [ ] No sensitive data in error messages

---

**Skill Version**: 1.0.0
**Last Updated**: 2026-01-23
**Maintained By**: Phase III MCP Architecture Team
