---
id: 0002
title: Generate Phase II Constitution
stage: constitution
date: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: nizam
command: /sp.constitution
labels: ["constitution", "phase-ii", "governance", "agents", "skills"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .claude/skills/phase2-quality-orchestrator.md
  - .claude/skills/spec-auditor-agent.md
  - .claude/skills/spec-kit-structure-guardian.md
  - .claude/skills/api-contract-auditor.md
  - .claude/skills/auth-integration-auditor.md
  - .claude/skills/security-baseline-agent.md
  - .claude/skills/data-model-auditor.md
  - .claude/skills/backend-code-quality-agent.md
  - .claude/skills/frontend-architecture-auditor.md
  - .claude/skills/web-ux-optimization-agent.md
  - .claude/skills/full-stack-consistency-agent.md
tests:
  - none
---

## Prompt

# 📝 CLAUDE PROMPT — GENERATE `CONSTITUTION.MD`

You are an expert AI System Architect and Spec-Driven Development specialist.

Your task: **Generate a complete `constitution.md` file** for Phase II of the Full-Stack Todo Web Application.

## OBJECTIVE
- Provide a **comprehensive, structured, and actionable constitution** for Phase II.
- Ensure it covers **all governance rules, requirements, and workflow**.
- Ensure Claude Code **strictly follows this constitution** during all code generation.
- **No manual coding** is allowed.

## REQUIRED SECTIONS
1. **Project Overview**
   - Phase II goal
   - Stack (Next.js, FastAPI, SQLModel, Neon, Better Auth)
   - Scope of Phase II

2. **Agents & Skills**
   - List all agents (Phase2-Quality-Orchestrator, Spec-Auditor-Agent, Spec-Kit-Structure-Guardian, API-Contract-Auditor, Auth-Integration-Auditor, Security-Baseline-Agent, Data-Model-Auditor, Backend-Code-Quality-Agent, Frontend-Architecture-Auditor, Web-UX-Optimization-Agent, Full-Stack-Consistency-Agent)
   - State that **all code generation must strictly use agents and skills**
   - Manual coding is prohibited

3. **Spec-Driven Workflow**
   - Reference spec files before generating any code
   - No code can be written outside spec-defined features
   - Updates must follow the spec-first workflow

4. **Monorepo Structure Enforcement**
   - `/frontend/` → Frontend code only
   - `/backend/` → Backend code only
   - `/specs/` → Specs only
   - Root CLAUDE.md and folder CLAUDE.md files
   - All file placement rules enforced by Spec-Kit-Structure-Guardian

5. **Frontend / UI Governance**
   - Professional, modern UI enforced via Web-UX-Optimization-Agent
   - Loading, empty, error states mandatory
   - Server/Client components correctly used
   - Accessible forms and consistent design

6. **Backend / API Governance**
   - API contract enforced via API-Contract-Auditor
   - JWT authentication enforced via Auth-Integration-Auditor
   - Data ownership & filtering enforced
   - SQLModel + Neon DB schema correctness via Data-Model-Auditor

7. **Security Rules**
   - JWT verification required for all endpoints
   - Shared secret configured via env vars
   - Unauthorized requests must return 401
   - No sensitive info leakage

8. **Error Prevention & Consistency**
   - Full-Stack-Consistency-Agent ensures frontend/backend alignment
   - Agents block inconsistencies, prevent misaligned code
   - Phase2-Quality-Orchestrator approves all generation

9. **Enforcement & Compliance**
   - Claude must always follow this constitution
   - All code generation is **agents + skills dependent**
   - Violations of rules must not be allowed

## OUTPUT STYLE
- Markdown format
- Use headings, subheadings, and bullet points
- Clear, explicit, and unambiguous
- Ready for Claude Code to reference and enforce automatically

---
Generate full constitution

## Response snapshot

Created comprehensive Phase II Constitution (v2.0.0) with:

1. **Complete Agent Registry**: Documented all 11 agents with their skills, purposes, and invocation rules
   - Quality & Governance: Phase2-Quality-Orchestrator, Spec-Auditor-Agent, Spec-Kit-Structure-Guardian
   - Backend & API: API-Contract-Auditor, Auth-Integration-Auditor, Security-Baseline-Agent, Data-Model-Auditor, Backend-Code-Quality-Agent
   - Frontend & Full-Stack: Frontend-Architecture-Auditor, Web-UX-Optimization-Agent, Full-Stack-Consistency-Agent

2. **Spec-Driven Workflow**: Enforced spec → plan → tasks → implementation workflow with agent validation at each stage

3. **Monorepo Structure**: Strict boundaries for frontend/, backend/, specs/ with Spec-Kit-Structure-Guardian enforcement

4. **Frontend Governance**: Professional UI standards with MANDATORY loading, error, and empty states

5. **Backend Governance**: Clean architecture, JWT authentication, data isolation, API contracts

6. **Security Rules**: JWT requirements, token lifecycle, input validation, secret management, CORS policy

7. **Full-Stack Consistency**: Type alignment, error symmetry, auth flow consistency, data transformation rules

8. **Agent-Based Code Generation**: NO manual coding allowed - all code generated via agents with skill-based validation

9. **Quality Gates**: Pre-implementation, implementation, integration, and deployment gates coordinated by Phase2-Quality-Orchestrator

10. **Completion Criteria**: 12 categories covering functional, process, technical, documentation, security, and scope compliance

Version: 2.0.0 (MAJOR bump from 1.0.0 - Phase I Python Console → Phase II Full-Stack Web)
Ratified: 2026-01-09

## Outcome

- ✅ Impact: MAJOR - Complete Phase II constitution created defining full-stack web app governance with 11-agent enforcement model
- 🧪 Tests: N/A (constitution document)
- 📁 Files: Updated constitution.md + created 11 agent skill files
- 🔁 Next prompts: Create Phase II feature specifications following new constitution, implement agent invocations in workflow
- 🧠 Reflection: Constitution successfully transitions from Phase I (Python console) to Phase II (Next.js + FastAPI + Neon). All agents and skills are now formally documented with clear invocation rules. The agent-driven development model ensures quality, security, and consistency enforcement automatically.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution generated successfully with all required sections
- Graders run and results (PASS/FAIL): N/A (constitution establishment, not code validation)
- Prompt variant (if applicable): N/A (initial Phase II constitution)
- Next experiment (smallest change to try): Test agent invocation workflow with first Phase II feature specification
