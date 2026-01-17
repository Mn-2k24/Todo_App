# Implementation Plan: Phase II - Full-Stack Todo Web Application

**Branch**: `003-phase-ii-full-stack` | **Date**: 2026-01-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-phase-ii-full-stack/spec.md`

## Summary

Build a production-ready full-stack web application that transforms the Phase I Python console app into a modern web app with multi-user support, persistent storage, and professional UI/UX. The application enables users to create accounts, securely authenticate, and manage personal tasks with priorities, tags, due dates, search, and filtering capabilities.

**Primary Requirements:**
- Multi-user authentication with Better Auth and JWT tokens
- Complete CRUD operations for tasks with user data isolation
- Task enhancements: priorities (High/Medium/Low), tags, due dates
- Search and filtering by text, status, priority, tags
- Sorting by title, date, due date, priority
- Professional responsive UI with loading, error, and empty states
- RESTful API with complete security and validation
- Persistent storage in Neon PostgreSQL database

**Technical Approach:**
- Frontend: Next.js 15+ (App Router) with TypeScript and Tailwind CSS
- Backend: FastAPI (Python 3.13+) with SQLModel ORM
- Database: Neon PostgreSQL (serverless)
- Authentication: Better Auth with stateless JWT tokens
- Development: Agent-driven code generation (no manual coding)
- Quality: 11 specialized agents enforce architecture, security, and consistency

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.3+, Node.js 20+
- Backend: Python 3.13+

**Primary Dependencies**:
- Frontend: Next.js 15.1+, React 19+, Tailwind CSS 4+, Better Auth client
- Backend: FastAPI 0.115+, SQLModel 0.0.22+, Pydantic 2.10+, python-jose (JWT), bcrypt, alembic

**Storage**: Neon PostgreSQL (serverless) with SQLModel ORM

**Testing**:
- Frontend: Jest + React Testing Library
- Backend: pytest + httpx (FastAPI test client)
- E2E: Playwright (optional for Phase II)

**Target Platform**: Web (browsers: Chrome, Firefox, Safari, Edge - last 2 versions)

**Project Type**: Web application (frontend + backend monorepo)

**Performance Goals**:
- API response time: < 2 seconds (per success criteria SC-003)
- Search response time: < 1 second for 1000 tasks (per SC-006)
- Support 100 concurrent users (per SC-007)
- Task creation: < 10 seconds (per SC-002)

**Constraints**:
- Stateless backend (no server-side sessions per constitution)
- JWT tokens for all authenticated requests
- User data isolation (no cross-user access)
- WCAG 2.1 AA accessibility compliance
- Mobile-first responsive design (320px to 2560px)

**Scale/Scope**:
- MVP: 100 concurrent users
- Initial deployment: Single region (US)
- Database: Neon free tier initially (can scale)
- Storage per user: ~1000 tasks expected

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase II Constitution Compliance

**✅ PASSED - All Constitution Requirements Met:**

1. **Spec-Driven Workflow** ✅
   - Spec created and validated (specs/003-phase-ii-full-stack/spec.md)
   - All 54 functional requirements documented
   - 7 prioritized user stories with acceptance criteria
   - No code will be generated without this approved plan

2. **Agent-Driven Code Generation** ✅
   - Manual coding prohibited per constitution
   - All 11 agents available and skill files created
   - Agent invocation plan defined in implementation phases below

3. **Monorepo Structure** ✅
   - Strict `frontend/` and `backend/` separation
   - `Spec-Kit-Structure-Guardian` will validate all file placements
   - No root-level source code or util directories

4. **Technology Stack Compliance** ✅
   - Frontend: Next.js 15+ ✓ (per constitution)
   - Backend: FastAPI + Python 3.13+ ✓ (per constitution)
   - Database: Neon PostgreSQL ✓ (per constitution)
   - Auth: Better Auth with JWT ✓ (per constitution)
   - Styling: Tailwind CSS ✓ (per constitution)

5. **Security Requirements** ✅
   - JWT authentication on all protected endpoints (FR-048 to FR-054)
   - Stateless backend design (no sessions)
   - Environment variables for secrets
   - CORS policy restricted to approved origins
   - Input validation and sanitization

6. **UI/UX Standards** ✅
   - Loading states mandatory (FR-041)
   - Error states mandatory (FR-042)
   - Empty states mandatory (FR-043)
   - Responsive design (FR-045)
   - Accessibility (FR-046)
   - All enforced by `Web-UX-Optimization-Agent`

7. **Type Safety** ✅
   - TypeScript strict mode for frontend
   - Python type hints for backend
   - Full-stack type alignment via `Full-Stack-Consistency-Agent`

**No Violations**: This plan complies with all Phase II Constitution requirements.

## Project Structure

### Documentation (this feature)

```text
specs/003-phase-ii-full-stack/
├── spec.md                      # Feature specification (DONE)
├── plan.md                      # This file (IN PROGRESS)
├── research.md                  # Technical research (Phase 0)
├── data-model.md                # Database models (Phase 1)
├── quickstart.md                # Local development guide (Phase 1)
├── contracts/                   # API contracts (Phase 1)
│   ├── auth.yaml               # Authentication endpoints
│   └── tasks.yaml              # Task management endpoints
├── checklists/
│   └── requirements.md         # Spec quality checklist (DONE)
└── tasks.md                    # Task breakdown (Phase 2 - /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/                  # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py             # User model (Better Auth integration)
│   │   └── task.py             # Task model with relationships
│   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── auth.py             # Login, register, token schemas
│   │   └── task.py             # Task create, update, response schemas
│   ├── services/                # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Authentication logic
│   │   └── task_service.py     # Task CRUD operations
│   ├── api/                     # FastAPI route handlers
│   │   ├── __init__.py
│   │   ├── auth.py             # Auth endpoints
│   │   └── tasks.py            # Task endpoints
│   ├── auth/                    # Authentication utilities
│   │   ├── __init__.py
│   │   ├── jwt.py              # JWT creation/verification
│   │   └── dependencies.py     # Auth dependencies (get_current_user)
│   ├── utils/                   # Backend utilities
│   │   ├── __init__.py
│   │   └── errors.py           # Error handlers and exceptions
│   ├── database.py              # Database connection and session
│   ├── config.py                # Settings and environment variables
│   └── main.py                  # FastAPI application entry point
├── tests/
│   ├── contract/                # API contract tests
│   ├── integration/             # Integration tests
│   └── unit/                    # Unit tests
├── alembic/                     # Database migrations
│   ├── versions/
│   └── env.py
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
├── alembic.ini                  # Alembic configuration
└── README.md                    # Backend setup instructions

frontend/
├── src/
│   ├── app/                     # Next.js App Router
│   │   ├── (auth)/             # Auth route group
│   │   │   ├── login/
│   │   │   │   └── page.tsx    # Login page
│   │   │   └── register/
│   │   │       └── page.tsx    # Registration page
│   │   ├── (protected)/        # Protected route group
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx    # Main task dashboard
│   │   │   └── tasks/
│   │   │       └── [id]/
│   │   │           └── page.tsx # Task detail page
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Landing page
│   │   └── globals.css         # Global styles
│   ├── components/              # React components
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   ├── TaskFilters.tsx
│   │   │   └── TaskSort.tsx
│   │   ├── ui/                  # Reusable UI components
│   │   │   ├── LoadingSpinner.tsx
│   │   │   ├── ErrorMessage.tsx
│   │   │   ├── EmptyState.tsx
│   │   │   └── Button.tsx
│   │   └── layout/
│   │       ├── Header.tsx
│   │       └── Navigation.tsx
│   ├── lib/                     # Utilities and helpers
│   │   ├── api.ts              # API client with fetch wrappers
│   │   ├── auth.ts             # Auth utilities (token management)
│   │   └── errors.ts           # Error handling utilities
│   ├── types/                   # TypeScript type definitions
│   │   ├── task.ts             # Task types
│   │   ├── user.ts             # User types
│   │   └── api.ts              # API response types
│   ├── styles/                  # Additional styles
│   │   └── tailwind.css
│   └── middleware.ts            # Next.js middleware (auth guards)
├── public/                      # Static assets
│   ├── favicon.ico
│   └── images/
├── tests/                       # Frontend tests
├── .env.local.example          # Frontend environment template
├── next.config.js              # Next.js configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
├── package.json                # Dependencies
└── README.md                   # Frontend setup instructions
```

**Structure Decision**: Web application structure (Option 2) selected because Phase II is a full-stack web application with separate frontend and backend. This aligns with constitution requirements for strict monorepo boundaries and separation of concerns.

## Complexity Tracking

**No Violations** - All architectural decisions comply with Phase II Constitution:

- ✅ Using 2 projects (frontend + backend) as required for web applications
- ✅ Clean architecture with separation of concerns (routes, services, models)
- ✅ Stateless backend (JWT tokens, no sessions)
- ✅ Type-safe implementation (TypeScript + Python type hints)
- ✅ Agent-driven code generation model

## Phase 0: Research & Technology Validation

**Goal**: Resolve all technical unknowns and validate technology choices against constitution requirements.

### Research Tasks

Since Technical Context is fully defined based on constitution and spec, minimal research needed. Focus on validation and best practices:

**1. Better Auth Integration Research**
- **Decision**: Better Auth with JWT tokens for stateless authentication
- **Why**: Constitution specifies Better Auth; provides modern auth with JWT out of box
- **Validation Needed**: Confirm Better Auth works with Next.js 15 App Router and FastAPI backend
- **Research**: Best practices for Better Auth + FastAPI integration
- **Output**: Integration patterns, configuration examples

**2. Neon PostgreSQL + SQLModel Research**
- **Decision**: Neon serverless PostgreSQL with SQLModel ORM
- **Why**: Constitution specifies Neon; SQLModel provides type-safe ORM for FastAPI
- **Validation Needed**: Confirm Neon connection pooling and migration strategy
- **Research**: SQLModel best practices, Alembic migration patterns
- **Output**: Connection string format, migration workflow

**3. Next.js 15 App Router + Server/Client Components**
- **Decision**: Next.js 15 App Router (not Pages Router)
- **Why**: Constitution specifies Next.js 15+; App Router is modern standard
- **Validation Needed**: Server vs Client component patterns for auth and task management
- **Research**: When to use 'use client' directive, server actions vs API routes
- **Output**: Component architecture patterns

**4. Tailwind CSS 4 + Design System**
- **Decision**: Tailwind CSS 4 for styling
- **Why**: Constitution specifies Tailwind; utility-first matches rapid development
- **Validation Needed**: Design token setup for consistent spacing, colors, typography
- **Research**: Tailwind 4 configuration, accessibility patterns
- **Output**: tailwind.config.js structure, color palette

**5. JWT Token Strategy**
- **Decision**: HS256 signing with shared secret (or RS256 with key pair)
- **Why**: Constitution requires JWT; HS256 simpler for single backend
- **Validation Needed**: Token expiration strategy (1h access, 7d refresh per constitution)
- **Research**: Token refresh flow, secure storage in frontend
- **Output**: JWT creation/verification utilities

**6. Error Handling Consistency**
- **Decision**: Standardized error codes across frontend/backend
- **Why**: Full-Stack-Consistency-Agent requires error symmetry
- **Validation Needed**: Error code taxonomy matching backend exceptions to frontend messages
- **Research**: FastAPI exception handling, Next.js error boundaries
- **Output**: Error code enumeration, error response schemas

**7. Type Alignment Strategy**
- **Decision**: Manual type mirroring (backend Pydantic → frontend TypeScript)
- **Why**: Full-Stack-Consistency-Agent requires type alignment
- **Validation Needed**: Process for keeping types in sync
- **Research**: Pydantic to TypeScript conversion patterns, field naming (snake_case vs camelCase)
- **Output**: Type alignment checklist

**Output Document**: `research.md` with above sections documented

## Phase 1: Design & API Contracts

**Prerequisites**: `research.md` complete

### 1.1 Data Model Design

**Create `data-model.md`** with following entities:

#### User Entity (Better Auth Managed)
```
User
├── id: UUID (primary key)
├── email: string (unique, indexed, not null)
├── password_hash: string (bcrypt, not null)
├── created_at: timestamp (default now)
└── Relationships:
    └── tasks: one-to-many Task (cascade delete)
```

**Validation Rules** (from FR-001 to FR-010):
- Email must be valid format (FR-002)
- Password minimum 8 characters (FR-003)
- Email must be unique (FR-008)
- Password must be hashed before storage (FR-009)

#### Task Entity
```
Task
├── id: UUID (primary key)
├── user_id: UUID (foreign key User.id, indexed, not null)
├── description: string(500) (not null)
├── completed: boolean (default false)
├── priority: enum('high', 'medium', 'low') (default 'medium')
├── tags: array<string> (default empty array)
├── due_date: date (nullable)
├── created_at: timestamp (default now, indexed)
├── updated_at: timestamp (default now, on update now)
└── Relationships:
    └── user: many-to-one User
```

**Validation Rules** (from FR-011 to FR-040):
- Description required, non-empty (FR-018)
- User_id required for data isolation (FR-016, FR-038)
- Priority defaults to medium (FR-020)
- Due_date optional (FR-022)
- Cascade delete when user deleted (FR-039)

**Indexes**:
- `user_id` (for user filtering)
- `created_at` (for sort by creation date)
- `due_date` (for sort by due date)
- Composite: `(user_id, completed)` (for status filtering)

**State Transitions**:
- `completed`: false ↔ true (toggle via FR-015)
- `priority`: high ↔ medium ↔ low (update via FR-025)
- `tags`: mutable array (add/remove via FR-021, FR-025)
- `due_date`: nullable → date → nullable (set/clear via FR-022, FR-025)

### 1.2 API Contract Generation

**Create `contracts/auth.yaml`** (OpenAPI 3.1):

```yaml
openapi: 3.1.0
info:
  title: Todo App - Authentication API
  version: 1.0.0

paths:
  /api/auth/register:
    post:
      summary: Register new user account
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: '#/components/schemas/User'
                  token:
                    type: string
                    description: JWT access token
        '400':
          description: Invalid input (email format, password length)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '409':
          description: Email already registered
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /api/auth/login:
    post:
      summary: Authenticate existing user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
      responses:
        '200':
          description: Authentication successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: '#/components/schemas/User'
                  token:
                    type: string
        '401':
          description: Invalid credentials
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /api/auth/logout:
    post:
      summary: Logout user (invalidate token)
      security:
        - BearerAuth: []
      responses:
        '200':
          description: Logout successful
        '401':
          description: Unauthorized (invalid/missing token)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        created_at:
          type: string
          format: date-time

    Error:
      type: object
      required: [error, code, status]
      properties:
        error:
          type: string
          description: User-friendly error message
        code:
          type: string
          description: Machine-readable error code
        status:
          type: integer
          description: HTTP status code

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

**Create `contracts/tasks.yaml`** (OpenAPI 3.1):

```yaml
openapi: 3.1.0
info:
  title: Todo App - Task Management API
  version: 1.0.0

security:
  - BearerAuth: []

paths:
  /api/tasks:
    get:
      summary: Retrieve all tasks for authenticated user
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [complete, incomplete]
        - name: priority
          in: query
          schema:
            type: string
            enum: [high, medium, low]
        - name: tags
          in: query
          schema:
            type: string
            description: Comma-separated tags
        - name: search
          in: query
          schema:
            type: string
            description: Search text for description
        - name: sort_by
          in: query
          schema:
            type: string
            enum: [title, created, due_date, priority]
            default: created
        - name: order
          in: query
          schema:
            type: string
            enum: [asc, desc]
            default: desc
      responses:
        '200':
          description: Tasks retrieved successfully
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Task'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create new task for authenticated user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [description]
              properties:
                description:
                  type: string
                  minLength: 1
                  maxLength: 500
                priority:
                  type: string
                  enum: [high, medium, low]
                  default: medium
                tags:
                  type: array
                  items:
                    type: string
                  default: []
                due_date:
                  type: string
                  format: date
                  nullable: true
      responses:
        '201':
          description: Task created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

  /api/tasks/{id}:
    get:
      summary: Retrieve specific task by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Task retrieved successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'

    put:
      summary: Update existing task
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                description:
                  type: string
                  minLength: 1
                  maxLength: 500
                priority:
                  type: string
                  enum: [high, medium, low]
                tags:
                  type: array
                  items:
                    type: string
                due_date:
                  type: string
                  format: date
                  nullable: true
      responses:
        '200':
          description: Task updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'

    delete:
      summary: Delete task permanently
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Task deleted successfully
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'

  /api/tasks/{id}/complete:
    patch:
      summary: Toggle task completion status
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Task completion toggled
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    Task:
      type: object
      properties:
        id:
          type: string
          format: uuid
        user_id:
          type: string
          format: uuid
        description:
          type: string
        completed:
          type: boolean
        priority:
          type: string
          enum: [high, medium, low]
        tags:
          type: array
          items:
            type: string
        due_date:
          type: string
          format: date
          nullable: true
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

  responses:
    Unauthorized:
      description: Unauthorized (invalid/missing token)
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: "Please log in to continue"
            code: "UNAUTHORIZED"
            status: 401

    Forbidden:
      description: Forbidden (not owner of resource)
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: "You don't have permission to access this resource"
            code: "FORBIDDEN"
            status: 403

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: "Task not found"
            code: "TASK_NOT_FOUND"
            status: 404

    BadRequest:
      description: Invalid request (validation error)
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: "Description cannot be empty"
            code: "INVALID_INPUT"
            status: 400

    Error:
      $ref: './auth.yaml#/components/schemas/Error'

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### 1.3 Quickstart Guide

**Create `quickstart.md`** with local development setup:

```markdown
# Quickstart Guide: Phase II Full-Stack Todo App

## Prerequisites

- Node.js 20+ and npm/yarn/pnpm
- Python 3.13+
- Git
- Neon PostgreSQL account (free tier)

## Setup

### 1. Clone Repository

\`\`\`bash
git clone <repo-url>
cd Todo_App
git checkout 003-phase-ii-full-stack
\`\`\`

### 2. Backend Setup

\`\`\`bash
cd backend

# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your values:
# DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/todo_db
# JWT_SECRET=your-secret-key-here
# BETTER_AUTH_SECRET=your-auth-secret-here

# Run migrations
alembic upgrade head

# Start development server
uvicorn src.main:app --reload --port 8000
\`\`\`

Backend running at `http://localhost:8000`

### 3. Frontend Setup

\`\`\`bash
cd frontend

# Install dependencies
npm install  # or: yarn install, pnpm install

# Copy environment template
cp .env.local.example .env.local

# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000
# BETTER_AUTH_SECRET=your-auth-secret-here

# Start development server
npm run dev
\`\`\`

Frontend running at `http://localhost:3000`

## Verify Setup

1. Visit `http://localhost:3000`
2. Register new account
3. Create a task
4. Verify task appears in list

## Running Tests

**Backend:**
\`\`\`bash
cd backend
pytest
\`\`\`

**Frontend:**
\`\`\`bash
cd frontend
npm test
\`\`\`

## Common Issues

- **Database connection fails**: Check Neon connection string, verify IP whitelist
- **CORS errors**: Verify NEXT_PUBLIC_API_URL matches backend CORS settings
- **JWT errors**: Ensure JWT_SECRET matches between frontend and backend .env files

## Next Steps

- Read `plan.md` for implementation phases
- Read `tasks.md` for task breakdown
- Run agents before implementation: `Spec-Kit-Structure-Guardian`, `Spec-Auditor-Agent`
\`\`\`

## Agent-Driven Implementation Workflow

**CRITICAL**: All code generation MUST use agents. Manual coding is prohibited per Phase II Constitution.

### Pre-Implementation Agent Checks

**Before any code generation:**

1. **Spec-Kit-Structure-Guardian**
   - Validate file placement before creating any new files
   - Ensure frontend/, backend/, specs/ boundaries
   - Block unauthorized file locations

2. **Spec-Auditor-Agent**
   - Validate spec completeness
   - Verify acceptance criteria
   - Check for scope creep

### Implementation Phases (Agent-Driven)

#### Phase 1: Backend Foundation

**Agent Sequence:**
1. **Spec-Kit-Structure-Guardian**: Validate `backend/` structure before file creation
2. Generate files via Claude Code using agents
3. **Security-Baseline-Agent**: Scan for hardcoded secrets, validate env var usage
4. **Backend-Code-Quality-Agent**: Validate clean architecture, error handling
5. **Data-Model-Auditor**: Validate SQLModel models, indexes, relationships

**Files to Generate** (via agents):
- `backend/src/database.py` - Database connection with Neon
- `backend/src/config.py` - Environment variable management
- `backend/src/models/user.py` - User SQLModel (Better Auth integration)
- `backend/src/models/task.py` - Task SQLModel with validations
- `backend/alembic/versions/001_initial.py` - Initial migration

**Agent Validations After Generation:**
- Security-Baseline-Agent.scan_for_secrets() → MUST pass
- Data-Model-Auditor.validate_schema_correctness() → MUST pass
- Backend-Code-Quality-Agent.enforce_clean_architecture() → MUST pass

#### Phase 2: Authentication System

**Agent Sequence:**
1. **Spec-Kit-Structure-Guardian**: Validate auth file locations
2. Generate auth files via Claude Code
3. **Auth-Integration-Auditor**: Validate JWT implementation, stateless backend
4. **Security-Baseline-Agent**: Validate password hashing, JWT secrets
5. **API-Contract-Auditor**: Validate auth endpoints against contracts/auth.yaml

**Files to Generate** (via agents):
- `backend/src/auth/jwt.py` - JWT creation/verification
- `backend/src/auth/dependencies.py` - get_current_user dependency
- `backend/src/schemas/auth.py` - Login, register, token schemas
- `backend/src/services/auth_service.py` - Registration, login logic
- `backend/src/api/auth.py` - Auth route handlers

**Agent Validations:**
- Auth-Integration-Auditor.validate_jwt_implementation() → MUST pass
- Auth-Integration-Auditor.enforce_stateless_backend() → MUST pass
- API-Contract-Auditor.validate_rest_contracts() → MUST pass (contracts/auth.yaml)
- Security-Baseline-Agent.validate_input_sanitization() → MUST pass

#### Phase 3: Task Management Backend

**Agent Sequence:**
1. **Spec-Kit-Structure-Guardian**: Validate task file locations
2. Generate task files via Claude Code
3. **Auth-Integration-Auditor**: Verify JWT protection on all endpoints
4. **Data-Model-Auditor**: Validate user_id filtering, data isolation
5. **API-Contract-Auditor**: Validate task endpoints against contracts/tasks.yaml
6. **Backend-Code-Quality-Agent**: Validate service layer separation

**Files to Generate** (via agents):
- `backend/src/schemas/task.py` - Task create, update, response schemas
- `backend/src/services/task_service.py` - Task CRUD with user filtering
- `backend/src/api/tasks.py` - Task route handlers
- `backend/src/utils/errors.py` - Error handlers and exceptions

**Agent Validations:**
- Auth-Integration-Auditor.audit_authorization_checks() → MUST pass (user ownership)
- Data-Model-Auditor.enforce_data_isolation() → MUST pass (no cross-user access)
- API-Contract-Auditor.validate_rest_contracts() → MUST pass (contracts/tasks.yaml)
- Backend-Code-Quality-Agent.audit_error_handling() → MUST pass

#### Phase 4: Frontend Foundation

**Agent Sequence:**
1. **Spec-Kit-Structure-Guardian**: Validate `frontend/` structure
2. Generate frontend foundation via Claude Code
3. **Frontend-Architecture-Auditor**: Validate component structure, type safety
4. **Web-UX-Optimization-Agent**: Validate professional UI standards

**Files to Generate** (via agents):
- `frontend/src/lib/api.ts` - Typed fetch wrapper with error handling
- `frontend/src/lib/auth.ts` - Token storage/retrieval utilities
- `frontend/src/lib/errors.ts` - Error mapping (backend codes → user messages)
- `frontend/src/types/user.ts` - User type definitions
- `frontend/src/types/task.ts` - Task type definitions (match backend schemas)
- `frontend/src/types/api.ts` - API response types
- `frontend/src/app/layout.tsx` - Root layout with providers
- `frontend/tailwind.config.js` - Tailwind configuration with design tokens

**Agent Validations:**
- Frontend-Architecture-Auditor.verify_type_safety() → MUST pass (strict mode, no any)
- Web-UX-Optimization-Agent.enforce_professional_ui() → MUST pass (design tokens)

#### Phase 5: Authentication UI

**Agent Sequence:**
1. **Spec-Kit-Structure-Guardian**: Validate auth component locations
2. Generate auth UI via Claude Code
3. **Frontend-Architecture-Auditor**: Validate form components, API integration
4. **Web-UX-Optimization-Agent**: Validate loading/error states, accessibility
5. **Full-Stack-Consistency-Agent**: Validate type alignment with backend

**Files to Generate** (via agents):
- `frontend/src/components/auth/LoginForm.tsx` - Login form with validation
- `frontend/src/components/auth/RegisterForm.tsx` - Registration form
- `frontend/src/components/ui/LoadingSpinner.tsx` - Loading indicator
- `frontend/src/components/ui/ErrorMessage.tsx` - Error display
- `frontend/src/app/(auth)/login/page.tsx` - Login page
- `frontend/src/app/(auth)/register/page.tsx` - Registration page
- `frontend/src/middleware.ts` - Auth guard middleware

**Agent Validations:**
- Frontend-Architecture-Auditor.audit_api_integration() → MUST pass (typed, error handling)
- Web-UX-Optimization-Agent.validate_loading_states() → MUST pass
- Web-UX-Optimization-Agent.audit_error_states() → MUST pass
- Web-UX-Optimization-Agent.enforce_accessibility() → MUST pass
- Full-Stack-Consistency-Agent.validate_type_alignment() → MUST pass
- Full-Stack-Consistency-Agent.audit_error_symmetry() → MUST pass

#### Phase 6: Task Management UI

**Agent Sequence:**
1. **Spec-Kit-Structure-Guardian**: Validate task component locations
2. Generate task UI via Claude Code
3. **Frontend-Architecture-Auditor**: Validate component complexity, state management
4. **Web-UX-Optimization-Agent**: Validate empty states, loading states, professional UI
5. **Full-Stack-Consistency-Agent**: Validate end-to-end type alignment

**Files to Generate** (via agents):
- `frontend/src/components/tasks/TaskList.tsx` - Task list with filters/sort
- `frontend/src/components/tasks/TaskItem.tsx` - Individual task row
- `frontend/src/components/tasks/TaskForm.tsx` - Create/edit task form
- `frontend/src/components/tasks/TaskFilters.tsx` - Filter controls
- `frontend/src/components/tasks/TaskSort.tsx` - Sort controls
- `frontend/src/components/ui/EmptyState.tsx` - Empty state component
- `frontend/src/components/ui/Button.tsx` - Reusable button
- `frontend/src/components/layout/Header.tsx` - App header with logout
- `frontend/src/app/(protected)/dashboard/page.tsx` - Main dashboard
- `frontend/src/app/(protected)/tasks/[id]/page.tsx` - Task detail page

**Agent Validations:**
- Frontend-Architecture-Auditor.validate_component_structure() → MUST pass (< 200 lines)
- Frontend-Architecture-Auditor.enforce_state_management() → MUST pass (no prop drilling)
- Web-UX-Optimization-Agent.verify_empty_states() → MUST pass
- Web-UX-Optimization-Agent.validate_loading_states() → MUST pass
- Web-UX-Optimization-Agent.enforce_professional_ui() → MUST pass
- Full-Stack-Consistency-Agent.validate_type_alignment() → MUST pass
- Full-Stack-Consistency-Agent.enforce_data_flow_integrity() → MUST pass

### Final Quality Gate

**Before Merge - Phase2-Quality-Orchestrator:**

1. **orchestrate_compliance_review()**
   - Verifies all 11 agents ran
   - Checks all agents passed (no BLOCKED status)
   - Validates workflow order (spec → plan → implementation)

2. **validate_workflow_order()**
   - Confirms spec approved before implementation
   - Verifies agent validations at each phase

3. **enforce_adr_requirements()**
   - Checks if architectural decisions need ADRs
   - Suggests ADR creation if significant decisions made

4. **coordinate_multi_agent_checks()**
   - Ensures dependent agents ran together
   - Validates cross-cutting concerns

**Gate Result**: GREEN = ready for merge | RED = fix issues and re-run agents

## Success Criteria Validation

After implementation, validate against spec success criteria:

- **SC-001**: Test account registration time (< 1 minute)
- **SC-002**: Test task creation time (< 10 seconds)
- **SC-003**: Test operation response times (< 2 seconds)
- **SC-004**: Test responsive design (320px to 2560px)
- **SC-005**: Test first-time task creation success rate
- **SC-006**: Test search performance (< 1 second for 1000 tasks)
- **SC-007**: Load test with 100 concurrent users
- **SC-008**: Security audit (no unauthorized data access)
- **SC-009**: Accessibility audit (keyboard navigation)
- **SC-010**: Test filter/sort performance (< 5 seconds)
- **SC-011**: Visual regression test (loading/error/empty states)
- **SC-012**: Test login success rate with valid credentials

## Next Steps

1. ✅ **Plan Complete** - This document
2. **Run `/sp.tasks`** - Generate task breakdown from plan
3. **Run `/sp.analyze`** - Validate cross-artifact consistency
4. **Run `/sp.implement`** - Execute agent-driven implementation
5. **Run quality gates** - Phase2-Quality-Orchestrator approval
6. **Deploy** - Vercel (frontend), Railway/Render (backend)

---

**REMEMBER**: All code generation uses agents. No manual coding. Agents enforce quality, security, and consistency automatically per Phase II Constitution.
