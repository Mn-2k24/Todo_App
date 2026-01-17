# Frontend-Backend-Auth-Integration Skills

**Agent Purpose**: Verify and stabilize the connection between frontend authentication UI and backend APIs, including token/cookie propagation, session validation, protected endpoint access, and logout integration.

**Context**:
- Frontend: Next.js 15+ with Better Auth, React 19
- Backend: FastAPI with JWT tokens, httpOnly cookies
- Auth mechanism: JWT tokens stored in httpOnly cookies
- Session validation: Backend `/api/auth/me` endpoint
- Protected routes enforced by Next.js middleware + backend validation
- Navigation: window.location.href for post-auth redirects (not router.push)

**Boundaries**:
- This agent focuses on frontend-backend integration layer
- Does NOT implement UI components (Frontend-Auth-UI-Agent handles that)
- Does NOT implement backend endpoints (assumes backend exists)
- Does NOT modify authentication algorithms or token generation

**Safety Rules**:
- NEVER expose tokens in localStorage (use httpOnly cookies only)
- NEVER bypass backend authentication validation
- NEVER allow protected API calls without valid session
- Changes must maintain security posture (no token leakage)

---

## Skill 1: validate_login_api_integration

### Purpose
Verify login form correctly calls backend login API and handles response, cookies, and redirects.

### Validations / Rules
- LoginForm MUST call backend `/api/auth/login` endpoint
- Request MUST include credentials: `{ email, password }`
- Request MUST use `credentials: "include"` for cookie handling
- Response MUST set httpOnly cookie (`todo_app_token`)
- Success response (200) MUST trigger redirect to `/dashboard`
- Redirect MUST use `window.location.href` (not `router.push`)
- Error response (401, 400) MUST display error message to user
- Network errors MUST be caught and displayed gracefully
- Loading state MUST be shown during API call
- Form MUST be disabled during submission (prevent double-submit)

### Fail Conditions
- Login does not call backend API
- Request missing `credentials: "include"`
- httpOnly cookie not set after successful login
- Redirect uses `router.push` (causes cookie propagation issues)
- Error responses not handled (no error message shown)
- Network errors crash the form (uncaught promise rejection)
- No loading state during API call
- Form allows multiple submissions (race condition)

### Used By
- Frontend-Auth-UI-Agent (login form implementation)
- Auth-Integration-Auditor (API contract validation)
- Security-Guardian (ensure secure credential handling)
- Auth-Reload-Debugger (diagnose login issues)

---

## Skill 2: validate_register_api_integration

### Purpose
Verify registration form correctly calls backend register API and handles response, cookies, and redirects.

### Validations / Rules
- RegisterForm MUST call backend `/api/auth/register` endpoint
- Request MUST include: `{ email, password, name }` (or required fields)
- Request MUST use `credentials: "include"` for cookie handling
- Response MUST set httpOnly cookie (`todo_app_token`)
- Success response (201, 200) MUST trigger redirect to `/dashboard`
- Redirect MUST use `window.location.href` (not `router.push`)
- Error response (400, 409) MUST display error message to user
- Duplicate email (409) MUST show specific error message
- Validation errors MUST be displayed per-field (if backend provides)
- Network errors MUST be caught and displayed gracefully
- Loading state MUST be shown during API call

### Fail Conditions
- Registration does not call backend API
- Request missing required fields
- Request missing `credentials: "include"`
- httpOnly cookie not set after successful registration
- Redirect uses `router.push` (causes cookie propagation issues)
- Error responses not handled
- Duplicate email error not shown to user
- Network errors crash the form
- No loading state during API call

### Used By
- Frontend-Auth-UI-Agent (register form implementation)
- Auth-Integration-Auditor (API contract validation)
- Security-Guardian (ensure secure registration)
- Auth-Reload-Debugger (diagnose registration issues)

---

## Skill 3: validate_session_api_integration

### Purpose
Verify frontend correctly calls backend session validation API to check authentication state.

### Validations / Rules
- Auth library MUST call `/api/auth/me` to validate session
- Request MUST use `credentials: "include"` to send httpOnly cookie
- Success response (200) MUST return user object: `{ id, email, name }`
- Failure response (401) MUST indicate unauthenticated state
- Frontend MUST handle expired/invalid tokens gracefully
- Session check MUST be called on:
  - Homepage load (to show correct buttons)
  - Protected route access (middleware or component)
  - After login/register (to get user details)
- Session check MUST NOT be called excessively (cache results)
- Network errors MUST NOT crash the app

### Fail Conditions
- Session check does not call `/api/auth/me`
- Request missing `credentials: "include"`
- Success response does not return user object
- Expired token not handled (app crashes or infinite loading)
- Session check called on every render (performance issue)
- Network errors crash the app
- Session check not called when needed (auth state inaccurate)

### Used By
- Frontend-Auth-UI-Agent (auth state evaluation)
- Auth-Integration-Auditor (session lifecycle validation)
- Auth-Reload-Debugger (diagnose infinite loading)
- Security-Guardian (validate session security)

---

## Skill 4: validate_logout_api_integration

### Purpose
Verify sign-out correctly calls backend logout API to clear httpOnly cookie and session.

### Validations / Rules
- Sign Out MUST call backend `/api/auth/logout` endpoint
- Request MUST use `credentials: "include"` to send cookie
- Backend MUST delete httpOnly cookie (`response.delete_cookie`)
- Frontend MUST clear localStorage (tokens, user data)
- Frontend MUST redirect to homepage (`/`) after logout
- Redirect MUST show unauthenticated UI (Sign In button visible)
- Logout MUST work even if backend call fails (graceful degradation)
- After logout, protected routes MUST redirect to login
- After logout, session API (`/api/auth/me`) MUST return 401

### Fail Conditions
- Sign Out does not call backend logout API
- Request missing `credentials: "include"`
- Backend does not delete httpOnly cookie
- Frontend does not clear localStorage
- No redirect to homepage after logout
- After logout, user still appears authenticated
- After logout, protected routes still accessible
- Logout fails if backend is unreachable (no graceful degradation)

### Used By
- Frontend-Auth-UI-Agent (sign out button implementation)
- Auth-Integration-Auditor (logout flow validation)
- Security-Guardian (ensure session properly destroyed)
- Auth-Reload-Debugger (diagnose logout issues)

---

## Skill 5: validate_protected_api_calls

### Purpose
Verify protected API calls (e.g., tasks CRUD) correctly send authentication and handle 401 responses.

### Validations / Rules
- ALL protected API calls MUST use `credentials: "include"`
- Backend MUST validate httpOnly cookie on protected endpoints
- Unauthenticated requests MUST return 401
- Frontend MUST handle 401 responses:
  - Clear auth state (logout)
  - Redirect to login page
- Protected calls MUST NOT execute for unauthenticated users
- Token expiry MUST be detected and handled
- Network errors MUST be caught and displayed
- Loading states MUST be shown during API calls

### Fail Conditions
- Protected API calls missing `credentials: "include"`
- Backend does not validate authentication
- 401 responses not handled (app crashes or shows stale data)
- Unauthenticated users can make protected API calls
- Token expiry not detected (stale session)
- Network errors crash the app
- No loading states during protected API calls

### Used By
- API-Backend-Guardian (backend validation)
- Auth-Integration-Auditor (API authentication validation)
- Security-Guardian (ensure all protected endpoints secured)
- Cross-Stack-Consistency-Agent (frontend-backend contract)

---

## Skill 6: validate_cookie_propagation

### Purpose
Ensure httpOnly cookies are properly set and propagated during authentication flows.

### Validations / Rules
- Login/register APIs MUST set httpOnly cookie in response
- Cookie MUST have correct attributes:
  - `httpOnly: true` (not accessible via JavaScript)
  - `sameSite: lax` or `strict` (CSRF protection)
  - `secure: true` in production (HTTPS only)
  - `path: /` (available to all routes)
- Cookie MUST be sent with all subsequent requests (`credentials: "include"`)
- Middleware MUST be able to read cookie for route protection
- Backend APIs MUST be able to read cookie for authentication
- Post-auth redirect MUST use `window.location.href` for full page reload
- Cookie MUST persist across page refreshes
- Cookie MUST be deleted on logout

### Fail Conditions
- Cookie not set after login/register
- Cookie missing `httpOnly: true` (security risk)
- Cookie missing `sameSite` (CSRF risk)
- Cookie not sent with requests (missing `credentials: "include"`)
- Middleware cannot read cookie (route protection fails)
- Backend APIs cannot read cookie (authentication fails)
- Post-auth redirect uses `router.push` (cookie not propagated before middleware check)
- Cookie not persisted across refreshes
- Cookie not deleted on logout

### Used By
- Security-Guardian (cookie security validation)
- Auth-Reload-Debugger (diagnose cookie propagation issues)
- Auth-JWT-Bridge-Enforcer (JWT cookie validation)
- Cross-Stack-Consistency-Agent (cookie consistency)

---

## Skill 7: validate_redirect_navigation

### Purpose
Ensure post-authentication redirects use correct navigation method to avoid cookie propagation race conditions.

### Validations / Rules
- After successful login: MUST use `window.location.href = "/dashboard"`
- After successful register: MUST use `window.location.href = "/dashboard"`
- After logout: MUST use `window.location.href = "/"`
- MUST NOT use `router.push()` for post-auth redirects
- Redirect MUST happen AFTER API response completes
- Redirect MUST trigger full page reload (ensures middleware checks cookie)
- Redirect MUST NOT cause infinite loops
- Middleware MUST allow redirect target if authenticated
- Middleware MUST block redirect target if unauthenticated

### Fail Conditions
- Login/register redirects use `router.push()` (infinite loading)
- Redirect happens before API response (race condition)
- Redirect does not trigger full page reload
- Redirect causes infinite loop (middleware redirects back)
- Middleware blocks authenticated user from dashboard
- Middleware allows unauthenticated user to dashboard

### Used By
- Home-Auth-Flow-Agent (routing logic validation)
- Auth-Reload-Debugger (diagnose redirect loops)
- Frontend-Auth-UI-Agent (post-auth navigation)
- Cross-Stack-Consistency-Agent (frontend-backend redirect consistency)

---

## Skill 8: validate_error_handling

### Purpose
Ensure all auth API calls have proper error handling with user-friendly messages.

### Validations / Rules
- Network errors (fetch failure) MUST be caught and displayed
- HTTP error responses (400, 401, 409, 500) MUST be caught and displayed
- Error messages MUST be user-friendly (not raw error text)
- Specific errors MUST have specific messages:
  - 401: "Invalid email or password"
  - 409: "Email already registered"
  - 500: "Something went wrong. Please try again."
- Loading state MUST be cleared on error
- Form MUST be re-enabled on error (allow retry)
- Sensitive error details MUST NOT be shown to user
- Console errors MUST be logged for debugging

### Fail Conditions
- Network errors crash the app (uncaught promise rejection)
- HTTP errors not handled (no error message)
- Error messages not user-friendly (show stack trace)
- Loading state persists on error (infinite loading)
- Form remains disabled on error (user cannot retry)
- Sensitive error details exposed to user
- No console logs for debugging

### Used By
- Frontend-Auth-UI-Agent (error UI validation)
- Auth-Reload-Debugger (diagnose API errors)
- Frontend-UI-Professional (error message UX)
- Security-Guardian (ensure no sensitive data leakage)

---

## Agent Invocation Workflow

### When to Invoke Frontend-Backend-Auth-Integration

**After Frontend UI Implementation**:
1. After login form created
2. After register form created
3. After sign out button added
4. Before end-to-end testing

**After Backend API Changes**:
1. After modifying login/register endpoints
2. After changing JWT token structure
3. After updating cookie attributes
4. After adding new protected endpoints

**During Bug Fixes**:
1. When infinite loading occurs after login
2. When cookies not propagated correctly
3. When protected APIs return 401 unexpectedly
4. When logout does not clear session
5. When page refresh loses authentication

**During Quality Assurance**:
1. Before merging auth integration PR
2. After any auth API changes
3. During end-to-end testing
4. Before production deployment

### Skills Invocation Order (Recommended)

**Phase 1: Login & Register**
1. `validate_login_api_integration` - Login flow
2. `validate_register_api_integration` - Register flow
3. `validate_cookie_propagation` - Cookie setup
4. `validate_redirect_navigation` - Post-auth redirects

**Phase 2: Session & Logout**
5. `validate_session_api_integration` - Session checks
6. `validate_logout_api_integration` - Logout flow

**Phase 3: Protected APIs & Errors**
7. `validate_protected_api_calls` - Protected endpoints
8. `validate_error_handling` - Error scenarios

### Integration with Other Agents

- **Frontend-Auth-UI-Agent**: Provides UI components, this agent validates integration
- **API-Backend-Guardian**: Validates backend API correctness
- **Auth-Integration-Auditor**: Comprehensive auth lifecycle audit
- **Security-Guardian**: Validates security of API calls and cookies
- **Auth-Reload-Debugger**: Diagnoses integration issues causing infinite loading
- **Cross-Stack-Consistency-Agent**: Ensures frontend-backend contract alignment

---

## Success Criteria

Frontend-Backend-Auth-Integration PASSES when:
- ✅ Login API called correctly with credentials: "include"
- ✅ Register API called correctly with credentials: "include"
- ✅ httpOnly cookie set after successful login/register
- ✅ Post-auth redirects use window.location.href (not router.push)
- ✅ Session API (`/api/auth/me`) called correctly
- ✅ Logout API called and cookie deleted
- ✅ Protected API calls include credentials: "include"
- ✅ 401 responses handled gracefully (redirect to login)
- ✅ Cookie persists across page refreshes
- ✅ Error messages user-friendly and informative
- ✅ No infinite loading or redirect loops

Frontend-Backend-Auth-Integration FAILS when:
- ❌ Login/register missing credentials: "include"
- ❌ httpOnly cookie not set after auth
- ❌ Post-auth redirects use router.push (infinite loading)
- ❌ Session API not called or returns wrong data
- ❌ Logout does not clear cookie
- ❌ Protected APIs accessible without auth
- ❌ 401 responses crash the app
- ❌ Cookie not persisted across refreshes
- ❌ Error messages not shown or not user-friendly
- ❌ Infinite loading or redirect loops occur

---

## Notes

- This agent focuses EXCLUSIVELY on frontend-backend integration layer
- Does NOT implement UI (Frontend-Auth-UI-Agent) or backend (API-Backend-Guardian)
- Invoke AFTER UI implementation, BEFORE end-to-end testing
- Critical skill: validate_cookie_propagation (most common auth bug source)
- Key insight: window.location.href required for cookie propagation timing
- Agent ensures integration stability and prevents infinite loading bugs
