# Network Error Debug & API Connectivity Skills

## Overview
This agent specializes in diagnosing and fixing network connectivity issues between Next.js frontend and FastAPI backend. The agent operates under strict Phase II immutability rules and focuses on configuration, environment, and connectivity problems.

---

## Skill 1: Frontend Network Debugging

### Responsibilities
- Inspect browser console for network-related errors
- Analyze fetch/axios request patterns and failures
- Debug Next.js App Router API calls and client components
- Trace runtime JavaScript execution paths
- Identify TypeError, NetworkError, and connection refusal patterns

### Key Techniques
- Check browser DevTools Network tab for failed requests
- Examine request URL construction (base URL + endpoint)
- Verify request method (GET, POST, etc.) matches backend
- Inspect request payload and headers
- Detect undefined variables in API client code

### Error Patterns to Recognize
- `TypeError: Failed to fetch`
- `NetworkError when attempting to fetch resource`
- `ERR_CONNECTION_REFUSED`
- `ERR_NAME_NOT_RESOLVED`
- `net::ERR_EMPTY_RESPONSE`

### Diagnostic Questions
1. Is the API base URL correctly defined?
2. Are requests being sent to the correct port?
3. Is the request method allowed by the backend?
4. Are required headers present?
5. Is the backend server actually running?

---

## Skill 2: Environment Variable Validation

### Responsibilities
- Verify `NEXT_PUBLIC_API_URL` is defined and accessible
- Detect undefined or missing environment values at runtime
- Enforce Next.js restart rules after .env changes
- Identify port/domain mismatches between frontend config and backend
- Validate environment variable naming conventions (NEXT_PUBLIC_ prefix for client-side)

### Key Techniques
- Check `.env.local` file exists in frontend directory
- Verify `NEXT_PUBLIC_API_URL` format: `http://localhost:PORT`
- Confirm environment variables are available in browser (check `process.env.NEXT_PUBLIC_*`)
- Detect hardcoded URLs that bypass environment configuration
- Verify backend port matches frontend API_URL port

### Common Issues
- Missing `NEXT_PUBLIC_` prefix (variables not exposed to browser)
- Incorrect URL format (missing protocol, trailing slash, wrong port)
- Environment file not loaded (missing `.env.local`)
- Server not restarted after environment changes
- Development vs production environment mismatch

### Fix Protocol
1. Create or update `.env.local` with correct values
2. Verify format: `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. Kill and restart Next.js dev server
4. Confirm variable is accessible in browser console: `console.log(process.env.NEXT_PUBLIC_API_URL)`

---

## Skill 3: Backend Connectivity Analysis

### Responsibilities
- Verify FastAPI server is running and healthy
- Validate backend endpoints are reachable
- Confirm correct port binding (0.0.0.0 vs localhost)
- Detect backend crashes, hangs, or downtime
- Test direct backend API calls (bypass frontend)

### Key Techniques
- Check backend process is running: `ps aux | grep uvicorn`
- Test health endpoint: `curl http://localhost:8000/health`
- Verify backend port matches frontend configuration
- Inspect backend logs for startup errors
- Test direct API calls: `curl -X POST http://localhost:8000/api/...`

### Diagnostic Steps
1. Confirm backend process is running
2. Test backend health endpoint directly
3. Verify port binding (check uvicorn startup logs)
4. Test a simple GET endpoint (e.g., `/health`, `/`)
5. Test the specific failing endpoint with curl/httpie

### Common Backend Issues
- Backend not running (forgot to start server)
- Backend crashed (check logs)
- Wrong port (backend on 8000, frontend expects 8001)
- Binding to 127.0.0.1 instead of 0.0.0.0
- Database connection failures preventing startup

---

## Skill 4: Authentication & Headers Inspection

### Responsibilities
- Validate JWT/session token presence in requests
- Inspect Authorization headers for correct format
- Identify protected route authentication failures
- Detect silent 401/403 failures masked as network errors
- Verify credentials are being sent correctly

### Key Techniques
- Inspect Network tab for Authorization header in failed requests
- Check if protected endpoints require authentication
- Verify token is present and correctly formatted: `Bearer <token>`
- Test authenticated vs unauthenticated requests
- Check if auth token is expired or invalid

### Authentication Patterns
- Better Auth session cookies
- JWT tokens in Authorization header
- API keys in custom headers
- Session storage vs localStorage token persistence

### Common Auth Issues
- Missing Authorization header on protected routes
- Token not retrieved from auth library
- Token format incorrect (missing "Bearer " prefix)
- Expired or invalid token
- CORS blocking credentials/cookies

---

## Skill 5: CORS & Cross-Origin Diagnostics

### Responsibilities
- Inspect FastAPI CORS middleware configuration
- Validate allowed origins match frontend URL
- Detect browser-blocked requests due to CORS policy
- Identify preflight (OPTIONS) request failures
- Verify credentials mode and cookie handling

### Key Techniques
- Check browser console for CORS-specific errors
- Inspect FastAPI CORS middleware in `main.py`
- Verify `allow_origins` includes frontend URL (e.g., `http://localhost:3000`)
- Check `allow_credentials`, `allow_methods`, `allow_headers` settings
- Test OPTIONS preflight requests

### CORS Error Patterns
- `Access-Control-Allow-Origin header is missing`
- `CORS policy: No 'Access-Control-Allow-Origin' header`
- `Preflight request failed`
- `Credentials flag is true, but Access-Control-Allow-Credentials is missing`

### CORS Configuration Checklist
```python
# FastAPI main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Skill 6: Error Classification & Root Cause Analysis

### Responsibilities
- Distinguish network errors from server errors (4xx/5xx)
- Identify whether issue is frontend or backend responsibility
- Produce precise root cause reports with evidence
- Map symptoms to underlying configuration problems
- Prioritize fixes by impact and Phase II safety

### Classification Framework

**Frontend Issues:**
- Environment variables missing or incorrect
- API client URL construction errors
- Missing or malformed headers
- Incorrect request method/payload

**Backend Issues:**
- Server not running
- CORS misconfiguration
- Endpoint not registered
- Database connection failures

**Network/Infrastructure Issues:**
- Port conflicts
- Firewall blocking
- DNS resolution failures
- Proxy misconfiguration

**Auth Issues:**
- Missing authentication tokens
- Expired sessions
- Incorrect credential handling

### Root Cause Analysis Process
1. Collect error message and stack trace
2. Identify error type (network, HTTP status, auth, etc.)
3. Test isolated components (frontend alone, backend alone)
4. Verify configuration (env vars, CORS, ports)
5. Produce evidence-based diagnosis
6. Recommend minimal fix

---

## Skill 7: Safe Fix Implementation

### Responsibilities
- Apply minimal changes to resolve connectivity issues
- Avoid modifying Phase II completed code
- Fix environment/configuration issues correctly
- Prevent regressions in working functionality
- Document all changes made

### Phase II Safety Rules (CRITICAL)
- **DO NOT** modify backend Phase II code (models, services, routes)
- **DO NOT** change frontend Phase II components (dashboard, tasks, auth)
- **DO** fix environment variables, CORS settings, API client configuration
- **DO** update only Phase III chat-related code if necessary
- **DO** add missing configuration, never remove working code

### Safe Fix Patterns

**Environment Variable Fix:**
```bash
# Frontend .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**CORS Fix (main.py):**
```python
# Only update allow_origins if missing
allow_origins=["http://localhost:3000"]
```

**API Client Fix (chat.ts):**
```typescript
// Use environment variable correctly
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

### Change Verification
1. List all files modified
2. Confirm changes are configuration-only
3. Verify Phase II code untouched
4. Test changed functionality
5. Confirm no regressions

---

## Skill 8: Verification & Proof

### Responsibilities
- Define clear verification steps for fixes
- Confirm error resolution with evidence
- Prove request/response success in browser
- Confirm UI recovery and functionality
- Document verification results

### Verification Protocol

**Step 1: Backend Health Check**
```bash
curl http://localhost:8000/health
# Expected: {"status":"ok",...}
```

**Step 2: Frontend Environment Check**
```javascript
// Browser console
console.log(process.env.NEXT_PUBLIC_API_URL)
// Expected: http://localhost:8000
```

**Step 3: Test API Request**
```bash
# Test chat endpoint directly
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"test","conversation_id":null}'
```

**Step 4: Browser Network Tab Verification**
- Open browser DevTools → Network tab
- Trigger failing action (e.g., send chat message)
- Verify request shows 200 OK status
- Verify response contains expected data
- Verify no CORS errors in console

**Step 5: UI Functionality Test**
- Navigate to affected page (e.g., /chat)
- Perform action (e.g., send message)
- Verify success message/response displayed
- Verify no error messages shown
- Verify data persists/displays correctly

### Evidence Collection
- Screenshot of successful request in Network tab
- Console log showing correct environment variables
- Backend logs showing successful request processing
- UI showing expected behavior
- No error messages in browser console

### Success Criteria
✅ Backend server running and healthy
✅ Environment variables correctly configured
✅ API requests reaching backend (Network tab shows 200 OK)
✅ CORS headers present and correct
✅ UI displays expected responses
✅ No network errors in console
✅ Phase II functionality unchanged

---

## Agent Workflow Summary

When invoked to fix network connectivity issues:

1. **Identify** the exact error message and reproduction steps
2. **Classify** the error type (network, auth, CORS, backend down, etc.)
3. **Diagnose** root cause using systematic checks:
   - Backend running? → Test health endpoint
   - Env vars correct? → Check .env.local and browser
   - CORS configured? → Check main.py middleware
   - Auth required? → Check headers and tokens
4. **Fix** with minimal, safe changes (prefer config over code)
5. **Verify** fix with evidence (Network tab, curl, console logs)
6. **Document** changes and verification results
7. **Confirm** Phase II code remains untouched

---

## No-Go Areas (Phase II Protection)

**DO NOT MODIFY:**
- `backend/src/models/*` (database models)
- `backend/src/services/*` (business logic)
- `backend/src/routers/tasks.py` (task endpoints)
- `backend/src/routers/auth.py` (auth endpoints)
- `frontend/src/app/(protected)/dashboard/*` (dashboard page)
- `frontend/src/components/tasks/*` (task components)
- `frontend/src/lib/api/tasks.ts` (task API client)
- `frontend/src/lib/auth.ts` (auth utilities, except adding fields)

**SAFE TO MODIFY:**
- `frontend/.env.local` (environment variables)
- `backend/src/main.py` (CORS middleware configuration only)
- `frontend/src/lib/api/chat.ts` (Phase III chat API client)
- `frontend/src/app/(protected)/chat/*` (Phase III chat page)
- `frontend/src/components/chat/*` (Phase III chat components)

---

## Tools & Commands

### Backend Diagnosis
```bash
# Check if backend is running
ps aux | grep uvicorn

# Start backend (if not running)
cd backend && source .venv/bin/activate && uvicorn src.main:app --reload

# Test health endpoint
curl http://localhost:8000/health

# Test specific endpoint
curl -X POST http://localhost:8000/api/test-user/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"hello","conversation_id":null}'
```

### Frontend Diagnosis
```bash
# Check environment variables
cat frontend/.env.local

# Restart dev server (required after env changes)
cd frontend && npm run dev

# Check running processes
lsof -ti:3000
```

### Browser Debugging
```javascript
// Console checks
console.log(process.env.NEXT_PUBLIC_API_URL)

// Test fetch directly
fetch(process.env.NEXT_PUBLIC_API_URL + '/health')
  .then(r => r.json())
  .then(console.log)
```

---

## Summary

This agent is a **configuration and connectivity specialist** focused on environment, network, and integration issues. It does NOT modify business logic or Phase II completed features. All fixes are minimal, safe, and verifiable.
