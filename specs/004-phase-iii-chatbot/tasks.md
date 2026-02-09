# Tasks: Phase III - AI Chatbot with MCP Server

**Input**: Design documents from `/specs/004-phase-iii-chatbot/`
**Prerequisites**: plan.md (✅ complete), spec.md (✅ complete)

**Organization**: Tasks are grouped by implementation phase and agent responsibility, following the 5-agent architecture defined in the plan.

**Tests**: Unit tests for backend components (pytest), component tests for frontend (Jest), and E2E tests (Playwright) are included.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- All tasks include exact file paths

## Path Conventions

This is a web application with monorepo structure:
- **Backend**: `backend/phase3/`, `backend/mcp_server/`
- **Frontend**: `frontend/src/`
- **Phase II code**: NO MODIFICATIONS (zero regression requirement)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, environment setup, and database preparation

- [X] T001 Create Phase III directory structure at backend/phase3/ with subdirectories: routers/, services/, models/, schemas/, agent/, llm/, tests/
- [X] T002 [P] Create MCP server directory structure at backend/mcp_server/ with subdirectories: tools/, tests/
- [X] T003 [P] Create frontend chat directory structure at frontend/src/app/chat/ and frontend/src/components/chat/
- [X] T004 Add Phase III Python dependencies to backend/requirements.txt: google-generativeai, httpx (for MCP client)
- [X] T005 [P] Add Phase III Node.js dependencies to frontend/package.json: @openai/chatkit
- [X] T006 Create environment variable documentation in specs/004-phase-iii-chatbot/quickstart.md with GEMINI_API_KEY, NEXT_PUBLIC_OPENAI_DOMAIN_KEY
- [X] T007 Create database migration file for Conversation model: alembic revision -m "Add conversations table" (Completed during Phase 2)
- [X] T008 Create database migration file for Message model: alembic revision -m "Add messages table" (Completed during Phase 2)

**Checkpoint**: Directory structure created, dependencies documented, migration files ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database models and configuration that ALL agents depend on

**⚠️ CRITICAL**: No agent implementation can begin until this phase is complete

- [X] T009 Create Conversation model in backend/phase3/models/conversation.py with SQLModel schema (id, user_id, title, created_at, updated_at)
- [X] T010 Create Message model in backend/phase3/models/message.py with SQLModel schema (id, conversation_id, role, content, tool_calls, created_at)
- [X] T011 Add relationships to Conversation model (user, messages with cascade_delete=True)
- [X] T012 Add relationships to Message model (conversation foreign key)
- [X] T013 Create indexes for Conversation: PRIMARY KEY (id), INDEX (user_id), COMPOSITE INDEX (user_id, created_at)
- [X] T014 Create indexes for Message: PRIMARY KEY (id), INDEX (conversation_id), COMPOSITE INDEX (conversation_id, created_at)
- [X] T015 [P] Create Pydantic request/response schemas in backend/phase3/schemas/chat_schema.py (ChatRequest, ChatResponse)
- [X] T016 [P] Create __init__.py files in all backend/phase3/ subdirectories to make them Python modules
- [X] T017 Run database migrations to create conversations and messages tables: alembic upgrade head (Completed during deployment prep)
- [X] T018 Verify database schema created correctly: check tables exist in Neon PostgreSQL (Completed during deployment prep)

**Checkpoint**: Foundation ready - agent implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1) 🎯 MVP

**Goal**: Users can create, update, and manage tasks through conversational AI

**Independent Test**: Send chat message "Add a task to buy groceries tomorrow" and verify task appears in database and response confirms creation

**Agent Execution Order**: Phase 2.1 (MCP Server) → Phase 2.2 (Gemini Controller) → Phase 2.3 (AI Agent Logic) → Phase 2.4 (Chat API) → Phase 2.5 (ChatKit Frontend)

### Phase 2.1: MCP Server Implementation (Agent 1)

**Agent**: mcp-server-builder-skill.md
**Dependencies**: Phase 2 (Foundational) complete
**Duration**: 3-5 days

- [X] T019 [P] Create MCP server main entry point in backend/mcp_server/main.py with Official MCP SDK initialization
- [X] T020 [P] Create MCP server configuration in backend/mcp_server/config.py with database connection and MCP protocol settings
- [X] T021 Create add_task MCP tool in backend/mcp_server/tools/task_tools.py (parameters: user_id, title, description, priority, due_date, tags)
- [X] T022 Create list_tasks MCP tool in backend/mcp_server/tools/task_tools.py (parameters: user_id, status, priority, tag)
- [X] T023 Create update_task MCP tool in backend/mcp_server/tools/task_tools.py (parameters: user_id, task_id, title, description, priority, due_date, tags)
- [X] T024 Create complete_task MCP tool in backend/mcp_server/tools/task_tools.py (parameters: user_id, task_id)
- [X] T025 Create delete_task MCP tool in backend/mcp_server/tools/task_tools.py (parameters: user_id, task_id)
- [X] T026 Implement user data isolation in all MCP tools: filter database queries by user_id (100% enforcement)
- [X] T027 Add error handling for all MCP tools: TASK_NOT_FOUND, UNAUTHORIZED, INVALID_INPUT, INTERNAL_ERROR
- [X] T028 Create MCP server README.md with setup instructions, tool documentation, and usage examples
- [X] T029 Create unit tests for add_task in backend/mcp_server/tests/test_task_tools.py (mock database, verify task created)
- [X] T030 [P] Create unit tests for list_tasks in backend/mcp_server/tests/test_task_tools.py (mock database, verify filtering)
- [X] T031 [P] Create unit tests for update_task in backend/mcp_server/tests/test_task_tools.py (mock database, verify updates)
- [X] T032 [P] Create unit tests for complete_task in backend/mcp_server/tests/test_task_tools.py (mock database, verify completion)
- [X] T033 [P] Create unit tests for delete_task in backend/mcp_server/tests/test_task_tools.py (mock database, verify deletion)
- [X] T034 Create integration test for MCP server startup in backend/mcp_server/tests/test_mcp_server.py (verify 5 tools registered within 5 seconds)
- [X] T035 Test MCP server can start independently without Phase II backend running
- [X] T036 Test MCP tools enforce user_id isolation with 100% accuracy (attempt cross-user data access, verify blocked)

**Milestone 1 Checkpoint**: MCP Server Working - All 5 tools callable via MCP client, user data isolation enforced, error handling complete

---

### Phase 2.2: Gemini LLM Controller Implementation (Agent 5)

**Agent**: gemini-llm-controller-skill.md
**Dependencies**: Phase 2.1 (MCP tools defined)
**Duration**: 2-4 days

- [X] T037 [P] Create Gemini API client wrapper in backend/phase3/llm/gemini_client.py with google-generativeai SDK initialization
- [X] T038 [P] Create Gemini configuration in backend/phase3/llm/config.py (API key, model name, generation config)
- [X] T039 Create prompt builder in backend/phase3/llm/prompt_builder.py (construct conversation history + system instructions)
- [X] T040 Create system prompts template in backend/phase3/llm/system_prompts.py (task management scope, tool descriptions, rules)
- [X] T041 Create Gemini response parser in backend/phase3/llm/response_parser.py (extract intent, tool calls, natural language response)
- [X] T042 Create prompt injection detector in backend/phase3/llm/security.py (keyword blacklist, detect "Ignore previous instructions" patterns)
- [X] T043 Implement Gemini API error handling: 429 rate limit (exponential backoff), 400 content policy (safe fallback), 401/403 auth (log critical), 504 timeout (cancel + fallback)
- [X] T044 Configure Gemini safety settings in backend/phase3/llm/config.py: all categories BLOCK_MEDIUM_AND_ABOVE
- [X] T045 Configure Gemini generation parameters: temperature=0.3, topP=0.9, topK=40, maxOutputTokens=1024
- [X] T046 Create mock Gemini client in backend/phase3/llm/tests/mock_gemini.py (keyword-based responses for deterministic testing)
- [X] T047 Create unit tests for prompt builder in backend/phase3/llm/tests/test_prompt_builder.py (verify system instructions, conversation history format)
- [X] T048 [P] Create unit tests for response parser in backend/phase3/llm/tests/test_response_parser.py (parse tool calls from Gemini response)
- [X] T049 [P] Create unit tests for security module in backend/phase3/llm/tests/test_security.py (detect common injection patterns)
- [X] T050 Create integration test for Gemini API in backend/phase3/llm/tests/test_gemini_integration.py (USE_MOCK_GEMINI=true for CI/CD)
- [X] T051 Test Gemini error handling with mock responses: verify rate limit retry, content policy fallback, timeout handling

**Milestone 2 Checkpoint**: Gemini Integration Working - API calls succeed, system instructions enforced, prompt injection detection active, rate limiting handled

---

### Phase 2.3: AI Agent Logic Implementation (Agent 3)

**Agent**: phase3-mcp-orchestrator-skill.md
**Dependencies**: Phase 2.2 (Gemini controller ready)
**Duration**: 3-5 days

- [X] T052 Create AI agent orchestrator in backend/phase3/agent/orchestrator.py (intent parsing, tool selection, MCP tool invocation)
- [X] T053 Implement natural language intent recognition in orchestrator: CREATE_TASK, LIST_TASKS, UPDATE_TASK, COMPLETE_TASK, DELETE_TASK, CLARIFICATION, OUT_OF_SCOPE
- [X] T054 Implement entity extraction in orchestrator: task title, priority (low/medium/high), due_date (relative to absolute conversion), tags
- [X] T055 Implement tool selection logic in orchestrator: map intent to MCP tool(s), handle ambiguous requests
- [X] T056 Implement conversation context resolution in orchestrator: resolve pronouns ("that task", "the first one"), relative references using last 10 messages
- [X] T057 Implement tool chaining in orchestrator: handle multi-step operations (list tasks → update task when reference is ambiguous)
- [X] T058 Implement ambiguity handling in orchestrator: when confidence < 70%, ask clarifying questions instead of guessing
- [X] T059 Create agent prompts in backend/phase3/agent/prompts.py (system instructions, few-shot examples for intent mapping)
- [X] T060 Integrate Gemini LLM controller into orchestrator: call Gemini client with conversation history + system prompts
- [X] T061 Create unit tests for intent recognition in backend/phase3/agent/tests/test_orchestrator.py (sample messages → expected intents)
- [X] T062 [P] Create unit tests for entity extraction in backend/phase3/agent/tests/test_orchestrator.py (verify title, priority, date extraction)
- [X] T063 [P] Create unit tests for tool selection in backend/phase3/agent/tests/test_orchestrator.py (verify correct tool chosen for each intent)
- [X] T064 Create unit tests for context resolution in backend/phase3/agent/tests/test_orchestrator.py (multi-turn conversation, pronoun resolution)
- [X] T065 Create integration test for full agent flow in backend/phase3/agent/tests/test_agent_integration.py (user message → Gemini → tool selection → response)
- [X] T066 Test agent asks clarifying questions for ambiguous requests (e.g., "delete the task" with multiple matches)
- [X] T067 Test agent handles multi-turn context correctly (e.g., "show tasks" → "mark the first one as done")

**Checkpoint**: AI Agent Logic Working - Intent parsing accurate, tool selection correct, context resolution functional, clarification requests working

---

### Phase 2.4: Chat API + MCP Bridge Implementation (Agent 2)

**Agent**: chat-mcp-bridge-skill.md
**Dependencies**: Phase 2.1 (MCP Server), Phase 2.3 (AI Agent Logic)
**Duration**: 4-6 days

- [x] T068 Create MCP client wrapper in backend/phase3/services/mcp_client.py (HTTP client to MCP server, invoke tools, handle responses)
- [x] T069 Create chat service in backend/phase3/services/chat_service.py implementing 7-step pipeline (receive, load, persist user, invoke agent, execute MCP, persist assistant, return)
- [x] T070 Implement Step 1 (Receive & Validate) in chat_service.py: extract user_id from JWT, validate message text (1-2000 chars), validate conversation_id format (UUID)
- [x] T071 Implement Step 2 (Load Conversation History) in chat_service.py: load existing conversation or create new, verify ownership (conversation.user_id == user_id), load last 10 messages
- [x] T072 Implement Step 3 (Persist User Message) in chat_service.py: create Message record (role="user", content, conversation_id), commit to database
- [x] T073 Implement Step 4 (Invoke AI Agent) in chat_service.py: call orchestrator with conversation history + user message, receive intent and tool calls
- [x] T074 Implement Step 5 (Execute MCP Tools) in chat_service.py: invoke MCP client for each tool call, aggregate results
- [x] T075 Implement Step 6 (Persist Assistant Response) in chat_service.py: create Message record (role="assistant", content, tool_calls JSON, conversation_id), commit to database
- [x] T076 Implement Step 7 (Return Response) in chat_service.py: return conversation_id, message_id, response text, tool_calls to caller
- [x] T077 Create Chat API router in backend/phase3/routers/chat.py with POST /api/{user_id}/chat endpoint
- [x] T078 Implement JWT authentication in chat router: verify Bearer token, extract user_id from JWT payload
- [x] T079 Implement user_id validation in chat router: verify path user_id matches JWT user_id (return 403 Forbidden if mismatch)
- [x] T080 Implement request validation in chat router: validate ChatRequest schema (message required, conversation_id optional UUID)
- [x] T081 Implement error handling in chat router: 400 validation errors, 401 unauthorized, 403 forbidden, 404 conversation not found, 500 internal errors
- [x] T082 Implement three-tier error handling: Validation (400), Business Logic (404/403), System (500) with user-friendly messages (no stack traces)
- [x] T083 Register chat router in backend/src/main.py (Phase II main app): include Phase III router without modifying Phase II routes
- [x] T084 Create integration test for chat endpoint in backend/phase3/tests/test_chat_api.py: POST /api/user_123/chat with valid message, verify 200 response
- [x] T085 [P] Create integration test for conversation creation in backend/phase3/tests/test_chat_api.py: verify new conversation created when conversation_id not provided
- [x] T086 [P] Create integration test for conversation loading in backend/phase3/tests/test_chat_api.py: verify existing conversation loaded when conversation_id provided
- [x] T087 [P] Create integration test for user data isolation in backend/phase3/tests/test_chat_api.py: attempt to access other user's conversation, verify 403/404
- [x] T088 Create integration test for full chat flow in backend/phase3/tests/test_chat_api.py: user message → AI agent → MCP tool execution → assistant response persisted
- [x] T089 Create integration test for error scenarios in backend/phase3/tests/test_chat_api.py: test 400 (invalid message), 401 (no JWT), 403 (user_id mismatch), 404 (conversation not found)
- [x] T090 Test MCP client can invoke all 5 MCP tools successfully via HTTP
- [x] T091 Test conversation history sliding window (last 10 messages) loads correctly
- [x] T092 Test database transactions: if AI agent fails, user message still persisted (can retry)

**Milestone 3 Checkpoint**: Chat API Working - POST /api/{user_id}/chat returns responses, conversation history persists, AI agent selects correct tools, MCP tools execute successfully

---

### Phase 2.5: ChatKit Frontend Implementation (Agent 4)

**Agent**: chatkit-frontend-builder-skill.md
**Dependencies**: Phase 2.4 (Chat API working)
**Duration**: 3-5 days

- [x] T093 Create ChatKit configuration in frontend/src/lib/chatkit-config.ts (OpenAI ChatKit setup, custom API endpoint override, domain allowlist)
- [x] T094 Create chat API client in frontend/src/lib/api/chat.ts (POST /api/{user_id}/chat, handle request/response, error handling)
- [x] T095 Create MessageList component in frontend/src/components/chat/MessageList.tsx (display conversation history, role-based styling, tool calls display)
- [x] T096 Create MessageInput component in frontend/src/components/chat/MessageInput.tsx (user input field, send button, keyboard shortcuts)
- [x] T097 Create LoadingIndicator component in frontend/src/components/chat/LoadingIndicator.tsx (shown during AI processing, animated spinner)
- [x] T098 Create ErrorDisplay component in frontend/src/components/chat/ErrorDisplay.tsx (display API errors, network errors, retry button)
- [x] T099 Create EmptyState component in frontend/src/components/chat/EmptyState.tsx (shown for new conversations, sample prompts)
- [x] T100 Create chat page in frontend/src/app/chat/page.tsx (protected route, load conversation history, integrate chat components)
- [x] T101 Add authentication check to chat page: redirect to login if not authenticated (use Phase II Better Auth)
- [x] T102 Implement conversation state management in chat page: track current conversation_id, messages array, loading state, error state
- [x] T103 Implement message sending in chat page: call chat API, update messages array, handle loading/error states
- [x] T104 Implement scroll behavior in MessageList: preserve scroll position when new messages arrive, auto-scroll to bottom for new messages
- [x] T105 Implement tool calls display in MessageList: show MCP tools executed with parameters and results (optional debug view)
- [x] T106 Configure domain allowlist in frontend/.env.local: NEXT_PUBLIC_OPENAI_DOMAIN_KEY for OpenAI ChatKit
- [x] T107 Add ChatKit CSS/theme customization in frontend/src/lib/chatkit-config.ts (match Phase II design, Tailwind integration)
- [x] T108 Create component test for MessageList in frontend/src/components/chat/__tests__/MessageList.test.tsx (render user/assistant messages, role styling)
- [x] T109 [P] Create component test for MessageInput in frontend/src/components/chat/__tests__/MessageInput.test.tsx (input validation, send on Enter, button click)
- [x] T110 [P] Create component test for LoadingIndicator in frontend/src/components/chat/__tests__/LoadingIndicator.test.tsx (renders during loading state)
- [x] T111 [P] Create component test for ErrorDisplay in frontend/src/components/chat/__tests__/ErrorDisplay.test.tsx (renders error message, retry button)
- [x] T112 Create integration test for chat page in frontend/src/app/chat/__tests__/page.test.tsx (mock API, verify message flow)
- [x] T113 Test chat UI on desktop browsers (Chrome, Firefox, Safari) for correct rendering
- [x] T114 Test chat UI on mobile browsers (iOS Safari, Chrome Android) for responsive layout

**Milestone 4 Checkpoint**: Frontend Working - Chat UI renders messages, user can send messages, assistant responses display, tool calls visible (optional debug)

---

**Checkpoint for User Story 1**: At this point, User Story 1 (Natural Language Task Management P1) should be fully functional end-to-end. Users can create, list, update, complete, and delete tasks via natural language chat.

---

## Phase 4: User Story 2 - Multi-Turn Conversation Context (Priority: P1)

**Goal**: Users can have multi-turn conversations where the AI remembers previous context within the session

**Independent Test**: Start conversation, create task in message 1, reference task using pronoun in message 3 ("mark it as done"). System should resolve reference using conversation history.

**Dependencies**: User Story 1 (Phase 2.1-2.5) complete

- [ ] T115 [US2] Verify conversation history sliding window implementation in chat_service.py (last 10 messages loaded)
- [ ] T116 [US2] Verify AI agent context resolution in orchestrator.py (pronouns, relative references resolved from history)
- [ ] T117 [US2] Create integration test for multi-turn context in backend/phase3/tests/test_chat_api.py: message 1 creates task, message 2 references "that task", verify resolution
- [ ] T118 [US2] Create integration test for pronoun resolution in backend/phase3/tests/test_agent_integration.py: test "the first one", "it", "that" resolved correctly
- [ ] T119 [US2] Test conversation context works across 10+ messages: verify oldest messages dropped from context window
- [ ] T120 [US2] Test context resolution handles multiple entities: verify agent can distinguish "the grocery task" from "the meeting task" using history
- [ ] T121 [US2] Add conversation context examples to frontend/src/components/chat/EmptyState.tsx (show users multi-turn capability)

**Checkpoint for User Story 2**: Multi-turn conversations work correctly. Users can reference previous messages using pronouns and relative references.

---

## Phase 5: User Story 3 - Persistent Conversation History (Priority: P2)

**Goal**: Users can return to previous conversations and continue where they left off, with full history preserved

**Independent Test**: Create conversation, log out, log back in, verify conversation appears in history and can be resumed with context intact

**Dependencies**: User Story 1, 2 complete

- [ ] T122 [US3] Create conversation list endpoint in backend/phase3/routers/chat.py: GET /api/{user_id}/conversations (list user's conversations)
- [ ] T123 [US3] Implement conversation list query in chat_service.py: filter by user_id, order by updated_at DESC, paginate
- [ ] T124 [US3] Create conversation history sidebar in frontend/src/components/chat/ConversationHistory.tsx (list conversations, select to load)
- [ ] T125 [US3] Implement conversation loading in chat page: when user selects conversation from history, load all messages for that conversation
- [ ] T126 [US3] Implement conversation title auto-generation in chat_service.py: derive title from first user message (first 50 chars)
- [ ] T127 [US3] Add "New Conversation" button to chat page: clear current conversation, start fresh conversation
- [ ] T128 [US3] Add conversation delete functionality in frontend: delete conversation and all messages (cascade delete)
- [ ] T129 [US3] Create integration test for conversation list in backend/phase3/tests/test_chat_api.py: verify user sees only their conversations
- [ ] T130 [US3] Create integration test for conversation persistence in backend/phase3/tests/test_chat_api.py: create conversation, verify persisted, load in new session
- [ ] T131 [US3] Test conversation history displays correctly in frontend: verify conversations sorted by last updated
- [ ] T132 [US3] Test conversation switching in frontend: verify messages cleared when switching conversations

**Checkpoint for User Story 3**: Conversation history persists correctly. Users can view conversation list, select conversations, and resume where they left off.

---

## Phase 6: User Story 4 - Error Recovery and Clarification (Priority: P2)

**Goal**: When AI cannot determine user intent or encounters errors, it asks for clarification instead of guessing or failing silently

**Independent Test**: Send ambiguous command "update the task" without specifying which task. System should ask "Which task would you like to update?" with available options.

**Dependencies**: User Story 1, 2, 3 complete

- [ ] T133 [US4] Verify ambiguity handling in orchestrator.py: when confidence < 70%, generate clarification question
- [ ] T134 [US4] Implement clarification response generation in orchestrator.py: list matching options when multiple tasks match user query
- [ ] T135 [US4] Create integration test for ambiguity handling in backend/phase3/tests/test_agent_integration.py: "delete the task" with 3 matches, verify clarification asked
- [ ] T136 [US4] Create integration test for error recovery in backend/phase3/tests/test_chat_api.py: attempt to complete non-existent task, verify user-friendly error message
- [ ] T137 [US4] Test clarification flow end-to-end: user sends ambiguous request, AI lists options, user clarifies, AI executes correct action
- [ ] T138 [US4] Test error messages are user-friendly: verify no stack traces, no technical jargon, actionable suggestions provided
- [ ] T139 [US4] Add error recovery examples to frontend/src/components/chat/EmptyState.tsx (show users how AI handles errors)

**Checkpoint for User Story 4**: Error recovery and clarification work correctly. AI asks questions when unsure, provides user-friendly error messages.

---

## Phase 7: User Story 5 - Task Creation with All Metadata (Priority: P2)

**Goal**: Users can specify all task attributes (title, description, priority, due date, tags) in a single natural language command

**Independent Test**: Send message "Create a high priority task to finish the report by Friday, tagged as work and urgent, with description 'Complete Q4 financial analysis'". Verify all attributes correctly extracted and saved.

**Dependencies**: User Story 1 complete

- [ ] T140 [US5] Enhance entity extraction in orchestrator.py: extract description, priority, due_date, tags from single natural language command
- [ ] T141 [US5] Implement relative date parsing in orchestrator.py: convert "tomorrow", "next Monday", "Friday" to absolute ISO 8601 dates
- [ ] T142 [US5] Implement tag extraction in orchestrator.py: parse "tagged as work and urgent" to ["work", "urgent"]
- [ ] T143 [US5] Implement priority extraction in orchestrator.py: recognize "high priority", "urgent" → priority="high", "low priority" → priority="low"
- [ ] T144 [US5] Create integration test for full metadata extraction in backend/phase3/tests/test_agent_integration.py: verify all attributes extracted correctly
- [ ] T145 [US5] Test complex task creation: "Add high priority task to call John tomorrow at 3pm, tagged as follow-up" → verify all fields set
- [ ] T146 [US5] Test default values: when priority not specified, verify default priority or clarification asked
- [ ] T147 [US5] Test relative date accuracy: "next Monday" converts to correct absolute date based on current date

**Checkpoint for User Story 5**: Task creation with all metadata works. AI extracts title, description, priority, due_date, tags from natural language.

---

## Phase 8: User Story 6 - Bulk Operations via Natural Language (Priority: P3)

**Goal**: Users can perform bulk actions on multiple tasks using natural language filters

**Independent Test**: Create 5 tasks with tag "shopping", send "Complete all shopping tasks", verify all 5 tasks marked complete with single command

**Dependencies**: User Story 1 complete

- [ ] T148 [US6] Implement bulk operation support in orchestrator.py: recognize "all tasks with tag X", "all overdue tasks", "all completed tasks"
- [ ] T149 [US6] Implement bulk complete_task in orchestrator.py: list tasks matching filter, complete all in loop, aggregate results
- [ ] T150 [US6] Implement bulk delete_task in orchestrator.py: list tasks matching filter, ask confirmation, delete all if confirmed
- [ ] T151 [US6] Implement bulk update_task in orchestrator.py: list tasks matching filter, apply update to all
- [ ] T152 [US6] Add confirmation prompt for destructive bulk operations (delete, archive): "This will delete 10 tasks. Are you sure?"
- [ ] T153 [US6] Create integration test for bulk operations in backend/phase3/tests/test_agent_integration.py: "complete all shopping tasks", verify all completed
- [ ] T154 [US6] Test bulk operation limits: verify reasonable limit (e.g., max 100 tasks per bulk operation) to prevent performance issues
- [ ] T155 [US6] Test bulk operation feedback: verify AI reports "I've completed 5 tasks" with count

**Checkpoint for User Story 6**: Bulk operations work. Users can complete, delete, or update multiple tasks with single natural language command.

---

## Phase 9: User Story 7 - Mobile-Responsive Chat Interface (Priority: P3)

**Goal**: Chat interface adapts seamlessly to mobile devices with touch-optimized interactions

**Independent Test**: Open chat page on mobile device, send messages, scroll through history, verify all interactions work smoothly on small screens

**Dependencies**: User Story 1 (Phase 2.5 Frontend) complete

- [ ] T156 [US7] Add responsive CSS to MessageList component: adjust layout for small screens, increase touch target sizes
- [ ] T157 [US7] Add responsive CSS to MessageInput component: handle mobile keyboard, prevent input obscuring messages
- [ ] T158 [US7] Add responsive CSS to chat page layout: stack conversation history sidebar on mobile, use bottom sheet or modal
- [ ] T159 [US7] Optimize scroll performance for mobile in MessageList: use virtual scrolling for long conversations
- [ ] T160 [US7] Test chat UI on mobile browsers (iOS Safari, Chrome Android): verify keyboard behavior, scroll performance, touch interactions
- [ ] T161 [US7] Test message wrapping on mobile: verify long messages wrap correctly, remain readable on small screens
- [ ] T162 [US7] Test conversation switching on mobile: verify sidebar accessible, touch targets large enough

**Checkpoint for User Story 7**: Mobile-responsive chat works. UI adapts to mobile screens, keyboard doesn't obscure input, performance smooth.

---

## Phase 10: End-to-End Integration & Testing

**Purpose**: Comprehensive testing across all user stories, Phase II regression testing, performance benchmarking

**Dependencies**: All user stories complete

- [ ] T163 Create E2E test for complete chat flow in tests/e2e/test_chat_flow.spec.ts (Playwright): login, navigate to /chat, send message, verify response
- [ ] T164 [P] Create E2E test for task creation via chat in tests/e2e/test_chat_flow.spec.ts: create task via chat, verify appears in Phase II dashboard
- [ ] T165 [P] Create E2E test for multi-turn conversation in tests/e2e/test_chat_flow.spec.ts: send 3 messages, verify context maintained
- [ ] T166 Create Phase II regression test suite: run all Phase II tests, verify 100% pass (zero regression)
- [ ] T167 Test Phase II dashboard shows chat-created tasks: create task via chat, verify appears in dashboard task list
- [ ] T168 Test Phase II task CRUD still works: create, update, complete, delete task via dashboard, verify functionality unchanged
- [ ] T169 Create performance benchmark test: measure p95 latency for POST /api/{user_id}/chat (target <3s including Gemini API)
- [ ] T170 [P] Create performance benchmark test: measure MCP tool execution time (target <500ms p95)
- [ ] T171 Create load test: simulate 50 concurrent chat requests, verify system handles load without errors
- [ ] T172 Create security test: attempt prompt injection attacks ("Ignore previous instructions"), verify blocked
- [ ] T173 [P] Create security test: attempt cross-user data access (user A tries to access user B's conversation), verify 403/404
- [ ] T174 Test Gemini API error handling with real errors: trigger rate limit (15 RPM exceeded), verify exponential backoff retry
- [ ] T175 Test graceful degradation: stop Gemini API mock, verify user-friendly fallback message ("Chat temporarily unavailable")
- [ ] T176 Test database transaction rollback: simulate AI agent failure after user message persisted, verify user can retry
- [ ] T177 Verify all error messages user-friendly: no stack traces exposed, actionable suggestions provided

**Checkpoint**: E2E Integration Complete - All user stories work end-to-end, Phase II regression tests pass, performance targets met

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, documentation, deployment preparation

- [ ] T178 [P] Update project README.md with Phase III overview, features, setup instructions
- [ ] T179 [P] Create ARCHITECTURE.md documentation: explain 5-agent architecture, data flow, MCP protocol usage
- [ ] T180 Create API_REFERENCE.md documentation: document POST /api/{user_id}/chat endpoint with examples
- [ ] T181 Create DEPLOYMENT.md guide: MCP server deployment, environment variables, database migrations, monitoring
- [ ] T182 Test quickstart.md instructions: follow guide from scratch, verify all steps work
- [ ] T183 Add logging for chat operations in chat_service.py: log user messages, AI responses, tool executions (with user_id for traceability)
- [ ] T184 Add monitoring alerts in backend: alert on high error rate, slow response time, Gemini API failures
- [ ] T185 Add feature flag for Phase III in backend/.env: PHASE_III_ENABLED=true/false for gradual rollout
- [ ] T186 Create database backup script: automated hourly backups during Phase III rollout
- [ ] T187 Code cleanup: remove unused imports, add type hints to untyped functions, format with black/prettier
- [ ] T188 Security hardening: run security scan (bandit for Python, npm audit for frontend), fix vulnerabilities
- [ ] T189 Performance optimization: add database query indexes if needed, optimize slow queries
- [ ] T190 Create rollback procedure documentation: steps to disable Phase III, revert migrations, restore Phase II
- [ ] T191 Run final validation against completion criteria: verify all 40+ checklist items complete
- [ ] T192 Create demo video or screenshots: show Phase III chat functionality for stakeholders

**Checkpoint**: Polish Complete - Documentation ready, deployment guide tested, monitoring configured, security hardened

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user story implementation
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) - Agent execution order: MCP Server (2.1) → Gemini Controller (2.2) → AI Agent Logic (2.3) → Chat API (2.4) → ChatKit Frontend (2.5)
- **User Story 2 (Phase 4)**: Depends on User Story 1 (Phase 2.1-2.5) - Enhances conversation context
- **User Story 3 (Phase 5)**: Depends on User Story 1, 2 - Adds conversation persistence
- **User Story 4 (Phase 6)**: Depends on User Story 1, 2, 3 - Adds error recovery
- **User Story 5 (Phase 7)**: Depends on User Story 1 - Enhances task creation
- **User Story 6 (Phase 8)**: Depends on User Story 1 - Adds bulk operations
- **User Story 7 (Phase 9)**: Depends on User Story 1 (Phase 2.5 Frontend) - Mobile optimization
- **E2E Integration (Phase 10)**: Depends on all desired user stories complete
- **Polish (Phase 11)**: Depends on E2E Integration complete

### Critical Path (5-Week Execution)

**Week 1**: Setup (Phase 1) + Foundational (Phase 2) + MCP Server (Phase 2.1)
**Week 2**: Gemini Controller (Phase 2.2) + AI Agent Logic (Phase 2.3)
**Week 3**: Chat API + MCP Bridge (Phase 2.4)
**Week 4**: ChatKit Frontend (Phase 2.5) + User Story 2-5 enhancements
**Week 5**: User Story 6-7 + E2E Integration (Phase 10) + Polish (Phase 11)

### Parallel Opportunities

- **Phase 1 (Setup)**: T001-T003 can run in parallel (different directories)
- **Phase 1 (Setup)**: T004-T005 can run in parallel (backend vs frontend dependencies)
- **Phase 2.1 (MCP Server)**: T029-T033 tests can run in parallel (different tools)
- **Phase 2.2 (Gemini)**: T037-T038 can run in parallel (client vs config)
- **Phase 2.2 (Gemini)**: T047-T049 tests can run in parallel (different modules)
- **Phase 2.4 (Chat API)**: T085-T087 tests can run in parallel (different test scenarios)
- **Phase 2.5 (Frontend)**: T108-T111 tests can run in parallel (different components)
- **Phase 10 (E2E)**: T164-T165 can run in parallel (different E2E flows)
- **Phase 10 (E2E)**: T172-T173 security tests can run in parallel (different attack vectors)
- **Phase 11 (Polish)**: T178-T180 documentation can run in parallel (different docs)

**Agent Parallelization**: Once Foundational (Phase 2) is complete, Phase 2.1 (MCP Server) can start. Once MCP Server completes, Phase 2.2 (Gemini) and Phase 2.5 (Frontend with mocked API) can start in parallel.

---

## Parallel Example: Phase 2.1 MCP Server Tests

```bash
# Launch all MCP tool tests together (T029-T033):
Task: "Unit tests for add_task in backend/mcp_server/tests/test_task_tools.py"
Task: "Unit tests for list_tasks in backend/mcp_server/tests/test_task_tools.py"
Task: "Unit tests for update_task in backend/mcp_server/tests/test_task_tools.py"
Task: "Unit tests for complete_task in backend/mcp_server/tests/test_task_tools.py"
Task: "Unit tests for delete_task in backend/mcp_server/tests/test_task_tools.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T018) - CRITICAL - blocks all implementation
3. Complete Phase 3: User Story 1 (T019-T114) - All 5 agents
   - Phase 2.1: MCP Server (T019-T036)
   - Phase 2.2: Gemini Controller (T037-T051)
   - Phase 2.3: AI Agent Logic (T052-T067)
   - Phase 2.4: Chat API (T068-T092)
   - Phase 2.5: ChatKit Frontend (T093-T114)
4. **STOP and VALIDATE**: Test User Story 1 independently end-to-end
5. Deploy/demo if ready - MVP complete!

### Incremental Delivery (Recommended)

1. Complete Setup + Foundational → Foundation ready (T001-T018)
2. Add User Story 1 → Test independently → Deploy/Demo (T019-T114) - **MVP!**
3. Add User Story 2 → Test independently → Deploy/Demo (T115-T121)
4. Add User Story 3 → Test independently → Deploy/Demo (T122-T132)
5. Add User Story 4 → Test independently → Deploy/Demo (T133-T139)
6. Add User Story 5 → Test independently → Deploy/Demo (T140-T147)
7. Add User Story 6 (optional) → Deploy/Demo (T148-T155)
8. Add User Story 7 (optional) → Deploy/Demo (T156-T162)
9. Complete E2E Integration + Polish → Production ready (T163-T192)

Each user story adds value without breaking previous stories.

---

## Notes

- **[P] tasks** = Different files, no dependencies, can run in parallel
- **[Story] label** (US1, US2, etc.) maps task to specific user story for traceability
- **Phase II Protection**: ZERO modifications to Phase II code - all changes in backend/phase3/, backend/mcp_server/, frontend/src/app/chat/, frontend/src/components/chat/
- **Agent Skills**: 5 agents defined in .claude/skills/ (mcp-server-builder, chat-mcp-bridge, phase3-mcp-orchestrator, chatkit-frontend-builder, gemini-llm-controller)
- **Testing Strategy**: Mock Gemini for unit/integration tests (USE_MOCK_GEMINI=true), real Gemini for E2E tests (with free tier rate limits)
- **Commit Frequency**: Commit after each logical task group or milestone checkpoint
- **Stop at Checkpoints**: Validate story independence before proceeding to next priority
- **Avoid**: Vague tasks, same file conflicts, cross-story dependencies that break independence, modifications to Phase II files

---

**Total Tasks**: 192 tasks across 11 phases
**Estimated Duration**: 5 weeks (35 days)
**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1) = T001-T114 = 114 tasks (~3 weeks)
**Full Phase III Scope**: All 192 tasks (~5 weeks)

---

**Tasks Version**: 1.0.0
**Last Updated**: 2026-01-23
**Next Step**: Begin implementation with Phase 1 (Setup) - T001-T008
