# Todo App - Backend API

FastAPI-based REST API for the Todo App with JWT authentication, PostgreSQL database, and async operations.

## Technology Stack

- **Framework**: FastAPI 0.115+
- **Database**: PostgreSQL with SQLModel (async)
- **Authentication**: JWT tokens via Better Auth
- **Migrations**: Alembic
- **Python**: 3.11+

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 14 or higher
- pip or poetry for package management

## Setup Instructions

### 1. Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/todo_db

# JWT Configuration (use strong secrets in production)
JWT_SECRET=your-secret-key-min-32-chars-long-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# CORS (frontend origin)
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
```

**Security Note**: Never commit `.env` files. The `JWT_SECRET` must be loaded from environment variables and never hardcoded per FR-051.

### 2. Database Setup

Create the PostgreSQL database:

```bash
createdb todo_db
```

### 3. Install Dependencies

Using pip:

```bash
cd backend
pip install -r requirements.txt
```

Or using poetry:

```bash
cd backend
poetry install
```

### 4. Run Database Migrations

Apply Alembic migrations to create tables:

```bash
alembic upgrade head
```

### 5. Start the Development Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and receive JWT token
- `POST /api/auth/logout` - Logout (invalidate token)
- `GET /api/auth/me` - Get current user info

### Tasks

All task endpoints require JWT authentication via `Authorization: Bearer <token>` header.

- `GET /api/tasks` - List all user's tasks with optional filters/sort
  - Query params: `priority`, `tags`, `search`, `status`, `sort_by`, `order`
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{task_id}` - Get single task by ID
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task
- `PATCH /api/tasks/{task_id}/complete` - Toggle task completion

## Project Structure

```
backend/
├── alembic/              # Database migrations
├── src/
│   ├── api/             # API route handlers
│   │   ├── auth.py      # Authentication endpoints
│   │   └── tasks.py     # Task CRUD endpoints
│   ├── models/          # SQLModel database models
│   │   ├── user.py      # User model
│   │   └── task.py      # Task model with Priority enum
│   ├── schemas/         # Pydantic request/response schemas
│   │   ├── auth.py      # Auth DTOs
│   │   └── task.py      # Task DTOs
│   ├── services/        # Business logic layer
│   │   ├── auth_service.py    # Authentication logic
│   │   └── task_service.py    # Task operations with data isolation
│   ├── auth/            # Authentication utilities
│   │   └── dependencies.py    # JWT verification, current user
│   ├── utils/           # Shared utilities
│   │   └── errors.py    # Custom exception classes
│   ├── config.py        # Configuration management
│   ├── database.py      # Database connection and session
│   └── main.py          # FastAPI application entry point
├── tests/               # Test suite
├── .env.example         # Example environment variables
├── alembic.ini          # Alembic configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Key Features

### Data Isolation (FR-050)
All task operations enforce user-level data isolation. Users can only access their own tasks through the `get_current_user` dependency.

### Authentication Flow
1. User registers with email/password
2. User logs in to receive JWT token
3. Token included in `Authorization` header for protected endpoints
4. Token validated on each request via `get_current_user` dependency

### Filtering & Sorting
- **Filter by**: Priority (high/medium/low), Tags (comma-separated), Status (completed/incomplete), Text search
- **Sort by**: Title (alphabetically), Created date (newest first), Due date (nearest first), Priority (High→Medium→Low)

### Database Performance
Optimized queries with indexes on:
- `user_id` (foreign key)
- `created_at` (for sorting)
- `due_date` (for sorting)
- Composite `(user_id, completed)` (for status filtering)

## Development

### Running Tests

```bash
pytest
```

### Creating Database Migrations

After modifying SQLModel models:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Code Quality

The backend follows these principles per constitution.md:
- Stateless design (no server-side sessions)
- Async/await for all database operations
- Pydantic validation for all inputs
- Custom exception handling with standardized error responses
- Data isolation enforced at service layer

## Security Considerations

- JWT secrets loaded from environment (never hardcoded)
- CORS restricted to frontend origin only (FR-053)
- Input validation via Pydantic prevents SQL injection (FR-052)
- Password hashing with bcrypt
- Authentication failure logging (FR-054)

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running: `pg_isready`
- Check DATABASE_URL in `.env`
- Ensure database exists: `psql -l`

### Migration Errors
- Reset migrations: `alembic downgrade base && alembic upgrade head`
- Check alembic version table: `SELECT * FROM alembic_version;`

### JWT Token Issues
- Verify JWT_SECRET is set and matches frontend configuration
- Check token expiration (default 60 minutes)
- Ensure `Authorization: Bearer <token>` header format

## Related Documentation

- [Frontend README](../frontend/README.md)
- [Quickstart Guide](../specs/003-phase-ii-full-stack/quickstart.md)
- [API Specification](../specs/003-phase-ii-full-stack/spec.md)
- [Architecture Plan](../specs/003-phase-ii-full-stack/plan.md)
