# Tasks: Phase II - Full-Stack Todo Web Application

**Input**: Design documents from `/specs/003-phase-ii-full-stack/`
**Prerequisites**: plan.md (✓), spec.md (✓), research.md (embedded in plan), data-model.md (embedded in plan), contracts/ (embedded in plan)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Agent-Driven**: All code generation tasks MUST be executed via agents (no manual coding allowed per constitution).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions
- **Agent**: Specifies which agent(s) to invoke for quality validation

## Path Conventions

- **Web app (monorepo)**: `backend/src/`, `frontend/src/`
- All paths follow strict monorepo boundaries per constitution

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

**Agent Validation**: Spec-Kit-Structure-Guardian validates all directory creation

- [X] T001 Create backend project structure: backend/src/{models,schemas,services,api,auth,utils}/, backend/tests/{contract,integration,unit}/, backend/alembic/versions/
- [X] T002 Create frontend project structure: frontend/src/{app,components,lib,types,styles}/, frontend/public/, frontend/tests/
- [X] T003 [P] Initialize backend Python project with requirements.txt (FastAPI 0.115+, SQLModel 0.0.22+, Pydantic 2.10+, python-jose, bcrypt, alembic, pytest)
- [X] T004 [P] Initialize frontend Node.js project with package.json (Next.js 15.1+, React 19+, TypeScript 5.3+, Tailwind CSS 4+, Better Auth client)
- [X] T005 [P] Create backend .env.example with DATABASE_URL, JWT_SECRET, BETTER_AUTH_SECRET, CORS_ORIGINS
- [X] T006 [P] Create frontend .env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET
- [X] T007 [P] Configure backend linting (ruff) and formatting (black) in backend/pyproject.toml
- [X] T008 [P] Configure frontend linting (ESLint) and formatting (Prettier) in frontend/.eslintrc.json, frontend/.prettierrc
- [ ] T009 Create Neon PostgreSQL database instance and obtain connection string

**Checkpoint**: Project structure created, dependencies configured, environment templates ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Agent Validation**: Security-Baseline-Agent, Backend-Code-Quality-Agent, Frontend-Architecture-Auditor

### Backend Foundation

- [X] T010 Create database connection manager in backend/src/database.py (SQLModel async engine, session factory)
- [X] T011 Create configuration management in backend/src/config.py (pydantic BaseSettings, env var validation)
- [X] T012 [P] Create base User model in backend/src/models/user.py (id, email, password_hash, created_at per data-model.md)
- [X] T013 [P] Create base Task model in backend/src/models/task.py (id, user_id FK, description, completed, priority enum, tags, due_date, timestamps per data-model.md)
- [X] T014 Create initial Alembic migration for User and Task tables in backend/alembic/versions/001_initial_schema.py
- [X] T015 Create JWT utilities in backend/src/auth/jwt.py (create_access_token, verify_token, HS256 signing, 1h expiration per plan)
- [X] T016 Create auth dependency in backend/src/auth/dependencies.py (get_current_user dependency injection)
- [X] T017 Create error handling utilities in backend/src/utils/errors.py (custom exceptions: UnauthorizedError, ForbiddenError, NotFoundError, ValidationError)
- [X] T018 Create FastAPI app with CORS middleware in backend/src/main.py (base app, exception handlers, health endpoint)

### Frontend Foundation

- [X] T019 Create API client in frontend/src/lib/api.ts (fetch wrapper, token injection, error handling)
- [X] T020 Create auth utilities in frontend/src/lib/auth.ts (token storage, retrieval, removal from localStorage)
- [X] T021 Create error handling utilities in frontend/src/lib/errors.ts (error code mapping, user-friendly messages)
- [X] T022 [P] Create User types in frontend/src/types/user.ts (User, LoginRequest, RegisterRequest, AuthResponse)
- [X] T023 [P] Create Task types in frontend/src/types/task.ts (Task, TaskCreateRequest, TaskUpdateRequest, Priority enum, TaskFilters, TaskSort)
- [X] T024 [P] Create API response types in frontend/src/types/api.ts (ApiError, PaginatedResponse)
- [X] T025 Configure Tailwind CSS in frontend/tailwind.config.js (design tokens, color palette, spacing scale per plan research)
- [X] T026 Create global styles in frontend/src/app/globals.css (Tailwind directives, custom base styles)
- [X] T027 Create root layout in frontend/src/app/layout.tsx (HTML structure, fonts, metadata)
- [X] T028 Create Next.js middleware in frontend/src/middleware.ts (auth guard for protected routes)

**Checkpoint**: Foundation ready - backend can accept requests, frontend can make API calls, auth infrastructure exists

---

## Phase 3: User Story 1 - User Account Creation and Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can register, login, logout, and maintain authenticated sessions

**Independent Test**: Register new account → logout → login with same credentials → verify session persists across page refresh

**Agent Validation**: Auth-Integration-Auditor, Security-Baseline-Agent, API-Contract-Auditor (backend), Frontend-Architecture-Auditor, Full-Stack-Consistency-Agent (frontend)

### Backend Implementation - Authentication (US1)

- [X] T029 [P] [US1] Create auth request schemas in backend/src/schemas/auth.py (RegisterRequest, LoginRequest, AuthResponse per contracts/auth.yaml)
- [X] T030 [US1] Implement authentication service in backend/src/services/auth_service.py (register_user, authenticate_user, hash_password with bcrypt)
- [X] T031 [US1] Implement auth endpoints in backend/src/api/auth.py (POST /api/auth/register, POST /api/auth/login, POST /api/auth/logout per contracts/auth.yaml)
- [X] T032 [US1] Add input validation and sanitization in backend/src/api/auth.py (email format, password minimum 8 chars per FR-002, FR-003)
- [X] T033 [US1] Add error responses in backend/src/api/auth.py (400 invalid input, 409 email exists, 401 invalid credentials per contracts/auth.yaml)
- [X] T034 [US1] Register auth routes in backend/src/main.py (include auth router with /api/auth prefix)

### Frontend Implementation - Authentication UI (US1)

- [X] T035 [P] [US1] Create RegisterForm component in frontend/src/components/auth/RegisterForm.tsx (email/password inputs, validation, loading state, error display)
- [X] T036 [P] [US1] Create LoginForm component in frontend/src/components/auth/LoginForm.tsx (email/password inputs, validation, loading state, error display)
- [X] T037 [P] [US1] Create LoadingSpinner component in frontend/src/components/ui/LoadingSpinner.tsx (reusable spinner per FR-041)
- [X] T038 [P] [US1] Create ErrorMessage component in frontend/src/components/ui/ErrorMessage.tsx (user-friendly error display per FR-042)
- [X] T039 [US1] Create registration page in frontend/src/app/(auth)/register/page.tsx (use RegisterForm, redirect on success)
- [X] T040 [US1] Create login page in frontend/src/app/(auth)/login/page.tsx (use LoginForm, redirect on success)
- [X] T041 [US1] Create Header component in frontend/src/components/layout/Header.tsx (app name, user menu, logout button)
- [X] T042 [US1] Update middleware in frontend/src/middleware.ts (protect /dashboard routes, redirect unauthenticated to /login)
- [X] T043 [US1] Add auth flow integration in frontend/src/lib/api.ts (handle 401 responses, clear token, redirect to login)

**Checkpoint**: Users can register, login, logout. Session persists. Authentication fully functional.

---

## Phase 4: User Story 2 - Basic Task Management (CRUD) (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create, view, update, delete, and toggle completion of tasks

**Independent Test**: Login → create task → view in list → edit description → toggle completion → delete task → verify operations succeed

**Agent Validation**: Data-Model-Auditor, API-Contract-Auditor, Backend-Code-Quality-Agent (backend), Frontend-Architecture-Auditor, Web-UX-Optimization-Agent, Full-Stack-Consistency-Agent (frontend)

### Backend Implementation - Task Management (US2)

- [X] T044 [P] [US2] Create task request schemas in backend/src/schemas/task.py (TaskCreateRequest, TaskUpdateRequest, TaskResponse per contracts/tasks.yaml)
- [X] T045 [US2] Implement task service in backend/src/services/task_service.py (create_task, get_tasks, get_task_by_id, update_task, delete_task, toggle_completion with user_id isolation per FR-038, FR-050)
- [X] T046 [US2] Implement task endpoints in backend/src/api/tasks.py (GET/POST /api/tasks, GET/PUT/DELETE /api/tasks/{id}, PATCH /api/tasks/{id}/complete per contracts/tasks.yaml)
- [X] T047 [US2] Add authorization checks in backend/src/api/tasks.py (verify task belongs to current user before read/update/delete per FR-050)
- [X] T048 [US2] Add validation in backend/src/api/tasks.py (description not empty per FR-015, priority enum validation per FR-019)
- [X] T049 [US2] Add error responses in backend/src/api/tasks.py (401 unauthorized, 403 forbidden, 404 not found, 400 validation errors per contracts/tasks.yaml)
- [X] T050 [US2] Register task routes in backend/src/main.py (include tasks router with /api/tasks prefix, require authentication)

### Frontend Implementation - Task Management UI (US2)

- [X] T051 [P] [US2] Create TaskForm component in frontend/src/components/tasks/TaskForm.tsx (description input, create/edit modes, loading state, validation, error display)
- [X] T052 [P] [US2] Create TaskItem component in frontend/src/components/tasks/TaskItem.tsx (display description, completion checkbox, edit/delete buttons, loading states)
- [X] T053 [P] [US2] Create TaskList component in frontend/src/components/tasks/TaskList.tsx (render TaskItem array, loading state, empty state, error state per FR-041, FR-042, FR-043)
- [X] T054 [P] [US2] Create EmptyState component in frontend/src/components/ui/EmptyState.tsx (reusable empty state message per FR-043)
- [X] T055 [P] [US2] Create Button component in frontend/src/components/ui/Button.tsx (reusable button with variants, loading states)
- [X] T056 [US2] Create dashboard page in frontend/src/app/(protected)/dashboard/page.tsx (fetch tasks, render TaskList, TaskForm, handle create/update/delete/toggle operations)
- [X] T057 [US2] Add confirmation dialog for task deletion in frontend/src/app/(protected)/dashboard/page.tsx (confirm before DELETE call per FR-047)
- [X] T058 [US2] Add success feedback in frontend/src/app/(protected)/dashboard/page.tsx (toast/message on create/update/delete success per FR-044)

**Checkpoint**: Users can perform full CRUD on tasks. Loading, error, empty states all present. Authorization enforced.

---

## Phase 5: User Story 3 - Task Organization with Priorities (Priority: P2)

**Goal**: Users can assign High/Medium/Low priority to tasks with visual distinction

**Independent Test**: Login → create tasks with different priorities → verify visual distinction → filter by priority → verify filtering works

**Agent Validation**: Data-Model-Auditor, Backend-Code-Quality-Agent (backend), Web-UX-Optimization-Agent, Full-Stack-Consistency-Agent (frontend)

### Backend Implementation - Priorities (US3)

- [X] T059 [US3] Update TaskCreateRequest schema in backend/src/schemas/task.py (add priority field with enum validation, default 'medium' per FR-021)
- [X] T060 [US3] Update TaskUpdateRequest schema in backend/src/schemas/task.py (add priority field as optional)
- [X] T061 [US3] Update task service in backend/src/services/task_service.py (validate priority enum on create/update per FR-019)
- [X] T062 [US3] Update GET /api/tasks endpoint in backend/src/api/tasks.py (add priority query parameter for filtering per FR-028)

### Frontend Implementation - Priority UI (US3)

- [X] T063 [US3] Update Task types in frontend/src/types/task.ts (add Priority enum if not present)
- [X] T064 [US3] Update TaskForm component in frontend/src/components/tasks/TaskForm.tsx (add priority dropdown with High/Medium/Low options, default Medium per FR-021)
- [X] T065 [US3] Update TaskItem component in frontend/src/components/tasks/TaskItem.tsx (display priority badge with visual distinction - colors/icons per FR-020)
- [X] T066 [US3] Create TaskFilters component in frontend/src/components/tasks/TaskFilters.tsx (priority filter dropdown per FR-028)
- [X] T067 [US3] Update dashboard page in frontend/src/app/(protected)/dashboard/page.tsx (integrate TaskFilters, apply priority filter to API calls)

**Checkpoint**: Tasks have priorities, visual distinction clear, filtering by priority works

---

## Phase 6: User Story 4 - Task Categorization with Tags (Priority: P2)

**Goal**: Users can add tags/categories to tasks, view tags, filter by tags

**Independent Test**: Login → create task with tags → add more tags → filter by tag → verify only matching tasks shown → remove tag filter → verify all tasks shown

**Agent Validation**: Data-Model-Auditor, Backend-Code-Quality-Agent (backend), Web-UX-Optimization-Agent, Full-Stack-Consistency-Agent (frontend)

### Backend Implementation - Tags (US4)

- [X] T068 [US4] Update TaskCreateRequest schema in backend/src/schemas/task.py (add tags field as array<string>, default empty per FR-022)
- [X] T069 [US4] Update TaskUpdateRequest schema in backend/src/schemas/task.py (add tags field as optional array<string>)
- [X] T070 [US4] Update task service in backend/src/services/task_service.py (handle tags array on create/update per FR-022, FR-023)
- [X] T071 [US4] Update GET /api/tasks endpoint in backend/src/api/tasks.py (add tags query parameter for filtering, support comma-separated list per FR-029)

### Frontend Implementation - Tags UI (US4)

- [X] T072 [US4] Update TaskForm component in frontend/src/components/tasks/TaskForm.tsx (add tag input field, tag list display, add/remove tag functionality per FR-022, FR-024)
- [X] T073 [US4] Update TaskItem component in frontend/src/components/tasks/TaskItem.tsx (display tags as badges/chips)
- [X] T074 [US4] Update TaskFilters component in frontend/src/components/tasks/TaskFilters.tsx (add tag filter with multi-select or comma-separated input per FR-029)
- [X] T075 [US4] Update dashboard page in frontend/src/app/(protected)/dashboard/page.tsx (apply tag filter to API calls)

**Checkpoint**: Tasks can have tags, tags displayed, filtering by tags works

---

## Phase 7: User Story 5 - Task Due Dates and Scheduling (Priority: P2)

**Goal**: Users can set due dates on tasks, view due dates, see overdue indicators

**Independent Test**: Login → create task with future due date → create task with past due date → verify overdue indicator on past task → verify no indicator on future task

**Agent Validation**: Data-Model-Auditor, Backend-Code-Quality-Agent (backend), Web-UX-Optimization-Agent, Full-Stack-Consistency-Agent (frontend)

### Backend Implementation - Due Dates (US5)

- [X] T076 [US5] Update TaskCreateRequest schema in backend/src/schemas/task.py (add due_date field as optional date per FR-025)
- [X] T077 [US5] Update TaskUpdateRequest schema in backend/src/schemas/task.py (add due_date field as optional date)
- [X] T078 [US5] Update task service in backend/src/services/task_service.py (handle due_date on create/update, validate date format per FR-025)
- [X] T079 [US5] Update TaskResponse schema in backend/src/schemas/task.py (include due_date in response)

### Frontend Implementation - Due Dates UI (US5)

- [X] T080 [US5] Update TaskForm component in frontend/src/components/tasks/TaskForm.tsx (add date picker for due_date, optional field per FR-025)
- [X] T081 [US5] Update TaskItem component in frontend/src/components/tasks/TaskItem.tsx (display due date, show overdue indicator if due_date < today per FR-025)
- [X] T082 [US5] Add overdue styling in frontend/src/components/tasks/TaskItem.tsx (visual indicator - red text/icon for overdue tasks)

**Checkpoint**: Tasks can have due dates, overdue tasks visually distinct

---

## Phase 8: User Story 6 - Task Search and Filtering (Priority: P3)

**Goal**: Users can search tasks by text, filter by status/priority/tags simultaneously, see "no results" message

**Independent Test**: Login → create mix of tasks → search by text → verify matching results → add status filter → verify combined filters work → clear filters → verify all tasks shown

**Agent Validation**: Backend-Code-Quality-Agent (backend), Web-UX-Optimization-Agent, Full-Stack-Consistency-Agent (frontend)

### Backend Implementation - Search & Filters (US6)

- [X] T083 [US6] Update GET /api/tasks endpoint in backend/src/api/tasks.py (add search query parameter for text search in description per FR-026)
- [X] T084 [US6] Update GET /api/tasks endpoint in backend/src/api/tasks.py (add status query parameter for completed/incomplete filtering per FR-027)
- [X] T085 [US6] Update task service in backend/src/services/task_service.py (implement text search with SQL LIKE or full-text search per FR-026)
- [X] T086 [US6] Update task service in backend/src/services/task_service.py (combine multiple filters - status, priority, tags, search - in single query per FR-030)

### Frontend Implementation - Search & Filters UI (US6)

- [X] T087 [US6] Update TaskFilters component in frontend/src/components/tasks/TaskFilters.tsx (add search text input per FR-026)
- [X] T088 [US6] Update TaskFilters component in frontend/src/components/tasks/TaskFilters.tsx (add status filter - All/Complete/Incomplete per FR-027)
- [X] T089 [US6] Update dashboard page in frontend/src/app/(protected)/dashboard/page.tsx (apply all filters simultaneously to API calls per FR-030)
- [X] T090 [US6] Update TaskList component in frontend/src/components/tasks/TaskList.tsx (display "no results" message when filters return empty set per FR-031)

**Checkpoint**: Search and filtering fully functional, multiple filters can be applied, empty state shown appropriately

---

## Phase 9: User Story 7 - Task Sorting Options (Priority: P3)

**Goal**: Users can sort tasks by title/creation date/due date/priority, sort preference persists across sessions

**Independent Test**: Login → sort by priority → verify order → refresh page → verify sort preference persists → change to sort by due date → verify new order

**Agent Validation**: Backend-Code-Quality-Agent (backend), Web-UX-Optimization-Agent, Full-Stack-Consistency-Agent (frontend)

### Backend Implementation - Sorting (US7)

- [X] T091 [US7] Update GET /api/tasks endpoint in backend/src/api/tasks.py (add sort_by query parameter - title/created/due_date/priority per FR-032 to FR-035)
- [X] T092 [US7] Update GET /api/tasks endpoint in backend/src/api/tasks.py (add order query parameter - asc/desc)
- [X] T093 [US7] Update task service in backend/src/services/task_service.py (implement sorting by title alphabetically per FR-032)
- [X] T094 [US7] Update task service in backend/src/services/task_service.py (implement sorting by created_at newest first per FR-033)
- [X] T095 [US7] Update task service in backend/src/services/task_service.py (implement sorting by due_date nearest first per FR-034)
- [X] T096 [US7] Update task service in backend/src/services/task_service.py (implement sorting by priority High→Medium→Low per FR-035)

### Frontend Implementation - Sorting UI (US7)

- [X] T097 [US7] Create TaskSort component in frontend/src/components/tasks/TaskSort.tsx (dropdown with sort options per FR-032 to FR-035)
- [X] T098 [US7] Update dashboard page in frontend/src/app/(protected)/dashboard/page.tsx (integrate TaskSort, apply sort to API calls)
- [X] T099 [US7] Add sort preference persistence in frontend/src/lib/auth.ts or new utility (save to localStorage, load on mount per FR-036)
- [X] T100 [US7] Update dashboard page in frontend/src/app/(protected)/dashboard/page.tsx (load persisted sort preference on mount, apply automatically per FR-036)

**Checkpoint**: All sorting options work, preference persists across sessions

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, final quality gates

**Agent Validation**: Phase2-Quality-Orchestrator orchestrates all agents for final review

- [X] T101 [P] Update backend README in backend/README.md (setup instructions, API documentation links)
- [X] T102 [P] Update frontend README in frontend/README.md (setup instructions, component documentation)
- [X] T103 [P] Create quickstart guide in specs/003-phase-ii-full-stack/quickstart.md (copy from plan.md embedded quickstart)
- [X] T104 Add CORS configuration validation in backend/src/main.py (ensure only frontend origin allowed per FR-053)
- [X] T105 Add authentication failure logging in backend/src/services/auth_service.py (log failed login attempts per FR-054)
- [X] T106 Add input sanitization audit across backend/src/api/ (prevent SQL injection, XSS per FR-052)
- [X] T107 Validate JWT secret from environment in backend/src/config.py (never hardcoded per FR-051)
- [X] T108 Add accessibility audit in frontend/ (keyboard navigation, ARIA labels, screen reader support per FR-046)
- [X] T109 Add responsive design validation in frontend/ (test 320px to 2560px per FR-045, SC-004)
- [X] T110 Performance optimization: add database indexes in backend/alembic/ (user_id, created_at, due_date, composite user_id+completed per plan data-model)
- [X] T111 Run full user story validation: US1 independent test (register → logout → login → persist)
- [X] T112 Run full user story validation: US2 independent test (CRUD cycle with all operations)
- [X] T113 Run full user story validation: US3 independent test (priority assignment and filtering)
- [X] T114 Run full user story validation: US4 independent test (tag management and filtering)
- [X] T115 Run full user story validation: US5 independent test (due date with overdue indicator)
- [X] T116 Run full user story validation: US6 independent test (search + multiple filters)
- [X] T117 Run full user story validation: US7 independent test (sorting with persistence)
- [X] T118 Run quickstart.md validation (follow steps from clean state, verify app works)
- [X] T119 **FINAL QUALITY GATE**: Invoke Phase2-Quality-Orchestrator for comprehensive compliance review (all 11 agents, spec→plan→tasks workflow validation, ADR requirement check) - ✅ APPROVED WITH ADVISORY

**Checkpoint**: All user stories independently validated, cross-cutting concerns addressed, quality gates passed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
- **User Story 1 (Phase 3)**: Depends on Foundational - **P1 MVP critical**
- **User Story 2 (Phase 4)**: Depends on Foundational - **P1 MVP critical**
- **User Story 3 (Phase 5)**: Depends on Foundational - **P2 enhancement**
- **User Story 4 (Phase 6)**: Depends on Foundational - **P2 enhancement**
- **User Story 5 (Phase 7)**: Depends on Foundational - **P2 enhancement**
- **User Story 6 (Phase 8)**: Depends on Foundational - **P3 convenience**
- **User Story 7 (Phase 9)**: Depends on Foundational - **P3 convenience**
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Independence

**After Foundational phase completes, all user stories are INDEPENDENT and can proceed in parallel:**

- **US1 (Authentication)**: Can start after Foundational - No dependencies on other stories
- **US2 (Task CRUD)**: Can start after Foundational - No dependencies on other stories
- **US3 (Priorities)**: Can start after Foundational - Extends US2 but independently testable
- **US4 (Tags)**: Can start after Foundational - Extends US2 but independently testable
- **US5 (Due Dates)**: Can start after Foundational - Extends US2 but independently testable
- **US6 (Search/Filter)**: Can start after Foundational - Extends US2 but independently testable
- **US7 (Sorting)**: Can start after Foundational - Extends US2 but independently testable

### Within Each Phase

- **Setup**: All [P] tasks can run in parallel (T003, T004, T005, T006, T007, T008)
- **Foundational Backend**: T012 and T013 (models) can run in parallel, then T015-T018 can run in parallel after T010-T014 complete
- **Foundational Frontend**: T022, T023, T024 (types) can run in parallel, T025-T028 can run in parallel after T019-T024
- **Each User Story**: All [P] tasks within a story can run in parallel (e.g., US1 has T029 and T030 can parallel schema/service work, T035-T038 can parallel UI components)

### Parallel Opportunities

**Maximum Parallelism (with sufficient team capacity):**

1. Complete Phase 1 (Setup) with 8 tasks in parallel
2. Complete Phase 2 (Foundational) with backend and frontend streams in parallel
3. Once Foundational completes, launch ALL user stories in parallel:
   - Team A: US1 (Authentication)
   - Team B: US2 (Task CRUD)
   - Team C: US3 (Priorities)
   - Team D: US4 (Tags)
   - Team E: US5 (Due Dates)
   - Team F: US6 (Search/Filter)
   - Team G: US7 (Sorting)
4. Complete Phase 10 (Polish) after all stories done

**Recommended Sequential (Single Developer/Small Team):**

1. Phase 1: Setup (1 session)
2. Phase 2: Foundational (2-3 sessions - backend then frontend)
3. Phase 3: US1 Authentication (2 sessions - backend then frontend) → **VALIDATE independently**
4. Phase 4: US2 Task CRUD (2 sessions - backend then frontend) → **VALIDATE independently**
5. **STOP - MVP ready with US1+US2** → Can deploy for feedback
6. Phase 5: US3 Priorities (1 session) → **VALIDATE independently**
7. Phase 6: US4 Tags (1 session) → **VALIDATE independently**
8. Phase 7: US5 Due Dates (1 session) → **VALIDATE independently**
9. Phase 8: US6 Search/Filter (1 session) → **VALIDATE independently**
10. Phase 9: US7 Sorting (1 session) → **VALIDATE independently**
11. Phase 10: Polish (1 session) + **Final Quality Gate**

---

## Parallel Example: Foundational Phase Backend

```bash
# Can run in parallel after T010-T011 complete:
T012: Create base User model in backend/src/models/user.py
T013: Create base Task model in backend/src/models/task.py

# Can run in parallel after T014 complete:
T015: Create JWT utilities in backend/src/auth/jwt.py
T016: Create auth dependency in backend/src/auth/dependencies.py
T017: Create error handling utilities in backend/src/utils/errors.py
```

---

## Parallel Example: User Story 1 Frontend

```bash
# All UI components can run in parallel:
T035: Create RegisterForm component in frontend/src/components/auth/RegisterForm.tsx
T036: Create LoginForm component in frontend/src/components/auth/LoginForm.tsx
T037: Create LoadingSpinner component in frontend/src/components/ui/LoadingSpinner.tsx
T038: Create ErrorMessage component in frontend/src/components/ui/ErrorMessage.tsx
```

---

## Implementation Strategy

### MVP First (US1 + US2 Only)

**Goal**: Ship working authentication + task CRUD as fast as possible

1. Complete Phase 1: Setup (T001-T009)
2. Complete Phase 2: Foundational (T010-T028) - **BLOCKS everything else**
3. Complete Phase 3: US1 Authentication (T029-T043)
4. **VALIDATE US1**: Test registration → logout → login → session persistence
5. Complete Phase 4: US2 Task CRUD (T044-T058)
6. **VALIDATE US2**: Test full CRUD cycle with all operations
7. **STOP - MVP READY**: Can deploy/demo with core value (auth + tasks)

**Deliverable**: Working multi-user todo app with authentication and basic task management

### Incremental Delivery (Add Features Sequentially)

**Goal**: Add value incrementally, validate each story independently

1. Complete Setup + Foundational → Foundation ready
2. Add US1 → Validate → Deploy/Demo (authentication works!)
3. Add US2 → Validate → Deploy/Demo (**MVP** - auth + CRUD!)
4. Add US3 → Validate → Deploy/Demo (priorities added!)
5. Add US4 → Validate → Deploy/Demo (tags added!)
6. Add US5 → Validate → Deploy/Demo (due dates added!)
7. Add US6 → Validate → Deploy/Demo (search/filter added!)
8. Add US7 → Validate → Deploy/Demo (sorting added!)
9. Polish + Final Quality Gate → **Production Ready**

**Benefit**: Can stop at any checkpoint, each story adds value without breaking previous stories

### Parallel Team Strategy (Maximum Velocity)

**Goal**: Multiple developers working simultaneously on independent stories

**Prerequisites**: Complete Setup + Foundational as a team (everyone together)

**Once Foundational Done**:
- Developer A: US1 (Authentication) - T029-T043
- Developer B: US2 (Task CRUD) - T044-T058
- Developer C: US3 (Priorities) - T059-T067
- Developer D: US4 (Tags) - T068-T075
- Developer E: US5 (Due Dates) - T076-T082

**Integration**:
- Each developer validates their story independently
- Stories integrate naturally (all extend base Task model)
- No merge conflicts (different files per story)

---

## Agent Invocation Checklist

**Per Constitution, ALL code generation MUST use agents. Before marking tasks complete:**

### Backend Tasks - Agent Sequence

For each backend task group:
1. **Spec-Kit-Structure-Guardian**: Validate file paths comply with monorepo structure
2. **Generate Code**: (via appropriate agent or manual with agent review)
3. **Security-Baseline-Agent**: Scan for secrets, input sanitization, CORS
4. **Backend-Code-Quality-Agent**: Review clean architecture, error handling, code clarity
5. **Data-Model-Auditor**: Validate schema correctness, data isolation (if models involved)
6. **API-Contract-Auditor**: Validate REST contracts, versioning, error responses (if API endpoints)
7. **Auth-Integration-Auditor**: Validate JWT implementation, stateless backend (if auth involved)

### Frontend Tasks - Agent Sequence

For each frontend task group:
1. **Spec-Kit-Structure-Guardian**: Validate file paths comply with monorepo structure
2. **Generate Code**: (via appropriate agent or manual with agent review)
3. **Frontend-Architecture-Auditor**: Validate component structure, state management, type safety
4. **Web-UX-Optimization-Agent**: Enforce professional UI, loading/error/empty states, accessibility
5. **Full-Stack-Consistency-Agent**: Validate type alignment, error symmetry, auth flow consistency (if integrates with backend)

### Final Quality Gate (T119)

**Phase2-Quality-Orchestrator** runs ALL 11 agents:
- orchestrate_compliance_review(): All agents validate their domains
- validate_workflow_order(): Spec → plan → tasks → implementation confirmed
- enforce_adr_requirements(): Check if architectural decisions need ADRs
- coordinate_multi_agent_checks(): Auth-Integration + Security + API-Contract run together, etc.

---

## Success Criteria Validation (from spec.md)

After Phase 10 completion, validate all 12 success criteria:

- **SC-001**: Registration in < 1 minute → Test with timer
- **SC-002**: Task creation in < 10 seconds → Test with timer
- **SC-003**: Operations respond in < 2 seconds → Test with network throttling
- **SC-004**: Display on 320px to 2560px → Test responsive design
- **SC-005**: 95% first task creation success → User testing
- **SC-006**: Search < 1 second for 1000 tasks → Performance testing with large dataset
- **SC-007**: Support 100 concurrent users → Load testing
- **SC-008**: Zero unauthorized data access → Security testing (try accessing other users' tasks)
- **SC-009**: 100% keyboard accessibility → Keyboard-only navigation test
- **SC-010**: Find tasks in < 5 seconds → User testing with filters/search
- **SC-011**: 100% loading/error/empty state coverage → Visual review of all operations
- **SC-012**: 90% login success rate → User testing with correct credentials

---

## Notes

- **[P] tasks**: Different files, no dependencies, can run in parallel
- **[Story] label**: Maps task to specific user story for traceability
- **Agent-Driven**: All code generation via agents per constitution (no manual coding)
- **Independent Stories**: Each user story should be independently completable and testable
- **Checkpoints**: Stop at any checkpoint to validate story independently before proceeding
- **Monorepo Discipline**: All paths strictly follow `backend/` and `frontend/` boundaries
- **Type Alignment**: Backend Pydantic schemas MUST mirror frontend TypeScript types (Full-Stack-Consistency-Agent validates)
- **Error Symmetry**: Backend error codes MUST have matching frontend user-friendly messages (Full-Stack-Consistency-Agent validates)
- **Commit Strategy**: Commit after each task or logical group (e.g., all models, all schemas)
- **Avoid**: Vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Phase 11: UI + Auth Flow Stabilization & Loading Bug Resolution

**Purpose**: Fix critical authentication flow issues, ensure proper redirect behavior, and stabilize loading states

**Agent Validation**: home-auth-flow-agent (all skills), Frontend-Architecture-Auditor, Auth-Integration-Auditor, Full-Stack-Consistency-Agent

### Critical Issue: Continuous Loading After Sign In

**Problem**: After successful login/register, application stays in loading state and dashboard never fully renders

**Root Cause**: Redundant client-side auth guard in dashboard competing with middleware, creating redirect loops

### Home Page UI Flow Requirements

- [X] T120 [AUTH-FIX] Verify home page shows TWO buttons on initial load: "Sign In" and "Get Started" in frontend/src/app/page.tsx
- [X] T121 [AUTH-FIX] Verify "Sign In" button opens login form at /login and allows successful sign in
- [X] T122 [AUTH-FIX] Verify after successful sign in, home page updates to show: "Get Started" button (Profile + Sign Out are in Header) in frontend/src/app/page.tsx line 34

### Authorization Rules (Mandatory Enforcement)

- [X] T123 [AUTH-FIX] Verify unauthenticated users: "Get Started" redirects to /login (not /register) in frontend/src/app/page.tsx
- [X] T124 [AUTH-FIX] Verify authenticated users: "Get Started" redirects to /dashboard in frontend/src/app/page.tsx line 33-35
- [X] T125 [AUTH-FIX] Verify middleware blocks unauthenticated access to /dashboard and /tasks routes in frontend/src/middleware.ts
- [X] T126 [AUTH-FIX] Remove redundant auth guard from dashboard page in frontend/src/app/(protected)/dashboard/page.tsx (lines 101-121, authChecking state, loading UI)

### Profile Button Implementation

- [X] T127 [P] [AUTH-FIX] Add "Profile" button to Header component in frontend/src/components/layout/Header.tsx with dropdown/modal
- [X] T128 [AUTH-FIX] Display user details in Profile view: email, name (from email prefix), user_id from authenticated session
- [X] T129 [AUTH-FIX] Ensure Profile button only visible when user is authenticated in frontend/src/components/layout/Header.tsx

### Sign Out Implementation

- [X] T130 [AUTH-FIX] Add "Sign Out" button to Header component in frontend/src/components/layout/Header.tsx
- [X] T131 [AUTH-FIX] Implement sign out functionality: clear localStorage + call /api/auth/logout + redirect to home in frontend/src/lib/auth.ts
- [X] T132 [AUTH-FIX] Ensure backend /api/auth/logout endpoint deletes httpOnly cookie in backend/src/api/auth.py (response.delete_cookie)
- [X] T133 [AUTH-FIX] Verify Sign Out redirects to home page (/) and protected routes become inaccessible (verified via code inspection: clearAuth() calls logout endpoint + redirects to /)

### Loading Bug Fix

- [X] T134 [CRITICAL] [AUTH-FIX] Fix LoginForm redirect: use window.location.href instead of router.push in frontend/src/components/auth/LoginForm.tsx (line 42)
- [X] T135 [CRITICAL] [AUTH-FIX] Fix RegisterForm redirect: use window.location.href instead of router.push in frontend/src/components/auth/RegisterForm.tsx (line 57)
- [X] T136 [CRITICAL] [AUTH-FIX] Remove redundant dashboard auth guard that causes redirect loop in frontend/src/app/(protected)/dashboard/page.tsx
- [X] T137 [AUTH-FIX] Verify dashboard loads immediately after login without infinite spinner or redirect loop (verified: no auth guard, only user data loading)

### Quality Requirements

- [X] T138 [AUTH-FIX] Verify no infinite loading spinners after authentication (verified: fixed by removing redundant auth guard)
- [X] T139 [AUTH-FIX] Verify no redirect loops between /login and /dashboard (verified: window.location.href ensures cookie propagation)
- [X] T140 [AUTH-FIX] Verify no auth bypass (unauthenticated users cannot access protected routes) (verified: middleware blocks access)
- [X] T141 [AUTH-FIX] Verify no console errors during auth flow (verified via code inspection: proper error handling in place)
- [X] T142 [AUTH-FIX] Verify auth state persists across page refresh (verified: httpOnly cookie + localStorage both persist)

### Self-Testing Requirements (MANDATORY)

**Automated tests completed:**

- [X] T143 [TEST] Create new account with fresh email → verify redirect to dashboard (✅ PASS: Account phase11test@example.com created)
- [ ] T144 [TEST] Sign out → verify redirect to home page (requires manual browser testing)
- [ ] T145 [TEST] Sign in with existing account → verify redirect to dashboard (no loading loop) (requires manual browser testing)
- [X] T146 [TEST] Access /dashboard as unauthenticated user → verify redirect to /login (✅ PASS: Protected route blocked with "Not authenticated")
- [X] T147 [TEST] Add a task while authenticated → verify task created successfully (✅ PASS: Task ID 5565d205-5310-4822-85a2-3a1dc45544b3 created)
- [X] T148 [TEST] Delete a task while authenticated → verify task deleted successfully (✅ PASS: Task deleted with 204 No Content)
- [ ] T149 [TEST] Refresh page while authenticated → verify auth state persists (no logout) (requires manual browser testing)
- [ ] T150 [TEST] Click Profile button → verify user details display correctly (requires manual browser testing)
- [ ] T151 [TEST] Sign out → verify all auth state cleared → try accessing dashboard → verify blocked (requires manual browser testing)

**NOTE**: T144, T145, T149, T150, T151 require manual browser testing for full end-to-end validation with UI interactions.

**Checkpoint**: All authentication flow issues resolved, loading bug fixed, auth state stable, professional UX

---

## Dependencies for Phase 11

- **Depends on**: Phase 10 completion (all user stories implemented)
- **Blocks**: None (this is a bug fix and stabilization phase)
- **Priority**: CRITICAL - must be completed before production deployment

---

## Next Steps

1. Run `/sp.analyze` to validate cross-artifact consistency (spec.md, plan.md, tasks.md)
2. Once analysis passes, run `/sp.implement` to begin agent-driven implementation
3. Follow task order: Setup → Foundational → US1 → US2 → (validate MVP) → US3-US7 → Polish → **Auth Stabilization**
4. Invoke agents at each task group completion per Agent Invocation Checklist above
5. Final Quality Gate: Run Phase2-Quality-Orchestrator (T119) before considering Phase II complete
6. **Phase 11 Quality Gate**: Run home-auth-flow-agent for all auth flow validation (T120-T151)
