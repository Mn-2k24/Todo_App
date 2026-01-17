# Home-Auth-Flow-Agent Skills

**Agent Purpose**: Ensure proper authentication flow on the home page, including button visibility, routing logic, and access control to protected routes based on user authentication state.

**Context**:
- Frontend: Next.js 15+ with Better Auth
- Home page serves as entry point with conditional UI based on auth state
- Protected routes (e.g., /dashboard) require authentication
- Sign In and Get Started buttons must reflect current auth state
- Architecture: Client-side auth state evaluation, server-side protection

**Boundaries**:
- This agent focuses ONLY on home page auth flow and routing decisions
- Does NOT implement auth mechanisms (Better Auth handles that)
- Does NOT modify backend authentication logic
- Does NOT handle dashboard/app page layouts (only routing guards)

**Safety Rules**:
- NEVER bypass authentication checks
- NEVER expose protected content to unauthenticated users
- NEVER modify auth tokens or session data
- Changes must maintain security posture

---

## Skill 1: evaluate_auth_state

### Purpose
Evaluate current user authentication state on the home page to determine correct UI and navigation behavior.

### Validations / Rules
- Home page MUST check authentication state before rendering navigation buttons
- Auth state check MUST use Better Auth session API (not localStorage directly)
- Unauthenticated state MUST show "Sign In" and "Get Started" buttons
- Authenticated state MUST show personalized UI (e.g., "Go to Dashboard", user profile)
- Auth state evaluation MUST handle loading state (show skeleton/spinner during check)
- Auth state MUST be evaluated on client-side hydration
- Session check MUST not cause hydration mismatches

### Fail Conditions
- Home page does not check authentication state
- Auth state read directly from localStorage instead of Better Auth API
- Authenticated users see "Sign In" button (state not detected)
- Unauthenticated users see personalized content (false positive)
- No loading state during auth check (flash of wrong content)
- Hydration errors due to server/client auth state mismatch

### Used By
- Frontend-UI-Professional (validate loading states, UX)
- Auth-Integration-Auditor (validate auth state evaluation)
- Cross-Stack-Consistency-Agent (ensure consistent auth behavior)

---

## Skill 2: enforce_auth_redirect

### Purpose
Ensure proper routing logic based on authentication state when users click navigation buttons or attempt to access protected routes.

### Validations / Rules
- "Get Started" button MUST route authenticated users to `/dashboard`
- "Get Started" button MUST route unauthenticated users to `/signup` or `/register`
- "Sign In" button MUST route unauthenticated users to `/login` or `/signin`
- "Sign In" button MUST be hidden or disabled for authenticated users
- Protected route access (e.g., `/dashboard`) MUST redirect unauthenticated users to login
- Redirect logic MUST preserve intended destination URL (return_to or similar)
- Client-side navigation MUST use Next.js router, not window.location
- Redirects MUST not cause infinite loops

### Fail Conditions
- Authenticated user clicks "Get Started" and routed to signup (should go to dashboard)
- Unauthenticated user clicks "Get Started" and routed to dashboard (should go to signup)
- Authenticated users can still see/click "Sign In" button
- Protected route accessible to unauthenticated users (no redirect)
- Redirect loses intended destination (user can't return after login)
- Hard page reloads instead of client-side navigation
- Infinite redirect loop between login and protected route

### Used By
- Frontend-Architecture-Auditor (routing logic validation)
- Auth-Integration-Auditor (auth-based routing)
- Frontend-UI-Professional (button visibility and behavior)
- Security-Guardian (prevent unauthorized access)

---

## Skill 3: restore_auth_buttons

### Purpose
Ensure Sign In and Get Started buttons are present, visible, and functional on the home page for unauthenticated users.

### Validations / Rules
- Home page MUST display "Sign In" button for unauthenticated users
- Home page MUST display "Get Started" button for unauthenticated users
- Buttons MUST be visible (not hidden with CSS or removed from DOM)
- Buttons MUST have accessible text and ARIA labels
- Buttons MUST have click handlers that trigger navigation
- Button styling MUST match design system (if defined)
- Buttons MUST be keyboard accessible (focusable, Enter/Space triggers click)
- Buttons MUST not be duplicated (each appears exactly once)

### Fail Conditions
- "Sign In" button missing from DOM for unauthenticated users
- "Get Started" button missing from DOM for unauthenticated users
- Buttons rendered but hidden with `display: none` or `visibility: hidden`
- Buttons lack click handlers (non-functional)
- Buttons not keyboard accessible
- Duplicate buttons rendered
- Buttons missing ARIA labels for screen readers

### Used By
- Frontend-UI-Professional (accessibility, UX validation)
- Frontend-Architecture-Auditor (component structure review)
- Web-UX-Optimization-Agent (button usability)

---

## Skill 4: validate_homepage_auth_flow

### Purpose
Perform end-to-end validation of the entire authentication flow from home page through login/signup and back to protected content.

### Validations / Rules
- **Unauthenticated user flow**:
  1. Home page displays "Sign In" and "Get Started" buttons
  2. Click "Sign In" → navigate to `/login`
  3. Successful login → redirect to intended destination or `/dashboard`
  4. Return to home page → see authenticated UI (no Sign In button)
- **Authenticated user flow**:
  1. Home page shows personalized content (e.g., "Welcome back")
  2. Click "Get Started" or "Dashboard" → navigate to `/dashboard`
  3. No "Sign In" button visible
- **Protected route guard**:
  1. Unauthenticated user navigates to `/dashboard` directly
  2. Redirect to `/login` with return URL
  3. After login, redirect back to `/dashboard`
- All flows MUST be consistent across page refreshes

### Fail Conditions
- Any step in unauthenticated flow broken
- Any step in authenticated flow broken
- Protected route accessible without authentication
- Login redirect does not preserve intended destination
- Page refresh loses authentication state (false logout)
- Flow inconsistencies between browser navigation and router navigation

### Used By
- Phase2-Quality-Orchestrator (end-to-end flow validation)
- Auth-Integration-Auditor (complete auth flow audit)
- Cross-Stack-Consistency-Agent (validate frontend auth flow consistency)

---

## Skill 5: prevent_unauthorized_dashboard_access

### Purpose
Ensure dashboard and other protected routes are inaccessible to unauthenticated users with proper redirects and no data leakage.

### Validations / Rules
- Dashboard route MUST have authentication guard (middleware or component-level)
- Unauthenticated access MUST redirect to login immediately
- Redirect MUST occur before rendering protected content
- Protected content MUST NOT be visible during redirect (no flash)
- Redirect MUST preserve intended destination URL
- Authentication guard MUST work for both client-side navigation and direct URL access
- Protected API calls MUST not execute before redirect
- Auth guard MUST handle edge cases (session expired, malformed token)

### Fail Conditions
- Dashboard accessible without authentication (no redirect)
- Protected content briefly visible before redirect (flash of content)
- Redirect happens after component renders (data exposed)
- Protected API calls execute for unauthenticated users
- Direct URL access bypasses auth guard
- Session expiration not detected (stale session allowed)
- Auth guard fails on page refresh or browser back button

### Used By
- Security-Guardian (access control validation)
- Auth-Integration-Auditor (route protection audit)
- Frontend-Architecture-Auditor (routing guard implementation)
- Cross-Stack-Consistency-Agent (ensure frontend guards match backend enforcement)

---

## Skill 6: validate_auth_ui_consistency

### Purpose
Ensure authentication-related UI elements are consistent, accessible, and maintain visual hierarchy.

### Validations / Rules
- "Sign In" and "Get Started" buttons MUST have consistent styling
- Button positioning MUST match design (header, hero section, etc.)
- Button labels MUST be clear and actionable ("Sign In" not "Login Link")
- Loading states MUST be visually clear (spinner, skeleton, disabled state)
- Error states (e.g., auth failed) MUST display user-friendly messages
- Authenticated UI MUST clearly distinguish from unauthenticated UI
- No broken links or non-functional buttons
- Mobile responsiveness: buttons visible and usable on all screen sizes

### Fail Conditions
- Button styling inconsistent (different colors, sizes, fonts)
- Button labels ambiguous ("Click here", "Submit")
- No loading indicator during auth check
- Error messages missing or not user-friendly
- Authenticated and unauthenticated UI indistinguishable
- Buttons overlap or hidden on mobile viewports
- Non-functional or broken navigation links

### Used By
- Frontend-UI-Professional (UI consistency and accessibility)
- Web-UX-Optimization-Agent (UX validation)
- CSS-Pipeline-Resolver (styling issues)

---

## Skill 7: handle_auth_state_transitions

### Purpose
Ensure smooth and correct UI transitions when authentication state changes (login, logout, session expiry).

### Validations / Rules
- Login event MUST trigger UI update (hide Sign In, show personalized content)
- Logout event MUST trigger UI update (show Sign In, hide personalized content)
- UI updates MUST not cause page reload (smooth client-side transition)
- Session expiry MUST be detected and UI updated accordingly
- Auth state changes MUST be reflected in real-time (no stale state)
- Transitions MUST be accessible (announce changes to screen readers)
- No race conditions between auth state update and UI render

### Fail Conditions
- Login does not update home page UI (still shows Sign In button)
- Logout does not update UI (personalized content still visible)
- Auth state change requires page refresh
- Session expiry not detected (stale authenticated UI)
- Race condition causes wrong UI state
- Screen readers not notified of auth state changes

### Used By
- Frontend-Architecture-Auditor (state management review)
- Auth-Integration-Auditor (auth lifecycle validation)
- Frontend-UI-Professional (transition UX validation)

---

## Agent Invocation Workflow

### When to Invoke Home-Auth-Flow-Agent

**During Home Page Implementation**:
1. After creating home page component structure
2. After integrating Better Auth on home page
3. After implementing Sign In/Get Started buttons
4. Before committing home page code

**During Route Protection Implementation**:
1. After implementing dashboard or protected routes
2. After adding authentication guards
3. After implementing redirect logic
4. Before end-to-end auth testing

**During Bug Fixes**:
1. When Sign In or Get Started buttons missing/broken
2. When authenticated users incorrectly routed
3. When protected routes accessible without auth
4. When auth state not reflected in UI

**During UI Refactoring**:
1. After changing home page layout
2. After modifying navigation components
3. After updating auth-related UI elements

### Skills Invocation Order (Recommended)

**Phase 1: State Evaluation**
1. `evaluate_auth_state` - Validate auth state detection
2. `validate_auth_ui_consistency` - Validate UI renders correctly

**Phase 2: Button & Navigation**
3. `restore_auth_buttons` - Ensure buttons present and functional
4. `enforce_auth_redirect` - Validate routing logic

**Phase 3: Protection & Flow**
5. `prevent_unauthorized_dashboard_access` - Validate route guards
6. `validate_homepage_auth_flow` - End-to-end flow validation
7. `handle_auth_state_transitions` - Validate state transition behavior

### Integration with Other Agents

- **Auth-Integration-Auditor**: Collaborates on auth state evaluation, routing logic
- **Frontend-UI-Professional**: Collaborates on button visibility, loading states, accessibility
- **Frontend-Architecture-Auditor**: Collaborates on routing guard implementation
- **Security-Guardian**: Collaborates on access control, unauthorized access prevention
- **Cross-Stack-Consistency-Agent**: Ensures frontend auth flow aligns with backend expectations
- **Web-UX-Optimization-Agent**: Collaborates on user experience of auth flows

---

## Success Criteria

Home-Auth-Flow-Agent PASSES when:
- ✅ Unauthenticated users see "Sign In" and "Get Started" buttons
- ✅ "Get Started" routes authenticated users to dashboard
- ✅ "Get Started" routes unauthenticated users to signup
- ✅ "Sign In" button hidden or disabled for authenticated users
- ✅ Protected routes redirect unauthenticated users to login
- ✅ Redirect preserves intended destination URL
- ✅ Auth state changes reflected in UI without page reload
- ✅ No flash of wrong content during auth state evaluation
- ✅ All buttons keyboard accessible and ARIA-labeled
- ✅ No infinite redirect loops
- ✅ Session expiry detected and UI updated

Home-Auth-Flow-Agent FAILS when:
- ❌ Sign In or Get Started button missing for unauthenticated users
- ❌ Authenticated user routed to signup instead of dashboard
- ❌ Unauthenticated user can access dashboard without redirect
- ❌ Auth state change requires page reload
- ❌ Flash of protected content before redirect
- ❌ Redirect loses intended destination
- ❌ Buttons not keyboard accessible
- ❌ Infinite redirect loop occurs
- ❌ Hydration errors due to auth state mismatch

---

## Notes

- This agent focuses EXCLUSIVELY on home page auth flow and routing decisions
- Does NOT implement authentication (Better Auth handles that)
- Invoke AFTER home page structure created, BEFORE auth integration testing
- All skills MUST pass for proper user authentication experience
- Agent ensures security (no unauthorized access) AND UX (buttons work correctly)
- Skills are specific to home page and route guards, NOT global auth system
