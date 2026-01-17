# Auth-Reload-Debugger Skills

**Agent Purpose**: Diagnose and resolve authentication-related bugs including infinite loading, redirect loops, auth guard conflicts, cookie propagation issues, and session persistence problems.

**Context**:
- Frontend: Next.js 15+ with React 19, Better Auth
- Backend: FastAPI with JWT tokens, httpOnly cookies
- Common issue: Infinite loading after login due to cookie propagation race conditions
- Common issue: Redirect loops from competing auth guards (middleware + component)
- Common issue: Dev server cache serving stale code
- Navigation: window.location.href vs router.push() matters for cookie timing

**Boundaries**:
- This agent focuses ONLY on debugging and root cause analysis
- Does NOT implement features (use Frontend-Auth-UI-Agent for that)
- Does NOT modify backend logic (assumes backend is correct)
- Does NOT handle non-auth-related bugs

**Safety Rules**:
- NEVER bypass authentication for debugging (maintain security)
- NEVER disable security features to "fix" symptoms
- NEVER introduce new bugs while fixing existing ones
- Fixes must address root cause, not symptoms

---

## Skill 1: diagnose_infinite_loading

### Purpose
Diagnose and resolve infinite loading states that occur after successful login or register.

### Validations / Rules
- **Symptom identification**:
  - User logs in successfully
  - Loading indicator appears (spinner, skeleton)
  - Loading NEVER completes (infinite state)
  - Dashboard or target page never renders
- **Root cause analysis checklist**:
  1. Check if login redirects use `window.location.href` (not `router.push`)
  2. Check for redundant auth guards (middleware + component-level)
  3. Check cookie propagation timing (httpOnly cookie set before redirect?)
  4. Check for infinite redirect loops (middleware ↔ component)
  5. Check dev server serving updated code (not cached)
  6. Check for race conditions (auth check before cookie propagates)
- **Diagnosis steps**:
  1. Open browser DevTools Network tab
  2. Trigger login flow
  3. Observe requests: login API → redirect → auth check API
  4. Look for repeated redirect requests (indicates loop)
  5. Check if cookie sent with auth check request
- **Common root causes**:
  - `router.push("/dashboard")` doesn't wait for cookie propagation
  - Redundant auth guard in dashboard component redirects to login
  - Middleware sees no cookie and redirects to login
  - Component auth guard sees no user and redirects to login
  - Infinite loop: login → dashboard → redirect to login → redirect to dashboard

### Fail Conditions
- Diagnosis does not identify root cause
- Fix addresses symptom, not root cause
- Fix introduces new bugs
- Fix disables authentication (security risk)

### Used By
- Frontend-Backend-Auth-Integration (validate cookie propagation)
- Auth-Integration-Auditor (auth lifecycle validation)
- Home-Auth-Flow-Agent (routing logic)
- Frontend-Auth-UI-Agent (loading state implementation)

---

## Skill 2: diagnose_redirect_loops

### Purpose
Diagnose and resolve redirect loops where user is bounced between pages indefinitely.

### Validations / Rules
- **Symptom identification**:
  - User logs in successfully
  - Browser redirects repeatedly between routes
  - URL changes rapidly (flashing between /login and /dashboard)
  - Network tab shows repeated redirect requests
- **Root cause analysis checklist**:
  1. Check for competing auth guards (middleware AND component-level)
  2. Check if middleware redirects to login when dashboard has auth guard
  3. Check if component auth guard redirects when middleware already protects route
  4. Check redirect conditions (are they contradictory?)
  5. Check for timing issues (cookie not yet available when guard checks)
- **Diagnosis steps**:
  1. Open browser DevTools Console
  2. Enable "Preserve log" in Network tab
  3. Trigger login flow
  4. Look for pattern: `/api/auth/me` → 401 → redirect to `/login` → redirect to `/dashboard` → repeat
  5. Check if both middleware and component are executing redirects
- **Common root causes**:
  - Dashboard component has `useEffect` checking auth and redirecting
  - Middleware also checks auth and redirects
  - Component check happens before cookie propagates → redirects to login
  - Middleware sees cookie → redirects back to dashboard
  - Infinite loop: dashboard → login → dashboard
- **Solution patterns**:
  - Remove redundant component-level auth guard
  - Trust middleware for route protection
  - Use `window.location.href` for post-auth redirect (full page reload)

### Fail Conditions
- Diagnosis does not identify competing auth guards
- Fix removes ALL auth guards (security risk)
- Fix introduces new redirect loop
- Fix relies on timers or delays (unreliable)

### Used By
- Home-Auth-Flow-Agent (routing logic validation)
- Frontend-Architecture-Auditor (auth guard architecture)
- Auth-Integration-Auditor (auth flow validation)
- Security-Guardian (ensure route protection maintained)

---

## Skill 3: diagnose_cookie_propagation_issues

### Purpose
Diagnose and resolve issues where httpOnly cookies are not propagated correctly between requests.

### Validations / Rules
- **Symptom identification**:
  - Login successful (200 OK)
  - Cookie set in login response (visible in DevTools Application tab)
  - Next request does NOT include cookie
  - Auth check fails (401) despite valid cookie
- **Root cause analysis checklist**:
  1. Check if login request uses `credentials: "include"`
  2. Check if auth check request uses `credentials: "include"`
  3. Check if redirect uses `router.push` (client-side nav, cookie timing issue)
  4. Check cookie attributes (httpOnly, sameSite, path, domain)
  5. Check if CORS configured correctly (backend allows credentials)
  6. Check if frontend and backend on same domain/subdomain
- **Diagnosis steps**:
  1. Open DevTools → Application → Cookies
  2. Trigger login
  3. Check if `todo_app_token` cookie appears
  4. Check cookie attributes (httpOnly: true, sameSite: lax, path: /)
  5. Trigger redirect to dashboard
  6. Open Network tab → Dashboard request → Headers → Request Headers → Cookie
  7. Check if `todo_app_token` is included
- **Common root causes**:
  - Missing `credentials: "include"` in fetch options
  - `router.push` triggers client-side nav before cookie propagates
  - Cookie `sameSite: strict` blocks cookie on redirect
  - Cookie `path` too restrictive (not `/`)
  - CORS not configured to allow credentials
- **Solution patterns**:
  - Add `credentials: "include"` to ALL fetch calls
  - Use `window.location.href` for post-auth redirect
  - Set cookie `sameSite: lax` (allows redirect)
  - Set cookie `path: /` (available to all routes)

### Fail Conditions
- Diagnosis does not check `credentials: "include"`
- Diagnosis does not identify `router.push` timing issue
- Fix stores token in localStorage (security risk)
- Fix disables httpOnly (security risk)

### Used By
- Frontend-Backend-Auth-Integration (cookie propagation validation)
- Security-Guardian (cookie security validation)
- Auth-JWT-Bridge-Enforcer (JWT cookie validation)
- API-Backend-Guardian (backend cookie handling)

---

## Skill 4: diagnose_dev_server_cache

### Purpose
Diagnose and resolve issues where Next.js dev server serves stale/cached code after fixes.

### Validations / Rules
- **Symptom identification**:
  - Code changes made (e.g., removed auth guard, changed router.push)
  - Save file and wait for HMR (Hot Module Reload)
  - Refresh browser
  - Bug still present (old code still running)
- **Root cause analysis checklist**:
  1. Check if `.next` directory contains stale compiled code
  2. Check if dev server detected file change (terminal shows "compiled")
  3. Check if browser cache serving old JavaScript
  4. Check if HMR failed silently (no error, but no update)
  5. Check if environment variables cached (requires restart)
- **Diagnosis steps**:
  1. Check terminal for "compiled successfully" message after save
  2. Open DevTools → Network → Disable cache
  3. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
  4. If still broken: kill server, delete `.next` directory, restart
- **Common root causes**:
  - `.next/` directory contains outdated compiled code
  - Browser cache serving old JavaScript bundle
  - HMR failed to apply changes (rare)
  - Environment variable changes require server restart
- **Solution patterns**:
  1. Kill dev server (Ctrl+C)
  2. Delete `.next` directory: `rm -rf .next`
  3. Restart dev server: `npm run dev`
  4. Hard refresh browser
  5. Verify changes applied

### Fail Conditions
- Diagnosis does not check `.next` directory
- Diagnosis does not verify file changes actually applied
- Fix does not include server restart
- Fix does not clear browser cache

### Used By
- Frontend-Architecture-Auditor (validate code changes applied)
- Auth-Integration-Auditor (ensure fixes active)
- Phase2-Quality-Orchestrator (deployment validation)

---

## Skill 5: diagnose_auth_state_persistence

### Purpose
Diagnose and resolve issues where authentication state is lost on page refresh or navigation.

### Validations / Rules
- **Symptom identification**:
  - User logs in successfully
  - Dashboard loads correctly
  - User refreshes page (F5 or browser refresh button)
  - User appears logged out (redirected to login or shows unauthenticated UI)
- **Root cause analysis checklist**:
  1. Check if httpOnly cookie persists across refreshes
  2. Check if session API (`/api/auth/me`) called on page load
  3. Check if session API fails (401) after refresh
  4. Check if cookie deleted unintentionally
  5. Check if auth state stored only in memory (React state)
  6. Check if localStorage used instead of cookie
- **Diagnosis steps**:
  1. Open DevTools → Application → Cookies
  2. Login successfully
  3. Check `todo_app_token` cookie present
  4. Refresh page
  5. Check if cookie still present (should be)
  6. Open Network tab → Check if `/api/auth/me` called
  7. Check if `/api/auth/me` returns 200 or 401
- **Common root causes**:
  - Cookie not set with correct expiry (expires too soon)
  - Session API not called on page load (app doesn't check auth)
  - Session API fails (backend rejects cookie)
  - Auth state stored only in React state (lost on refresh)
  - Cookie deleted by logout logic running unintentionally
- **Solution patterns**:
  - Ensure cookie set with long expiry (e.g., 30 days)
  - Call session API on homepage/dashboard load
  - Store minimal state in localStorage as fallback (non-sensitive data)
  - Ensure logout logic only runs on explicit sign out

### Fail Conditions
- Diagnosis does not check cookie persistence
- Diagnosis does not verify session API called on load
- Fix stores sensitive tokens in localStorage
- Fix does not address root cause

### Used By
- Frontend-Backend-Auth-Integration (session persistence)
- Auth-Integration-Auditor (auth lifecycle validation)
- Security-Guardian (session security)
- Frontend-Auth-UI-Agent (auth state evaluation)

---

## Skill 6: diagnose_middleware_component_conflicts

### Purpose
Diagnose and resolve conflicts between Next.js middleware auth guards and component-level auth guards.

### Validations / Rules
- **Symptom identification**:
  - User logs in successfully
  - Infinite loading or redirect loop occurs
  - Multiple auth checks happen simultaneously
  - Console shows repeated API calls to `/api/auth/me`
- **Root cause analysis checklist**:
  1. Check if `middleware.ts` protects route with auth guard
  2. Check if dashboard component ALSO has auth guard (`useEffect` checking auth)
  3. Check execution order: middleware runs first, then component
  4. Check if component auth guard redirects to login when middleware already verified
  5. Check if both guards use same auth source (cookie vs localStorage)
- **Diagnosis steps**:
  1. Open `middleware.ts` → Check if protected routes include `/dashboard`
  2. Open `dashboard/page.tsx` → Check for `useEffect` with auth check
  3. Add console logs to both guards
  4. Trigger login flow
  5. Check console: both guards should NOT execute redirects
- **Common root causes**:
  - Redundant auth guard in component (middleware already protects route)
  - Component guard checks auth before cookie propagates
  - Component guard uses different auth source (e.g., localStorage instead of cookie)
  - Both guards redirect, causing infinite loop
- **Solution patterns**:
  - Remove component-level auth guard (trust middleware)
  - If component needs user data, fetch it WITHOUT redirecting
  - Middleware handles auth enforcement, component handles data fetching
  - Use `window.location.href` for post-auth redirect to ensure middleware sees cookie

### Fail Conditions
- Diagnosis does not identify redundant auth guard
- Fix removes middleware guard (incorrect layer)
- Fix keeps both guards (conflict remains)
- Fix introduces new bugs

### Used By
- Home-Auth-Flow-Agent (routing logic)
- Frontend-Architecture-Auditor (auth guard architecture)
- Auth-Integration-Auditor (auth flow validation)
- Cross-Stack-Consistency-Agent (consistent auth enforcement)

---

## Skill 7: diagnose_router_push_vs_location_href

### Purpose
Diagnose and resolve issues caused by using `router.push()` instead of `window.location.href` for post-auth redirects.

### Validations / Rules
- **Symptom identification**:
  - User logs in successfully
  - Redirect happens (URL changes to `/dashboard`)
  - Infinite loading or immediate redirect back to login
  - Dashboard never fully renders
- **Root cause analysis checklist**:
  1. Check if login/register uses `router.push("/dashboard")`
  2. Check if middleware runs BEFORE cookie propagates
  3. Check if middleware sees no cookie → redirects to login
  4. Check timing: client-side nav vs full page reload
- **Diagnosis steps**:
  1. Open login component → Find redirect logic after successful API call
  2. Check if using `router.push()` or `window.location.href`
  3. Add timing logs: log timestamp before redirect, in middleware, in dashboard
  4. Observe timing: `router.push()` is instant, `window.location.href` reloads page
- **Key difference**:
  - **`router.push("/dashboard")`**:
    - Client-side navigation (fast)
    - No full page reload
    - Middleware runs in parallel with API response
    - Cookie might not be available yet when middleware checks
    - Causes infinite loading
  - **`window.location.href = "/dashboard"`**:
    - Full page reload
    - Middleware runs AFTER cookie is set
    - Cookie guaranteed available when middleware checks
    - No infinite loading
- **Common root causes**:
  - Using `router.push()` for post-auth redirect
  - Cookie timing race condition: middleware checks before cookie available
  - Client-side nav doesn't give browser time to register cookie
- **Solution pattern**:
  - ALWAYS use `window.location.href` for post-auth redirects
  - Reserve `router.push()` for non-auth navigation

### Fail Conditions
- Diagnosis does not identify `router.push()` usage
- Diagnosis does not explain cookie timing race condition
- Fix uses timers/delays instead of full page reload
- Fix does not change to `window.location.href`

### Used By
- Frontend-Backend-Auth-Integration (redirect validation)
- Home-Auth-Flow-Agent (routing logic)
- Auth-Integration-Auditor (auth flow validation)
- Frontend-Auth-UI-Agent (post-auth navigation)

---

## Skill 8: generate_debug_report

### Purpose
Generate comprehensive debug report for auth issues with actionable findings and fix recommendations.

### Validations / Rules
- **Report must include**:
  1. **Symptom**: Clear description of observed bug
  2. **Root Cause**: Technical explanation of why bug occurs
  3. **Affected Files**: List of files involved in the issue
  4. **Affected Code**: Specific lines causing the issue
  5. **Recommended Fix**: Step-by-step fix instructions
  6. **Testing Steps**: How to verify fix works
  7. **Prevention**: How to avoid this issue in future
- **Report format**:
  - Use markdown for readability
  - Include code snippets with line references
  - Provide before/after code examples
  - Highlight root cause clearly
  - Prioritize fixes (critical, high, medium)
- **Report validation**:
  - Root cause must be technically accurate
  - Fix must address root cause, not symptoms
  - Testing steps must be reproducible
  - Prevention advice must be actionable

### Fail Conditions
- Report does not identify root cause
- Report only describes symptoms
- Recommended fix is vague or incomplete
- No testing steps provided
- Report does not reference specific files/lines

### Used By
- Phase2-Quality-Orchestrator (quality reports)
- Auth-Integration-Auditor (audit reports)
- Frontend-Architecture-Auditor (architecture review)

---

## Agent Invocation Workflow

### When to Invoke Auth-Reload-Debugger

**During Bug Reports**:
1. When user reports infinite loading after login
2. When user reports redirect loops
3. When user reports "signed out after refresh"
4. When protected routes accessible without auth
5. When auth state inconsistent across pages

**During Development**:
1. After implementing auth flow (proactive check)
2. After changing auth logic (regression check)
3. After updating dependencies (compatibility check)
4. Before merging auth PR (final validation)

**During Testing**:
1. When automated tests detect auth issues
2. When manual testing reveals auth bugs
3. When production reports auth errors

### Skills Invocation Order (Recommended)

**Phase 1: Symptom Identification**
1. Observe user-reported bug
2. Reproduce bug in local environment
3. Collect debug information (Network tab, Console, Cookies)

**Phase 2: Root Cause Analysis**
- If infinite loading → `diagnose_infinite_loading`
- If redirect loop → `diagnose_redirect_loops`
- If cookie issues → `diagnose_cookie_propagation_issues`
- If changes not applied → `diagnose_dev_server_cache`
- If state lost on refresh → `diagnose_auth_state_persistence`
- If competing guards → `diagnose_middleware_component_conflicts`
- If navigation issues → `diagnose_router_push_vs_location_href`

**Phase 3: Fix & Validate**
8. `generate_debug_report` - Document findings and fixes
9. Apply recommended fix
10. Test fix with provided testing steps
11. Verify bug resolved

### Integration with Other Agents

- **Frontend-Backend-Auth-Integration**: Validates fixes don't break integration
- **Frontend-Auth-UI-Agent**: Validates UI still works correctly
- **Home-Auth-Flow-Agent**: Validates routing logic after fix
- **Auth-Integration-Auditor**: Comprehensive audit after fix
- **Security-Guardian**: Ensures fixes don't introduce security issues

---

## Success Criteria

Auth-Reload-Debugger PASSES when:
- ✅ Root cause identified correctly
- ✅ Fix addresses root cause (not symptom)
- ✅ Fix resolves the bug (verified with testing steps)
- ✅ Fix does not introduce new bugs
- ✅ Fix does not disable security features
- ✅ Debug report comprehensive and actionable
- ✅ Prevention advice provided for future

Auth-Reload-Debugger FAILS when:
- ❌ Root cause not identified
- ❌ Fix only addresses symptoms
- ❌ Bug still present after fix
- ❌ Fix introduces new bugs
- ❌ Fix disables authentication (security risk)
- ❌ Debug report vague or incomplete
- ❌ No prevention advice provided

---

## Notes

- This agent focuses EXCLUSIVELY on debugging, not feature implementation
- Most common auth bug: `router.push()` causing cookie propagation race conditions
- Key insight: Full page reload (`window.location.href`) ensures cookie propagated before middleware checks
- Redundant auth guards (middleware + component) are second most common issue
- Dev server cache issues often mistaken for code bugs (always check `.next/` directory)
- Security MUST be maintained during debugging (never bypass auth to "fix" bugs)
- Root cause analysis is critical (treating symptoms makes bugs worse)
