---
id: 0002
title: Phase III Implementation Plan Complete
stage: plan
date: 2026-01-23
surface: agent
model: claude-sonnet-4-5
feature: 004-phase-iii-chatbot
branch: 004-phase-iii-chatbot
user: Claude Sonnet 4.5
command: /sp.plan
labels: ["phase-iii", "implementation-plan", "gemini", "mcp-server", "architecture", "design"]
links:
  spec: specs/004-phase-iii-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-phase-iii-chatbot/plan.md
 - history/prompts/004-phase-iii-chatbot/0002-phase-iii-implementation-plan-complete.plan.prompt.md
tests:
 - none
---

## Prompt

/sp.plan

User provided detailed requirements for Phase III:
- Add AI-powered Todo Chatbot
- Use Google Gemini Flash 2.5 (NO OpenAI)
- Custom AI Agent Logic (NO OpenAI Agents SDK)
- MCP Server with Official MCP SDK
- ChatKit frontend (UI only, NOT OpenAI LLM)
- 5 Agents: MCP Server, Chat API, AI Agent Logic, ChatKit Frontend, Gemini LLM Controller
- Stateless backend architecture
- Phase II code MUST NOT be modified
- Database: Neon PostgreSQL with 2 new tables (Conversation, Message)
- 5 MCP tools: add_task, list_tasks, update_task, complete_task, delete_task

## Response snapshot

Created comprehensive Phase III implementation plan with:

**Technical Context**:
- Language/Version: Python 3.13+, TypeScript 5+, Node.js 20+
- Primary Dependencies: FastAPI, SQLModel, Google Generative AI SDK, MCP SDK, ChatKit
- Performance Goals: <3s p95 chat latency, <500ms MCP tools, 50 concurrent users
- Constraints: Phase II protection, stateless architecture, Gemini Flash 2.5 only, user data isolation

**Constitution Check**: 8 gates PASSED
- Phase II Protection, Stateless Architecture, User Data Isolation, Agent-Based Development, Type Safety, Testing, LLM Provider, Security

**Project Structure**: Defined complete directory layout
- `backend/phase3/` (routers, services, models, schemas, agent, llm)
- `backend/mcp_server/` (main, tools, tests)
- `frontend/src/app/chat/` and `frontend/src/components/chat/`
- All 5 agent skills already created in `.claude/skills/`

**Phase 0: Research & Unknowns Resolution**:
- R1: Gemini Flash 2.5 Integration → Use `google-generativeai` SDK
- R2: MCP Server SDK Selection → Use Official MCP SDK (Node.js) via HTTP
- R3: ChatKit Integration → Use ChatKit for UI, custom API endpoint
- R4: Stateless Conversation Management → Sliding window (last 10 messages)
- R5: Prompt Injection Prevention → Keyword detection + Gemini safety filters
- R6: Error Handling → Three-tier strategy (400, 404/403, 500)

**Phase 1: Design & Contracts**:
- Database Schema: Conversation and Message models with complete SQLModel schemas
- API Contracts: chat-api.yaml (OpenAPI 3.0), mcp-tools.json, gemini-api.md
- Quickstart Guide: Complete setup instructions for Phase III
- Agent Context Update: Script to add Phase III tech to Claude context

**Phase 2: Implementation Roadmap** (5 phases, 5 weeks):
- Phase 2.1: MCP Server (Agent 1) - 3-5 days
- Phase 2.2: Gemini LLM Controller (Agent 5) - 2-4 days
- Phase 2.3: AI Agent Logic (Agent 3) - 3-5 days
- Phase 2.4: Chat API + MCP Bridge (Agent 2) - 4-6 days
- Phase 2.5: ChatKit Frontend (Agent 4) - 3-5 days
- Phase 2.6: E2E Integration - 2-3 days

**Testing Milestones**: 5 milestones defined (MCP Tools, Gemini, Chat API, Frontend, Phase II Regression)

**Rollback & Safety Strategy**: Complete rollback procedure and safety measures (feature flags, backups, canary deployment)

**Completion Criteria**: 6 categories with 40+ checklist items (Functional, Quality, Security, Phase II Protection, Documentation, Deployment)

**Mock vs Real Gemini**: 3-phase strategy (Mock → Sandbox → Production) with complete mock implementation code

**Agent Execution Order**: Dependency graph and 5-week execution sequence

## Outcome

- ✅ Impact: Complete implementation plan created with technical context, constitution check (8 gates PASSED), project structure, research findings, database schemas, API contracts, quickstart guide, 5-phase implementation roadmap, testing milestones, rollback strategy, completion criteria, mock/real Gemini handling, and agent execution order.
- 🧪 Tests: No tests run (planning phase). Test strategy defined: Unit tests (mocked Gemini), Integration tests (Chat API flow), E2E tests (Playwright), Phase II regression tests.
- 📁 Files: Created `specs/004-phase-iii-chatbot/plan.md` (comprehensive 1333-line implementation plan with all phases, contracts, and strategies)
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation tasks from this plan, OR begin Phase 0 research if unknowns need investigation.
- 🧠 Reflection: Plan provides clear path from research through deployment with 5 agents, stateless architecture using Gemini Flash 2.5 (NO OpenAI), complete Phase II protection, and comprehensive testing/rollback strategies.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan generation successful. All user requirements incorporated (Gemini instead of OpenAI, 5 agents, stateless architecture, Phase II protection).
- Graders run and results (PASS/FAIL): Constitution Check PASS (8/8 gates), Complexity Tracking PASS (no violations).
- Prompt variant (if applicable): Standard /sp.plan command with user-provided detailed requirements for Gemini-based architecture.
- Next experiment (smallest change to try): None needed - plan is complete. Future enhancement: Add performance benchmarking strategy in more detail (specific metrics, tools, thresholds).
