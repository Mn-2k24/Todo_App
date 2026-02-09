# Implementation Plan: Phase III - AI Chatbot with MCP Server

**Branch**: `004-phase-iii-chatbot` | **Date**: 2026-01-23 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-phase-iii-chatbot/spec.md`

## Summary

Phase III extends the Todo Full-Stack Web Application with an AI-powered chatbot that enables users to manage tasks through natural language conversations. The system uses a stateless backend architecture where:
- **Google Gemini Flash 2.5** handles LLM interactions (NO OpenAI)
- **Custom AI Agent Logic** parses natural language and selects MCP tools
- **MCP Server** exposes 5 stateless task management tools (add_task, list_tasks, update_task, complete_task, delete_task)
- **Chat API** orchestrates conversation persistence, AI invocation, and MCP tool execution
- **OpenAI ChatKit** provides the frontend UI (UI framework only, NOT for LLM)

The architecture is fully stateless with all conversation state persisted in Neon PostgreSQL. Phase II code remains completely untouched.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5+ (frontend), Node.js 20+ (frontend runtime)

**Primary Dependencies**:
- Backend:
  - FastAPI (existing from Phase II)
  - SQLModel (existing from Phase II)
  - Google Generative AI SDK (`google-generativeai` for Gemini Flash 2.5)
  - Official MCP SDK (`@modelcontextprotocol/sdk` or Python equivalent)
  - Pydantic (existing from Phase II)
- Frontend:
  - Next.js 15+ (existing from Phase II)
  - OpenAI ChatKit (`@openai/chatkit` - UI components only)
  - React 19+ (existing from Phase II)
  - Tailwind CSS (existing from Phase II)

**Storage**: Neon PostgreSQL (existing from Phase II) - Add 2 new tables: `conversations`, `messages`

**Testing**:
- Backend: pytest (existing from Phase II)
- Frontend: Jest + React Testing Library (existing from Phase II)
- E2E: Playwright or Cypress
- LLM Testing: Mock Gemini responses for deterministic tests

**Target Platform**:
- Backend: Linux server (Railway/Render deployment)
- Frontend: Vercel Edge Runtime
- Database: Neon Serverless PostgreSQL

**Project Type**: Web application (existing monorepo structure: frontend/ + backend/)

**Performance Goals**:
- Chat API response time: <3s (p95) including Gemini API latency
- MCP tool execution: <500ms (p95)
- Database queries: <100ms (p95)
- Frontend chat UI: 60 FPS, <100ms input lag
- Concurrent users: Support 50 simultaneous chat requests

**Constraints**:
- Phase II code MUST NOT be modified (zero regression requirement)
- Stateless architecture (no in-memory session state)
- Gemini Flash 2.5 only (NO model switching)
- NO OpenAI API usage (Gemini only)
- User data isolation (all queries filtered by user_id)
- JWT authentication (reuse Phase II Better Auth)
- Conversation history window: Last 10 messages max

**Scale/Scope**:
- 5 MCP tools (add_task, list_tasks, update_task, complete_task, delete_task)
- 5 agents (MCP Server, Chat API, AI Agent Logic, ChatKit Frontend, Gemini LLM Controller)
- 2 new database models (Conversation, Message)
- 1 new API endpoint (POST /api/{user_id}/chat)
- 1 new frontend route (/chat)
- 5 frontend components (MessageList, MessageInput, LoadingIndicator, ErrorDisplay, EmptyState)
- 7 natural language intents (CREATE_TASK, LIST_TASKS, UPDATE_TASK, COMPLETE_TASK, DELETE_TASK, CLARIFICATION, OUT_OF_SCOPE)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase II Protection ✅ PASS
- **Requirement**: Phase II code MUST NOT be modified
- **Validation**: All Phase III code in new directories (`backend/phase3/`, `backend/mcp_server/`, `frontend/src/app/chat/`, `frontend/src/components/chat/`)
- **Enforcement**: Git diff before merge must show zero changes to Phase II paths

### Stateless Architecture ✅ PASS
- **Requirement**: Backend must be horizontally scalable with no in-memory state
- **Validation**: All state in database, no global variables, no session caches
- **Enforcement**: Architecture review before implementation

### User Data Isolation ✅ PASS
- **Requirement**: Users can only access their own data
- **Validation**: All database queries filter by user_id, JWT auth enforced
- **Enforcement**: Security review + integration tests

### Agent-Based Development ✅ PASS
- **Requirement**: All code generated via agents and skills
- **Validation**: 5 agent skills defined in `.claude/skills/`
- **Enforcement**: Code review ensures agent boundaries respected

### Type Safety ✅ PASS
- **Requirement**: TypeScript strict mode (frontend), Python type hints (backend)
- **Validation**: No `any` types, all functions typed
- **Enforcement**: TypeScript compiler + mypy checks

### Testing ✅ PASS
- **Requirement**: >80% test coverage for Phase III code
- **Validation**: Unit tests per agent, integration tests, E2E tests
- **Enforcement**: CI/CD pipeline blocks merge if coverage <80%

### LLM Provider ✅ PASS
- **Requirement**: Google Gemini Flash 2.5 only (NO OpenAI)
- **Validation**: No OpenAI dependencies in package.json or requirements.txt
- **Enforcement**: Code review + dependency audit

### Security ✅ PASS
- **Requirement**: API keys in environment variables, no hardcoded secrets
- **Validation**: `.env` in `.gitignore`, secrets documented in deployment guide
- **Enforcement**: Pre-commit hooks scan for hardcoded secrets

## Project Structure

### Documentation (this feature)

```text
specs/004-phase-iii-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (dependencies, best practices, patterns)
├── data-model.md        # Phase 1 output (database schemas for Conversation, Message)
├── quickstart.md        # Phase 1 output (setup instructions for Phase III)
├── contracts/           # Phase 1 output (API contracts, MCP tool signatures)
│   ├── chat-api.yaml        # POST /api/{user_id}/chat OpenAPI spec
│   ├── mcp-tools.json       # MCP tool definitions (5 tools)
│   └── gemini-api.md        # Gemini API integration contract
├── checklists/          # Quality validation checklists
│   └── requirements.md      # Spec quality checklist (already created)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── phase3/                       # NEW - Phase III backend code
│   ├── __init__.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── chat.py              # POST /api/{user_id}/chat endpoint
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py      # 7-step chat pipeline logic
│   │   └── mcp_client.py        # MCP client wrapper
│   ├── models/
│   │   ├── __init__.py
│   │   ├── conversation.py      # Conversation SQLModel
│   │   └── message.py           # Message SQLModel
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── chat_schema.py       # Pydantic request/response schemas
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── orchestrator.py      # AI Agent Logic (intent parsing, tool selection)
│   │   └── prompts.py           # System prompts for AI agent
│   ├── llm/                     # NEW - Gemini LLM Controller
│   │   ├── __init__.py
│   │   ├── gemini_client.py     # Gemini API client wrapper
│   │   ├── prompt_builder.py    # Prompt construction logic
│   │   ├── response_parser.py   # Parse Gemini responses
│   │   ├── system_prompts.py    # System instructions templates
│   │   ├── security.py          # Prompt injection detection
│   │   └── config.py            # Gemini API configuration
│   └── tests/
│       ├── test_chat_api.py
│       ├── test_agent_logic.py
│       ├── test_mcp_client.py
│       └── test_gemini_controller.py
│
├── mcp_server/                   # NEW - Standalone MCP Server
│   ├── __init__.py
│   ├── main.py                  # MCP server entry point
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── task_tools.py        # 5 MCP tool implementations
│   │   └── utils.py             # Helper functions
│   ├── config.py                # Database + MCP configuration
│   ├── requirements.txt         # MCP server dependencies
│   ├── README.md                # MCP server setup guide
│   └── tests/
│       ├── test_task_tools.py
│       └── test_mcp_server.py
│
└── src/                          # Phase II backend (NO MODIFICATIONS)
    ├── models/                   # Existing Task, User models (read-only imports)
    ├── api/                      # Phase II APIs (untouched)
    └── ...

frontend/
├── src/
│   ├── app/
│   │   ├── chat/                # NEW - Phase III chat route
│   │   │   ├── page.tsx         # /chat route (protected)
│   │   │   └── layout.tsx       # Chat layout (optional)
│   │   ├── dashboard/           # Phase II (untouched)
│   │   ├── login/               # Phase II (untouched)
│   │   └── ...
│   ├── components/
│   │   ├── chat/                # NEW - Phase III chat components
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   ├── LoadingIndicator.tsx
│   │   │   ├── ErrorDisplay.tsx
│   │   │   ├── EmptyState.tsx
│   │   │   └── __tests__/
│   │   │       ├── MessageList.test.tsx
│   │   │       └── MessageInput.test.tsx
│   │   └── ...                  # Phase II components (untouched)
│   ├── lib/
│   │   ├── chatkit-config.ts    # NEW - OpenAI ChatKit configuration
│   │   ├── api/
│   │   │   └── chat.ts          # NEW - Chat API client
│   │   └── ...                  # Phase II libs (untouched)
│   └── ...
└── ...

.claude/
└── skills/
    ├── mcp-server-builder-skill.md          # Agent 1 skill (already created)
    ├── chat-mcp-bridge-skill.md             # Agent 2 skill (already created)
    ├── phase3-mcp-orchestrator-skill.md     # Agent 3 skill (already created)
    ├── chatkit-frontend-builder-skill.md    # Agent 4 skill (already created)
    └── gemini-llm-controller-skill.md       # Agent 5 skill (already created)

.specify/
└── memory/
    └── phase-iii-constitution.md            # Phase III rules (already created)
```

**Structure Decision**: Web application (Option 2) - Monorepo with `frontend/` and `backend/` directories. Phase III adds new subdirectories (`backend/phase3/`, `backend/mcp_server/`, `frontend/src/app/chat/`, `frontend/src/components/chat/`) without modifying Phase II structure. This maintains clean separation and enables independent deployment if needed.

## Complexity Tracking

> **No violations** - Phase III follows constitution requirements:
> - Uses existing monorepo structure
> - No new repositories or projects
> - Stateless architecture with database persistence
> - Agent-based development with 5 defined skills
> - Type-safe implementation (TypeScript + Python type hints)

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

---

## Phase 0: Research & Unknowns Resolution

**Prerequisites**: Constitution Check PASSED

**Goal**: Resolve all technical unknowns, research best practices, and evaluate alternatives for key technology choices.

### Research Tasks

#### R1: Google Gemini Flash 2.5 Integration
**Unknown**: How to integrate Gemini Flash 2.5 API with Python FastAPI backend
**Research Questions**:
- What is the official Python SDK for Gemini? (`google-generativeai`)
- How to authenticate with Gemini API? (API key in environment variable)
- What is the request/response format for Gemini Flash 2.5? (JSON with `contents`, `systemInstruction`, `generationConfig`)
- How to handle rate limits? (Free tier: 15 RPM, 1M TPM - implement exponential backoff)
- What are the safety settings? (HARM_CATEGORY_*, BLOCK_MEDIUM_AND_ABOVE)
- How to stream responses? (Optional for Phase III - defer to Phase IV)

**Decision Criteria**:
- Must support system instructions (for task management scope)
- Must support conversation history (multi-turn context)
- Must have error handling for rate limits, timeouts, safety violations
- Must be production-ready (official Google SDK preferred)

#### R2: MCP Server SDK Selection
**Unknown**: Which MCP SDK to use for Python backend
**Research Questions**:
- Is there an official Python MCP SDK? (Check @modelcontextprotocol GitHub)
- If no Python SDK, can we use Node.js MCP server called from Python? (via subprocess)
- What is the MCP protocol specification? (JSON-RPC over stdio or HTTP)
- How to register tools with MCP server? (Tool schema with parameters, returns, descriptions)
- How to invoke MCP tools from Python? (MCP client library or HTTP requests)

**Decision Criteria**:
- Must support Python (preferred) or Node.js (fallback)
- Must support tool registration with parameter validation
- Must support stdio or HTTP transport
- Must be actively maintained

#### R3: OpenAI ChatKit Frontend Integration
**Unknown**: How to use OpenAI ChatKit for UI without using OpenAI LLM
**Research Questions**:
- Can ChatKit UI components be used independently from OpenAI API? (YES - ChatKit is a UI framework)
- How to configure ChatKit to point to our custom chat API? (Override `apiEndpoint` in config)
- What is the domain allowlist setup? (NEXT_PUBLIC_OPENAI_DOMAIN_KEY environment variable)
- How to customize ChatKit theme? (Pass `theme` object in config)
- Are there alternatives to ChatKit? (Build custom React components - more work, more control)

**Decision Criteria**:
- Must support custom API endpoint (not tied to OpenAI API)
- Must be compatible with Next.js 15+ App Router
- Must support TypeScript
- Must be easy to customize (theme, styling)

#### R4: Stateless Conversation Management
**Unknown**: Best practices for stateless conversation persistence
**Research Questions**:
- How to structure conversation history in database? (Conversation + Message models with foreign keys)
- How to handle conversation context window limits? (Sliding window - last 10 messages)
- How to prevent concurrent message creation race conditions? (Database transactions)
- How to handle long-running Gemini requests? (Async with timeout, store "processing" state)

**Decision Criteria**:
- Must support horizontal scaling (no in-memory state)
- Must handle concurrent users without conflicts
- Must maintain conversation order (timestamps + indexes)
- Must support resuming conversations (load by conversation_id)

#### R5: Prompt Injection Prevention
**Unknown**: Best practices for securing Gemini prompts against injection
**Research Questions**:
- What are common prompt injection attack patterns? ("Ignore previous instructions", role manipulation, output format manipulation)
- How to detect injection attempts? (Regex patterns, keyword blacklists, semantic analysis)
- How to handle detected injections? (Reject request, return safe fallback message)
- How to enforce system instructions immutability? (Gemini's `systemInstruction` field is separate from user input)

**Decision Criteria**:
- Must detect common attack patterns
- Must prevent system instruction override
- Must log security violations for monitoring
- Must return user-friendly error messages

#### R6: Error Handling Strategies
**Unknown**: Comprehensive error handling for LLM, MCP, and Chat API layers
**Research Questions**:
- What errors can Gemini API return? (429 rate limit, 400 content policy, 401 auth, 504 timeout, network errors)
- What errors can MCP tools return? (404 task not found, 403 unauthorized, 400 invalid params, 500 database errors)
- How to cascade errors through layers? (Gemini error → AI Agent → Chat API → Frontend)
- What are safe fallback messages? ("I'm having trouble right now. Please try again.")

**Decision Criteria**:
- Must handle all known error types
- Must never expose stack traces to users
- Must log errors internally for debugging
- Must provide actionable error messages

### Research Outputs (research.md)

**Decision**: Use Google Generative AI SDK (`google-generativeai`) for Gemini Flash 2.5
**Rationale**: Official Google SDK with production support, native Python integration, comprehensive error handling
**Alternatives Considered**:
- REST API directly: More control but more boilerplate, harder error handling
- Third-party wrappers: Potential maintenance risk if abandoned

**Decision**: Use Official MCP SDK (Node.js) via HTTP transport
**Rationale**: Most mature MCP implementation, well-documented, supports HTTP transport for cross-language communication
**Alternatives Considered**:
- Python MCP SDK: Not yet available or mature
- Custom MCP implementation: High complexity, maintenance burden

**Decision**: Use OpenAI ChatKit for frontend UI
**Rationale**: Production-ready chat UI components, customizable, supports custom API endpoints, saves development time
**Alternatives Considered**:
- Build custom React components: More control but significantly more development time, harder to maintain

**Decision**: Sliding window conversation history (last 10 messages)
**Rationale**: Balances context richness with API costs and latency, prevents context window overflow
**Alternatives Considered**:
- Full conversation history: Expensive, slow, may exceed Gemini context limits
- Conversation summarization: Complex, may lose important context

**Decision**: Keyword-based prompt injection detection + Gemini safety filters
**Rationale**: Catches common attack patterns, low false positive rate, complements Gemini's built-in safety
**Alternatives Considered**:
- Semantic analysis with ML model: Overkill for MVP, adds latency and complexity
- No detection: Unacceptable security risk

**Decision**: Three-tier error handling (Validation 400, Business Logic 404/403, System 500)
**Rationale**: Industry standard, clear error categorization, actionable for frontend
**Alternatives Considered**:
- Single generic error: Poor UX, harder to debug
- Fine-grained error codes: Over-engineering for MVP

---

## Phase 1: Design & Contracts

**Prerequisites**: Phase 0 research.md complete

**Goal**: Design database schemas, API contracts, and MCP tool signatures. Generate quickstart guide.

### D1: Database Schema Design (data-model.md)

#### Conversation Model
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str | None = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow,
                                  sa_column_kwargs={"onupdate": datetime.utcnow})

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(back_populates="conversation",
                                              cascade_delete=True)
```

**Indexes**:
- Primary key: `id` (UUID)
- Foreign key index: `user_id`
- Composite index: `(user_id, created_at)` for listing user's conversations

**Constraints**:
- `user_id` must reference existing User
- Cascade delete: When Conversation deleted, all Messages deleted
- `title` is optional (can be derived from first message)

**Validation Rules**:
- `user_id` must not be empty
- `title` max length 200 characters
- `created_at` must be <= now()

#### Message Model
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: str = Field(...)  # "user" | "assistant"
    content: str = Field(..., max_length=10000)
    tool_calls: str | None = Field(default=None)  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
```

**Indexes**:
- Primary key: `id` (UUID)
- Foreign key index: `conversation_id`
- Composite index: `(conversation_id, created_at)` for loading messages in order

**Constraints**:
- `conversation_id` must reference existing Conversation
- `role` must be "user" or "assistant"
- `content` cannot be null or empty

**Validation Rules**:
- `role` must be in ["user", "assistant"]
- `content` min length 1, max length 10000 characters
- `tool_calls` must be valid JSON if not null
- `created_at` must be >= conversation.created_at

**tool_calls JSON Structure** (when role="assistant"):
```json
[
  {
    "tool_name": "add_task",
    "parameters": {"user_id": "...", "title": "..."},
    "result": {"id": 42, "title": "...", "status": "..."}
  }
]
```

#### Task Model (Existing - Reference Only)
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(..., max_length=200)
    description: str | None = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Usage**: MCP tools read/write to this table. NO schema changes allowed (Phase II protection).

#### Entity Relationships
```
User (Phase II)
  └── has many → Conversation (Phase III)
                    └── has many → Message (Phase III)

User (Phase II)
  └── has many → Task (Phase II - used by MCP tools)
```

### D2: API Contracts (contracts/)

#### contracts/chat-api.yaml (OpenAPI 3.0)
```yaml
openapi: 3.0.0
info:
  title: Phase III Chat API
  version: 1.0.0
  description: Stateless chat API for AI-powered task management

paths:
  /api/{user_id}/chat:
    post:
      summary: Send chat message and receive AI response
      operationId: sendChatMessage
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
          description: User ID (must match JWT token user_id)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - message
              properties:
                message:
                  type: string
                  minLength: 1
                  maxLength: 2000
                  description: User's natural language message
                conversation_id:
                  type: string
                  format: uuid
                  description: Optional conversation ID to continue existing conversation
      responses:
        '200':
          description: Successful response with assistant message
          content:
            application/json:
              schema:
                type: object
                required:
                  - conversation_id
                  - message_id
                  - response
                  - tool_calls
                  - created_at
                properties:
                  conversation_id:
                    type: string
                    format: uuid
                  message_id:
                    type: string
                    format: uuid
                  response:
                    type: string
                    description: Assistant's natural language response
                  tool_calls:
                    type: array
                    items:
                      type: object
                      properties:
                        tool_name:
                          type: string
                        parameters:
                          type: object
                        result:
                          type: object
                  created_at:
                    type: string
                    format: date-time
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '403':
          description: Forbidden (user_id mismatch)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '404':
          description: Conversation not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    Error:
      type: object
      required:
        - error
        - code
      properties:
        error:
          type: string
        code:
          type: string
        details:
          type: string
        message:
          type: string
```

#### contracts/mcp-tools.json
```json
{
  "tools": [
    {
      "name": "add_task",
      "description": "Creates a new task for the authenticated user",
      "parameters": {
        "type": "object",
        "required": ["user_id", "title"],
        "properties": {
          "user_id": {
            "type": "string",
            "description": "User ID (owner of task)"
          },
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200,
            "description": "Task title"
          },
          "description": {
            "type": "string",
            "description": "Optional task description"
          }
        }
      },
      "returns": {
        "type": "object",
        "properties": {
          "task_id": {"type": "integer"},
          "status": {"type": "string"},
          "title": {"type": "string"}
        }
      }
    },
    {
      "name": "list_tasks",
      "description": "Lists tasks for the authenticated user with optional filtering",
      "parameters": {
        "type": "object",
        "required": ["user_id"],
        "properties": {
          "user_id": {"type": "string"},
          "status": {
            "type": "string",
            "enum": ["all", "pending", "completed"],
            "description": "Filter by completion status"
          }
        }
      },
      "returns": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "task_id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "completed": {"type": "boolean"}
          }
        }
      }
    },
    {
      "name": "complete_task",
      "description": "Marks a task as completed (idempotent)",
      "parameters": {
        "type": "object",
        "required": ["user_id", "task_id"],
        "properties": {
          "user_id": {"type": "string"},
          "task_id": {"type": "integer"}
        }
      },
      "returns": {
        "type": "object",
        "properties": {
          "task_id": {"type": "integer"},
          "status": {"type": "string"},
          "title": {"type": "string"}
        }
      }
    },
    {
      "name": "update_task",
      "description": "Updates task title or description",
      "parameters": {
        "type": "object",
        "required": ["user_id", "task_id"],
        "properties": {
          "user_id": {"type": "string"},
          "task_id": {"type": "integer"},
          "title": {"type": "string"},
          "description": {"type": "string"}
        }
      },
      "returns": {
        "type": "object",
        "properties": {
          "task_id": {"type": "integer"},
          "status": {"type": "string"},
          "title": {"type": "string"}
        }
      }
    },
    {
      "name": "delete_task",
      "description": "Permanently deletes a task",
      "parameters": {
        "type": "object",
        "required": ["user_id", "task_id"],
        "properties": {
          "user_id": {"type": "string"},
          "task_id": {"type": "integer"}
        }
      },
      "returns": {
        "type": "object",
        "properties": {
          "task_id": {"type": "integer"},
          "status": {"type": "string"},
          "title": {"type": "string"}
        }
      }
    }
  ]
}
```

#### contracts/gemini-api.md
```markdown
# Gemini API Integration Contract

## Model
- **Provider**: Google Gemini
- **Model**: `gemini-2.0-flash-exp` (Gemini Flash 2.5)
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent`

## Authentication
- **Method**: API Key
- **Header**: `x-goog-api-key: ${GEMINI_API_KEY}`
- **Environment Variable**: `GEMINI_API_KEY` (stored in `.env`, never committed)

## Request Format
```json
{
  "contents": [
    {"role": "user", "parts": [{"text": "..."}]},
    {"role": "model", "parts": [{"text": "..."}]}
  ],
  "systemInstruction": {
    "parts": [{"text": "You are a task management assistant..."}]
  },
  "generationConfig": {
    "temperature": 0.3,
    "topP": 0.9,
    "topK": 40,
    "maxOutputTokens": 1024
  },
  "safetySettings": [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
  ]
}
```

## Response Format
```json
{
  "candidates": [
    {
      "content": {
        "parts": [{"text": "..."}],
        "role": "model"
      },
      "finishReason": "STOP"
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 123,
    "candidatesTokenCount": 456,
    "totalTokenCount": 579
  }
}
```

## Error Codes
- **429**: Rate limit exceeded → Retry with exponential backoff
- **400**: Content policy violation → Return safe fallback message
- **401/403**: Authentication failure → Log critical error, return fallback
- **504**: Timeout → Cancel request, return fallback
- **Network errors**: Retry once, then fallback

## Rate Limits
- **Free tier**: 15 RPM (requests per minute), 1M TPM (tokens per minute)
- **Mitigation**: Exponential backoff (1s, 2s, 4s, 8s, 16s), max 5 retries

## Safety Settings
- All categories: `BLOCK_MEDIUM_AND_ABOVE`
- Cannot be disabled (enforced by Gemini)

## System Instructions
```
You are a task management assistant for a Todo application.

Your ONLY purpose is to help users:
- Create new tasks
- List and filter existing tasks
- Update task details
- Mark tasks as complete
- Delete tasks

You have access to these tools:
- add_task(user_id, title, description)
- list_tasks(user_id, status)
- update_task(user_id, task_id, title, description)
- complete_task(user_id, task_id)
- delete_task(user_id, task_id)

Rules:
1. NEVER help with anything outside task management
2. If unsure, ask clarifying questions
3. If multiple tasks match, list them and ask which one
4. Provide natural, friendly responses
```
```

### D3: Quickstart Guide (quickstart.md)

```markdown
# Phase III Quickstart Guide

## Prerequisites
- Phase II fully deployed and working
- Neon PostgreSQL database accessible
- Google Gemini API key obtained
- Node.js 20+ and Python 3.13+ installed

## Environment Setup

### 1. Obtain Gemini API Key
```bash
# Visit https://ai.google.dev/
# Click "Get API Key"
# Create new project or use existing
# Copy API key
```

### 2. Configure Backend Environment
```bash
# backend/.env
DATABASE_URL=postgresql://user:pass@host:5432/db  # Existing from Phase II
GEMINI_API_KEY=AIza...your-key-here  # NEW - Gemini API key
JWT_SECRET=...existing-secret...      # Existing from Phase II
```

### 3. Configure Frontend Environment
```bash
# frontend/.env.local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000  # Existing from Phase II
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key   # NEW - ChatKit domain key
```

### 4. Install Dependencies
```bash
# Backend (Phase III dependencies)
cd backend
pip install google-generativeai  # Gemini SDK
# MCP SDK (if Python version available, else use Node.js)

# Frontend (Phase III dependencies)
cd frontend
npm install @openai/chatkit  # ChatKit UI components
```

### 5. Run Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "Add Phase III tables (conversations, messages)"
alembic upgrade head
```

### 6. Start MCP Server (Terminal 1)
```bash
cd backend/mcp_server
python main.py
# Should see: "MCP Server started, 5 tools registered"
```

### 7. Start Backend API (Terminal 2)
```bash
cd backend
uvicorn src.main:app --reload --port 8000
# Should see: "POST /api/{user_id}/chat" route registered
```

### 8. Start Frontend (Terminal 3)
```bash
cd frontend
npm run dev
# Should see: http://localhost:3000
```

### 9. Test Chat Flow
```
1. Login to http://localhost:3000 (use Phase II credentials)
2. Navigate to http://localhost:3000/chat
3. Type: "Add a task to buy groceries"
4. Verify: Task appears in chat response AND in Phase II dashboard
5. Type: "Show me all my tasks"
6. Verify: Chat lists all tasks including the one just created
```

## Troubleshooting

**Issue**: "Gemini API key invalid"
- **Solution**: Check `.env` has correct `GEMINI_API_KEY`, restart backend

**Issue**: "MCP server not reachable"
- **Solution**: Ensure MCP server running on correct port, check logs

**Issue**: "ChatKit domain key error"
- **Solution**: Register domain at OpenAI ChatKit dashboard, add key to `.env.local`

**Issue**: "Conversation not persisting"
- **Solution**: Check database migrations ran, check `conversations` and `messages` tables exist

## Development Workflow
1. Make changes to Phase III code only (`backend/phase3/`, `backend/mcp_server/`, `frontend/src/app/chat/`)
2. Run tests: `pytest backend/phase3/tests/` and `npm test` in frontend
3. Verify Phase II still works: Test dashboard, task CRUD, auth
4. Commit changes to `004-phase-iii-chatbot` branch
5. Create PR when ready for review
```

### D4: Agent Context Update

Run the agent context update script to add Phase III technologies:

```bash
.specify/scripts/bash/update-agent-context.sh claude
```

This will update `.claude/context.md` (or equivalent) with:
- Google Gemini Flash 2.5
- MCP Server SDK
- OpenAI ChatKit (UI only)
- New database models (Conversation, Message)
- New API endpoint (/api/{user_id}/chat)

---

## Phase 2: Implementation Roadmap (NOT EXECUTED BY /sp.plan)

**Note**: Phase 2 is executed by `/sp.tasks` command, not `/sp.plan`. This section provides the implementation sequence for reference.

### Implementation Phases

#### Phase 2.1: MCP Server (Agent 1)
**Dependencies**: None (standalone)
**Duration**: 3-5 days
**Deliverables**:
- `backend/mcp_server/main.py` - MCP server entry point
- `backend/mcp_server/tools/task_tools.py` - 5 MCP tool implementations
- `backend/mcp_server/tests/` - Unit tests for all tools
- MCP server can start independently and register 5 tools

**Testing**:
- Unit tests: Each tool with mocked database
- Integration tests: MCP client → MCP server → database
- Manual test: Start MCP server, invoke tools via MCP client

#### Phase 2.2: Gemini LLM Controller (Agent 5)
**Dependencies**: Phase 2.1 complete (needs MCP tool definitions)
**Duration**: 2-4 days
**Deliverables**:
- `backend/phase3/llm/gemini_client.py` - Gemini API wrapper
- `backend/phase3/llm/prompt_builder.py` - Prompt construction
- `backend/phase3/llm/response_parser.py` - Response parsing
- `backend/phase3/llm/security.py` - Prompt injection detection
- `backend/phase3/llm/tests/` - Unit tests with mocked Gemini API

**Testing**:
- Unit tests: Mock Gemini API responses
- Security tests: Prompt injection attack scenarios
- Error tests: Rate limits, timeouts, content policy violations

#### Phase 2.3: AI Agent Logic (Agent 3)
**Dependencies**: Phase 2.2 complete (needs Gemini controller)
**Duration**: 3-5 days
**Deliverables**:
- `backend/phase3/agent/orchestrator.py` - Intent parsing, tool selection
- `backend/phase3/agent/prompts.py` - System prompts
- `backend/phase3/agent/tests/` - Unit tests for intent recognition

**Testing**:
- Unit tests: Intent parsing with sample messages
- Tool selection tests: Verify correct tools chosen for each intent
- Context resolution tests: Multi-turn conversation handling

#### Phase 2.4: Chat API + MCP Bridge (Agent 2)
**Dependencies**: Phase 2.1, 2.3 complete (needs MCP server and AI agent)
**Duration**: 4-6 days
**Deliverables**:
- `backend/phase3/models/conversation.py` - Conversation model
- `backend/phase3/models/message.py` - Message model
- `backend/phase3/routers/chat.py` - Chat API endpoint
- `backend/phase3/services/chat_service.py` - 7-step pipeline
- `backend/phase3/services/mcp_client.py` - MCP client wrapper
- Database migrations for new tables
- `backend/phase3/tests/` - Integration tests

**Testing**:
- Integration tests: Full chat flow with mocked Gemini and MCP
- Database tests: Conversation and message persistence
- Auth tests: JWT validation, user_id matching
- Error tests: Conversation not found, user mismatch

#### Phase 2.5: ChatKit Frontend (Agent 4)
**Dependencies**: Phase 2.4 complete (needs Chat API)
**Duration**: 3-5 days
**Deliverables**:
- `frontend/src/app/chat/page.tsx` - Chat route
- `frontend/src/components/chat/MessageList.tsx` - Message display
- `frontend/src/components/chat/MessageInput.tsx` - User input
- `frontend/src/components/chat/LoadingIndicator.tsx` - Loading state
- `frontend/src/components/chat/ErrorDisplay.tsx` - Error handling
- `frontend/src/components/chat/EmptyState.tsx` - Empty conversation
- `frontend/src/lib/chatkit-config.ts` - ChatKit configuration
- `frontend/src/lib/api/chat.ts` - API client
- Component tests

**Testing**:
- Component tests: Each component with React Testing Library
- Integration tests: Chat flow with mocked API
- E2E tests: Full user journey with Playwright

#### Phase 2.6: End-to-End Integration
**Dependencies**: All phases complete
**Duration**: 2-3 days
**Deliverables**:
- E2E test suite (Playwright)
- Phase II regression tests
- Performance benchmarks
- Documentation updates

**Testing**:
- E2E tests: Complete user flows
- Regression tests: Verify Phase II untouched
- Performance tests: Load testing, latency measurements
- Security tests: Penetration testing, prompt injection

### Testing Milestones

**Milestone 1: MCP Tools Working**
- All 5 tools callable via MCP server
- User data isolation enforced
- Error handling covers all cases

**Milestone 2: Gemini Integration Working**
- Gemini API calls succeed
- System instructions enforced
- Prompt injection detection active
- Rate limiting handled

**Milestone 3: Chat API Working**
- POST /api/{user_id}/chat returns responses
- Conversation history persists
- AI agent selects correct tools
- MCP tools execute successfully

**Milestone 4: Frontend Working**
- Chat UI renders messages
- User can send messages
- Assistant responses display
- Tool calls visible (optional debug view)

**Milestone 5: Phase II Regression Passed**
- All Phase II tests pass
- Dashboard shows chat-created tasks
- Phase II task operations work unchanged

### Rollback & Safety Strategy

**Rollback Triggers**:
- Phase II tests fail
- Critical security vulnerability discovered
- Production outage caused by Phase III
- Data corruption detected

**Rollback Procedure**:
1. **Immediate**: Disable Phase III routes (`/chat`, `/api/{user_id}/chat`)
2. **Database**: Rollback migrations (drop `conversations`, `messages` tables if safe)
3. **Code**: Revert to Phase II commit
4. **Verification**: Run Phase II smoke tests
5. **Communication**: Notify users of rollback, estimated fix time

**Safety Measures**:
- **Feature Flag**: Environment variable `PHASE_III_ENABLED=true/false`
- **Database Backups**: Automated hourly backups during Phase III rollout
- **Canary Deployment**: Deploy to 10% of users first, monitor errors
- **Monitoring**: Track Phase III API errors, latency, user complaints
- **Graceful Degradation**: If Gemini API down, show "Chat temporarily unavailable" message

### Completion Criteria

Phase III is considered complete when ALL of the following are true:

**Functional Criteria**:
- [ ] All 5 MCP tools implemented and tested
- [ ] Gemini Flash 2.5 integration working
- [ ] Chat API endpoint functional
- [ ] Conversation history persists correctly
- [ ] Frontend chat UI renders and works
- [ ] Natural language commands execute correctly
- [ ] Multi-turn conversations work (context maintained)
- [ ] Error handling graceful (no crashes)

**Quality Criteria**:
- [ ] >80% test coverage for Phase III code
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] E2E tests passing
- [ ] Performance benchmarks met (<3s p95 latency)

**Security Criteria**:
- [ ] User data isolation enforced (100%)
- [ ] JWT authentication working
- [ ] Prompt injection detection active
- [ ] No hardcoded secrets in code
- [ ] All error messages user-friendly (no stack traces)

**Phase II Protection Criteria**:
- [ ] All Phase II tests passing (zero regression)
- [ ] Git diff shows zero changes to Phase II files
- [ ] Phase II dashboard shows chat-created tasks
- [ ] Phase II task CRUD works unchanged
- [ ] Phase II authentication unchanged

**Documentation Criteria**:
- [ ] README.md updated with Phase III overview
- [ ] API documentation complete (OpenAPI spec)
- [ ] MCP server README complete
- [ ] Deployment guide complete
- [ ] Quickstart guide tested and working

**Deployment Criteria**:
- [ ] MCP server deployable independently
- [ ] Backend deploys without Phase II changes
- [ ] Frontend deploys without Phase II changes
- [ ] Database migrations reversible
- [ ] Environment variables documented
- [ ] Monitoring and alerting configured

---

## Mock vs Real Gemini Handling

### Development Strategy

**Phase 1: Mock Gemini Responses**
- Use fixed JSON responses for deterministic testing
- No Gemini API calls during unit tests
- Fast test execution, no API costs

**Phase 2: Gemini Sandbox**
- Use real Gemini API in development environment
- Free tier limits (15 RPM, 1M TPM)
- Test real behavior, error handling

**Phase 3: Production Gemini**
- Upgrade to paid tier if free limits exceeded
- Monitor usage, costs, latency
- Implement caching if needed

### Mock Implementation

```python
# backend/phase3/llm/tests/mock_gemini.py
class MockGeminiClient:
    def generate_content(self, request):
        # Parse user message
        user_message = request["contents"][-1]["parts"][0]["text"]

        # Simple keyword-based responses for testing
        if "add" in user_message.lower() and "task" in user_message.lower():
            return {
                "candidates": [{
                    "content": {
                        "parts": [{"text": "INTENT: CREATE_TASK\nTOOLS: [{\"tool_name\": \"add_task\", \"parameters\": {\"user_id\": \"test_user\", \"title\": \"Buy groceries\"}}]\nRESPONSE: I'll add that task for you."}],
                        "role": "model"
                    },
                    "finishReason": "STOP"
                }]
            }
        elif "show" in user_message.lower() or "list" in user_message.lower():
            return {
                "candidates": [{
                    "content": {
                        "parts": [{"text": "INTENT: LIST_TASKS\nTOOLS: [{\"tool_name\": \"list_tasks\", \"parameters\": {\"user_id\": \"test_user\", \"status\": \"all\"}}]\nRESPONSE: Here are your tasks."}],
                        "role": "model"
                    },
                    "finishReason": "STOP"
                }]
            }
        else:
            return {
                "candidates": [{
                    "content": {
                        "parts": [{"text": "INTENT: CLARIFICATION\nTOOLS: []\nRESPONSE: I'm not sure what you'd like to do. Can you rephrase?"}],
                        "role": "model"
                    },
                    "finishReason": "STOP"
                }]
            }
```

### Test Configuration

```python
# backend/phase3/llm/config.py
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USE_MOCK_GEMINI = os.getenv("USE_MOCK_GEMINI", "false").lower() == "true"

def get_gemini_client():
    if USE_MOCK_GEMINI:
        from .tests.mock_gemini import MockGeminiClient
        return MockGeminiClient()
    else:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        return genai.GenerativeModel('gemini-2.0-flash-exp')
```

**Usage in Tests**:
```bash
# Run tests with mocked Gemini
USE_MOCK_GEMINI=true pytest backend/phase3/tests/

# Run tests with real Gemini
GEMINI_API_KEY=your-key pytest backend/phase3/tests/
```

---

## Agent Execution Order

### Dependency Graph

```
Phase 2.1: MCP Server (Agent 1)
    ↓
Phase 2.2: Gemini LLM Controller (Agent 5)
    ↓
Phase 2.3: AI Agent Logic (Agent 3)
    ↓
Phase 2.4: Chat API + MCP Bridge (Agent 2)
    ↓
Phase 2.5: ChatKit Frontend (Agent 4)
    ↓
Phase 2.6: E2E Integration
```

**Critical Path**: MCP Server → Gemini → AI Agent → Chat API → Frontend
**Parallelizable**: Gemini and MCP Server can start in parallel, but AI Agent needs both

### Recommended Execution Sequence

1. **Week 1**: MCP Server Agent (Agent 1)
   - Standalone implementation
   - Can be tested independently
   - Blocks all other agents

2. **Week 2**: Gemini LLM Controller (Agent 5) + AI Agent Logic (Agent 3)
   - Gemini controller can start once MCP tools defined
   - AI Agent starts once Gemini controller ready
   - Can partially overlap if interfaces defined upfront

3. **Week 3**: Chat API + MCP Bridge (Agent 2)
   - Needs MCP server and AI agent complete
   - Database migrations created
   - Backend fully functional

4. **Week 4**: ChatKit Frontend (Agent 4)
   - Needs Chat API complete
   - Can use mocked API responses early
   - UI polish and testing

5. **Week 5**: E2E Integration + Phase II Regression
   - Full system testing
   - Performance benchmarking
   - Security audit

---

**Plan Version**: 1.0.0
**Last Updated**: 2026-01-23
**Next Step**: Run `/sp.tasks` to generate implementation tasks
