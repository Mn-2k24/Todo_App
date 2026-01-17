<!--
  Sync Impact Report:

  Version Change: 1.0.0 → 2.0.0 (MAJOR - Phase II Constitution)

  Modified Principles:
  - Complete rewrite for Phase II Full-Stack Web Application
  - Phase I (Python Console App) → Phase II (Next.js + FastAPI + Neon)
  - Manual code prohibition replaced with Agent + Skills enforcement model

  Added Sections:
  - Phase II Project Overview
  - Agent Registry & Skills Framework
  - Spec-Driven Workflow Enforcement
  - Monorepo Structure Rules (frontend/backend separation)
  - Frontend/UI Governance (Web-UX-Optimization-Agent)
  - Backend/API Governance (API-Contract-Auditor, Auth-Integration-Auditor)
  - Security Rules (JWT, Auth, Data Isolation)
  - Full-Stack Consistency Enforcement
  - Agent-Based Code Generation Rules
  - Phase II Completion Criteria

  Removed Sections:
  - Phase I specific scope (5 features: Add/Delete/Update/View/Mark Complete)
  - Python-specific coding standards
  - Console application requirements
  - In-memory data structure rules
  - Phase I out-of-scope items

  Templates Requiring Updates:
  - ✅ .specify/templates/plan-template.md (aligned - web app structure option exists)
  - ✅ .specify/templates/spec-template.md (aligned - user story prioritization)
  - ✅ .specify/templates/tasks-template.md (aligned - test-first approach, user story organization)
  - ⚠ .specify/templates/commands/*.md (review for Phase II context)

  Follow-up TODOs:
  - Review all command files for Phase II alignment
  - Ensure all agent skill files in .claude/skills/ are complete
  - Create Phase II feature specifications following this constitution
-->

# Full-Stack Todo Web Application Constitution (Phase II)

## Project Purpose

This constitution governs **Phase II** of the Todo Web Application project.

**Goal**: Transform the Phase I console prototype into a production-ready, full-stack web application with user authentication, persistent storage, and modern UI/UX. The application will enable users to manage tasks through a professional web interface with secure multi-user support.

**Phase II Vision**: Deliver a fully functional web application with:
- Modern, responsive frontend (Next.js 15+)
- RESTful API backend (FastAPI)
- Persistent database (Neon PostgreSQL with SQLModel ORM)
- Secure authentication (Better Auth with JWT)
- Professional UI/UX with loading, error, and empty states
- Full CRUD operations with user data isolation
- Type-safe full-stack implementation

**Development Model**: All code generation MUST be driven by agents and skills. Manual coding is prohibited. Agents enforce architecture, security, and quality standards automatically.

---

## Phase II Scope

Phase II expands the five console features into a web application with:

### Core Features (from Phase I)
1. **Add Task**: Create tasks via web form
2. **Delete Task**: Remove tasks with confirmation
3. **Update Task**: Edit task descriptions inline or via modal
4. **View Tasks**: Display tasks in responsive list/card layout
5. **Mark Task Complete/Incomplete**: Toggle completion status with visual feedback

### New Phase II Features
6. **User Authentication**: Sign up, login, logout with JWT tokens
7. **User Registration**: Create account with email and password
8. **User Profile**: View and manage user profile
9. **Protected Routes**: Secure task operations per user
10. **Data Persistence**: Store tasks in Neon PostgreSQL database
11. **Responsive UI**: Mobile-first design with Tailwind CSS
12. **Error Handling**: Graceful error messages and recovery
13. **Loading States**: Spinners and skeletons during async operations
14. **Empty States**: Helpful messages when no tasks exist

### Technology Stack
- **Frontend**: Next.js 15+ (App Router), React 19+, TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python 3.13+), SQLModel, Pydantic
- **Database**: Neon PostgreSQL (serverless)
- **Authentication**: Better Auth (JWT-based, stateless)
- **Deployment**: Vercel (frontend), Railway/Render (backend)
- **Type Safety**: TypeScript (frontend), Python type hints (backend)

### Monorepo Structure
```
Todo_App/
├── frontend/       # Next.js application
├── backend/        # FastAPI application
├── specs/          # Feature specifications
├── .specify/       # SpecKit Plus templates
└── .claude/        # Agent and skill definitions
```

---

## Agent Registry & Skills Framework

Phase II uses **11 specialized agents** to enforce governance, quality, and consistency. All code generation MUST invoke appropriate agents based on the work context.

### Quality & Governance Agents

#### 1. Phase2-Quality-Orchestrator
**Purpose**: Coordinates all agent checks and enforces workflow compliance

**Skills**:
- `orchestrate_compliance_review`: Verifies all required agents ran
- `validate_workflow_order`: Enforces spec → plan → tasks → implementation
- `enforce_adr_requirements`: Ensures architectural decisions are documented
- `coordinate_multi_agent_checks`: Manages dependent agent invocations

**When to invoke**: Before merging, before deployment, after major feature completion

#### 2. Spec-Auditor-Agent
**Purpose**: Validates specifications for completeness and testability

**Skills**:
- `validate_acceptance_criteria`: Ensures measurable criteria exist
- `verify_error_scenarios`: Checks error case documentation
- `audit_spec_completeness`: Validates required spec sections
- `detect_scope_creep`: Blocks undocumented features

**When to invoke**: After `/sp.specify`, before `/sp.plan`

#### 3. Spec-Kit-Structure-Guardian
**Purpose**: Enforces monorepo structure and naming conventions

**Skills**:
- `enforce_directory_structure`: Validates file placement (frontend/, backend/, specs/)
- `validate_naming_conventions`: Checks spec.md, plan.md, tasks.md naming
- `protect_template_integrity`: Prevents template modification
- `verify_artifact_linking`: Ensures spec → plan → tasks references

**When to invoke**: Before creating ANY new file, during file moves/renames

### Backend & API Agents

#### 4. API-Contract-Auditor
**Purpose**: Validates REST API contracts and versioning

**Skills**:
- `validate_rest_contracts`: Checks request/response schemas
- `enforce_versioning_strategy`: Validates breaking vs non-breaking changes
- `audit_error_responses`: Ensures documented error codes
- `verify_idempotency`: Checks retry safety

**When to invoke**: After API endpoint implementation, before API changes

#### 5. Auth-Integration-Auditor
**Purpose**: Enforces JWT authentication and stateless backend

**Skills**:
- `validate_jwt_implementation`: Checks JWT signing, expiration, secrets
- `enforce_stateless_backend`: Blocks server-side sessions
- `audit_authorization_checks`: Verifies user ownership checks
- `verify_token_lifecycle`: Validates token refresh/expiration

**When to invoke**: After auth implementation, before protected endpoint changes

#### 6. Security-Baseline-Agent
**Purpose**: Scans for security vulnerabilities

**Skills**:
- `scan_for_secrets`: Detects hardcoded credentials
- `validate_input_sanitization`: Checks for injection vulnerabilities
- `enforce_cors_policy`: Validates CORS configuration
- `audit_dependency_vulnerabilities`: Scans for CVEs

**When to invoke**: Before commits, before deployment

#### 7. Data-Model-Auditor
**Purpose**: Validates database schemas and data integrity

**Skills**:
- `validate_schema_correctness`: Checks model/schema alignment
- `enforce_data_isolation`: Validates user/tenant filtering
- `audit_migration_safety`: Checks rollback plans
- `verify_data_validation`: Ensures validation rules

**When to invoke**: After model changes, before migrations

#### 8. Backend-Code-Quality-Agent
**Purpose**: Enforces clean architecture in backend

**Skills**:
- `enforce_clean_architecture`: Validates separation of concerns
- `audit_error_handling`: Checks error catching and logging
- `validate_code_clarity`: Reviews function naming and complexity
- `verify_test_coverage`: Ensures business logic tests

**When to invoke**: After backend implementation, during code reviews

### Frontend & Full-Stack Agents

#### 9. Frontend-Architecture-Auditor
**Purpose**: Validates frontend component structure and state management

**Skills**:
- `validate_component_structure`: Checks single-responsibility principle
- `enforce_state_management`: Validates global state patterns
- `audit_api_integration`: Checks typed API calls and error handling
- `verify_type_safety`: Ensures TypeScript strict mode

**When to invoke**: After frontend implementation, during component reviews

#### 10. Web-UX-Optimization-Agent
**Purpose**: Enforces professional, modern UI standards

**Skills**:
- `enforce_professional_ui`: Validates consistent design tokens
- `validate_loading_states`: Checks loading indicators
- `audit_error_states`: Validates user-friendly error messages
- `verify_empty_states`: Checks helpful empty state content
- `enforce_accessibility`: Validates ARIA labels and keyboard navigation

**When to invoke**: After UI implementation, before user testing

#### 11. Full-Stack-Consistency-Agent
**Purpose**: Ensures frontend/backend alignment

**Skills**:
- `validate_type_alignment`: Checks frontend types match backend DTOs
- `audit_error_symmetry`: Validates error code consistency
- `verify_auth_flow_consistency`: Checks token handling alignment
- `enforce_data_flow_integrity`: Validates data transformation consistency

**When to invoke**: After full-stack feature completion, during integration testing

### Agent Invocation Rules

**MANDATORY**: All code generation MUST invoke appropriate agents:

1. **Before any file creation**: Invoke `Spec-Kit-Structure-Guardian`
2. **After spec creation**: Invoke `Spec-Auditor-Agent`
3. **After backend implementation**: Invoke `Backend-Code-Quality-Agent`, `API-Contract-Auditor`, `Security-Baseline-Agent`
4. **After frontend implementation**: Invoke `Frontend-Architecture-Auditor`, `Web-UX-Optimization-Agent`
5. **After full-stack feature**: Invoke `Full-Stack-Consistency-Agent`
6. **Before merge/deployment**: Invoke `Phase2-Quality-Orchestrator`

**Violation Handling**: If any agent reports FAIL or BLOCKED status, code generation MUST stop and issues MUST be resolved before proceeding.

---

## Spec-Driven Workflow Enforcement

All Phase II development MUST follow strict spec-first workflow:

### Rule 1: No Code Without Spec
- Every feature MUST have an approved specification in `specs/<feature-name>/spec.md`
- Specifications MUST pass `Spec-Auditor-Agent` validation
- Implementation MUST NOT begin until spec is approved

### Rule 2: Agent-Driven Code Generation
- **ALL code MUST be generated by Claude Code using agents and skills**
- Manual coding is strictly prohibited
- Direct edits to source files in `frontend/src/` or `backend/src/` are forbidden

### Rule 3: Spec-Plan-Tasks-Implement Workflow
1. **Specify**: Run `/sp.specify` → creates `spec.md`
2. **Validate Spec**: `Spec-Auditor-Agent` must approve
3. **Plan**: Run `/sp.plan` → creates `plan.md`, `research.md`, `data-model.md`, `contracts/`
4. **Tasks**: Run `/sp.tasks` → creates `tasks.md`
5. **Analyze**: Run `/sp.analyze` → validates consistency
6. **Implement**: Run `/sp.implement` → generates code via agents

### Rule 4: Behavior Changes via Spec Updates
To change behavior:
1. Update `spec.md` with new requirements
2. Re-run `/sp.plan` to update plan
3. Re-run `/sp.tasks` to update tasks
4. Re-run `/sp.implement` to regenerate code
5. Validate with appropriate agents

### Rule 5: Traceability
- Every code change MUST trace to spec requirement
- Every task MUST map to user story
- Every commit MUST reference spec/task/issue
- Prompt History Records (PHRs) MUST be created for all major activities

---

## Monorepo Structure Enforcement

Phase II uses strict monorepo boundaries enforced by `Spec-Kit-Structure-Guardian`:

### Frontend Boundary (`/frontend/`)
```
frontend/
├── src/
│   ├── app/              # Next.js App Router pages
│   ├── components/       # React components
│   ├── lib/              # Utilities and helpers
│   ├── types/            # TypeScript type definitions
│   └── styles/           # Global styles
├── public/               # Static assets
├── tests/                # Frontend tests
└── package.json
```

**Rules**:
- All frontend code MUST reside in `frontend/src/`
- No backend logic in frontend (API calls only via `fetch` or client)
- All components MUST be in `components/` subdirectories
- Server/Client components MUST be explicitly marked

### Backend Boundary (`/backend/`)
```
backend/
├── src/
│   ├── models/          # SQLModel database models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── services/        # Business logic
│   ├── api/             # FastAPI route handlers
│   ├── auth/            # Authentication logic
│   └── utils/           # Backend utilities
├── tests/               # Backend tests
├── alembic/             # Database migrations
└── requirements.txt
```

**Rules**:
- All backend code MUST reside in `backend/src/`
- No frontend logic in backend
- Business logic MUST be in `services/`, NOT in route handlers
- Database models MUST be in `models/`, separate from schemas

### Specs Boundary (`/specs/`)
```
specs/
└── <feature-name>/
    ├── spec.md
    ├── plan.md
    ├── tasks.md
    ├── research.md
    ├── data-model.md
    ├── quickstart.md
    └── contracts/
```

**Rules**:
- One feature per directory
- Follow naming convention: `<###>-<feature-name>/`
- All specs MUST follow template structure

### Root Level Files
```
Todo_App/
├── README.md            # Project overview
├── CLAUDE.md            # Claude Code rules
├── .gitignore
└── .env.example         # Environment template
```

**Rules**:
- No source code at root level
- No utility directories like `utils/` or `lib/` at root
- Configuration files only at root

### Violation Handling
- `Spec-Kit-Structure-Guardian` MUST block any file creation outside these boundaries
- Claude Code MUST consult guardian before creating ANY new file
- Violations MUST be corrected before proceeding

---

## Frontend / UI Governance

All frontend code MUST meet professional UI standards enforced by `Web-UX-Optimization-Agent` and `Frontend-Architecture-Auditor`:

### UI Design Standards

#### Professional Visual Design
- **Design System**: Use consistent design tokens (colors, spacing, typography)
- **Layout**: Responsive grid with mobile-first approach
- **Spacing**: Consistent padding/margin using Tailwind scale (4, 8, 12, 16, 24, 32px)
- **Typography**: Clear hierarchy with defined font sizes and weights
- **Colors**: Accessible contrast ratios (WCAG 2.1 AA minimum)

#### Loading States (MANDATORY)
- **All async operations MUST show loading indicators**
- Acceptable patterns:
  - Spinners for buttons and small components
  - Skeleton screens for lists and cards
  - Progress bars for multi-step operations
- No blank screens or frozen UI during loading

#### Error States (MANDATORY)
- **All failures MUST show user-friendly error messages**
- Requirements:
  - Clear explanation of what went wrong
  - Actionable guidance on how to recover
  - Retry buttons where appropriate
  - No technical error dumps (stack traces, API errors)
- Examples:
  - ❌ "Error: 500 Internal Server Error"
  - ✅ "We couldn't save your task. Please try again."

#### Empty States (MANDATORY)
- **All empty lists/data MUST show helpful empty states**
- Requirements:
  - Friendly message explaining why empty
  - Call-to-action to add first item
  - Optional illustration or icon
- Example: "No tasks yet. Click 'Add Task' to get started!"

#### Accessibility (MANDATORY)
- **All interactive elements MUST be keyboard accessible**
- **All forms MUST have proper labels**
- **All buttons MUST have descriptive text or aria-labels**
- **Color MUST NOT be the only indicator of state**
- Use semantic HTML where possible

### Component Architecture

#### Component Structure
- **Single Responsibility**: Each component does one thing
- **Maximum Size**: 200 lines (guideline, not hard limit)
- **Props**: Clear, typed interfaces
- **Naming**: Descriptive PascalCase names

#### Server vs Client Components
- **Default to Server Components** where possible
- Use Client Components (`'use client'`) ONLY when:
  - Component uses hooks (useState, useEffect, etc.)
  - Component needs event handlers
  - Component uses browser APIs
- Document why Client Component is needed (comment at top)

#### State Management
- **Local State**: Use `useState` for component-specific state
- **Global State**: Use React Context for shared state
- **Server State**: Use server components and server actions
- **No prop drilling beyond 2 levels** (use context or composition)

#### API Integration
- **All API calls MUST be typed**
- **All API calls MUST handle errors**
- **All API calls MUST show loading states**
- Use typed fetch wrappers or client libraries

### Type Safety

#### TypeScript Standards
- **Strict mode MUST be enabled** in `tsconfig.json`
- **No `any` types** (use `unknown` or proper types)
- **All props MUST be typed**
- **All API responses MUST be typed**

#### Type Definitions
- Define types in `frontend/src/types/`
- Share types between components via imports
- Keep backend and frontend types aligned

### Enforcement

- `Web-UX-Optimization-Agent` MUST validate all UI implementations
- `Frontend-Architecture-Auditor` MUST validate component structure
- Both agents MUST pass before merge

---

## Backend / API Governance

All backend code MUST meet clean architecture and security standards enforced by multiple agents:

### API Contract Standards

#### REST API Design
- **Endpoint Naming**: Use RESTful conventions
  - Collections: `GET /api/tasks`
  - Single Resource: `GET /api/tasks/{id}`
  - Actions: `POST /api/tasks`, `PUT /api/tasks/{id}`, `DELETE /api/tasks/{id}`
- **HTTP Methods**: Use correct verbs (GET, POST, PUT, DELETE, PATCH)
- **Status Codes**: Use appropriate codes
  - 200: Success
  - 201: Created
  - 400: Bad Request
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found
  - 500: Server Error

#### Request/Response Schemas
- **All endpoints MUST have Pydantic schemas**
- **Schemas MUST be in `backend/src/schemas/`**
- **Request validation MUST be automatic** (FastAPI dependency)
- **Response models MUST be explicit** (no raw dicts)

Example:
```python
# backend/src/schemas/task.py
from pydantic import BaseModel

class TaskCreate(BaseModel):
    description: str

class TaskResponse(BaseModel):
    id: int
    description: str
    completed: bool
    user_id: int
```

#### Error Responses
- **All errors MUST return consistent format**:
  ```json
  {
    "error": "Task not found",
    "code": "TASK_NOT_FOUND",
    "status": 404
  }
  ```
- **All error codes MUST be documented** in contracts
- **Client-friendly messages** (no stack traces in production)

#### API Versioning
- **Breaking changes MUST increment version**
- Use path versioning: `/api/v1/tasks`
- Document migration paths for version changes

### Authentication & Authorization

#### JWT Authentication (MANDATORY)
- **All protected endpoints MUST verify JWT**
- **JWT MUST be in Authorization header**: `Bearer <token>`
- **JWT MUST include user ID claim**
- **JWT secret MUST be in environment variable** (never hardcoded)

Example:
```python
# backend/src/auth/dependencies.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)) -> User:
    # Verify JWT and return user
    payload = verify_jwt(token.credentials)
    return get_user(payload["user_id"])
```

#### Stateless Backend (MANDATORY)
- **NO server-side sessions**
- **NO session cookies for auth**
- **ALL state MUST be in JWT or database**
- Auth state travels with request, not stored on server

#### Authorization (MANDATORY)
- **All endpoints MUST check user ownership**
- Users MUST only access their own data
- Filter all queries by user ID

Example:
```python
@router.get("/tasks")
async def get_tasks(current_user: User = Depends(get_current_user)):
    # CORRECT: Filter by user
    return db.query(Task).filter(Task.user_id == current_user.id).all()

    # WRONG: Returns all users' tasks
    # return db.query(Task).all()
```

### Data Model Standards

#### SQLModel Models
- **All models MUST be in `backend/src/models/`**
- **All models MUST inherit from `SQLModel`**
- **All models MUST have `user_id` foreign key** (for user data)
- **All models MUST have validation**

Example:
```python
# backend/src/models/task.py
from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str = Field(min_length=1, max_length=500)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id")
```

#### Data Isolation (MANDATORY)
- **All queries MUST filter by user_id**
- **NO cross-user data access**
- **Validate user owns resource before update/delete**

#### Database Migrations
- **Use Alembic for schema changes**
- **All migrations MUST be reversible**
- **Test migrations on development data**

### Clean Architecture

#### Separation of Concerns
- **Route handlers in `backend/src/api/`**: Handle HTTP only
- **Business logic in `backend/src/services/`**: Reusable logic
- **Data access in `backend/src/models/`**: Database operations
- **NO business logic in route handlers**

Example:
```python
# WRONG: Business logic in route handler
@router.post("/tasks")
async def create_task(task: TaskCreate, user: User = Depends(get_current_user)):
    new_task = Task(description=task.description, user_id=user.id)
    db.add(new_task)
    db.commit()
    return new_task

# CORRECT: Business logic in service
# backend/src/api/tasks.py
@router.post("/tasks")
async def create_task(task: TaskCreate, user: User = Depends(get_current_user)):
    return task_service.create_task(task, user.id)

# backend/src/services/task_service.py
def create_task(task: TaskCreate, user_id: int) -> Task:
    new_task = Task(description=task.description, user_id=user_id)
    db.add(new_task)
    db.commit()
    return new_task
```

#### Error Handling
- **All exceptions MUST be caught**
- **All errors MUST be logged**
- **All errors MUST return appropriate HTTP status**
- Use FastAPI exception handlers for consistency

#### Code Quality
- **Functions MUST be small and focused** (< 50 lines guideline)
- **Clear naming** (intention-revealing)
- **Type hints on all functions**
- **Docstrings for public functions**

### Enforcement

- `API-Contract-Auditor` MUST validate all API contracts
- `Auth-Integration-Auditor` MUST validate JWT and authorization
- `Data-Model-Auditor` MUST validate models and migrations
- `Backend-Code-Quality-Agent` MUST validate architecture
- `Security-Baseline-Agent` MUST scan for vulnerabilities
- ALL agents MUST pass before merge

---

## Security Rules

Security is enforced by `Security-Baseline-Agent` and `Auth-Integration-Auditor`:

### Authentication Security

#### JWT Requirements
- **Algorithm**: Use RS256 or HS256 with strong secret
- **Secret Storage**: Environment variable only (NEVER hardcode)
- **Expiration**: Tokens MUST expire (e.g., 1 hour for access, 7 days for refresh)
- **Claims**: MUST include user ID, issued at, expiration
- **Verification**: MUST verify signature, expiration, and claims

#### Token Lifecycle
- **Access Tokens**: Short-lived (1 hour)
- **Refresh Tokens**: Longer-lived (7 days), stored securely
- **Rotation**: Implement refresh token rotation
- **Revocation**: Support token revocation (blacklist or short expiry)

### Authorization Security

#### Endpoint Protection
- **ALL data endpoints MUST be protected**
- **Verify user owns resource** before access
- **Return 401 for invalid/missing token**
- **Return 403 for insufficient permissions**

#### Data Isolation
- **NEVER trust client-provided user IDs**
- **ALWAYS filter by authenticated user ID**
- **NEVER expose other users' data**

### Input Security

#### Validation
- **Validate all inputs** (Pydantic handles this)
- **Sanitize user content** (escape HTML, SQL)
- **Reject invalid data** with clear errors

#### Injection Prevention
- **Use parameterized queries** (SQLModel ORM handles this)
- **NO raw SQL with string interpolation**
- **NO direct command execution with user input**

### Secret Management

#### Environment Variables
- **ALL secrets MUST be in `.env` files**
- **`.env` MUST be in `.gitignore`**
- **Provide `.env.example` with placeholders**

Example `.env.example`:
```bash
DATABASE_URL=postgresql://user:pass@localhost/dbname
JWT_SECRET=your-secret-key-here
BETTER_AUTH_SECRET=your-auth-secret-here
```

#### Secret Scanning
- **NEVER commit secrets to git**
- **Run `Security-Baseline-Agent.scan_for_secrets()` before commits**
- **Rotate secrets if exposed**

### CORS Policy

#### Configuration
- **PRODUCTION**: Whitelist specific origins only
- **DEVELOPMENT**: Can use `localhost` origins
- **NEVER use `*` (wildcard) in production**

Example:
```python
# backend/src/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Dependency Security

#### CVE Scanning
- **Scan dependencies before deployment**
- **Block deployment with high/critical CVEs**
- **Update dependencies regularly**

#### Minimal Dependencies
- **Only include necessary packages**
- **Review new dependencies before adding**
- **Remove unused dependencies**

### Enforcement

- `Security-Baseline-Agent` MUST pass before ANY commit
- `Auth-Integration-Auditor` MUST validate all auth flows
- Security violations MUST block merge/deployment

---

## Full-Stack Consistency Enforcement

`Full-Stack-Consistency-Agent` ensures frontend and backend remain aligned:

### Type Alignment

#### Shared Type Definitions
- **Frontend types MUST match backend schemas**
- **Use code generation or shared types** where possible
- **Document type mappings** if manual

Example:
```typescript
// frontend/src/types/task.ts
export interface Task {
  id: number;
  description: string;
  completed: boolean;
  user_id: number;
}
```

```python
# backend/src/schemas/task.py
class TaskResponse(BaseModel):
    id: int
    description: str
    completed: bool
    user_id: int
```

#### Type Validation
- `Full-Stack-Consistency-Agent.validate_type_alignment()` MUST verify matches
- Mismatches MUST be resolved before merge

### Error Handling Symmetry

#### Backend Error Codes
- Define standard error codes in backend

Example:
```python
# backend/src/errors.py
class ErrorCode(str, Enum):
    TASK_NOT_FOUND = "TASK_NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_INPUT = "INVALID_INPUT"
```

#### Frontend Error Handling
- Frontend MUST handle all backend error codes
- Map error codes to user-friendly messages

Example:
```typescript
// frontend/src/lib/errors.ts
const ERROR_MESSAGES = {
  TASK_NOT_FOUND: "Task not found. It may have been deleted.",
  UNAUTHORIZED: "Please log in to continue.",
  INVALID_INPUT: "Please check your input and try again.",
};
```

#### Error Validation
- `Full-Stack-Consistency-Agent.audit_error_symmetry()` MUST verify all codes are handled

### Auth Flow Consistency

#### Token Handling
- **Backend**: Issue JWT on login, verify on protected routes
- **Frontend**: Store JWT in memory or secure cookie, send in headers
- **BOTH**: Use same token format, expiration, claims

#### Auth State
- **Backend**: Stateless (no sessions)
- **Frontend**: Derive auth state from token presence/validity
- **BOTH**: Handle token expiration and refresh

#### Auth Validation
- `Full-Stack-Consistency-Agent.verify_auth_flow_consistency()` MUST verify alignment

### Data Transformation Consistency

#### Field Naming
- **Backend**: Use snake_case (Python convention)
- **Frontend**: Use camelCase (JavaScript convention)
- **Transformation**: Convert at API boundary

Example:
```python
# backend/src/schemas/task.py
class TaskResponse(BaseModel):
    user_id: int  # snake_case

    class Config:
        # Automatically convert to camelCase for frontend
        alias_generator = to_camel_case
```

```typescript
// frontend/src/types/task.ts
export interface Task {
  userId: number;  // camelCase
}
```

#### Data Validation
- `Full-Stack-Consistency-Agent.enforce_data_flow_integrity()` MUST verify transformations

### Enforcement

- `Full-Stack-Consistency-Agent` MUST run after ANY full-stack feature
- All consistency checks MUST pass before merge
- Integration tests MUST validate end-to-end flows

---

## Error Prevention & Consistency

All agents work together to PREVENT errors, not just detect them:

### Prevention Strategy

#### Proactive Validation
- **Before file creation**: `Spec-Kit-Structure-Guardian` validates path
- **Before implementation**: `Spec-Auditor-Agent` validates spec completeness
- **During implementation**: Agents validate as code is generated
- **Before commit**: All agents run final validation

#### Blocking vs Warning
- **BLOCKED**: Code generation stops, issue MUST be fixed
  - Security vulnerabilities
  - Structure violations
  - Missing authentication
  - Type mismatches
- **WARNING**: Issue should be fixed but doesn't block
  - Code style issues
  - Missing documentation
  - Optimization opportunities

### Quality Gates

#### Phase2-Quality-Orchestrator
Coordinates all agent checks and enforces gates:

1. **Pre-Implementation Gate**
   - Spec complete and approved
   - Plan follows constitution
   - Tasks properly organized

2. **Implementation Gate**
   - Structure guardian approved all files
   - Backend quality checks pass
   - Frontend quality checks pass
   - Security scan passes

3. **Integration Gate**
   - Full-stack consistency verified
   - API contracts validated
   - Auth flows tested
   - Type alignment verified

4. **Deployment Gate**
   - All agents pass
   - Tests pass
   - No high/critical issues

### Enforcement

- `Phase2-Quality-Orchestrator.orchestrate_compliance_review()` MUST pass before merge
- All BLOCKED issues MUST be resolved
- No manual override of agent decisions

---

## Agent-Based Code Generation Rules

ALL code generation in Phase II MUST follow agent-driven workflow:

### Rule 1: No Manual Coding
- **Developers MUST NOT write or edit source code manually**
- **ALL production code MUST be generated via Claude Code using agents**
- **Direct edits to files in `frontend/src/` or `backend/src/` are FORBIDDEN**

### Rule 2: Agent Consultation Required
Before generating ANY code:
1. **Consult `Spec-Kit-Structure-Guardian`** for file placement
2. **Consult relevant quality agents** for implementation guidance
3. **Generate code following agent recommendations**
4. **Validate with agents** after generation

### Rule 3: Agent Approval Required
After generating ANY code:
1. **Backend code**: Run `Backend-Code-Quality-Agent`, `API-Contract-Auditor`, `Security-Baseline-Agent`
2. **Frontend code**: Run `Frontend-Architecture-Auditor`, `Web-UX-Optimization-Agent`
3. **Full-stack feature**: Run `Full-Stack-Consistency-Agent`
4. **Before merge**: Run `Phase2-Quality-Orchestrator`

### Rule 4: Fix via Regeneration
If agent reports issues:
1. **Update the specification** (if requirements were unclear)
2. **Regenerate code** using updated guidance
3. **Validate with agents** again
4. **Repeat until agents approve**

**NEVER fix issues by manually editing generated code**

### Rule 5: Skill-Driven Validation
Each agent has multiple skills:
- **Invoke specific skills** for targeted checks
- **Skills block or warn** based on severity
- **All blocking issues MUST be resolved**

Example:
```
# After implementing protected API endpoint:
1. Run API-Contract-Auditor.validate_rest_contracts()
2. Run Auth-Integration-Auditor.audit_authorization_checks()
3. Run Security-Baseline-Agent.validate_input_sanitization()
4. If any BLOCKED: regenerate code with fixes
5. If all PASS: proceed to commit
```

---

## Phase II Completion Criteria

Phase II is considered **complete** when ALL criteria are met:

### Functional Completeness

1. ✅ **All core features implemented**:
   - User registration and login
   - Create, read, update, delete tasks
   - Mark tasks complete/incomplete
   - User profile management
   - Protected routes

2. ✅ **Application runs successfully**:
   - Frontend: `cd frontend && npm run dev` works
   - Backend: `cd backend && uvicorn src.main:app --reload` works
   - Database: Neon connection succeeds
   - Authentication: Login/logout flow works

3. ✅ **All acceptance criteria satisfied**:
   - Each spec's acceptance criteria validated
   - Edge cases handled as specified
   - Error messages match spec expectations

### Process Compliance

4. ✅ **All code generated via agent workflow**:
   - No manually authored code in `frontend/src/` or `backend/src/`
   - All features have specs in `specs/<feature>/`
   - PHRs exist for all major activities

5. ✅ **Quality gates passed**:
   - ALL 11 agents approve (no BLOCKED status)
   - `Phase2-Quality-Orchestrator` shows GREEN
   - No high/critical security issues

### Technical Requirements

6. ✅ **Frontend quality standards met**:
   - Loading states on all async operations
   - Error states on all failures
   - Empty states on all empty data
   - Responsive design (mobile, tablet, desktop)
   - Accessible (WCAG 2.1 AA)
   - TypeScript strict mode, no `any`

7. ✅ **Backend quality standards met**:
   - JWT authentication on all protected endpoints
   - User data isolation (no cross-user access)
   - Clean architecture (routes → services → models)
   - Error handling on all operations
   - Input validation on all endpoints
   - Type hints on all functions

8. ✅ **Full-stack consistency verified**:
   - Frontend types match backend schemas
   - Error codes handled on both sides
   - Auth flow consistent (JWT in header)
   - Data transformations correct (snake_case ↔ camelCase)

### Documentation Completeness

9. ✅ **README.md exists and includes**:
   - Project description
   - Setup instructions (frontend, backend, database)
   - Environment variables documentation
   - Usage examples

10. ✅ **CLAUDE.md exists and includes**:
    - Agent registry and invocation rules
    - Spec-driven workflow instructions
    - Phase II governance rules

### Security Compliance

11. ✅ **Security baseline met**:
    - No hardcoded secrets
    - No SQL injection vulnerabilities
    - No XSS vulnerabilities
    - CORS properly configured
    - No high/critical CVEs in dependencies
    - JWT properly implemented

### No Scope Creep

12. ✅ **No unauthorized features implemented**:
    - Only features in approved specs
    - No advanced features (AI, analytics, etc.)
    - Codebase contains only Phase II scope

**Acceptance**: Phase II completion is formally accepted when `Phase2-Quality-Orchestrator` shows GREEN status and all above criteria are verified.

---

## Governance

### Constitution Authority

- This constitution is the **supreme governing document** for Phase II development
- All specifications, plans, and implementations MUST comply with this constitution
- All agents enforce constitution principles automatically
- Any conflict between this constitution and other documents is resolved in favor of the constitution

### Amendment Process

- **Phase II Constitution can be amended** with proper justification
- Amendments require:
  1. **Documented justification** (ADR explaining why change needed)
  2. **User approval** (explicit consent)
  3. **Version increment** (follow semantic versioning)
  4. **Template propagation** (update dependent files)
  5. **Agent coordination** (ensure agents align with new rules)

### Semantic Versioning

- **MAJOR** (X.0.0): Backward-incompatible changes (e.g., removing principles, changing stack)
- **MINOR** (0.X.0): New principles/sections, material expansions (e.g., new agent, new rules)
- **PATCH** (0.0.X): Clarifications, typos, non-semantic refinements

### Compliance Verification

- **All PRs MUST pass agent validation**
- **`Phase2-Quality-Orchestrator` is final approval gate**
- **No merge without GREEN status from orchestrator**
- **Security violations block deployment immediately**

### Architectural Decision Records (ADRs)

- **Significant decisions MUST be documented** in ADRs
- Significant = meets THREE criteria:
  1. **Impact**: Long-term consequences (framework, data model, API, security)
  2. **Alternatives**: Multiple viable options considered
  3. **Scope**: Cross-cutting, influences system design
- Store ADRs in `history/adr/`
- Link ADRs from plan.md and spec.md

### Version Control

- **Constitution changes MUST be tracked** in version history
- **Git commit format**: `docs: amend constitution to vX.Y.Z (brief change description)`
- **Maintain sync impact report** (HTML comment at top of file)

---

**Version**: 2.0.0
**Ratified**: 2026-01-09
**Last Amended**: 2026-01-09
**Supersedes**: 1.0.0 (Phase I - Python Console App)
