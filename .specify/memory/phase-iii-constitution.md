<!--
  Sync Impact Report:

  Version Change: 2.0.0 → 3.0.0 (MAJOR - Phase III AI Chatbot Constitution)

  Modified Principles:
  - Phase II Constitution (2.0.0) → Phase III Constitution (3.0.0)
  - Added AI-powered chatbot functionality
  - Added MCP (Model Context Protocol) server architecture
  - Added OpenAI Agents SDK integration
  - Added ChatKit frontend components
  - Added conversation persistence and management

  Added Sections:
  - Phase III Project Overview and Objectives
  - MCP Server Architecture and Tool Definitions
  - AI Agent Logic and Natural Language Processing
  - Chat API Bridge and Conversation Management
  - ChatKit Frontend Integration
  - Four specialized Phase III agents with detailed responsibilities
  - Stateless architecture principles for scalability
  - Natural language to MCP tool mapping
  - Conversation persistence strategy

  Removed Sections:
  - None (Phase II remains valid; Phase III extends it)

  Critical Constraints:
  - Phase II code is IMMUTABLE (no modifications allowed)
  - All Phase III work must coexist with Phase II without breaking changes
  - MCP-first architecture: AI agents NEVER access database directly
  - Stateless design: all state in database, no in-memory sessions

  Templates Requiring Updates:
  - ✅ .specify/templates/plan-template.md (aligned - supports multi-agent architecture)
  - ✅ .specify/templates/spec-template.md (aligned - supports AI/MCP features)
  - ✅ .specify/templates/tasks-template.md (aligned - agent-based task execution)
  - ⚠ .specify/templates/commands/*.md (review for Phase III context)

  Follow-up TODOs:
  - Review all command files for Phase III alignment
  - Ensure all four Phase III agent skill files are complete and accurate
  - Create Phase III feature specifications following this constitution
  - Validate MCP server compatibility with OpenAI Agents SDK
-->

# Full-Stack Todo Web Application Constitution (Phase III)

## Project Purpose

This constitution governs **Phase III** of the Todo Web Application project.

**Goal**: Extend the fully functional Phase II web application with AI-powered chatbot capabilities, enabling users to manage tasks through natural language conversations while maintaining all existing functionality intact.

**Phase III Vision**: Deliver an intelligent conversational interface that:
- Enables natural language task management via AI chatbot
- Integrates MCP (Model Context Protocol) server for tool-based task operations
- Uses OpenAI Agents SDK for intent understanding and orchestration
- Provides modern chat UI via OpenAI ChatKit
- Persists conversation history in Neon PostgreSQL database
- Maintains stateless, horizontally scalable architecture
- Preserves 100% of Phase II functionality without modification

**Development Model**: All code generation MUST be driven by four specialized agents with defined skills. Each agent operates within strict boundaries, ensuring architectural integrity and zero Phase II regressions.

---

## Phase III Scope

### What Phase III Covers

Phase III adds **AI-powered conversational task management** on top of Phase II:

#### Core Phase III Features

1. **MCP Server Implementation**
   - Standalone MCP server exposing 5 task operation tools
   - Stateless architecture with database as single source of truth
   - Tool signatures: `add_task`, `list_tasks`, `update_task`, `complete_task`, `delete_task`
   - Independent startup capability (runs separately from Phase II backend)

2. **Chat API Endpoint**
   - RESTful endpoint: `POST /api/{user_id}/chat`
   - Stateless request/response model
   - Conversation persistence in database
   - MCP tool invocation via client
   - AI agent integration for intent processing

3. **AI Agent Logic**
   - Natural language understanding using OpenAI Agents SDK
   - Intent parsing: map user messages to MCP tool actions
   - Multi-step tool orchestration
   - Ambiguity detection and clarification requests
   - Response generation: technical outputs → conversational language

4. **ChatKit Frontend Interface**
   - Protected chat route: `/chat`
   - OpenAI ChatKit component integration
   - Real-time message display
   - Conversation state management (React memory)
   - Domain allowlist configuration for production

5. **Conversation Management**
   - Database-backed conversation persistence
   - Message history with role tracking (user/assistant)
   - Tool execution metadata storage
   - Conversation threading and continuity

#### Technology Stack Extensions

**Backend Additions**:
- **MCP Server**: Official MCP SDK (Python)
- **AI Framework**: OpenAI Agents SDK
- **New Models**: Conversation, Message (SQLModel)
- **New Endpoints**: `POST /api/{user_id}/chat`

**Frontend Additions**:
- **UI Framework**: OpenAI ChatKit
- **New Routes**: `/chat` (protected)
- **New Components**: MessageList, MessageInput, ChatInterface

**Infrastructure**:
- **MCP Server**: Independent process
- **Database**: Extended schema (conversations, messages tables)
- **Environment**: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` for ChatKit

#### Folder Structure (Phase III Only)

```
Todo_App/
├── backend/
│   ├── mcp_server/          # NEW: MCP server implementation
│   │   ├── main.py
│   │   ├── tools/
│   │   │   └── task_tools.py
│   │   ├── config.py
│   │   └── README.md
│   ├── phase3/              # NEW: Phase III backend logic
│   │   ├── routers/
│   │   │   └── chat.py      # Chat API endpoint
│   │   ├── services/
│   │   │   ├── chat_orchestrator.py
│   │   │   └── mcp_client.py
│   │   ├── models/
│   │   │   ├── conversation.py
│   │   │   └── message.py
│   │   ├── schemas/
│   │   │   └── chat.py
│   │   └── agent/           # AI agent logic
│   │       ├── intent_parser.py
│   │       ├── tool_selector.py
│   │       └── orchestrator.py
│   └── alembic/
│       └── versions/
│           └── xxxx_add_chat_tables.py  # Migration for Phase III
├── frontend/
│   └── src/
│       ├── app/
│       │   └── chat/        # NEW: Chat page route
│       │       ├── page.tsx
│       │       └── components/
│       ├── components/
│       │   └── chat/        # NEW: Shared chat components
│       ├── lib/
│       │   └── chat.ts      # NEW: Chat API client
│       └── types/
│           └── chat.ts      # NEW: Chat type definitions
└── specs/
    └── 004-phase-iii-chatbot/  # NEW: Phase III specifications
        ├── spec.md
        ├── plan.md
        └── tasks.md
```

### What Phase III Does NOT Cover

Phase III explicitly **excludes** the following (Phase II territory):

#### Out of Scope - Phase II Components (IMMUTABLE)

1. **Existing Frontend Pages**:
   - Dashboard (`/dashboard`)
   - Task CRUD pages
   - Authentication pages (`/login`, `/register`)
   - User profile pages
   - ALL Phase II React components

2. **Existing Backend APIs**:
   - Task CRUD endpoints (`/api/tasks/*`)
   - User authentication endpoints (`/api/auth/*`)
   - User profile endpoints (`/api/users/*`)
   - ALL Phase II FastAPI routers

3. **Existing Database Models**:
   - Task model (can be READ by MCP server, NEVER modified)
   - User model (can be READ for validation, NEVER modified)
   - ANY Phase II SQLModel definitions

4. **Existing Authentication System**:
   - Better Auth configuration
   - JWT token generation and validation
   - Password hashing and security
   - Session management (stateless design)

5. **Phase II Frontend Infrastructure**:
   - Layout components
   - Navigation components
   - Existing UI libraries and configurations
   - Tailwind CSS configuration

#### Out of Scope - Advanced Features (Future Phases)

- Voice input/output for chat
- Multi-language support
- Task recommendations via ML
- Analytics and insights
- Notifications and reminders
- Collaborative task sharing
- Mobile native applications
- Third-party integrations (Calendar, Slack, etc.)

---

## Rules & Restrictions

### Phase II Protection Clause (IMMUTABLE LAW)

**ABSOLUTE RULE**: Phase II code is **sacrosanct** and **MUST NOT** be modified in any way.

#### Enforcement Mechanisms

1. **File-Level Protection**:
   - NO edits to files in:
     - `backend/src/api/` (Phase II API routes)
     - `backend/src/services/` (Phase II business logic)
     - `backend/src/schemas/` (Phase II Pydantic schemas)
     - `backend/src/models/task.py` (Task model definition)
     - `frontend/src/app/(auth)/` (Phase II auth pages)
     - `frontend/src/app/dashboard/` (Phase II dashboard)
     - `frontend/src/components/tasks/` (Phase II task components)

2. **Import-Only Access**:
   - Phase III code MAY import Phase II models (READ-ONLY)
   - Example (ALLOWED):
     ```python
     from backend.src.models import Task, User  # Read-only import
     tasks = session.query(Task).filter(Task.user_id == user_id).all()
     ```
   - Example (FORBIDDEN):
     ```python
     # ❌ Modifying Task model definition
     class Task(SQLModel, table=True):
         new_field: str = Field()  # FORBIDDEN
     ```

3. **Regression Testing**:
   - ALL Phase II functionality MUST continue working
   - Phase II test suite MUST pass without modification
   - No breaking changes to Phase II APIs or UI

4. **Git Verification**:
   - Before merge: verify no Phase II files in `git diff`
   - Automated checks: reject PRs modifying Phase II paths

#### Violations and Consequences

- **Any violation** of Phase II protection is **grounds for immediate rejection**
- Code reviews MUST verify Phase II isolation
- Automated CI checks MUST enforce file-level protection

---

### Agent-Based Development Rules

**RULE**: Every Phase III task MUST be executed by a specialized agent with defined skills.

#### Four Specialized Agents

1. **MCP Server Builder Agent**
   - Skill File: `.claude/skills/mcp-server-builder-skill.md`
   - Invocation: When implementing MCP server or MCP tools
   - Validation: Self-test MCP server startup and tool invocation

2. **Chat + MCP Bridge Agent**
   - Skill File: `.claude/skills/chat-mcp-bridge-skill.md`
   - Invocation: When implementing chat API endpoint
   - Validation: Self-test API responses and database persistence

3. **AI Agent Logic Agent (MCP Orchestrator)**
   - Skill File: `.claude/skills/phase3-mcp-orchestrator-skill.md`
   - Invocation: When implementing AI logic and tool orchestration
   - Validation: Self-test intent parsing and tool selection

4. **ChatKit Frontend Builder Agent**
   - Skill File: `.claude/skills/chatkit-frontend-builder-skill.md`
   - Invocation: When implementing chat UI
   - Validation: Self-test UI rendering and API integration

#### Agent Execution Requirements

- **Skills Compliance**: Agents MUST follow their skill definitions exactly
- **No Cross-Domain Work**: Agents MUST NOT perform work outside their scope
- **Self-Testing**: Agents MUST verify their work before completion
- **Error Handling**: Agents MUST implement all error scenarios from skills
- **Documentation**: Agents MUST document all created files and dependencies

---

### MCP Architecture Rules

**RULE**: AI agents MUST NEVER access database directly; ALL data operations via MCP tools.

#### MCP-First Principle

```
CORRECT Flow:
User Message → AI Agent → MCP Tool → Database
                  ↓
            (Intent parsing,
             tool selection,
             orchestration)

FORBIDDEN Flow:
User Message → AI Agent → Database  ❌
                  ↓
            (Direct DB access)
```

#### MCP Server Constraints

1. **Stateless Design**:
   - MCP server holds ZERO state in memory
   - Every tool invocation is independent
   - Database is the ONLY source of truth
   - No caching, no session storage

2. **Tool Signatures (EXACT)**:
   ```python
   # 1. Add Task
   async def add_task(
       user_id: str,
       title: str,
       description: str | None = None,
       priority: str | None = None,
       due_date: str | None = None,
       tags: list[str] | None = None
   ) -> dict

   # 2. List Tasks
   async def list_tasks(
       user_id: str,
       status: str | None = None,
       priority: str | None = None,
       tag: str | None = None
   ) -> list[dict]

   # 3. Update Task
   async def update_task(
       user_id: str,
       task_id: int,
       title: str | None = None,
       description: str | None = None,
       priority: str | None = None,
       due_date: str | None = None,
       tags: list[str] | None = None
   ) -> dict

   # 4. Complete Task
   async def complete_task(
       user_id: str,
       task_id: int
   ) -> dict

   # 5. Delete Task
   async def delete_task(
       user_id: str,
       task_id: int
   ) -> dict
   ```

3. **User-ID Authentication**:
   - ALL tools accept `user_id` as first parameter
   - MCP server does NOT verify JWT (caller handles auth)
   - MCP tools enforce user data isolation via `user_id` filter

4. **Error Responses (Standardized)**:
   ```python
   # Success
   {"id": 42, "title": "Task title", ...}

   # Validation Error
   {
       "error": "Validation failed",
       "code": "INVALID_INPUT",
       "details": "Field 'title' is required"
   }

   # Not Found Error
   {
       "error": "Task not found",
       "code": "TASK_NOT_FOUND",
       "task_id": 42,
       "user_id": "abc"
   }

   # System Error
   {
       "error": "Internal error occurred",
       "code": "INTERNAL_ERROR",
       "message": "Please try again"
   }
   ```

5. **Independent Startup**:
   - MCP server MUST start independently: `python backend/mcp_server/main.py`
   - No dependency on Phase II backend running
   - Separate process, separate port (if HTTP transport)

---

### Chat API Rules

**RULE**: Chat endpoint MUST be stateless; conversation state ONLY in database.

#### Stateless Design Mandate

1. **No In-Memory Sessions**:
   - No server-side session storage
   - No conversation caching
   - Each request is independent

2. **Database Persistence Required**:
   ```python
   # Conversation Model
   class Conversation(SQLModel, table=True):
       id: str              # Primary key: "conv_abc123"
       user_id: int         # Foreign key to User
       created_at: datetime
       updated_at: datetime

   # Message Model
   class Message(SQLModel, table=True):
       id: str              # Primary key: "msg_456"
       conversation_id: str # Foreign key to Conversation
       role: str            # "user" or "assistant"
       content: str         # Message text
       tool_calls: dict | None  # JSON: tool execution metadata
       created_at: datetime
   ```

3. **Request/Response Contract**:
   ```typescript
   // Request
   POST /api/{user_id}/chat
   {
     "message": "Add a task to buy groceries",
     "conversation_id": "conv_abc123"  // Optional
   }

   // Response
   {
     "conversation_id": "conv_abc123",
     "message_id": "msg_456",
     "response": "I've added the task 'Buy groceries' for you.",
     "tool_calls": [
       {
         "tool": "add_task",
         "parameters": {...},
         "result": {...}
       }
     ]
   }
   ```

4. **7-Step Processing Pipeline**:
   1. Receive user message
   2. Load conversation history from database
   3. Persist user message to database
   4. Invoke AI agent logic
   5. Execute MCP tools (if needed)
   6. Persist assistant response to database
   7. Return response to client

5. **Transaction Safety**:
   - Use database transactions for atomic operations
   - Rollback on any error in pipeline
   - Prevent partial conversation state

---

### AI Agent Logic Rules

**RULE**: AI agents MUST ask clarifying questions for ambiguous requests; NEVER assume intent.

#### Intent Parsing Requirements

1. **Natural Language to Intent Mapping**:
   ```
   User Input                    → Intent           → MCP Tool
   ─────────────────────────────────────────────────────────────
   "Add a task to buy groceries" → add_task         → add_task()
   "Show my tasks"               → list_tasks       → list_tasks()
   "Change task 5 to high"       → update_task      → update_task()
   "Mark task 3 as done"         → complete_task    → complete_task()
   "Delete task 7"               → delete_task      → delete_task()
   "Add a task"                  → AMBIGUOUS        → ask_clarification()
   ```

2. **Ambiguity Detection**:
   - Missing required parameters → Ask for missing info
   - Multiple valid interpretations → Present options
   - Unknown intent → Request clarification

3. **Confirmation for Destructive Actions**:
   ```
   User: "Delete task 5"
   Agent: "Are you sure you want to delete task 5? This cannot be undone."
   User: "Yes"
   Agent: [executes delete_task(task_id=5)]
   ```

4. **Multi-Step Orchestration**:
   - Maximum 5 tool calls per conversation turn
   - Each tool call depends on previous results
   - Partial failure handling: report what succeeded

5. **Response Formatting**:
   - Technical output → Conversational language
   - Example:
     ```
     Tool Result: {"id": 42, "title": "Buy groceries", "completed": false}
     User Response: "I've added the task 'Buy groceries' for you."
     ```

---

### ChatKit Frontend Rules

**RULE**: Chat UI MUST use OpenAI ChatKit; domain allowlist MUST be configured.

#### ChatKit Integration Requirements

1. **Protected Route**:
   - Path: `/chat`
   - Authentication: Reuse Phase II auth system (import only)
   - Redirect unauthenticated users to `/login`

2. **ChatKit Configuration**:
   ```typescript
   // Environment variable
   NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key

   // ChatKit initialization
   import { ChatKit } from '@openai/chatkit';

   const chatKit = new ChatKit({
     domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,
     // ... other config
   });
   ```

3. **Component Structure**:
   - `MessageList`: Display conversation history
   - `MessageInput`: User input field with send button
   - `LoadingIndicator`: Show during API calls
   - `ErrorDisplay`: User-friendly error messages
   - `EmptyState`: Initial state before first message

4. **State Management**:
   - Conversation ID: React state (useState)
   - Message history: React state (useState or useReducer)
   - NO localStorage or sessionStorage for chat data
   - State cleared on page refresh (intentional)

5. **UI/UX Standards**:
   - Auto-scroll to latest message
   - Loading indicator during API calls
   - Error states with retry button
   - Responsive design (mobile, tablet, desktop)
   - Accessible (keyboard navigation, screen reader support)

---

### Confirmation Message Requirements

**RULE**: Every successful task operation MUST result in a confirmation message to the user.

#### Confirmation Templates

```
Action: Add Task
Confirmation: "I've added the task '[title]' for you."

Action: List Tasks
Confirmation: "You have [count] tasks: [list]"

Action: Update Task
Confirmation: "I've updated task [id] with [changes]."

Action: Complete Task
Confirmation: "Task [id] is now marked as complete."

Action: Delete Task
Confirmation: "Task [id] has been deleted."

Action: Error
Confirmation: "I couldn't complete that action. [helpful explanation]"
```

---

### Error Handling Requirements

**RULE**: ALL operations MUST handle errors gracefully with user-friendly messages.

#### Error Scenarios and Responses

1. **Task Not Found**:
   ```
   User: "Delete task 999"
   Agent: "I couldn't find task 999. Could you check the task number?"
   ```

2. **Invalid Input**:
   ```
   User: "Add a task with priority urgent"
   Agent: "Priority must be 'low', 'medium', or 'high'. Which would you like?"
   ```

3. **MCP Server Unavailable**:
   ```
   User: "Add a task to buy milk"
   Agent: "I'm unable to perform task operations right now. Please try again in a moment."
   ```

4. **Database Connection Failure**:
   ```
   Internal: Log full error with stack trace
   User: "I'm experiencing technical difficulties. Please try again shortly."
   ```

5. **Network Timeout**:
   ```
   User: "Show my tasks"
   Agent: "The request took too long. Please try again."
   ```

---

## Architecture Overview

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PHASE III ARCHITECTURE                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  User                                                               │
│   │                                                                 │
│   ├─► Phase II Routes (IMMUTABLE)                                  │
│   │    /dashboard, /tasks, /login, etc.                            │
│   │                                                                 │
│   └─► Phase III Route (NEW)                                        │
│        /chat                                                        │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         │ HTTP POST
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  FRONTEND (Next.js 15 + App Router)                                │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Phase III: /chat Route (NEW)                                 │ │
│  │  - ChatKit UI Components                                     │ │
│  │  - Message List & Input                                      │ │
│  │  - Conversation State (React Memory)                         │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Phase II: Dashboard, Tasks, Auth (IMMUTABLE)                 │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         │ POST /api/{user_id}/chat
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  BACKEND (FastAPI + SQLModel)                                      │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Phase III: Chat API Endpoint (NEW)                           │ │
│  │  POST /api/{user_id}/chat                                    │ │
│  │                                                               │ │
│  │  7-Step Pipeline:                                            │ │
│  │  1. Receive user message                                     │ │
│  │  2. Load conversation history ◄────────┐                     │ │
│  │  3. Persist user message ──────────────┤                     │ │
│  │  4. Invoke AI Agent ─────────┐         │                     │ │
│  │  5. Execute MCP Tools ────────┼────┐    │                     │ │
│  │  6. Persist assistant msg ────┼────┼────┘                     │ │
│  │  7. Return response           │    │                          │ │
│  └───────────────────────────────┼────┼──────────────────────────┘ │
│                                  │    │                            │
│  ┌──────────────────────────────┼────┼──────────────────────────┐ │
│  │ AI Agent Logic (NEW)         │    │                          │ │
│  │  - Intent Parser      ◄──────┘    │                          │ │
│  │  - Tool Selector                  │                          │ │
│  │  - Orchestrator ──────────────────┼───┐                      │ │
│  │  - Response Formatter             │   │                      │ │
│  └───────────────────────────────────┼───┼──────────────────────┘ │
│                                      │   │                        │
│  ┌──────────────────────────────────┼───┼──────────────────────┐ │
│  │ Phase II APIs (IMMUTABLE)        │   │                      │ │
│  │  /api/tasks, /api/auth, etc.     │   │                      │ │
│  └──────────────────────────────────┼───┼──────────────────────┘ │
└─────────────────────────────────────┼───┼────────────────────────┘
                                      │   │
                                      │   │ MCP Protocol
                                      │   ▼
┌─────────────────────────────────────┼──────────────────────────────┐
│  MCP SERVER (Independent Process)   │                              │
│                                     │                              │
│  ┌─────────────────────────────────┼──────────────────────────┐   │
│  │ MCP Tools (5 operations) ◄──────┘                          │   │
│  │  - add_task(user_id, title, ...)                           │   │
│  │  - list_tasks(user_id, filters...)                         │   │
│  │  - update_task(user_id, task_id, ...)                      │   │
│  │  - complete_task(user_id, task_id)                         │   │
│  │  - delete_task(user_id, task_id)                           │   │
│  │                                                             │   │
│  │  Stateless: NO in-memory state                             │   │
│  └─────────────────────────────────┬────────────────────────────┘   │
└─────────────────────────────────────┼────────────────────────────────┘
                                      │
                                      │ SQLModel Queries
                                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│  DATABASE (Neon PostgreSQL)                                        │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Phase III Tables (NEW)                                       │ │
│  │  - conversations (id, user_id, created_at, updated_at)       │ │
│  │  - messages (id, conversation_id, role, content, tool_calls) │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Phase II Tables (IMMUTABLE - Read by MCP)                    │ │
│  │  - tasks (id, title, description, completed, user_id, ...)   │ │
│  │  - users (id, email, name, ...)                              │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Stateless Flow Explanation

**Key Principle**: No server-side state; all state in database.

#### Request Flow (Example: Add Task)

```
1. User types: "Add a task to buy groceries"
   │
   ├─► Frontend ChatKit sends: POST /api/user_123/chat
   │   { "message": "Add a task to buy groceries" }
   │
2. Chat API receives request
   │
   ├─► Load conversation history from DB (if exists)
   │
   ├─► Save user message to DB
   │   INSERT INTO messages (role='user', content='Add a task...')
   │
3. Invoke AI Agent
   │
   ├─► Intent Parser: "user wants to add a task"
   │
   ├─► Tool Selector: "use add_task tool"
   │
   ├─► Orchestrator: prepare tool call
   │
4. Execute MCP Tool
   │
   ├─► MCP Client calls: add_task(user_id='123', title='Buy groceries')
   │
   ├─► MCP Server queries DB:
   │   INSERT INTO tasks (title='Buy groceries', user_id=123)
   │
   ├─► MCP Server returns: {"id": 42, "title": "Buy groceries", ...}
   │
5. Format Response
   │
   ├─► Response Formatter: "I've added the task 'Buy groceries' for you."
   │
6. Save Assistant Message
   │
   ├─► INSERT INTO messages (role='assistant', content='I've added...',
   │                          tool_calls=[...])
   │
7. Return to User
   │
   └─► { "response": "I've added the task...", "tool_calls": [...] }
```

#### Why Stateless?

- **Horizontal Scaling**: Add more server instances without session management
- **Reliability**: Server crashes don't lose conversation state
- **Simplicity**: No distributed cache or session synchronization
- **Cost Efficiency**: No memory overhead for session storage

---

## Agents and Responsibilities

### Agent 1: MCP Server Builder Agent

**Skill File**: `.claude/skills/mcp-server-builder-skill.md`

#### Responsibilities

1. **Create MCP Server Structure**:
   - Initialize MCP server in `backend/mcp_server/`
   - Configure Official MCP SDK
   - Set up database connection (reuse Phase II connection string)
   - Implement independent startup capability

2. **Implement 5 MCP Tools**:
   - `add_task`: Create new task with optional metadata
   - `list_tasks`: Retrieve tasks with optional filters
   - `update_task`: Modify existing task fields
   - `complete_task`: Mark task as done
   - `delete_task`: Remove task permanently

3. **Ensure Stateless Design**:
   - Zero in-memory state
   - Database as single source of truth
   - Pure functions: inputs → DB operation → outputs

4. **Implement Error Handling**:
   - Validation errors (400-level)
   - Business logic errors (404, 403)
   - System errors (500-level)

5. **Provide Documentation**:
   - README with startup instructions
   - Tool reference (inputs, outputs, errors)
   - Environment variables

#### Allowed Scope

**Full Write Access**:
```
backend/mcp_server/
├── __init__.py
├── main.py
├── tools/
│   ├── __init__.py
│   ├── task_tools.py
│   └── utils.py
├── config.py
├── requirements.txt
└── README.md
```

**Read-Only Access**:
```
backend/src/models/task.py     # Import Task model
backend/src/models/user.py     # Import User model
backend/.env                   # Read DATABASE_URL
```

**FORBIDDEN**:
```
backend/src/api/               # Phase II APIs
backend/src/services/          # Phase II business logic
backend/src/schemas/           # Phase II schemas
frontend/                      # Frontend code
```

#### Database Models

**Direct Access** (Read/Write via SQLModel):
- **Task**: `id`, `title`, `description`, `completed`, `priority`, `due_date`, `tags`, `user_id`, `created_at`, `updated_at`
- **User** (Read-Only): `id`, `email`, `name` (for validation)

**Constraint**: ALL queries MUST filter by `user_id` for data isolation.

#### Restrictions

**MUST NOT**:
- Modify Phase II code in `backend/src/`
- Implement AI logic or frontend UI
- Use in-memory caching or sessions
- Hardcode secrets or database URLs
- Allow cross-user data access
- Modify database schema (use existing Task model)

**MUST DO**:
- Accept `user_id` as first parameter in all tools
- Return standardized error responses
- Use type hints on all functions
- Implement comprehensive docstrings
- Start independently: `python backend/mcp_server/main.py`

#### Success Criteria

- [ ] All 5 MCP tools implemented with exact signatures
- [ ] MCP server starts independently
- [ ] All tools successfully query/modify database
- [ ] User data isolation enforced (no cross-user access)
- [ ] Error handling covers all three tiers
- [ ] Phase II code untouched (verify with git diff)
- [ ] Documentation complete (README, tool reference)

---

### Agent 2: Chat + MCP Bridge Agent

**Skill File**: `.claude/skills/chat-mcp-bridge-skill.md`

#### Responsibilities

1. **Implement Chat API Endpoint**:
   - Route: `POST /api/{user_id}/chat`
   - FastAPI router with Pydantic schemas
   - Request/response validation
   - Authentication enforcement (if applicable)

2. **Execute 7-Step Pipeline**:
   - Receive user message
   - Load conversation history from database
   - Persist user message
   - Invoke AI agent logic
   - Execute MCP tools via client
   - Persist assistant response
   - Return response to frontend

3. **Manage Conversation Persistence**:
   - Create/update Conversation records
   - Store Message records with roles and tool_calls
   - Maintain message ordering (timestamp ASC)

4. **Integrate MCP Client**:
   - Abstract MCP communication
   - Implement retry logic and timeouts
   - Parse and validate tool responses

5. **Handle Errors Gracefully**:
   - Database connection failures (503)
   - MCP server unavailable (503)
   - Agent logic errors (500)
   - Invalid input (400)

#### Allowed Scope

**Full Write Access**:
```
backend/phase3/
├── __init__.py
├── routers/
│   ├── __init__.py
│   └── chat.py
├── services/
│   ├── __init__.py
│   ├── chat_orchestrator.py
│   └── mcp_client.py
├── models/
│   ├── __init__.py
│   ├── conversation.py
│   └── message.py
├── schemas/
│   ├── __init__.py
│   └── chat.py
└── config.py

backend/alembic/versions/
└── xxxx_add_chat_tables.py    # Migration
```

**Read-Only Access**:
```
backend/src/models/user.py     # Import for validation
backend/src/auth/              # Import auth dependencies
backend/mcp_server/            # Understand tool signatures
```

**FORBIDDEN**:
```
backend/src/api/               # Phase II APIs
backend/src/services/          # Phase II services
backend/src/schemas/           # Phase II schemas
frontend/                      # Frontend code
```

#### Database Models

**Create New Models**:

1. **Conversation**:
   ```python
   class Conversation(SQLModel, table=True):
       id: str = Field(primary_key=True)
       user_id: int = Field(foreign_key="user.id")
       created_at: datetime
       updated_at: datetime
   ```

2. **Message**:
   ```python
   class Message(SQLModel, table=True):
       id: str = Field(primary_key=True)
       conversation_id: str = Field(foreign_key="conversations.id")
       role: str  # "user" or "assistant"
       content: str
       tool_calls: dict | None = Field(sa_column=Column(JSON))
       created_at: datetime
   ```

**Use Existing Models** (Read-Only):
- **User**: Validate user exists

#### Restrictions

**MUST NOT**:
- Modify Phase II code
- Implement AI logic (delegate to AI Agent)
- Implement frontend UI
- Call database directly for task operations (use MCP tools)
- Use in-memory session storage
- Expose stack traces to users

**MUST DO**:
- Use database transactions for atomic operations
- Implement all 7 pipeline steps
- Invoke MCP tools for ALL task operations
- Persist conversation and message history
- Return standardized response format
- Handle all error scenarios

#### Success Criteria

- [ ] POST `/api/{user_id}/chat` endpoint responds correctly
- [ ] All 7 pipeline steps implemented
- [ ] Conversations and messages persisted in database
- [ ] MCP tools invoked successfully
- [ ] AI agent integrated (stub acceptable initially)
- [ ] Error handling complete (DB, MCP, agent failures)
- [ ] Phase II code untouched
- [ ] Unit and integration tests pass

---

### Agent 3: AI Agent Logic Agent (MCP Orchestrator)

**Skill File**: `.claude/skills/phase3-mcp-orchestrator-skill.md`

#### Responsibilities

1. **Parse Natural Language Intent**:
   - Extract user goals from messages
   - Identify intent category (add, list, update, complete, delete)
   - Extract parameters (task title, ID, filters, etc.)

2. **Select Appropriate MCP Tools**:
   - Map intent to specific tool(s)
   - Validate required parameters available
   - Determine tool execution order for multi-step operations

3. **Orchestrate Tool Chains**:
   - Execute single-tool operations
   - Coordinate multi-step tool sequences
   - Handle dependencies between tool calls
   - Limit chains to max 5 steps

4. **Detect and Handle Ambiguity**:
   - Identify missing required parameters
   - Recognize unclear or ambiguous requests
   - Generate clarifying questions
   - Present options when multiple interpretations exist

5. **Format Responses**:
   - Convert technical tool outputs to conversational language
   - Translate errors to user-friendly messages
   - Explain what actions were taken and why

6. **Integrate OpenAI Agents SDK**:
   - Configure agent with system prompts
   - Register MCP tools as callable functions
   - Process agent responses
   - Implement fallback behaviors

#### Allowed Scope

**Full Write Access**:
```
backend/phase3/agent/
├── __init__.py
├── intent_parser.py
├── tool_selector.py
├── orchestrator.py
├── response_formatter.py
├── agent_runner.py
├── tool_schemas.py
├── config.py
└── prompts/
    ├── system_prompt.txt
    └── tool_descriptions.json
```

**Read-Only Access**:
```
backend/mcp_server/tools/      # Understand tool signatures
backend/phase3/services/mcp_client.py  # MCP client interface
```

**FORBIDDEN**:
```
backend/src/models/            # NO direct database access
backend/src/api/               # Phase II APIs
frontend/                      # Frontend code
```

#### Database Models

**CRITICAL**: This agent MUST NEVER access database directly.

All data operations MUST go through MCP tools.

#### Restrictions

**MUST NOT**:
- Access database directly (import models, execute queries)
- Modify Phase II code
- Implement frontend UI or MCP server
- Assume user intent on ambiguous requests
- Hardcode tool names or parameters
- Proceed with destructive actions without confirmation
- Use in-memory state between invocations

**MUST DO**:
- Parse all 5 intent types (add, list, update, complete, delete)
- Ask clarifying questions for ambiguous requests
- Confirm destructive operations (delete)
- Translate tool outputs to conversational responses
- Handle tool execution errors gracefully
- Limit tool chains to prevent infinite loops
- Operate statelessly (receive conversation history from caller)

#### Success Criteria

- [ ] Intent parsing works for all 5 categories
- [ ] Tool selection logic implemented
- [ ] Multi-step orchestration functional
- [ ] Ambiguity detection triggers clarification
- [ ] Response formatting produces natural language
- [ ] OpenAI Agents SDK integrated
- [ ] NO direct database access (verified)
- [ ] Error handling complete
- [ ] Conversation context used correctly

---

### Agent 4: ChatKit Frontend Builder Agent

**Skill File**: `.claude/skills/chatkit-frontend-builder-skill.md`

#### Responsibilities

1. **Create Protected Chat Route**:
   - Implement `/chat` page under Next.js App Router
   - Apply Phase II authentication guards (reuse existing)
   - Redirect unauthenticated users to login

2. **Build ChatKit UI Components**:
   - `MessageList`: Display conversation history
   - `MessageInput`: User input field with send button
   - `LoadingIndicator`: Show during API calls
   - `ErrorDisplay`: User-friendly error messages
   - `EmptyState`: Initial state before first message

3. **Implement API Integration**:
   - Type-safe client for `POST /api/{user_id}/chat`
   - Handle network errors, timeouts, HTTP errors
   - Prevent duplicate sends (debounce/disable during request)

4. **Manage Conversation State**:
   - Store `conversation_id` in React state
   - Maintain message history in component state
   - Clear state on unmount (intentional, no persistence)

5. **Configure ChatKit Domain Allowlist**:
   - Read `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` from environment
   - Initialize ChatKit with domain key
   - Document environment variable setup

6. **Ensure Responsive Design**:
   - Mobile, tablet, desktop layouts
   - Auto-scroll to latest message
   - Accessible (keyboard navigation, screen reader support)

#### Allowed Scope

**Full Write Access**:
```
frontend/src/app/chat/
├── page.tsx
├── layout.tsx
└── components/
    ├── MessageList.tsx
    ├── MessageInput.tsx
    ├── LoadingIndicator.tsx
    ├── ErrorDisplay.tsx
    └── EmptyState.tsx

frontend/src/components/chat/   # Alternative location

frontend/src/lib/chat.ts        # API client
frontend/src/types/chat.ts      # Type definitions

frontend/.env.local             # Add NEXT_PUBLIC_OPENAI_DOMAIN_KEY
```

**Read-Only Access**:
```
frontend/src/app/               # Existing routing patterns
frontend/src/components/        # Reusable components
frontend/src/lib/api.ts         # Existing API patterns
frontend/src/lib/auth.ts        # Auth utilities (import only)
```

**FORBIDDEN**:
```
frontend/src/app/(auth)/        # Phase II auth pages
frontend/src/app/dashboard/     # Phase II dashboard
frontend/src/components/tasks/  # Phase II task components
backend/                        # Backend code
```

#### Database Models

**CRITICAL**: Frontend NEVER accesses database directly.

All backend communication via `POST /api/{user_id}/chat` endpoint.

#### Restrictions

**MUST NOT**:
- Modify any Phase II frontend files
- Implement AI logic or backend APIs
- Call MCP tools directly
- Use localStorage/sessionStorage for chat data
- Modify Phase II authentication code
- Add external UI libraries (use ChatKit only)
- Hardcode API keys or domain keys

**MUST DO**:
- Use OpenAI ChatKit components
- Protect `/chat` route with authentication
- Use TypeScript with strict types
- Handle all API error scenarios
- Implement responsive design
- Clear conversation state on refresh (intentional)
- Document domain key configuration

#### Success Criteria

- [ ] `/chat` route accessible and protected
- [ ] ChatKit UI integrated correctly
- [ ] User can send and receive messages
- [ ] Conversation history displays properly
- [ ] Auto-scroll works
- [ ] Loading states during API calls
- [ ] Error states with retry buttons
- [ ] Empty state before first message
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Accessible (keyboard, screen reader)
- [ ] Phase II code untouched (verify with git diff)
- [ ] Domain key configuration documented

---

## Agent Workflow

### Sequential Execution Order

Phase III agents MUST execute in this exact order:

```
Step 1: MCP Server Builder Agent
   │
   ├─► Creates MCP server in backend/mcp_server/
   ├─► Implements 5 MCP tools
   ├─► Self-test: MCP server starts, tools callable
   │
   └─► ✅ CHECKPOINT: MCP server functional

Step 2: Chat + MCP Bridge Agent
   │
   ├─► Creates chat API endpoint
   ├─► Implements conversation persistence
   ├─► Integrates MCP client
   ├─► Self-test: API responds, DB persists messages
   │
   └─► ✅ CHECKPOINT: Chat API functional

Step 3: AI Agent Logic Agent
   │
   ├─► Implements intent parsing
   ├─► Builds tool selection logic
   ├─► Creates orchestration layer
   ├─► Self-test: Intent → Tool mapping works
   │
   └─► ✅ CHECKPOINT: AI agent functional

Step 4: ChatKit Frontend Builder Agent
   │
   ├─► Creates /chat route
   ├─► Builds ChatKit UI
   ├─► Integrates with chat API
   ├─► Self-test: UI renders, API calls succeed
   │
   └─► ✅ CHECKPOINT: Chat UI functional

Final: Integration Testing
   │
   ├─► End-to-end test: User message → Chat UI → API → AI Agent → MCP → DB
   ├─► Verify conversation persistence
   ├─► Verify Phase II still works
   │
   └─► ✅ Phase III COMPLETE
```

### Checkpoint Requirements

Each agent MUST pass self-testing before next agent begins:

#### Checkpoint 1: MCP Server Functional
- [ ] MCP server starts: `python backend/mcp_server/main.py`
- [ ] All 5 tools registered and discoverable
- [ ] Test tool invocation: `add_task(user_id="test", title="Test Task")`
- [ ] Database query successful (verify task created)
- [ ] Error handling works (test invalid input)

#### Checkpoint 2: Chat API Functional
- [ ] Endpoint responds: `POST /api/test_user/chat`
- [ ] Conversation created in database
- [ ] User message persisted in database
- [ ] MCP tool invoked (verify with logs)
- [ ] Assistant message persisted in database
- [ ] Response returned with correct format

#### Checkpoint 3: AI Agent Functional
- [ ] Intent parsing: "Add a task" → `add_task` intent
- [ ] Tool selection: Intent → Correct MCP tool
- [ ] Parameter extraction: "Buy groceries" → `title="Buy groceries"`
- [ ] Ambiguity detection: "Add a task" (no title) → Clarification
- [ ] Response formatting: Tool result → Conversational response

#### Checkpoint 4: Chat UI Functional
- [ ] `/chat` route accessible (authenticated users only)
- [ ] ChatKit UI renders
- [ ] User can type and send message
- [ ] API call triggered on send
- [ ] Response displayed in message list
- [ ] Auto-scroll to latest message
- [ ] Error states work (test network failure)

---

### Skill Compliance Requirements

**RULE**: Agents MUST follow their skill definitions exactly.

#### Skill Adherence Verification

Before marking work complete, agents MUST verify:

1. **Scope Compliance**:
   - All created files within ALLOWED scope
   - No files created in FORBIDDEN scope
   - Phase II files unmodified

2. **Functionality Compliance**:
   - All responsibilities from skill file implemented
   - All inputs handled correctly
   - All outputs match expected format

3. **Restriction Compliance**:
   - All "MUST NOT" rules followed
   - All "MUST DO" requirements met
   - No violations of critical constraints

4. **Success Criteria Met**:
   - All functional success criteria pass
   - All quality success criteria pass
   - All integration success criteria pass

5. **Documentation Complete**:
   - All created files documented
   - Dependencies identified
   - Example usage provided

---

## Database & MCP Guidelines

### Stateless MCP Server Design

**Principle**: MCP server holds ZERO state in memory.

#### Stateless Patterns

**CORRECT**:
```python
async def list_tasks(user_id: str, status: str | None = None):
    # Read current state from database
    query = session.query(Task).filter(Task.user_id == user_id)
    if status:
        completed = (status == "complete")
        query = query.filter(Task.completed == completed)
    tasks = query.all()
    # Return current state
    return [task.dict() for task in tasks]
```

**INCORRECT**:
```python
# ❌ FORBIDDEN: In-memory cache
task_cache = {}

async def list_tasks(user_id: str, status: str | None = None):
    if user_id in task_cache:
        return task_cache[user_id]  # ❌ Stale data!
    # ...
```

#### Benefits of Stateless Design

1. **Horizontal Scaling**: Add MCP server instances without coordination
2. **Reliability**: Crash recovery is instantaneous (no lost state)
3. **Consistency**: Always read latest data from database
4. **Simplicity**: No cache invalidation, no distributed state

---

### SQLModel Schema Definitions

#### Phase III Models

**Conversation Model**:
```python
from sqlmodel import Field, SQLModel
from datetime import datetime

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(primary_key=True)  # e.g., "conv_abc123"
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "conv_abc123",
                "user_id": 1,
                "created_at": "2026-01-23T10:00:00Z",
                "updated_at": "2026-01-23T10:30:00Z"
            }
        }
```

**Message Model**:
```python
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import JSON
from datetime import datetime

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(primary_key=True)  # e.g., "msg_456"
    conversation_id: str = Field(foreign_key="conversations.id")
    role: str = Field()  # "user" or "assistant"
    content: str = Field()
    tool_calls: dict | None = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "msg_456",
                "conversation_id": "conv_abc123",
                "role": "assistant",
                "content": "I've added the task for you.",
                "tool_calls": [
                    {
                        "tool": "add_task",
                        "parameters": {"user_id": "123", "title": "Buy groceries"},
                        "result": {"id": 42, "title": "Buy groceries"}
                    }
                ],
                "created_at": "2026-01-23T10:30:01Z"
            }
        }
```

#### Database Migration

**Alembic Migration for Phase III Tables**:
```python
"""Add Phase III chat tables

Revision ID: xxxx
Revises: yyyy
Create Date: 2026-01-23

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('conversation_id', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('tool_calls', JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for performance
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])

def downgrade():
    op.drop_table('messages')
    op.drop_table('conversations')
```

---

### MCP Tool Specification (Exact)

All MCP tools MUST match these signatures exactly.

#### Tool 1: add_task

```python
async def add_task(
    user_id: str,
    title: str,
    description: str | None = None,
    priority: str | None = None,  # "low" | "medium" | "high"
    due_date: str | None = None,  # ISO 8601 format
    tags: list[str] | None = None
) -> dict:
    """
    Create a new task for the user.

    Args:
        user_id: Authenticated user identifier
        title: Task title (1-200 characters, required)
        description: Optional task description
        priority: Optional priority level
        due_date: Optional due date in ISO 8601 format
        tags: Optional list of tags

    Returns:
        dict: Created task with all fields

    Raises:
        ValidationError: If title is missing or invalid
        InternalError: If database operation fails
    """
    # Implementation...
```

**Example**:
```python
# Input
add_task(
    user_id="user_123",
    title="Buy groceries",
    priority="high",
    tags=["shopping", "urgent"]
)

# Output
{
    "id": 42,
    "title": "Buy groceries",
    "description": None,
    "completed": False,
    "priority": "high",
    "due_date": None,
    "tags": ["shopping", "urgent"],
    "user_id": "user_123",
    "created_at": "2026-01-23T10:30:00Z",
    "updated_at": "2026-01-23T10:30:00Z"
}
```

#### Tool 2: list_tasks

```python
async def list_tasks(
    user_id: str,
    status: str | None = None,      # "complete" | "incomplete"
    priority: str | None = None,    # "low" | "medium" | "high"
    tag: str | None = None
) -> list[dict]:
    """
    List tasks for the user with optional filters.

    Args:
        user_id: Authenticated user identifier
        status: Filter by completion status
        priority: Filter by priority level
        tag: Filter by tag

    Returns:
        list[dict]: List of matching tasks

    Raises:
        ValidationError: If filter values are invalid
        InternalError: If database operation fails
    """
    # Implementation...
```

**Example**:
```python
# Input
list_tasks(user_id="user_123", status="incomplete", priority="high")

# Output
[
    {
        "id": 42,
        "title": "Buy groceries",
        "completed": False,
        "priority": "high",
        # ... other fields
    },
    {
        "id": 43,
        "title": "Finish report",
        "completed": False,
        "priority": "high",
        # ... other fields
    }
]
```

#### Tool 3: update_task

```python
async def update_task(
    user_id: str,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    due_date: str | None = None,
    tags: list[str] | None = None
) -> dict:
    """
    Update fields of an existing task.

    Args:
        user_id: Authenticated user identifier
        task_id: ID of task to update
        title: New title (optional)
        description: New description (optional)
        priority: New priority (optional)
        due_date: New due date (optional)
        tags: New tags (optional)

    Returns:
        dict: Updated task with all fields

    Raises:
        NotFoundError: If task doesn't exist or user doesn't own it
        ValidationError: If update values are invalid
        InternalError: If database operation fails
    """
    # Implementation...
```

#### Tool 4: complete_task

```python
async def complete_task(
    user_id: str,
    task_id: int
) -> dict:
    """
    Mark a task as complete.

    Args:
        user_id: Authenticated user identifier
        task_id: ID of task to complete

    Returns:
        dict: Updated task with completed=True

    Raises:
        NotFoundError: If task doesn't exist or user doesn't own it
        InternalError: If database operation fails
    """
    # Implementation...
```

#### Tool 5: delete_task

```python
async def delete_task(
    user_id: str,
    task_id: int
) -> dict:
    """
    Permanently delete a task.

    Args:
        user_id: Authenticated user identifier
        task_id: ID of task to delete

    Returns:
        dict: Confirmation message with task_id

    Raises:
        NotFoundError: If task doesn't exist or user doesn't own it
        InternalError: If database operation fails
    """
    # Implementation...
```

**Example**:
```python
# Input
delete_task(user_id="user_123", task_id=42)

# Output
{
    "message": "Task deleted successfully",
    "task_id": 42
}
```

---

## Frontend ChatKit Guidelines

### Protected Route Implementation

**Route**: `/chat`

**Protection Mechanism**:
```typescript
// frontend/src/app/chat/page.tsx
'use client';

import { useAuth } from '@/lib/auth';  // Phase II auth hook
import { redirect } from 'next/navigation';

export default function ChatPage() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!user) {
    redirect('/login');  // Redirect to Phase II login
    return null;
  }

  return <ChatInterface user={user} />;
}
```

---

### ChatKit UI Components

#### Component: MessageList

**Purpose**: Display conversation history with role differentiation.

**Implementation**:
```typescript
interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  tool_calls?: any[];
}

export function MessageList({ messages }: { messages: Message[] }) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="message-list">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`message ${message.role}`}
        >
          <div className="message-content">{message.content}</div>
          <div className="message-timestamp">{message.timestamp}</div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}
```

#### Component: MessageInput

**Purpose**: User input field with send button.

**Implementation**:
```typescript
export function MessageInput({
  onSend,
  disabled
}: {
  onSend: (message: string) => void;
  disabled: boolean;
}) {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="message-input">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type a message..."
        disabled={disabled}
      />
      <button onClick={handleSend} disabled={disabled || !input.trim()}>
        Send
      </button>
    </div>
  );
}
```

#### Component: LoadingIndicator

**Purpose**: Show during API calls.

```typescript
export function LoadingIndicator() {
  return (
    <div className="loading-indicator">
      <div className="spinner" />
      <span>Thinking...</span>
    </div>
  );
}
```

#### Component: ErrorDisplay

**Purpose**: User-friendly error messages.

```typescript
export function ErrorDisplay({
  error,
  onRetry
}: {
  error: { message: string };
  onRetry: () => void;
}) {
  return (
    <div className="error-display">
      <p>⚠️ {error.message}</p>
      <button onClick={onRetry}>Retry</button>
    </div>
  );
}
```

#### Component: EmptyState

**Purpose**: Initial state before first message.

```typescript
export function EmptyState() {
  return (
    <div className="empty-state">
      <h2>💬 Start a conversation</h2>
      <p>Ask me to add tasks, view your tasks, or manage your to-do list.</p>
      <div className="example-prompts">
        <button>"Add a task to buy groceries"</button>
        <button>"Show my tasks"</button>
        <button>"Mark task 5 as complete"</button>
      </div>
    </div>
  );
}
```

---

### Domain Allowlist Configuration

**Environment Variable**:
```bash
# frontend/.env.local
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-production-domain-key
```

**ChatKit Initialization**:
```typescript
import { ChatKit } from '@openai/chatkit';

const chatKit = new ChatKit({
  domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,
  // ... other configuration
});
```

**Documentation** (in README):
```markdown
## ChatKit Domain Configuration

For production deployment, you must configure the OpenAI domain allowlist:

1. Obtain domain key from OpenAI ChatKit dashboard
2. Add to `.env.local`:
   ```
   NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-key-here
   ```
3. Restart Next.js development server

For Vercel deployment:
- Add environment variable in Vercel dashboard
- Redeploy application
```

---

## Error Handling & Testing

### Graceful Error Handling Requirements

#### Error Scenario 1: Task Not Found

**Trigger**: User requests operation on non-existent task.

**Flow**:
```
User: "Delete task 999"
  ↓
AI Agent: Selects delete_task(task_id=999)
  ↓
MCP Tool: Returns NotFoundError
  ↓
AI Agent: Formats error response
  ↓
User: "I couldn't find task 999. Could you check the task number and try again?"
```

**Implementation**:
```python
# MCP Tool
try:
    task = session.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()
    if not task:
        raise NotFoundError(f"Task {task_id} not found")
except NotFoundError as e:
    return {
        "error": "Task not found",
        "code": "TASK_NOT_FOUND",
        "task_id": task_id,
        "user_id": user_id
    }
```

#### Error Scenario 2: Conversation Not Found

**Trigger**: User provides invalid conversation_id.

**Flow**:
```
POST /api/user_123/chat
{
  "message": "Show my tasks",
  "conversation_id": "conv_invalid"
}
  ↓
Chat API: Load conversation → Not found
  ↓
Chat API: Create new conversation (fallback)
  ↓
User: (New conversation started, previous history lost)
```

**Implementation**:
```python
conversation = session.query(Conversation).filter(
    Conversation.id == conversation_id,
    Conversation.user_id == user_id
).first()

if not conversation:
    # Fallback: Create new conversation
    conversation = Conversation(
        id=generate_conversation_id(),
        user_id=user_id
    )
    session.add(conversation)
    session.commit()
```

#### Error Scenario 3: Invalid Tool Input

**Trigger**: MCP tool receives invalid parameters.

**Flow**:
```
User: "Add a task with priority urgent"
  ↓
AI Agent: Extracts priority="urgent" (invalid)
  ↓
MCP Tool: Validates priority → Error
  ↓
AI Agent: Detects validation error
  ↓
User: "Priority must be 'low', 'medium', or 'high'. Which would you like?"
```

**Implementation**:
```python
VALID_PRIORITIES = ["low", "medium", "high"]

if priority and priority not in VALID_PRIORITIES:
    return {
        "error": "Invalid priority",
        "code": "INVALID_INPUT",
        "details": f"Priority must be one of: {', '.join(VALID_PRIORITIES)}"
    }
```

#### Error Scenario 4: Network Errors

**Trigger**: Frontend cannot reach backend API.

**Flow**:
```
User: Sends message
  ↓
Frontend: POST /api/user_123/chat → Timeout
  ↓
Frontend: Displays error
  ↓
User: "⚠️ Unable to connect. Please check your connection and try again. [Retry]"
```

**Implementation**:
```typescript
try {
  const response = await fetch(`/api/${userId}/chat`, {
    method: 'POST',
    body: JSON.stringify({ message }),
    signal: AbortSignal.timeout(10000)  // 10s timeout
  });
  // ...
} catch (error) {
  if (error.name === 'AbortError') {
    setError({
      message: 'Unable to connect. Please check your connection and try again.',
      retryable: true
    });
  }
}
```

---

### Confirmation Message Templates

**Add Task Success**:
```
User: "Add a task to buy groceries"
Agent: "I've added the task 'Buy groceries' for you."
```

**List Tasks Success**:
```
User: "Show my tasks"
Agent: "You have 3 tasks:
1. Buy groceries (high priority, incomplete)
2. Finish report (medium priority, incomplete)
3. Call dentist (low priority, complete)"
```

**Update Task Success**:
```
User: "Change task 5 to high priority"
Agent: "I've updated task 5 to high priority."
```

**Complete Task Success**:
```
User: "Mark task 3 as done"
Agent: "Task 3 is now marked as complete."
```

**Delete Task Success**:
```
User: "Delete task 7"
Agent: "Task 7 has been deleted."
```

---

### End-to-End Testing Strategy

#### Test Case 1: Complete Chat Flow

**Objective**: Verify entire chat pipeline from UI to database.

**Steps**:
1. Open `/chat` page (authenticated)
2. Type: "Add a task to buy milk"
3. Click Send
4. Verify loading indicator appears
5. Verify message appears in UI: "I've added the task 'Buy milk' for you."
6. Verify database: Task with title "Buy milk" exists
7. Verify database: Conversation and messages created

**Expected Results**:
- [ ] Frontend displays user message
- [ ] Frontend displays assistant response
- [ ] Database contains new task
- [ ] Database contains conversation record
- [ ] Database contains 2 message records (user + assistant)
- [ ] Assistant message includes tool_calls metadata

#### Test Case 2: Multi-Step Conversation

**Objective**: Verify conversation continuity.

**Steps**:
1. Send: "Add a task to buy groceries"
2. Wait for response
3. Send: "Make it high priority"
4. Verify AI agent uses context to identify task

**Expected Results**:
- [ ] Second message updates the correct task (from first message)
- [ ] AI agent resolves "it" to task ID from previous context
- [ ] Conversation history maintained in database

#### Test Case 3: Error Recovery

**Objective**: Verify graceful error handling.

**Steps**:
1. Stop MCP server
2. Send: "Add a task"
3. Verify error message displayed
4. Start MCP server
5. Click Retry
6. Verify success

**Expected Results**:
- [ ] Error message: "Task operations unavailable"
- [ ] Retry button appears
- [ ] After retry: Task created successfully

#### Test Case 4: Phase II Regression

**Objective**: Ensure Phase II still works.

**Steps**:
1. Navigate to `/dashboard`
2. Verify dashboard loads
3. Create task via Phase II UI
4. Navigate to `/chat`
5. Send: "Show my tasks"
6. Verify task from Phase II appears in list

**Expected Results**:
- [ ] Phase II dashboard functional
- [ ] Phase II task creation works
- [ ] Phase III chat can see Phase II tasks
- [ ] No errors or regressions in Phase II

---

## Phase II Protection Clause (Enforcement)

### Immutability Verification

**Before ANY merge to main**:

1. **Git Diff Check**:
   ```bash
   # Verify no Phase II files modified
   git diff main --name-only | grep -E '^(backend/src|frontend/src/app/(auth|dashboard)|frontend/src/components/tasks)'
   # Should return empty (exit code 1)
   ```

2. **Automated CI Check**:
   ```yaml
   # .github/workflows/phase-ii-protection.yml
   name: Phase II Protection
   on: [pull_request]
   jobs:
     verify-phase-ii:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Check Phase II files
           run: |
             PHASE_II_FILES=$(git diff origin/main --name-only | grep -E '^(backend/src|frontend/src/app/(auth|dashboard)|frontend/src/components/tasks)' || true)
             if [ -n "$PHASE_II_FILES" ]; then
               echo "ERROR: Phase II files modified:"
               echo "$PHASE_II_FILES"
               exit 1
             fi
   ```

3. **Manual Code Review Checklist**:
   - [ ] No files in `backend/src/` modified
   - [ ] No files in `frontend/src/app/(auth)/` modified
   - [ ] No files in `frontend/src/app/dashboard/` modified
   - [ ] No files in `frontend/src/components/tasks/` modified
   - [ ] All new files in Phase III directories only

---

### Coexistence Requirements

Phase III MUST coexist with Phase II:

1. **Separate Routes**:
   - Phase II: `/`, `/login`, `/register`, `/dashboard`, `/tasks`
   - Phase III: `/chat`
   - No route conflicts

2. **Separate Backend Endpoints**:
   - Phase II: `/api/tasks/*`, `/api/auth/*`, `/api/users/*`
   - Phase III: `/api/{user_id}/chat`
   - No endpoint conflicts

3. **Shared Database**:
   - Phase II tables: `tasks`, `users` (READ-ONLY by Phase III MCP)
   - Phase III tables: `conversations`, `messages` (NEW)
   - No schema conflicts

4. **Shared Authentication**:
   - Phase II: Better Auth (IMMUTABLE)
   - Phase III: Reuse Phase II auth (import only)
   - No auth conflicts

---

## Deliverables & Success Criteria

### Deliverables

1. **MCP Server** (`backend/mcp_server/`):
   - [ ] Standalone MCP server implementation
   - [ ] 5 MCP tools: add_task, list_tasks, update_task, complete_task, delete_task
   - [ ] Independent startup script
   - [ ] README with usage instructions
   - [ ] Tool reference documentation

2. **Chat API** (`backend/phase3/`):
   - [ ] POST `/api/{user_id}/chat` endpoint
   - [ ] Conversation and Message models
   - [ ] MCP client integration
   - [ ] 7-step pipeline implementation
   - [ ] Database migration for chat tables

3. **AI Agent Logic** (`backend/phase3/agent/`):
   - [ ] Intent parser
   - [ ] Tool selector
   - [ ] Orchestrator
   - [ ] Response formatter
   - [ ] OpenAI Agents SDK integration

4. **ChatKit Frontend** (`frontend/src/app/chat/`):
   - [ ] `/chat` protected route
   - [ ] ChatKit UI components
   - [ ] Chat API client
   - [ ] Conversation state management
   - [ ] Domain key configuration

5. **Database Schema**:
   - [ ] `conversations` table
   - [ ] `messages` table
   - [ ] Alembic migration scripts
   - [ ] Indexes for performance

6. **Documentation**:
   - [ ] Phase III README
   - [ ] MCP server documentation
   - [ ] Chat API documentation
   - [ ] Frontend integration guide
   - [ ] Environment variables guide

---

### Success Criteria (Phase III Complete)

#### Functional Completeness

- [ ] User can access `/chat` page (authenticated users only)
- [ ] User can send messages to chatbot
- [ ] Chatbot understands natural language requests
- [ ] Chatbot successfully executes task operations via MCP tools
- [ ] Chatbot confirms actions with friendly messages
- [ ] Conversation history persists across page refreshes
- [ ] All 5 MCP tools functional (add, list, update, complete, delete)

#### Integration Success

- [ ] Frontend ChatKit → Chat API → AI Agent → MCP Server → Database (full flow works)
- [ ] Conversation and message records created in database
- [ ] Tool execution metadata stored in messages
- [ ] Phase II dashboard still functional
- [ ] Phase II task CRUD still functional
- [ ] Phase II authentication still functional

#### Quality Standards

- [ ] All 4 agents followed their skill definitions
- [ ] All agents passed self-testing checkpoints
- [ ] No Phase II code modified (verified with git diff)
- [ ] All error scenarios handled gracefully
- [ ] Confirmation messages for all successful actions
- [ ] User-friendly error messages (no technical jargon)

#### Performance Standards

- [ ] Chat API response time < 2s (without tool calls)
- [ ] Chat API response time < 5s (with MCP tool execution)
- [ ] Database queries optimized (indexed foreign keys)
- [ ] No memory leaks (stateless architecture)

#### Security Standards

- [ ] `/chat` route protected by authentication
- [ ] User can only access own conversations
- [ ] User can only see own tasks (via MCP tools)
- [ ] No cross-user data access
- [ ] No hardcoded secrets in code
- [ ] Environment variables used for all configuration

#### Documentation Standards

- [ ] README explains how to start MCP server
- [ ] README explains how to access chat feature
- [ ] Environment variables documented (`.env.example`)
- [ ] API contracts documented (request/response formats)
- [ ] Tool signatures documented (MCP tools)

---

## Final Enforcement Note

### Constitution Authority

This Phase III Constitution is the **supreme governing document** for all Phase III development.

**Any work that violates this constitution is INVALID and MUST be rejected.**

### Enforcement Mechanisms

1. **Agent Skills**: Agents MUST follow their skill files exactly
2. **Code Review**: All PRs MUST pass constitution compliance checks
3. **Automated CI**: Phase II protection checks MUST pass
4. **Self-Testing**: Agents MUST verify their work before completion
5. **Manual Verification**: Human review MUST confirm compliance

### Violation Consequences

- **Phase II Modification**: IMMEDIATE REJECTION, revert changes
- **Agent Skill Violation**: REJECT work, re-execute with correct agent
- **Missing Error Handling**: BLOCK merge until fixed
- **Hardcoded Secrets**: IMMEDIATE REJECTION, security review
- **Missing Documentation**: BLOCK merge until documented

### Amendment Process

This constitution can be amended with:
1. **Documented justification** (ADR explaining why change needed)
2. **User approval** (explicit consent)
3. **Version increment** (follow semantic versioning)
4. **Template propagation** (update dependent files)
5. **Agent coordination** (ensure agents align with new rules)

### Semantic Versioning

- **MAJOR** (X.0.0): Backward-incompatible changes (e.g., removing agents, changing architecture)
- **MINOR** (0.X.0): New agents, new sections, material expansions
- **PATCH** (0.0.X): Clarifications, typos, non-semantic refinements

---

**Version**: 3.0.0
**Ratified**: 2026-01-23
**Last Amended**: 2026-01-23
**Supersedes**: 2.0.0 (Phase II - Full-Stack Web Application)
**Authority**: Phase III AI Chatbot Development Team
