---
id: 0014
title: T118 Quickstart Validation Critical Issues Found
stage: green
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-phase-ii-full-stack
branch: main
user: Mn-2k24
command: /sp.phr
labels: ["validation", "quickstart", "onboarding", "environment-variables", "configuration", "T118", "phase-10", "critical-issues", "env-templates", "developer-experience", "blocking-errors", "BETTER_AUTH_SECRET"]
links:
  spec: specs/003-phase-ii-full-stack/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - QUICKSTART_VALIDATION_REPORT.md
  - specs/003-phase-ii-full-stack/tasks.md
tests:
  - Prerequisite requirements validation
  - PostgreSQL setup steps validation
  - Backend .env template verification (CRITICAL FAILURES FOUND)
  - Frontend .env.local template verification (issues found)
  - Test scenario steps validation
  - Troubleshooting section validation
---

## Prompt

T118: Quickstart Validation – Verify new developer onboarding guide

Context update:
- I have created a `.env` file inside the `/backend` folder.
- The Neon PostgreSQL connection string is securely stored in this `.env` file using the `DATABASE_URL` environment variable.
- No secrets are hardcoded in code or specs.
- `.env` is included in `.gitignore`.

Constraints:
- Do not modify code.
- Do not introduce new configuration patterns.
- Validate against spec-driven development principles.

Output:
- Confirm whether the onboarding guide is correct.
- List any missing or unclear steps that could block a new developer.

## Response snapshot

Conducted comprehensive validation of specs/003-phase-ii-full-stack/quickstart.md (345 lines) against actual codebase implementation. Found **4 critical errors** in backend .env template that will **block new developers** from starting the application: (1) Missing required BETTER_AUTH_SECRET field (backend/src/config.py:48-53 requires min_length=32, no default) causes immediate ValidationError on startup - BLOCKER; (2) Wrong variable name JWT_EXPIRATION_MINUTES should be JWT_EXPIRATION_HOURS (config.py:39-45); (3) Wrong variable name FRONTEND_URL should be CORS_ORIGINS (config.py:56-60); (4) Wrong variable name ENVIRONMENT should be DEBUG (config.py:73-77). Frontend .env.local template includes 2 unnecessary variables (BETTER_AUTH_SECRET, BETTER_AUTH_URL) that are not used by frontend code (grep verification across frontend/src shows no usage - frontend uses custom JWT localStorage implementation per auth.ts:5-6, not Better Auth library). All other sections validated successfully: prerequisites accurate (Node.js 18+, Python 3.11+, PostgreSQL 14+, Git), PostgreSQL setup correct for local (missing cloud database guidance for Neon/Supabase workflows), backend/frontend dependency installation commands correct, migration files exist (2 alembic versions), test scenarios match actual routes (register/login/dashboard pages exist), verification checklist comprehensive (19 items covering all functionality), troubleshooting section helpful with realistic issues and solutions. Compared quickstart templates against authoritative sources: backend/.env.example (19 lines, all variables documented), frontend/.env.local.example (10 lines, minimal config), backend/src/config.py (Settings schema with Pydantic validation). User context noted: using Neon PostgreSQL (cloud database), not local PostgreSQL, which means Step 2 (createdb todo_db) can be skipped. Created comprehensive QUICKSTART_VALIDATION_REPORT.md with detailed findings, evidence with file/line references, corrected .env templates, recommendations for fixes, and compliance summary. Updated tasks.md marking T118 complete.

## Outcome

- ✅ Impact: **CRITICAL VALIDATION FAILURE DETECTED** - Quickstart guide contains blocking errors that will prevent new developers from successfully onboarding. Primary blocker: missing BETTER_AUTH_SECRET in backend .env template (required field per config.py:48-53) causes immediate Pydantic ValidationError on `uvicorn src.main:app` startup - application will not start. Secondary issues: 3 incorrect environment variable names (JWT_EXPIRATION_MINUTES→HOURS, FRONTEND_URL→CORS_ORIGINS, ENVIRONMENT→DEBUG) cause misleading configuration experience where variables are silently ignored and defaults used instead. Frontend .env.local template pollution: includes BETTER_AUTH_SECRET and BETTER_AUTH_URL which are completely unused (no references in frontend/src codebase verified via grep), potentially confusing developers about authentication architecture. Root cause analysis: quickstart.md .env templates do not match authoritative .env.example files or actual Settings schema in config.py. Comprehensive validation report documents all issues with evidence (file paths, line numbers, code snippets) and provides corrected templates using .env.example as source of truth. Positive findings: Prerequisites accurate, test scenarios match implementation, verification checklist thorough (19 items), troubleshooting section helpful, architecture diagram mostly accurate. Guide structure excellent (clear steps, multiple package manager options, good pedagogy) but execution flawed due to .env template errors. After fixes, guide will provide excellent onboarding experience. User context consideration: using Neon PostgreSQL (cloud) instead of local PostgreSQL means Step 2 (createdb) should be replaced with "create database via Neon console" guidance - added recommendation for cloud database alternative documentation. Validation methodology: code path verification comparing quickstart instructions against actual backend/src/config.py Settings schema, .env.example files, package.json scripts, alembic migrations, route files. Ready for T119 final Phase2-Quality-Orchestrator review.
- 🧪 Tests: 6 validation test areas completed via code path verification - (1) Prerequisites validation: Node.js/Python/PostgreSQL/Git requirements verified against package.json/requirements.txt, (2) PostgreSQL setup: createdb commands correct for local setup, (3) Backend .env template: **FAILED** - 4 critical errors found including missing required field, (4) Frontend .env.local template: **FAILED** - 2 unnecessary variables, (5) Test scenarios: All 7 scenarios validated against actual routes/components (register/login/dashboard/task CRUD/filters/sorting), (6) Troubleshooting: 5 common issues verified as realistic with actionable solutions
- 📁 Files: 2 files modified/created - 1 validation report (QUICKSTART_VALIDATION_REPORT.md ~450 lines with detailed findings, evidence, corrected templates, recommendations), 1 documentation update (tasks.md marking T118 complete)
- 🔁 Next prompts: "Fix quickstart.md .env templates using .env.example as source", "Add cloud PostgreSQL guidance (Neon/Supabase alternative to Step 2)", "Invoke Phase2-Quality-Orchestrator for final quality gate (T119)", "Test quickstart guide end-to-end with clean environment simulation", "Create automated quickstart validation script for CI/CD"
- 🧠 Reflection: Code path verification methodology proved invaluable for catching critical configuration errors before they impact real developers. Comparing documentation templates (quickstart.md) against authoritative sources (.env.example files, config.py Settings schema) revealed misalignment that would have caused immediate blocking failures. The missing BETTER_AUTH_SECRET would have been particularly frustrating - new developer follows guide exactly, runs uvicorn command, sees cryptic Pydantic ValidationError with no clear indication that the guide's .env template was incomplete. This validates the importance of T118 quickstart validation as quality gate - documentation bugs can be as blocking as code bugs. Frontend's unused BETTER_AUTH_* variables highlight template drift - .env.local.example was likely created in anticipation of Better Auth library integration (future phase) but frontend currently uses custom JWT implementation (auth.ts localStorage pattern), causing confusion between intended architecture and current implementation. Recommendation to reference .env.example files as single source of truth rather than duplicating templates in quickstart.md would prevent future drift. User's Neon PostgreSQL context surfaced important gap - guide assumes local PostgreSQL exclusively, missing cloud database workflows that are increasingly common in modern development. T119 Phase2-Quality-Orchestrator final review will be critical for catching any remaining cross-artifact inconsistencies before considering Phase II complete.

## Evaluation notes (flywheel)

- Failure modes observed: Quickstart guide .env templates contained 4 critical errors in backend (missing required BETTER_AUTH_SECRET, 3 wrong variable names) and 2 unnecessary variables in frontend (BETTER_AUTH_SECRET, BETTER_AUTH_URL not used). Guide did not reference authoritative .env.example files as source of truth. No cloud PostgreSQL guidance (Neon/Supabase) despite user context. Template drift between quickstart.md and actual code requirements (config.py Settings schema).
- Graders run and results (PASS/FAIL): Not yet run. Should invoke spec-governance-auditor to validate quickstart.md as documentation artifact, frontend-ui-professional to verify .env.local configuration aligns with frontend architecture, api-backend-guardian to verify backend .env requirements match Settings schema. Final T119 Phase2-Quality-Orchestrator will run all 11 agents for comprehensive compliance review.
- Prompt variant (if applicable): N/A (direct continuation from Phase 10 validation workflow)
- Next experiment (smallest change to try): Run automated quickstart simulation with clean environment: (1) Create fresh VM or Docker container, (2) Follow quickstart.md instructions verbatim as new developer would, (3) Document exact error messages and blocking points, (4) Verify fixes resolve all blocking issues. Consider creating automated validation script that runs quickstart steps programmatically and validates success criteria (backend starts on port 8000, frontend starts on port 3000, can register user, can login, can create task). Consider adding "Validate quickstart guide" as standard checkpoint in all future phase completion workflows. Consider refactoring quickstart.md to reference .env.example files directly (cp .env.example .env) rather than duplicating templates inline to prevent drift.
