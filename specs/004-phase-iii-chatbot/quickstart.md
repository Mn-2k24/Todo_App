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

## Environment Variables Reference

### Backend (.env)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | Yes | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `GEMINI_API_KEY` | Yes | Google Gemini API key | `AIzaSyA...` |
| `JWT_SECRET` | Yes | Secret for JWT token signing | `your-secret-key` |
| `USE_MOCK_GEMINI` | No | Use mock Gemini for testing | `true` or `false` (default: `false`) |
| `PHASE_III_ENABLED` | No | Feature flag for Phase III | `true` or `false` (default: `true`) |

### Frontend (.env.local)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | Yes | Backend API base URL | `http://localhost:8000` |
| `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` | Yes | OpenAI ChatKit domain key | `your-domain-key` |

## Testing with Mock Gemini

To run tests without consuming Gemini API quota:

```bash
# Backend tests with mocked Gemini
cd backend
USE_MOCK_GEMINI=true pytest phase3/tests/

# This uses keyword-based responses defined in backend/phase3/llm/tests/mock_gemini.py
```

## Next Steps

- Review [ARCHITECTURE.md](./ARCHITECTURE.md) for system design overview
- Review [API_REFERENCE.md](./API_REFERENCE.md) for endpoint documentation
- Review [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment guide
