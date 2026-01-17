---
id: 0017
title: Define Home Auth Flow Agent Skills
stage: misc
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-phase-ii-full-stack
branch: 003-phase-ii-full-stack
user: nizam
command: Define skills for home-auth-flow-agent
labels: ["skills", "agent-definition", "home-auth-flow", "authentication", "routing"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .claude/skills/home-auth-flow-agent.md
tests:
 - none
---

## Prompt

SKILLS TO DEFINE in .claude/skills
----------------------------------
Define skills for this agent "home-auth-flow-agent"including but not limited to:

- evaluate_auth_state
- enforce_auth_redirect
- restore_auth_buttons
- validate_homepage_auth_flow
- prevent_unauthorized_dashboard_access

----------------------------------
OUTPUT REQUIRED
----------------------------------
- Agent definition
- Clear description of each skill
- Boundaries and safety rules

Do NOT execute any fixes yet.
ONLY create its skills.

## Response snapshot

Created comprehensive skills definition for home-auth-flow-agent with 7 skills:

1. **evaluate_auth_state**: Evaluate authentication state on home page to determine correct UI and navigation
2. **enforce_auth_redirect**: Ensure proper routing based on auth state (Get Started → dashboard vs signup)
3. **restore_auth_buttons**: Ensure Sign In and Get Started buttons are present and functional
4. **validate_homepage_auth_flow**: End-to-end validation of auth flow from home page through login/signup
5. **prevent_unauthorized_dashboard_access**: Ensure protected routes redirect unauthenticated users
6. **validate_auth_ui_consistency**: Ensure auth UI elements are consistent and accessible
7. **handle_auth_state_transitions**: Ensure smooth UI transitions on login/logout/session expiry

**Agent Purpose**: Ensure proper authentication flow on the home page, including button visibility, routing logic, and access control to protected routes.

**Boundaries**:
- Focuses ONLY on home page auth flow and routing decisions
- Does NOT implement auth mechanisms (Better Auth handles that)
- Does NOT modify backend authentication logic
- Does NOT handle dashboard/app page layouts (only routing guards)

**Safety Rules**:
- NEVER bypass authentication checks
- NEVER expose protected content to unauthenticated users
- NEVER modify auth tokens or session data
- Changes must maintain security posture

## Outcome

- ✅ Impact: Created complete skills definition for home-auth-flow-agent with clear validation rules, fail conditions, and integration points
- 🧪 Tests: No tests required (skill definition only)
- 📁 Files: Created .claude/skills/home-auth-flow-agent.md (419 lines)
- 🔁 Next prompts: Agent ready to be invoked for home page auth flow issues; test by implementing actual auth flow on home page
- 🧠 Reflection: Skills follow established pattern from auth-jwt-bridge-enforcer; comprehensive coverage of home page auth scenarios including state evaluation, routing, button visibility, and protection

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A (skill definition task)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Invoke home-auth-flow-agent on actual home page implementation to validate skill effectiveness
