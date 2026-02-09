# Todo MCP Server

Model Context Protocol (MCP) server that exposes task management operations as tools for AI agents.

## Overview

This MCP server provides 5 core task management operations:

1. **add_task** - Create new tasks
2. **list_tasks** - Query tasks with filtering
3. **update_task** - Modify task properties
4. **complete_task** - Mark tasks as completed
5. **delete_task** - Remove tasks

All operations enforce **strict user_id isolation** - users can only access their own tasks.

## Architecture

```
mcp_server/
├── main.py              # MCP server entry point
├── config.py            # Database configuration
├── tools/
│   ├── task_tools.py    # 5 MCP tool implementations
│   └── __init__.py
└── tests/
    ├── test_task_tools.py      # Unit tests
    └── test_mcp_server.py      # Integration tests
```

## Prerequisites

- Python 3.11+
- PostgreSQL database (Neon or local)
- Official MCP Python SDK: `pip install mcp`

## Environment Variables

```bash
# Required
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db

# Optional
MCP_SERVER_LOG_LEVEL=INFO
```

## Installation

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export DATABASE_URL="your-neon-postgres-url"
```

3. Run database migrations (if not already done):
```bash
python3 -m alembic upgrade head
```

## Running the Server

### Standalone Mode (stdio transport)

```bash
cd backend
python3 -m mcp_server.main
```

The server will communicate via stdin/stdout using the MCP protocol.

### Testing with MCP Inspector

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run inspector
mcp-inspector python3 -m mcp_server.main
```

## Tool Documentation

### 1. add_task

Create a new task for the authenticated user.

**Parameters:**
```json
{
  "user_id": "uuid-string",          // Required
  "title": "Task title",              // Required (1-500 chars)
  "description": "Optional details",  // Optional (ignored in Phase II)
  "priority": "medium",               // Optional: low|medium|high
  "due_date": "2026-02-01",          // Optional: ISO 8601 date
  "tags": ["work", "urgent"]         // Optional: array of strings
}
```

**Response:**
```json
{
  "success": true,
  "task": {
    "id": "task-uuid",
    "user_id": "user-uuid",
    "description": "Task title",
    "completed": false,
    "priority": "medium",
    "tags": ["work", "urgent"],
    "due_date": "2026-02-01",
    "created_at": "2026-01-27T10:00:00",
    "updated_at": "2026-01-27T10:00:00"
  },
  "message": "Task created successfully"
}
```

**Example:**
```python
result = await client.call_tool(
    "add_task",
    {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Buy groceries",
        "priority": "high",
        "tags": ["shopping"]
    }
)
```

### 2. list_tasks

List tasks for the authenticated user with optional filtering.

**Parameters:**
```json
{
  "user_id": "uuid-string",    // Required
  "status": "pending",         // Optional: pending|completed|all (default: all)
  "priority": "high",          // Optional: low|medium|high
  "tag": "work"               // Optional: filter by single tag
}
```

**Response:**
```json
{
  "success": true,
  "tasks": [
    {
      "id": "task-uuid",
      "user_id": "user-uuid",
      "description": "Task title",
      "completed": false,
      "priority": "high",
      "tags": ["work"],
      "due_date": "2026-02-01",
      "created_at": "2026-01-27T10:00:00",
      "updated_at": "2026-01-27T10:00:00"
    }
  ],
  "count": 1,
  "filters": {
    "status": "pending",
    "priority": "high",
    "tag": "work"
  }
}
```

**Example:**
```python
result = await client.call_tool(
    "list_tasks",
    {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "status": "pending",
        "priority": "high"
    }
)
```

### 3. update_task

Update an existing task (user can only update their own tasks).

**Parameters:**
```json
{
  "user_id": "uuid-string",          // Required
  "task_id": "uuid-string",          // Required
  "title": "New title",              // Optional (1-500 chars)
  "description": "New details",      // Optional (ignored in Phase II)
  "priority": "high",                // Optional: low|medium|high
  "due_date": "2026-02-15",         // Optional: ISO 8601 date or null
  "tags": ["updated", "work"]       // Optional: array of strings
}
```

**Response:**
```json
{
  "success": true,
  "task": {
    "id": "task-uuid",
    "user_id": "user-uuid",
    "description": "New title",
    "completed": false,
    "priority": "high",
    "tags": ["updated", "work"],
    "due_date": "2026-02-15",
    "created_at": "2026-01-27T10:00:00",
    "updated_at": "2026-01-27T11:00:00"
  },
  "message": "Task updated successfully"
}
```

**Example:**
```python
result = await client.call_tool(
    "update_task",
    {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "task_id": "660e8400-e29b-41d4-a716-446655440001",
        "title": "Buy groceries and cook dinner",
        "priority": "high"
    }
)
```

### 4. complete_task

Mark a task as completed (user can only complete their own tasks).

**Parameters:**
```json
{
  "user_id": "uuid-string",    // Required
  "task_id": "uuid-string"     // Required
}
```

**Response:**
```json
{
  "success": true,
  "task": {
    "id": "task-uuid",
    "user_id": "user-uuid",
    "description": "Task title",
    "completed": true,
    "priority": "medium",
    "tags": ["work"],
    "due_date": "2026-02-01",
    "created_at": "2026-01-27T10:00:00",
    "updated_at": "2026-01-27T12:00:00"
  },
  "message": "Task completed successfully"
}
```

**Example:**
```python
result = await client.call_tool(
    "complete_task",
    {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "task_id": "660e8400-e29b-41d4-a716-446655440001"
    }
)
```

### 5. delete_task

Delete a task (user can only delete their own tasks).

**Parameters:**
```json
{
  "user_id": "uuid-string",    // Required
  "task_id": "uuid-string"     // Required
}
```

**Response:**
```json
{
  "success": true,
  "task_id": "task-uuid",
  "message": "Task deleted successfully"
}
```

**Example:**
```python
result = await client.call_tool(
    "delete_task",
    {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "task_id": "660e8400-e29b-41d4-a716-446655440001"
    }
)
```

## Error Handling

All tools return standardized error responses:

```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": "Optional technical details"
}
```

**Error Codes:**

- `TASK_NOT_FOUND` - Task doesn't exist or user doesn't have access
- `UNAUTHORIZED` - User doesn't own the task (enforced by user_id isolation)
- `INVALID_INPUT` - Invalid parameters (bad UUID, empty title, etc.)
- `INTERNAL_ERROR` - Database or server error

## Security Features

### 1. User Data Isolation (100% Enforcement)

All database queries include `WHERE user_id = :user_id` to prevent cross-user data access:

```python
# Example from list_tasks
query = select(Task).where(Task.user_id == user_id)
```

### 2. SQL Injection Prevention

Uses SQLAlchemy parameterized queries - no string concatenation:

```python
# Safe: parameterized
query = select(Task).where(Task.id == task_id, Task.user_id == user_id)

# Unsafe: never do this
query = f"SELECT * FROM tasks WHERE id = '{task_id}'"  # ❌ VULNERABLE
```

### 3. Input Validation

All inputs validated before database operations:
- UUIDs must be valid UUID format
- Titles limited to 1-500 characters
- Priority must be one of: low|medium|high
- Dates must be valid ISO 8601 format

## Testing

### Run Unit Tests

```bash
cd backend
pytest mcp_server/tests/test_task_tools.py -v
```

### Run Integration Tests

```bash
pytest mcp_server/tests/test_mcp_server.py -v
```

### Test Coverage

```bash
pytest --cov=mcp_server --cov-report=html
```

## Troubleshooting

### Server Won't Start

**Problem:** `ValueError: DATABASE_URL environment variable is required`

**Solution:** Set DATABASE_URL:
```bash
export DATABASE_URL="postgresql+asyncpg://user:pass@host:5432/db"
```

---

**Problem:** `ImportError: No module named 'mcp'`

**Solution:** Install MCP SDK:
```bash
pip install mcp
```

### Database Connection Errors

**Problem:** `asyncpg.exceptions.InvalidPasswordError`

**Solution:** Check DATABASE_URL credentials and ensure using asyncpg driver:
```
postgresql+asyncpg://user:pass@host:5432/db
               ^^^^^^^
               Must include asyncpg
```

---

**Problem:** `asyncpg.exceptions.CannotConnectNowError`

**Solution:** Database not accepting connections. Check:
1. Neon project is running (not paused)
2. IP allowlist includes your IP
3. Connection string is correct

### Tool Execution Errors

**Problem:** `TASK_NOT_FOUND` when task exists

**Solution:** Verify `user_id` matches task owner. Users can only access their own tasks.

---

**Problem:** `INVALID_INPUT: Invalid user_id`

**Solution:** Ensure user_id is a valid UUID string:
```python
# ✅ Correct
"550e8400-e29b-41d4-a716-446655440000"

# ❌ Wrong
"123"  # Not a UUID
"user-123"  # Not a UUID
```

## Performance Considerations

### Database Indexing

Phase II tasks table includes indexes for optimal query performance:

```sql
-- Primary key index
CREATE INDEX ON tasks(id);

-- User isolation queries
CREATE INDEX ON tasks(user_id);

-- Sorting by creation time
CREATE INDEX ON tasks(created_at);
```

### Connection Pooling

MCP server uses SQLAlchemy connection pooling:
- Pool size: 5 connections
- Max overflow: 10 connections
- Pre-ping enabled (verifies connections before use)

### Query Optimization

All list_tasks queries order by `created_at DESC` using indexed column.

Tag filtering uses PostgreSQL JSON `contains` operator with GIN index support.

## Phase III Integration

This MCP server is **Agent 1** in the Phase III architecture:

```
User → Frontend (Agent 4: ChatKit)
         ↓
      Chat API (Agent 2: /api/{user_id}/chat)
         ↓
      AI Agent Logic (Agent 3: Orchestrator)
         ↓
      Gemini LLM (Agent 5: Gemini Flash 2.5)
         ↓
      MCP Server (Agent 1: This Server) ← YOU ARE HERE
         ↓
      PostgreSQL Database (Phase II Tasks)
```

The MCP server:
1. **Receives tool calls** from AI Agent via MCP protocol
2. **Enforces user_id isolation** at database level
3. **Returns JSON responses** for AI to interpret
4. **Operates independently** - can start without Phase II backend running

## License

Part of the Todo App project. See project root LICENSE file.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review MCP SDK docs: https://github.com/modelcontextprotocol/python-sdk
3. Check Phase III spec: `specs/004-phase-iii-chatbot/spec.md`
