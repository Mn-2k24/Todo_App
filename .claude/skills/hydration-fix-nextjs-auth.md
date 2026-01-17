# Hydration-Fix-NextJS-Auth Skills

**Agent Purpose**: Detect, analyze, and fix Next.js hydration errors caused by server/client HTML mismatches, particularly in authentication UI components where server-side rendering cannot access auth state stored in cookies or localStorage.

**Context**:
- Frontend: Next.js 15+ with App Router (React 19)
- Auth state: Available only on client (cookies checked via JavaScript)
- SSR renders unauthenticated state, client hydration renders authenticated state
- Common symptom: "Hydration failed because the server rendered HTML didn't match the client"
- Auth components: Homepage buttons, Header (Profile/Sign Out), Protected pages

**Boundaries**:
- This agent focuses ONLY on hydration errors related to auth UI
- Does NOT fix general React rendering bugs
- Does NOT modify authentication logic or backend
- Does NOT change overall component architecture

**Safety Rules**:
- NEVER bypass hydration checks by suppressing warnings
- NEVER use dangerouslySetInnerHTML to "fix" hydration
- NEVER remove "use client" from components that need it
- Fixes must maintain security (no auth bypass)

---

## Skill 1: diagnose_hydration_error

### Purpose
Detect and diagnose hydration errors in browser console related to authentication UI mismatches between server and client rendering.

### Validations / Rules
- **Check browser console** for hydration warnings:
  - "Hydration failed because the server rendered HTML didn't match the client"
  - "Warning: Did not expect server HTML to contain a <div> in <div>"
  - "Warning: Expected server HTML to contain a matching <button>"
- **Identify affected components**:
  - Homepage (Sign In / Get Started buttons)
  - Header (Profile / Sign Out buttons)
  - Dashboard (Welcome message with username)
- **Identify root cause**:
  - Server renders without auth state (cookies not accessible in SSR)
  - Client hydrates with auth state (cookies available in browser)
  - HTML structure differs between server and client
- **Document exact mismatch**:
  - What HTML does server render?
  - What HTML does client render?
  - Which DOM nodes differ?

### Fail Conditions
- Diagnosis does not identify specific component causing error
- Diagnosis does not explain why server/client HTML differs
- Diagnosis only shows error message without analysis
- Does not identify auth state as root cause

### Used By
- Frontend-Auth-UI-Agent (validate hydration-free auth UI)
- Frontend-Architecture-Auditor (component structure review)
- Phase2-Quality-Orchestrator (production readiness)

---

## Skill 2: fix_auth_dependent_rendering

### Purpose
Fix hydration errors by ensuring server and client render identical HTML initially, then update UI on client after mount.

### Validations / Rules
- **Pattern: Use "mounted" state guard**:
  ```typescript
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <div>Loading...</div>;  // Server and initial client render same
  }

  // After mount, show auth-dependent UI
  return user ? <AuthUI /> : <UnauthUI />;
  ```
- **Never render auth-dependent content on server**:
  - Server cannot access cookies reliably
  - Server should render neutral/loading state
  - Client updates after mount with correct state
- **Ensure "use client" directive present**:
  - Components checking auth must be client components
  - Add "use client" at top of file if missing
- **Loading state matches final UI structure**:
  - Same DOM structure (div, button positions)
  - Avoid layout shift when transitioning
  - Use skeleton UI with correct dimensions

### Fail Conditions
- Fix still causes hydration errors
- Loading state removed (server/client render auth immediately)
- Missing "use client" directive
- Layout shift occurs when mounted state changes
- Auth bypass introduced (security risk)

### Used By
- Frontend-Auth-UI-Agent (implement loading states)
- Frontend-UI-Professional (UX validation)
- Cross-Stack-Consistency-Agent (consistent rendering)

---

## Skill 3: validate_use_client_directive

### Purpose
Ensure all components that access browser APIs (cookies, localStorage, window) have "use client" directive.

### Validations / Rules
- **Check for "use client" at top of file** (must be first line):
  ```typescript
  "use client";  // ✅ Correct placement

  import React from "react";
  // ... rest of component
  ```
- **Components requiring "use client"**:
  - Any component using `useState`, `useEffect`
  - Any component calling `getCurrentUser()` (fetches from cookies)
  - Any component reading `localStorage`
  - Any component accessing `window` object
  - Any component with click handlers (client-side interactivity)
- **Verify directive format**:
  - Must be string literal: `"use client"`
  - Must be first line (before imports)
  - Case-sensitive (lowercase "use client")
- **Parent components**:
  - If child needs "use client", parent can be server component
  - Only the component accessing browser APIs needs directive

### Fail Conditions
- Missing "use client" on component accessing browser APIs
- "use client" placed after imports (wrong position)
- Wrong string format ('use client' with single quotes may not work in all cases)
- All components marked "use client" (over-use, loses SSR benefits)

### Used By
- Frontend-Architecture-Auditor (component architecture)
- Phase2-Quality-Orchestrator (build validation)

---

## Skill 4: implement_mounted_state_guard

### Purpose
Implement mounted state pattern to prevent auth-dependent content from rendering on server.

### Validations / Rules
- **Add mounted state**:
  ```typescript
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);
  ```
- **Guard auth-dependent rendering**:
  ```typescript
  if (!mounted) {
    // Server and initial client render
    return (
      <div className="flex gap-4">
        <div className="h-10 w-32 bg-gray-200 animate-pulse rounded" />
        <div className="h-10 w-32 bg-gray-200 animate-pulse rounded" />
      </div>
    );
  }

  // After client mount, show actual auth state
  return isAuthenticated ? <AuthButtons /> : <UnauthButtons />;
  ```
- **Loading state structure**:
  - Match final UI dimensions (height, width)
  - Use skeleton UI (bg-gray-200 animate-pulse)
  - Maintain layout (same flex/grid structure)
  - Accessible (screen reader announces loading)
- **useEffect runs once** (empty dependency array):
  - Prevents infinite loops
  - Sets mounted to true immediately after client mount

### Fail Conditions
- Mounted state never set to true (stuck in loading)
- Loading state has different DOM structure than final UI
- useEffect has dependencies causing re-renders
- Skeleton UI dimensions wildly different (layout shift)

### Used By
- Frontend-Auth-UI-Agent (loading states)
- Frontend-UI-Professional (loading UX)
- Web-UX-Optimization-Agent (prevent layout shift)

---

## Skill 5: test_hydration_errors

### Purpose
Systematically test for hydration errors across all auth flows in development mode.

### Validations / Rules
- **Open browser DevTools Console** (development mode)
- **Test unauthenticated flow**:
  1. Clear cookies and localStorage
  2. Visit homepage → Check console for hydration errors
  3. Visit /login → Check console
  4. Visit /dashboard (should redirect) → Check console
- **Test authenticated flow**:
  1. Login successfully
  2. Visit homepage → Check console for hydration errors
  3. Visit /dashboard → Check console
  4. Refresh page (F5) → Check console
- **Test state transitions**:
  1. Login → Check console during redirect
  2. Logout → Check console during redirect
  3. Open Profile dropdown → Check console
- **Zero tolerance**:
  - ANY hydration warning is a FAIL
  - "Did not expect server HTML" = FAIL
  - Must fix all hydration errors before production

### Fail Conditions
- Hydration errors present in any flow
- Testing skipped (not validated)
- Errors suppressed instead of fixed
- Only tested one auth state (must test both)

### Used By
- Phase2-Quality-Orchestrator (quality gate)
- Frontend-Auth-UI-Agent (auth flow validation)
- Cross-Stack-Consistency-Agent (consistency check)

---

## Skill 6: fix_header_hydration

### Purpose
Fix hydration errors in Header component where Profile/Sign Out buttons appear conditionally based on auth state.

### Validations / Rules
- **Root cause**: Server cannot know if user is authenticated
  - Server renders: No buttons (empty header)
  - Client renders: Profile + Sign Out buttons (if authenticated)
  - HTML mismatch → Hydration error
- **Fix pattern**:
  ```typescript
  "use client";

  import { useState, useEffect } from "react";
  import { getUser } from "@/lib/auth";

  export default function Header() {
    const [mounted, setMounted] = useState(false);
    const [user, setUser] = useState(null);

    useEffect(() => {
      setMounted(true);
      setUser(getUser());
    }, []);

    return (
      <header>
        <h1>Todo App</h1>
        {!mounted ? (
          // Server and initial client render: empty or skeleton
          <div className="h-10 w-48 bg-gray-200 animate-pulse rounded" />
        ) : user ? (
          // After mount: show auth buttons
          <>
            <button>Profile</button>
            <button>Sign Out</button>
          </>
        ) : null}
      </header>
    );
  }
  ```
- **Alternative: Client-only component**:
  - Use dynamic import with `{ ssr: false }`
  - Header only renders on client
  - No server-side rendering of header

### Fail Conditions
- Hydration error still occurs
- Header missing "use client"
- No mounted state guard
- Buttons render on server (check page source)

### Used By
- Frontend-Auth-UI-Agent (header implementation)
- Frontend-UI-Professional (header UX)

---

## Skill 7: fix_homepage_hydration

### Purpose
Fix hydration errors on homepage where Sign In/Get Started buttons appear conditionally based on auth state.

### Validations / Rules
- **Root cause**: Server renders unauthenticated buttons, client may render authenticated button
  - Server: "Sign In" + "Get Started" (no auth)
  - Client after mount: "Get Started" only (if authenticated)
  - Button count mismatch → Hydration error
- **Fix pattern**:
  ```typescript
  "use client";

  import { useState, useEffect } from "react";
  import { getCurrentUser } from "@/lib/auth";

  export default function HomePage() {
    const [mounted, setMounted] = useState(false);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
      getCurrentUser().then((user) => {
        setIsAuthenticated(!!user);
        setMounted(true);
      });
    }, []);

    return (
      <div>
        <h1>Welcome</h1>
        {!mounted ? (
          // Server and initial client: skeleton buttons
          <div className="flex gap-4">
            <div className="h-12 w-40 bg-gray-200 animate-pulse rounded" />
            <div className="h-12 w-40 bg-gray-200 animate-pulse rounded" />
          </div>
        ) : isAuthenticated ? (
          // After mount: authenticated UI
          <Link href="/dashboard">Get Started</Link>
        ) : (
          // After mount: unauthenticated UI
          <>
            <Link href="/login">Get Started</Link>
            <Link href="/login">Sign In</Link>
          </>
        )}
      </div>
    );
  }
  ```
- **Loading state matches button count**:
  - Show 2 skeleton buttons (matches unauthenticated state)
  - Prevents layout shift

### Fail Conditions
- Hydration error still occurs
- Loading state has wrong number of buttons
- Auth check in useEffect never completes
- Homepage missing "use client"

### Used By
- Frontend-Auth-UI-Agent (homepage buttons)
- Home-Auth-Flow-Agent (routing logic)

---

## Skill 8: generate_hydration_fix_report

### Purpose
Generate comprehensive report documenting hydration errors found, fixes applied, and validation results.

### Validations / Rules
- **Report must include**:
  1. **Errors Found**: List all hydration errors with component names
  2. **Root Cause**: Explain why server/client HTML differed
  3. **Fix Applied**: Code changes with before/after examples
  4. **Files Modified**: List of files changed
  5. **Validation**: Test results showing zero hydration errors
  6. **Prevention**: Guidelines to avoid future hydration issues
- **Before/after code snippets**:
  - Show original code causing hydration error
  - Show fixed code with mounted state guard
  - Explain what changed and why
- **Test results**:
  - Screenshots or console logs showing no errors
  - List of flows tested (unauthenticated, authenticated, transitions)

### Fail Conditions
- Report missing root cause analysis
- No before/after code examples
- Validation results not documented
- Prevention guidelines missing

### Used By
- Phase2-Quality-Orchestrator (quality documentation)
- Frontend-Architecture-Auditor (architectural review)

---

## Agent Invocation Workflow

### When to Invoke Hydration-Fix-NextJS-Auth

**During Development**:
1. When hydration warnings appear in browser console
2. After implementing auth-dependent UI components
3. Before merging PR with auth UI changes
4. During code review if hydration errors detected

**During Bug Fixes**:
1. User reports "flashing content" on page load
2. User reports "page looks broken briefly"
3. Console shows hydration errors
4. Layout shift occurs when page loads

**During Testing**:
1. QA finds hydration errors in dev mode
2. Production monitoring detects hydration issues
3. Before deploying auth UI changes

### Skills Invocation Order (Recommended)

**Phase 1: Diagnosis**
1. `diagnose_hydration_error` - Identify affected components
2. `validate_use_client_directive` - Check "use client" present

**Phase 2: Fix Implementation**
3. `fix_auth_dependent_rendering` - Implement mounted pattern
4. `implement_mounted_state_guard` - Add loading states
- If header affected → `fix_header_hydration`
- If homepage affected → `fix_homepage_hydration`

**Phase 3: Validation**
5. `test_hydration_errors` - Verify all errors fixed
6. `generate_hydration_fix_report` - Document fixes

### Integration with Other Agents

- **Frontend-Auth-UI-Agent**: Collaborates on loading state implementation
- **Frontend-UI-Professional**: Validates loading UI/UX
- **Frontend-Architecture-Auditor**: Validates component structure
- **Phase2-Quality-Orchestrator**: Validates production readiness

---

## Success Criteria

Hydration-Fix-NextJS-Auth PASSES when:
- ✅ Zero hydration errors in browser console
- ✅ All auth components have "use client" directive
- ✅ Mounted state guard implemented where needed
- ✅ Loading states match final UI structure
- ✅ Tested across all auth flows (unauth, auth, transitions)
- ✅ No layout shift when page loads
- ✅ Screen readers announce loading states
- ✅ Page source shows neutral/loading state (not auth content)

Hydration-Fix-NextJS-Auth FAILS when:
- ❌ Any hydration warnings in console
- ❌ Missing "use client" on components accessing browser APIs
- ❌ No mounted state guard (auth renders on server)
- ❌ Layout shift occurs when loading completes
- ❌ Not tested in all auth states
- ❌ Auth-dependent content in page source (SSR)
- ❌ Loading state has different DOM structure

---

## Notes

- Hydration errors ONLY occur in development mode (suppressed in production)
- However, they indicate real bugs that cause flashing/layout shift
- NEVER suppress hydration warnings - always fix root cause
- Mounted state pattern is standard Next.js solution for client-only content
- Auth state is inherently client-side (cookies, localStorage)
- Server cannot reliably check auth, so must render neutral state
- Loading states should be fast (< 100ms) to avoid noticeable flash
