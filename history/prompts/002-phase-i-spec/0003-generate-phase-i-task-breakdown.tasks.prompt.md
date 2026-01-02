---
id: 0003
title: Generate Phase I Task Breakdown
stage: tasks
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5
feature: 002-phase-i-spec
branch: 002-phase-i-spec
user: nizam
command: /sp.tasks
labels: ["phase-i", "tasks", "implementation", "task-breakdown", "todo-app"]
links:
  spec: specs/002-phase-i-spec/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-phase-i-spec/tasks.md
tests:
  - N/A (task planning document, not implementation)
---

## Prompt

You are generating a Phase I task breakdown for the project:
"Todo In-Memory Python Console App".

Use Spec-Driven Development principles and organize tasks by user story for independent implementation and testing.

Task:
Create a **tasks.md file** containing granular, actionable tasks organized by user story.

The tasks must include:

1. **Task Format**: Each task MUST follow strict checklist format:
   - `- [ ] [TaskID] [P?] [Story?] Description with file path`
   - TaskID: Sequential (T001, T002, T003...)
   - [P]: Only if parallelizable (different files, no dependencies)
   - [Story]: Required for user story tasks (US1, US2, US3, US4, US5)

2. **Phase Structure**:
   - Phase 1: Setup (project initialization)
   - Phase 2: Foundational (blocking prerequisites for ALL stories)
   - Phase 3-7: User Stories (one phase per story, in priority order)
   - Phase 8: Main Menu & Application Loop
   - Phase 9: Polish & Cross-Cutting Concerns

3. **User Story Organization**:
   Extract from spec.md:
   - US1: Add Task (FR-ADD-001 through FR-ADD-010)
   - US2: View Task List (FR-VIEW-001 through FR-VIEW-008)
   - US3: Update Task (FR-UPDATE-001 through FR-UPDATE-012)
   - US4: Delete Task (FR-DELETE-001 through FR-DELETE-008)
   - US5: Mark Task Complete/Incomplete (FR-MARK-001 through FR-MARK-008)

4. **Each User Story Phase**:
   - Goal: Brief description of story value
   - Independent Test: How to verify story works standalone
   - Implementation Tasks: Specific, executable tasks with file paths
   - Checkpoint: Definition of done for this story

5. **Dependencies & Execution Order**:
   - Phase dependencies (Setup → Foundational → User Stories → Menu → Polish)
   - User story dependencies (all independent after Foundational)
   - Parallel opportunities identified with [P] marker
   - Sequential execution guidance for Claude Code

6. **Implementation Strategy**:
   - MVP First: Setup + Foundational + US1 only
   - Incremental Delivery: Add one story at a time, test independently
   - Sequential Execution: Recommended task order T001 → T033

Constraints:
- All tasks reference exact file paths from plan.md structure
- No automated tests (spec states "Manual CLI testing")
- Each user story independently testable at checkpoint
- Tasks granular enough for Claude Code to execute

Output:
- One `tasks.md` file with 33 tasks organized across 9 phases

## Response snapshot

Created comprehensive task breakdown for Phase I implementation:

**File**: `specs/002-phase-i-spec/tasks.md`
**Total Tasks**: 33 tasks organized across 9 phases

**Phase Breakdown**:
- **Phase 1: Setup** (2 tasks) - Project structure creation
- **Phase 2: Foundational** (4 tasks) - CRITICAL blocking prerequisites
  - T003: Task model dataclass (src/models/task.py)
  - T004: Global state initialization (src/services/todo_service.py)
  - T005: Menu display function (src/cli/menu.py)
  - T006: Menu choice validation (src/cli/menu.py)
- **Phase 3: User Story 1 - Add Task** 🎯 MVP (3 tasks)
  - T007: add_task() service (validate, create, store)
  - T008: add_task_handler() CLI
  - T009: Wire to menu choice 1
  - Independent Test: Add → View → Verify task appears
- **Phase 4: User Story 2 - View Tasks** (4 tasks)
  - T010: get_all_tasks() service
  - T011: display_tasks() formatter (src/cli/task_view.py)
  - T012: view_tasks_handler() CLI
  - T013: Wire to menu choice 2
  - Independent Test: Add 3 → View → Verify all displayed
- **Phase 5: User Story 3 - Update Task** (4 tasks)
  - T014: get_task_by_id() service (shared utility)
  - T015: update_task() service (validate, update description)
  - T016: update_task_handler() CLI (prompt, validate, display)
  - T017: Wire to menu choice 3
  - Independent Test: Update description → Verify ID/status preserved
- **Phase 6: User Story 4 - Delete Task** (3 tasks)
  - T018: delete_task() service (remove from list)
  - T019: delete_task_handler() CLI
  - T020: Wire to menu choice 4
  - Independent Test: Delete task 2 → Verify IDs 1,3 remain, gap preserved
- **Phase 7: User Story 5 - Mark Complete/Incomplete** (3 tasks)
  - T021: mark_task() service (toggle status)
  - T022: mark_task_handler() CLI (show current, toggle, display new)
  - T023: Wire to menu choice 5
  - Independent Test: Toggle status → Verify infinite toggling works
- **Phase 8: Main Menu & Application Loop** (3 tasks)
  - T024: main_loop() (while loop, menu, routing, exit)
  - T025: Entry point (src/main.py)
  - T026: Error handling wrapper
- **Phase 9: Polish** (7 tasks)
  - T027-T030: Verify all messages match spec.md exact text
  - T031: Test quickstart.md scenarios
  - T032: Verify constitution compliance
  - T033: Run all 41 manual test cases from plan.md

**Key Features**:
- **User Story Organization**: Each story independently testable with checkpoints
- **Parallel Opportunities**: 6 tasks marked [P] (T002, T005, T006, T027-T030)
- **MVP Scope**: T001-T009 (11 tasks) = Setup + Foundational + Add Task
- **Dependencies Documented**: Clear phase and story dependencies
- **File Paths**: All 33 tasks include exact file paths
- **Format Compliance**: ALL tasks follow checklist format with IDs, [P], [Story] labels

**Implementation Strategy**:
1. **MVP First**: T001-T009 → Can add tasks via console
2. **Incremental**: Add one story at a time, test independently
3. **Sequential**: Recommended execution T001 → T033 for Claude Code

**Task Count by Story**:
- Setup: 2
- Foundational: 4 (BLOCKS all stories)
- US1 (Add): 3
- US2 (View): 4
- US3 (Update): 4
- US4 (Delete): 3
- US5 (Mark): 3
- Menu: 3
- Polish: 7

## Outcome

- ✅ Impact: Created complete task breakdown for Phase I implementation; organized 33 granular tasks across 9 phases; each user story independently testable; clear MVP path (11 tasks); identified 6 parallel opportunities; all tasks reference exact file paths from plan.md; ready for `/sp.implement`
- 🧪 Tests: Manual testing strategy (41 test cases from plan.md in T033); no automated tests per spec requirement
- 📁 Files: 1 file created (tasks.md with 33 tasks)
- 🔁 Next prompts: Run `/sp.implement` to execute tasks and generate code; Can start with MVP scope (T001-T009) or full implementation (T001-T033)
- 🧠 Reflection: Task breakdown provides clear execution path; each story has checkpoint for independent validation; foundational phase (T003-T006) correctly identified as blocker for all stories; MVP scope (11 tasks) enables early validation; sequential execution recommended for Claude Code; all tasks actionable with specific file paths and clear descriptions

## Evaluation notes (flywheel)

- Failure modes observed: None (successful task generation on first attempt; all user stories correctly extracted from spec.md; proper checklist format applied to all 33 tasks)
- Graders run and results (PASS/FAIL): Format validation (PASS - all tasks follow `- [ ] [ID] [P?] [Story?] Description` format); User story organization (PASS - 5 stories mapped to 5 phases); File path inclusion (PASS - all 33 tasks include exact paths)
- Prompt variant (if applicable): Standard /sp.tasks workflow
- Next experiment (smallest change to try): Execute `/sp.implement` with MVP scope (T001-T009) first to validate foundational setup and User Story 1; then incrementally add remaining stories
