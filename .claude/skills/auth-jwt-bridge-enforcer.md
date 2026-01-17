# Auth-JWT-Bridge-Enforcer Agent Skills

**Agent Purpose**: Enforce secure authentication bridge between Next.js frontend (Better Auth) and FastAPI backend (JWT tokens)

**Context**:
- Frontend: Next.js 15+ with Better Auth client (JWT plugin enabled)
- Backend: FastAPI with python-jose for JWT verification
- Shared Secret: `BETTER_AUTH_SECRET` environment variable
- Architecture: Stateless backend, JWT-based authentication, user data isolation

---

## Skill 1: validate_better_auth_jwt_issuance

### Purpose
Validate that Better Auth is correctly configured to issue JWT tokens with required claims and proper signing.

### Validations / Rules
- Better Auth JWT plugin MUST be enabled in frontend auth configuration
- JWT tokens MUST include standard claims: `sub` (user_id), `exp` (expiration), `iat` (issued at)
- JWT signing algorithm MUST be HS256 or RS256 (no 'none' algorithm)
- Token expiration MUST be set (recommended: 1 hour for access tokens per constitution)
- JWT secret MUST be loaded from environment variable `BETTER_AUTH_SECRET`
- Better Auth configuration file MUST NOT hardcode secrets
- Tokens MUST include user identifier that matches backend User model primary key

### Fail Conditions
- JWT plugin not enabled in Better Auth configuration
- JWT secret is hardcoded in configuration file
- Token expiration not configured or set to > 24 hours
- Algorithm set to 'none' or insecure algorithm
- Required claims (`sub`, `exp`, `iat`) missing from token payload
- User identifier in token does not match backend User.id format (e.g., UUID vs integer mismatch)

### Used By
- Frontend-Architecture-Auditor (when reviewing auth setup)
- Security-Baseline-Agent (secret management validation)
- Full-Stack-Consistency-Agent (ensure frontend/backend user_id alignment)

---

## Skill 2: enforce_frontend_jwt_attachment

### Purpose
Ensure all API requests from frontend to backend include valid JWT token in Authorization header.

### Validations / Rules
- All API client functions MUST attach JWT token to requests
- Token MUST be sent in `Authorization: Bearer <token>` header format
- API client MUST retrieve token from Better Auth session (not localStorage directly)
- Requests to protected endpoints MUST fail fast if no token available
- Token retrieval MUST handle cases where user is not authenticated
- API client MUST NOT send tokens to external domains (only to configured backend API URL)
- Frontend MUST NOT cache tokens beyond Better Auth's session management

### Fail Conditions
- API request function to protected endpoint does not include Authorization header
- Token retrieved from localStorage instead of Better Auth session
- Token sent in query parameter or request body (insecure)
- Token sent to external domain (security violation)
- Hardcoded tokens in API client code
- Missing error handling when token retrieval fails

### Used By
- Frontend-Architecture-Auditor (API client review)
- Security-Baseline-Agent (prevent token leakage)
- Full-Stack-Consistency-Agent (verify auth flow)

---

## Skill 3: verify_fastapi_jwt_middleware

### Purpose
Validate that FastAPI backend has proper JWT verification middleware protecting all endpoints that require authentication.

### Validations / Rules
- JWT verification dependency MUST be implemented (e.g., `get_current_user` dependency)
- Verification MUST use python-jose or equivalent with HS256/RS256 algorithm matching frontend
- JWT secret MUST be loaded from environment variable `BETTER_AUTH_SECRET` (same as frontend)
- Verification MUST validate token signature, expiration, and required claims
- Protected endpoints MUST use authentication dependency injection
- Middleware MUST return 401 Unauthorized for invalid/missing tokens
- Middleware MUST return 401 for expired tokens
- Middleware MUST extract user_id from `sub` claim and make available to endpoint handlers

### Fail Conditions
- No JWT verification middleware implemented
- JWT secret hardcoded in backend code
- JWT secret different from frontend's `BETTER_AUTH_SECRET`
- Algorithm mismatch between frontend issuance and backend verification
- Protected endpoint does not use authentication dependency
- Token expiration not validated
- Invalid tokens return 200 OK or 403 instead of 401
- User identity not extracted from token

### Used By
- Auth-Integration-Auditor (authentication system review)
- Security-Baseline-Agent (secret management, middleware validation)
- API-Contract-Auditor (ensure protected endpoints require auth)
- Backend-Code-Quality-Agent (dependency injection pattern review)

---

## Skill 4: extract_and_validate_user_identity_from_jwt

### Purpose
Ensure user identity is correctly extracted from JWT token claims and validated before use in business logic.

### Validations / Rules
- User ID MUST be extracted from JWT `sub` claim (not from request body/params)
- Extracted user_id MUST match backend User model ID type (UUID, integer, etc.)
- User_id MUST be validated (not null, proper format)
- Extracted user_id MUST be passed to service layer for data isolation
- Endpoint handlers MUST NOT accept user_id from request parameters when JWT is available
- User identity MUST be verified to exist in database before processing requests

### Fail Conditions
- User_id taken from request body/query params instead of JWT token
- User_id not extracted from JWT at all
- Type mismatch between JWT user_id and database User.id type
- User_id accepted as null or empty string
- Endpoint allows overriding JWT user_id with request parameter
- No validation that user exists in database

### Used By
- Auth-Integration-Auditor (validate user identity extraction)
- Backend-Code-Quality-Agent (service layer design review)
- Data-Model-Auditor (ensure ID type consistency)
- Full-Stack-Consistency-Agent (type alignment check)

---

## Skill 5: enforce_route_userid_matching

### Purpose
Ensure that route parameters containing user_id match the authenticated user's ID from JWT token (prevent unauthorized access).

### Validations / Rules
- Routes with `/users/{user_id}` or similar patterns MUST validate user_id matches JWT user_id
- Endpoints accessing user-specific resources MUST check resource ownership
- GET/PUT/DELETE operations on user resources MUST verify current_user.id == resource.user_id
- Admin bypass logic (if any) MUST be explicit and documented
- Authorization check MUST return 403 Forbidden (not 404) when user_id mismatch detected
- Task, Todo, or similar user-owned entities MUST enforce user_id matching

### Fail Conditions
- Route accepts any user_id without checking against JWT user_id
- Endpoint returns another user's data when user_id in URL doesn't match JWT
- Authorization check missing on endpoints that modify user-specific data
- 404 returned instead of 403 when user tries to access another user's resource
- Service layer does not filter queries by current user_id

### Used By
- Auth-Integration-Auditor (authorization logic review)
- API-Contract-Auditor (ensure proper error codes for unauthorized access)
- Security-Baseline-Agent (prevent unauthorized data access)
- Backend-Code-Quality-Agent (authorization pattern review)

---

## Skill 6: enforce_database_user_isolation

### Purpose
Ensure all database queries filter by authenticated user_id to enforce data isolation between users.

### Validations / Rules
- All SELECT queries for user-owned entities MUST include `WHERE user_id = current_user.id`
- All INSERT operations MUST set user_id to current_user.id (not from request)
- All UPDATE/DELETE operations MUST include `WHERE user_id = current_user.id`
- Database models for user-owned entities MUST have user_id foreign key
- ORM queries MUST filter by user_id before executing
- No raw SQL queries that bypass user_id filtering
- Service layer MUST accept current_user from dependency injection

### Fail Conditions
- Query returns all records without user_id filter
- INSERT allows client to specify user_id in request body
- UPDATE/DELETE does not filter by user_id (can modify other users' data)
- Service function does not accept current_user parameter
- Raw SQL query bypasses ORM without user_id filtering
- Query filters by user_id from request parameter instead of JWT token

### Used By
- Data-Model-Auditor (database query review)
- Auth-Integration-Auditor (validate data isolation)
- Security-Baseline-Agent (prevent data leakage)
- Backend-Code-Quality-Agent (service layer pattern review)

---

## Skill 7: validate_shared_secret_usage

### Purpose
Ensure JWT secret is properly shared between frontend and backend via environment variables, never hardcoded.

### Validations / Rules
- Frontend MUST load `BETTER_AUTH_SECRET` from `.env.local` or environment
- Backend MUST load `BETTER_AUTH_SECRET` from `.env` or environment
- Both frontend and backend MUST use identical secret value
- Secret MUST be at least 32 characters (256 bits recommended)
- Secret MUST NOT be committed to version control (`.env` in `.gitignore`)
- `.env.example` files MUST show placeholder, not actual secret
- Deployment documentation MUST specify secret must be set in production environment

### Fail Conditions
- Secret hardcoded in source code (frontend or backend)
- Frontend and backend use different secret values
- Secret committed to git repository
- Secret length < 32 characters
- `.env.example` contains actual secret value
- No environment variable validation on application startup

### Used By
- Security-Baseline-Agent (secret management audit)
- Full-Stack-Consistency-Agent (ensure frontend/backend secret alignment)
- Spec-Kit-Structure-Guardian (validate .env files in .gitignore)

---

## Skill 8: validate_token_expiry_and_security

### Purpose
Ensure JWT tokens have proper expiration, refresh strategy, and security configurations.

### Validations / Rules
- Access tokens MUST have expiration time (recommended: 1 hour per constitution)
- Token expiration MUST be validated on every request
- Expired tokens MUST return 401 Unauthorized with clear error message
- Frontend MUST handle 401 responses by clearing session and redirecting to login
- Token refresh logic (if implemented) MUST use refresh tokens, not extend access token lifetime
- JWT payload MUST NOT contain sensitive data (password, payment info, etc.)
- Tokens MUST be transmitted only over HTTPS in production

### Fail Conditions
- Access token has no expiration or expiration > 24 hours
- Backend does not validate token expiration
- Expired token returns 200 OK or 403 instead of 401
- Frontend does not handle 401 responses (stale sessions persist)
- Token refresh extends access token lifetime instead of issuing new token
- Sensitive data (password hash, etc.) included in JWT payload
- Application allows JWT transmission over HTTP in production

### Used By
- Security-Baseline-Agent (token security audit)
- Auth-Integration-Auditor (token lifecycle validation)
- API-Contract-Auditor (ensure 401 responses for expired tokens)
- Frontend-Architecture-Auditor (401 error handling)

---

## Skill 9: prevent_stateful_backend_violations

### Purpose
Ensure backend remains stateless by preventing session storage, token caching, or server-side user state.

### Validations / Rules
- Backend MUST NOT store JWT tokens in database or cache
- Backend MUST NOT maintain server-side sessions
- All user identity MUST come from JWT token on each request
- No in-memory user session storage (e.g., global dicts, Redis sessions)
- User state MUST be reconstructed from JWT + database on every request
- Logout MUST be client-side only (clear frontend token, no backend state change)

### Fail Conditions
- Backend stores JWT tokens in database
- Backend uses session middleware (e.g., Flask sessions, FastAPI sessions)
- Backend caches user authentication state in Redis/memory
- Logout endpoint modifies backend state instead of being client-side only
- Backend maintains global user session dict

### Used By
- Auth-Integration-Auditor (stateless backend validation)
- Backend-Code-Quality-Agent (architecture review)
- Phase2-Quality-Orchestrator (constitution compliance check)

---

## Skill 10: validate_cors_and_token_security

### Purpose
Ensure CORS policy and token transmission security prevent cross-origin attacks.

### Validations / Rules
- Backend CORS MUST allow only specific frontend origin (not `*`)
- CORS credentials MUST be enabled for cookie-based auth (if used)
- Authorization header MUST be allowed in CORS policy
- Frontend API client MUST only send tokens to configured backend URL
- Tokens MUST NOT be exposed in URL query parameters
- Tokens MUST NOT be logged in frontend console or backend logs
- Production environment MUST enforce HTTPS for all API requests

### Fail Conditions
- CORS allows all origins (`Access-Control-Allow-Origin: *`)
- Authorization header not in CORS allowed headers
- Frontend sends tokens to external domains
- Tokens passed in URL query string (e.g., `/api/tasks?token=...`)
- Tokens logged in application logs or browser console
- Production allows HTTP for API requests (not HTTPS only)

### Used By
- Security-Baseline-Agent (CORS and transport security)
- API-Contract-Auditor (header validation)
- Frontend-Architecture-Auditor (API client security)

---

## Skill 11: enforce_error_response_consistency

### Purpose
Ensure authentication errors return consistent, informative responses across frontend and backend.

### Validations / Rules
- 401 responses MUST have consistent format: `{"error": "message", "code": "UNAUTHORIZED", "status": 401}`
- Frontend MUST map 401 responses to user-friendly messages
- Backend MUST NOT leak sensitive information in auth error messages
- Token expiration errors MUST be distinguishable from invalid token errors
- Frontend error handling MUST clear token and redirect to login on 401
- Error messages MUST be symmetric (backend error codes match frontend error handling)

### Fail Conditions
- 401 responses have inconsistent structure across endpoints
- Error messages expose sensitive information (secret key, token payload)
- Frontend does not handle 401 responses consistently
- Token expiration and invalid token return same generic error
- Frontend does not clear token on 401 response

### Used By
- Full-Stack-Consistency-Agent (error symmetry validation)
- API-Contract-Auditor (error response schema validation)
- Frontend-Architecture-Auditor (error handling review)
- Backend-Code-Quality-Agent (error response consistency)

---

## Agent Invocation Workflow

### When to Invoke Auth-JWT-Bridge-Enforcer

**During Backend Authentication Implementation**:
1. After implementing JWT verification middleware
2. After creating protected endpoints
3. After implementing user_id extraction logic
4. Before committing authentication code

**During Frontend Authentication Implementation**:
1. After configuring Better Auth with JWT plugin
2. After creating API client with token attachment
3. After implementing 401 error handling
4. Before committing authentication code

**During Cross-Stack Integration**:
1. After both frontend and backend auth implemented
2. Before end-to-end authentication testing
3. After any changes to JWT configuration
4. During security audits

### Skills Invocation Order (Recommended)

**Phase 1: Configuration Validation**
1. `validate_shared_secret_usage` - Ensure secrets properly configured
2. `validate_better_auth_jwt_issuance` - Validate frontend token generation
3. `verify_fastapi_jwt_middleware` - Validate backend token verification

**Phase 2: Identity & Authorization**
4. `extract_and_validate_user_identity_from_jwt` - Validate user extraction
5. `enforce_route_userid_matching` - Validate route authorization
6. `enforce_database_user_isolation` - Validate data isolation

**Phase 3: Security & Compliance**
7. `validate_token_expiry_and_security` - Validate token lifecycle
8. `prevent_stateful_backend_violations` - Validate stateless backend
9. `validate_cors_and_token_security` - Validate CORS and transport
10. `enforce_frontend_jwt_attachment` - Validate frontend token attachment
11. `enforce_error_response_consistency` - Validate error handling

### Integration with Other Agents

- **Security-Baseline-Agent**: Collaborates on secret management, CORS, HTTPS
- **Full-Stack-Consistency-Agent**: Collaborates on type alignment, error symmetry
- **API-Contract-Auditor**: Collaborates on 401 error responses, protected endpoints
- **Data-Model-Auditor**: Collaborates on user_id foreign keys, data isolation
- **Phase2-Quality-Orchestrator**: Invokes Auth-JWT-Bridge-Enforcer during final compliance review

---

## Success Criteria

Auth-JWT-Bridge-Enforcer PASSES when:
- ✅ Frontend issues JWT tokens via Better Auth with correct claims
- ✅ All API requests include JWT token in Authorization header
- ✅ Backend verifies JWT tokens on all protected endpoints
- ✅ User_id extracted from JWT token, never from request parameters
- ✅ Route authorization checks prevent unauthorized access (403)
- ✅ Database queries filtered by user_id enforce data isolation
- ✅ Shared secret loaded from environment, never hardcoded
- ✅ Tokens have proper expiration and security configurations
- ✅ Backend remains stateless (no sessions, no token storage)
- ✅ CORS configured correctly, tokens transmitted securely
- ✅ Error responses consistent across frontend and backend

Auth-JWT-Bridge-Enforcer FAILS when:
- ❌ Any JWT secret is hardcoded
- ❌ Protected endpoint missing authentication dependency
- ❌ User can access another user's data via URL manipulation
- ❌ Database query does not filter by user_id
- ❌ Backend stores JWT tokens or maintains sessions
- ❌ CORS allows all origins or tokens sent over HTTP in production
- ❌ Error responses inconsistent or leak sensitive information

---

## Notes

- This agent is CRITICAL for multi-user applications with authentication
- Invoke BEFORE deploying any authentication code to production
- All skills MUST pass for Phase II compliance
- Skills are reusable across different endpoints and components
- Agent enforces both security and consistency between frontend/backend
