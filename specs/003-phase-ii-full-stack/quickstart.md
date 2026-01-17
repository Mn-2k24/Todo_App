# Todo App - Quickstart Guide

Get the full-stack Todo App running locally in under 10 minutes.

## Prerequisites

Before starting, ensure you have:

- **Node.js** 18+ (check: `node --version`)
- **Python** 3.11+ (check: `python --version`)
- **PostgreSQL** 14+ (check: `psql --version`)
- **Git** (check: `git --version`)

## Quick Start Steps

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Todo_App
```

### Step 2: Setup PostgreSQL Database

Create a new PostgreSQL database:

```bash
createdb todo_db
```

Or using psql:

```bash
psql
CREATE DATABASE todo_db;
\q
```

### Step 3: Setup Backend

#### 3.1 Navigate to Backend Directory

```bash
cd backend
```

#### 3.2 Create Environment File

Create `.env` file:

```bash
cat > .env << 'EOF'
DATABASE_URL=postgresql+asyncpg://localhost:5432/todo_db
JWT_SECRET=change-this-to-a-secure-random-string-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
EOF
```

**Important**: Replace `JWT_SECRET` with a secure random string (min 32 characters).

Generate a secure secret:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 3.3 Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or with virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 3.4 Run Database Migrations

```bash
alembic upgrade head
```

#### 3.5 Start Backend Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Verify backend is running: Open http://localhost:8000/docs

**Keep this terminal open** and proceed to frontend setup in a new terminal.

### Step 4: Setup Frontend

#### 4.1 Navigate to Frontend Directory

Open a **new terminal** and run:

```bash
cd Todo_App/frontend
```

#### 4.2 Create Environment File

Create `.env.local` file:

```bash
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=change-this-to-a-secure-random-string-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
EOF
```

**Important**: Replace `BETTER_AUTH_SECRET` with a secure random string (can use same method as backend).

#### 4.3 Install Node Dependencies

```bash
npm install
```

Or with yarn/pnpm:

```bash
yarn install
# or
pnpm install
```

#### 4.4 Start Frontend Server

```bash
npm run dev
```

Or with yarn/pnpm:

```bash
yarn dev
# or
pnpm dev
```

Verify frontend is running: Open http://localhost:3000

### Step 5: Test the Application

#### 5.1 Register a New Account

1. Navigate to http://localhost:3000
2. Click "Register" or go to http://localhost:3000/register
3. Enter email and password
4. Click "Register"

#### 5.2 Login

1. Use the credentials you just created
2. Go to http://localhost:3000/login
3. Enter email and password
4. Click "Login"

You should be redirected to the dashboard.

#### 5.3 Create Your First Task

1. In the dashboard, find the "Create New Task" form
2. Enter a task description (e.g., "Buy groceries")
3. Select a priority (High/Medium/Low)
4. Optionally add tags (comma-separated, e.g., "shopping, errands")
5. Optionally set a due date
6. Click "Add Task"

#### 5.4 Test Features

**Task Operations:**
- ✅ Click checkbox to toggle completion
- ✏️ Click "Edit" button to modify task
- 🗑️ Click "Delete" button to remove task

**Filtering:**
- Use the search bar to find tasks by text
- Filter by status (All/Completed/Incomplete)
- Filter by priority
- Filter by tags (comma-separated)

**Sorting:**
- Use the "Sort by" dropdown to change task order
- Options: Newest First, Title (A-Z), Due Date, Priority
- Sort preference persists after page refresh

**Logout:**
- Click your email in the header
- Click "Logout"

## Verification Checklist

Ensure the following work correctly:

- [ ] Backend API running at http://localhost:8000
- [ ] Frontend app running at http://localhost:3000
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] User registration successful
- [ ] User login successful
- [ ] Dashboard displays after login
- [ ] Can create task with all fields
- [ ] Can edit task
- [ ] Can delete task (with confirmation)
- [ ] Can toggle task completion
- [ ] Search filters tasks correctly
- [ ] Status filter works (all/completed/incomplete)
- [ ] Priority filter works
- [ ] Tags filter works
- [ ] Sort options work (all 4 options)
- [ ] Sort preference persists after refresh
- [ ] Overdue tasks show red indicator
- [ ] Logout redirects to login page
- [ ] Protected routes redirect to login when not authenticated

## Common Issues & Solutions

### Backend Won't Start

**Issue**: `alembic.util.exc.CommandError: Can't locate revision identified by...`

**Solution**: Reset database migrations
```bash
# Drop and recreate database
dropdb todo_db
createdb todo_db
alembic upgrade head
```

### Database Connection Error

**Issue**: `sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server failed`

**Solution**:
- Check PostgreSQL is running: `pg_isready`
- Start PostgreSQL: `brew services start postgresql` (macOS) or `sudo service postgresql start` (Linux)
- Verify DATABASE_URL in `.env`

### Frontend API Connection Error

**Issue**: Network errors or CORS errors in browser console

**Solution**:
- Verify backend is running at http://localhost:8000
- Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
- Verify CORS allows `http://localhost:3000` in backend configuration

### JWT Token Invalid

**Issue**: "Invalid or expired token" errors

**Solution**:
- Clear browser localStorage and cookies
- Verify `JWT_SECRET` in backend `.env` matches `BETTER_AUTH_SECRET` in frontend `.env.local`
- Re-login to get fresh token

### Port Already in Use

**Issue**: `Error: listen EADDRINUSE: address already in use :::8000`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
uvicorn src.main:app --reload --port 8001
```

## Next Steps

Now that your Todo App is running:

1. **Explore the codebase**:
   - Backend: [backend/README.md](../../backend/README.md)
   - Frontend: [frontend/README.md](../../frontend/README.md)

2. **Read the specifications**:
   - Feature spec: [spec.md](./spec.md)
   - Architecture plan: [plan.md](./plan.md)
   - Task breakdown: [tasks.md](./tasks.md)

3. **Development workflow**:
   - Follow Spec-Driven Development principles
   - Create PHRs for significant work
   - Run agent validations before major commits

4. **Production deployment**:
   - Use proper secrets management (environment variables, not .env files)
   - Set up PostgreSQL with connection pooling
   - Configure CORS for production domain
   - Enable HTTPS
   - Set `ENVIRONMENT=production`

## Architecture Overview

```
┌─────────────────┐         ┌──────────────────┐
│  Next.js 15     │         │  FastAPI         │
│  Frontend       │  HTTP   │  Backend         │
│  Port 3000      │────────▶│  Port 8000       │
└─────────────────┘         └──────────────────┘
       │                              │
       │                              │
       │  Better Auth JWT             │  SQLModel
       │                              │  (Async)
       ▼                              ▼
  localStorage              ┌──────────────────┐
  (sort pref)               │  PostgreSQL      │
                           │  Database        │
                           └──────────────────┘
```

## Support

- **Documentation**: See README files in `backend/` and `frontend/`
- **API Reference**: http://localhost:8000/docs (when backend running)
- **Issues**: Check `specs/003-phase-ii-full-stack/tasks.md` for known tasks

## Success Criteria

You've successfully completed the quickstart when:

✅ Both backend and frontend are running
✅ You can register a new account
✅ You can login and see the dashboard
✅ You can create, edit, delete, and complete tasks
✅ All filters and sorting options work
✅ Sort preference persists after page refresh

**Congratulations! Your Todo App is now fully operational.** 🎉
