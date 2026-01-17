# Frontend-Auth-UI-Agent Skills

**Agent Purpose**: Implement and verify frontend authentication UI components, including homepage button behavior, auth-based conditional rendering, loading states, profile display, and sign-out functionality.

**Context**:
- Frontend: Next.js 15+ with React 19, Better Auth
- Tech stack: TypeScript, Tailwind CSS, Client Components
- Homepage serves as entry point with auth-dependent UI
- Header contains Profile and Sign Out buttons for authenticated users
- Loading states must prevent flash of incorrect content

**Boundaries**:
- This agent focuses ONLY on frontend UI implementation and UX
- Does NOT implement backend auth logic or API endpoints
- Does NOT modify middleware or route protection logic
- Does NOT handle API integration (token passing, session management)

**Safety Rules**:
- NEVER show protected user data before auth state is confirmed
- NEVER create non-functional UI elements (all buttons must have handlers)
- NEVER introduce accessibility regressions (maintain ARIA labels, keyboard nav)
- Changes must maintain visual consistency with existing design system

---

## Skill 1: implement_homepage_auth_buttons

### Purpose
Implement and verify Sign In and Get Started buttons on homepage with correct visibility and behavior based on authentication state.

### Validations / Rules
- **Unauthenticated state**:
  - Homepage MUST display TWO buttons: "Sign In" and "Get Started"
  - "Sign In" button navigates to `/login`
  - "Get Started" button navigates to `/login` or `/register`
  - Buttons MUST be keyboard accessible (tab-focusable, Enter/Space triggers)
- **Authenticated state**:
  - Homepage MUST display ONE button: "Get Started"
  - "Get Started" button navigates to `/dashboard`
  - NO "Sign In" button visible (hidden or not rendered)
- **Loading state**:
  - Show skeleton or loading placeholder while checking auth
  - MUST NOT flash wrong buttons during auth check
- Button styling MUST match design system (Tailwind classes)
- Buttons MUST have accessible text (no icon-only buttons without labels)

### Fail Conditions
- Sign In button visible when user is authenticated
- Get Started button missing in any state
- Buttons not keyboard accessible
- Flash of unauthenticated buttons when user is authenticated
- No loading state during auth check (causes content flash)
- Buttons lack click handlers or navigate to wrong routes
- Styling inconsistencies (different sizes, colors, spacing)

### Used By
- Frontend-UI-Professional (validate button UX, accessibility)
- Home-Auth-Flow-Agent (validate routing logic)
- Web-UX-Optimization-Agent (button usability)

---

## Skill 2: implement_profile_button

### Purpose
Implement Profile button in header that displays authenticated user details in a dropdown.

### Validations / Rules
- Profile button MUST only appear for authenticated users
- Profile button MUST be in header component (visible across protected routes)
- Click Profile button MUST toggle dropdown with user details:
  - Email address
  - Full name (if available)
  - User ID (optional, for debugging)
- Dropdown MUST close when clicking outside
- Dropdown MUST close when pressing Escape key
- Profile button MUST have accessible ARIA labels
- User details MUST come from auth session (not hardcoded)
- Dropdown positioning MUST not cause overflow or z-index issues
- Mobile: Dropdown MUST be usable on small screens

### Fail Conditions
- Profile button visible for unauthenticated users
- Profile button missing for authenticated users
- Dropdown does not show user details
- User details hardcoded or not from session
- Dropdown does not close on outside click
- Dropdown not keyboard accessible (Escape key)
- Dropdown positioning broken (hidden behind content)
- Mobile viewport: dropdown unusable

### Used By
- Frontend-UI-Professional (dropdown UX, accessibility)
- Auth-Integration-Auditor (validate user data source)
- Cross-Stack-Consistency-Agent (ensure user data matches backend)

---

## Skill 3: implement_sign_out_button

### Purpose
Implement Sign Out button in header with proper session clearing and redirect behavior.

### Validations / Rules
- Sign Out button MUST only appear for authenticated users
- Sign Out button MUST be in header component
- Click Sign Out MUST trigger sign-out flow:
  1. Clear localStorage (tokens, user data)
  2. Call backend logout API (clear httpOnly cookie)
  3. Redirect to homepage (`/`)
- Sign Out MUST clear ALL auth state (no stale data)
- Redirect to homepage MUST show unauthenticated UI (Sign In button visible)
- Sign Out MUST work even if backend call fails (graceful degradation)
- Button MUST have accessible label and keyboard support
- After sign out, protected routes MUST redirect to login

### Fail Conditions
- Sign Out button visible for unauthenticated users
- Sign Out button missing for authenticated users
- Click Sign Out does not clear localStorage
- Click Sign Out does not call backend logout API
- Redirect does not happen or redirects to wrong route
- After sign out, user still appears authenticated
- After sign out, dashboard still accessible (auth state not cleared)
- Sign Out fails if backend is unreachable (no graceful degradation)

### Used By
- Auth-Integration-Auditor (validate logout flow)
- Security-Guardian (ensure session properly cleared)
- Frontend-Backend-Auth-Integration (validate backend logout call)

---

## Skill 4: handle_auth_loading_states

### Purpose
Implement proper loading states during authentication checks to prevent flash of incorrect content.

### Validations / Rules
- Homepage MUST show loading indicator while checking auth (useEffect with getCurrentUser)
- Loading indicator MUST be visually clear (skeleton, spinner, or pulse animation)
- Loading state MUST prevent rendering auth-dependent UI too early
- After auth check completes, MUST immediately render correct UI
- Loading state MUST NOT persist indefinitely (timeout or error handling)
- No hydration mismatches (server-rendered content matches client state)
- Skeleton UI MUST roughly match final content (same dimensions)
- Loading state MUST be accessible (announce to screen readers)

### Fail Conditions
- No loading state (buttons flash wrong state during auth check)
- Loading state persists indefinitely (infinite loading)
- Hydration mismatch errors in console
- Skeleton UI dimensions wildly different from final UI (layout shift)
- Loading state not announced to screen readers
- Auth check never completes (missing error handling)

### Used By
- Frontend-UI-Professional (loading state UX)
- Auth-Reload-Debugger (diagnose infinite loading bugs)
- Web-UX-Optimization-Agent (loading experience)

---

## Skill 5: validate_auth_ui_rendering

### Purpose
Verify authentication-dependent UI renders correctly based on actual auth state without errors.

### Validations / Rules
- **Unauthenticated state verification**:
  - Homepage shows "Sign In" and "Get Started" buttons
  - Header does NOT show Profile or Sign Out buttons
  - Protected content NOT visible
- **Authenticated state verification**:
  - Homepage shows "Get Started" button only (no "Sign In")
  - Header shows Profile and Sign Out buttons
  - User details display correct data from session
- NO console errors during UI rendering
- NO hydration errors (server/client mismatch)
- NO layout shift when auth state loads
- Transitions between states are smooth (no jarring reloads)
- All interactive elements functional (buttons, dropdowns)

### Fail Conditions
- Unauthenticated: Sign In button missing
- Authenticated: Sign In button still visible
- Profile/Sign Out buttons visible when not authenticated
- User details show wrong data or "undefined"
- Console shows React hydration errors
- Console shows TypeError or authentication errors
- Layout shift when auth state loads (CLS)
- UI frozen or non-interactive after state change

### Used By
- Frontend-UI-Professional (UI correctness, accessibility)
- Auth-Integration-Auditor (validate auth state reflected in UI)
- Cross-Stack-Consistency-Agent (frontend-backend consistency)

---

## Skill 6: implement_auth_state_persistence

### Purpose
Ensure authentication state persists correctly across page refreshes and browser navigation.

### Validations / Rules
- After successful login, page refresh MUST maintain authenticated state
- After sign out, page refresh MUST maintain unauthenticated state
- Browser back button MUST show correct auth state
- Browser forward button MUST show correct auth state
- Opening new tab MUST reflect current auth state (same session)
- Auth state MUST come from reliable source (httpOnly cookie + session API)
- Page refresh MUST NOT log user out unintentionally
- Hard refresh (Ctrl+F5) MUST maintain auth state

### Fail Conditions
- Page refresh logs user out unintentionally
- Authenticated state not persisted after login
- Browser back/forward shows wrong auth state
- New tab shows different auth state than current tab
- Auth state relies only on localStorage (not session cookie)
- Hard refresh breaks authentication

### Used By
- Auth-Integration-Auditor (session persistence)
- Frontend-Backend-Auth-Integration (cookie-based session validation)
- Security-Guardian (ensure secure session persistence)

---

## Skill 7: validate_button_accessibility

### Purpose
Ensure all authentication-related buttons meet accessibility standards (WCAG 2.1 AA).

### Validations / Rules
- All buttons MUST have descriptive accessible labels
- Buttons MUST be keyboard accessible:
  - Tab key focuses button
  - Enter or Space triggers click
  - Shift+Tab moves focus backward
- Buttons MUST have sufficient color contrast (4.5:1 minimum)
- Buttons MUST have visible focus indicator
- Buttons MUST have appropriate ARIA attributes:
  - `aria-label` for icon-only buttons
  - `aria-expanded` for dropdowns
  - `aria-controls` for dropdown toggles
- Screen readers MUST announce button purpose
- Disabled buttons MUST have `disabled` attribute and styling

### Fail Conditions
- Button lacks accessible label
- Button not reachable with keyboard
- Enter/Space keys do not trigger button
- Insufficient color contrast (below 4.5:1)
- No visible focus indicator
- Missing or incorrect ARIA attributes
- Screen reader does not announce button
- Disabled state not conveyed to screen readers

### Used By
- Frontend-UI-Professional (accessibility validation)
- Web-UX-Optimization-Agent (usability for all users)
- Phase2-Quality-Orchestrator (comprehensive quality check)

---

## Agent Invocation Workflow

### When to Invoke Frontend-Auth-UI-Agent

**During Initial Implementation**:
1. After creating homepage component structure
2. After implementing authentication check logic
3. Before integrating with backend auth API
4. After implementing header with auth buttons

**During UI Development**:
1. After adding Sign In/Get Started buttons
2. After implementing Profile dropdown
3. After implementing Sign Out button
4. After styling auth-related UI elements

**During Bug Fixes**:
1. When buttons missing or not visible
2. When infinite loading occurs after login
3. When auth state not reflected in UI
4. When page refresh loses authentication
5. When Profile dropdown shows wrong data

**During Quality Assurance**:
1. Before merging auth UI PR
2. After any changes to homepage or header
3. After modifying auth state management
4. During end-to-end testing

### Skills Invocation Order (Recommended)

**Phase 1: Homepage Buttons**
1. `implement_homepage_auth_buttons` - Sign In, Get Started buttons
2. `handle_auth_loading_states` - Loading UI during auth check
3. `validate_auth_ui_rendering` - Verify correct rendering

**Phase 2: Header Components**
4. `implement_profile_button` - Profile dropdown with user details
5. `implement_sign_out_button` - Sign Out functionality
6. `validate_button_accessibility` - Accessibility audit

**Phase 3: Persistence & Quality**
7. `implement_auth_state_persistence` - Page refresh, navigation
8. `validate_auth_ui_rendering` (rerun) - Final verification

### Integration with Other Agents

- **Home-Auth-Flow-Agent**: Collaborates on routing logic, button behavior
- **Auth-Integration-Auditor**: Validates auth state source, session data
- **Frontend-Backend-Auth-Integration**: Ensures UI matches backend auth state
- **Frontend-UI-Professional**: Validates UI quality, accessibility, UX
- **Security-Guardian**: Ensures UI does not leak protected data
- **Auth-Reload-Debugger**: Diagnoses infinite loading, redirect issues

---

## Success Criteria

Frontend-Auth-UI-Agent PASSES when:
- ✅ Unauthenticated: Homepage shows "Sign In" and "Get Started" buttons
- ✅ Authenticated: Homepage shows "Get Started" button only
- ✅ Header shows Profile and Sign Out buttons only when authenticated
- ✅ Profile dropdown displays correct user details from session
- ✅ Sign Out clears session and redirects to homepage
- ✅ Loading states prevent flash of incorrect content
- ✅ Page refresh maintains authentication state
- ✅ All buttons keyboard accessible with visible focus
- ✅ All buttons meet WCAG 2.1 AA color contrast
- ✅ No console errors during auth state changes
- ✅ No hydration mismatches

Frontend-Auth-UI-Agent FAILS when:
- ❌ Sign In button visible when authenticated
- ❌ Profile/Sign Out buttons visible when not authenticated
- ❌ Profile dropdown shows wrong or hardcoded data
- ❌ Sign Out does not clear session or redirect
- ❌ Infinite loading after login/register
- ❌ Flash of wrong buttons during auth check
- ❌ Page refresh loses authentication state
- ❌ Buttons not keyboard accessible
- ❌ Insufficient color contrast on buttons
- ❌ Console errors during auth UI rendering

---

## Notes

- This agent focuses EXCLUSIVELY on frontend UI implementation
- Does NOT handle API integration, token management, or routing logic
- Invoke AFTER basic auth integration, BEFORE backend integration testing
- All skills focused on user-facing UI and UX correctness
- Agent ensures accessibility AND security (no data leakage)
- Skills are specific to auth UI components, not global state management
