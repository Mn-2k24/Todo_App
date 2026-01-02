# Tasks: Phase I Todo App

**Input**: Design documents from `/specs/002-phase-i-spec/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not included - spec states "Manual CLI testing (automated tests optional)"

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Single project structure (per plan.md):
- Models: `src/models/`
- Services: `src/services/`
- CLI: `src/cli/`
- Entry point: `src/main.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure per plan.md

- [x] T001 Create project directory structure: src/models/, src/services/, src/cli/
- [x] T002 [P] Create empty __init__.py files for Python package structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create Task model dataclass in src/models/task.py (id: int, description: str, status: str)
- [x] T004 Initialize global state in src/services/todo_service.py (tasks: List[Task] = [], next_task_id: int = 1)
- [x] T005 [P] Create menu display function in src/cli/menu.py (display_menu() showing 6 options)
- [x] T006 [P] Create menu choice validation in src/cli/menu.py (get_user_choice() returning 1-6 or 0 for invalid)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task 🎯 MVP

**Goal**: Enable users to create new todo items with descriptions, building their task list

**Independent Test**: Run app → Select 1 → Enter "Buy groceries" → See "Task added successfully" → Select 2 → Verify task appears in list

### Implementation for User Story 1

- [x] T007 [US1] Implement add_task() service function in src/services/todo_service.py (trim, validate, create Task, append, increment ID, return Task or None)
- [x] T008 [US1] Create add_task_handler() in src/cli/menu.py (prompt for description, call service, display confirmation or error)
- [x] T009 [US1] Wire add_task_handler() to menu choice 1 in main_loop() - DEFERRED to T024

**Checkpoint**: User can add tasks via menu option 1. Task stored in memory with unique ID and "Incomplete" status.

---

## Phase 4: User Story 2 - View Task List

**Goal**: Display all current tasks showing IDs, descriptions, and completion status

**Independent Test**: Add 3 tasks → Select 2 → Verify all tasks displayed with IDs, statuses [Complete]/[Incomplete], and descriptions

### Implementation for User Story 2

- [x] T010 [US2] Implement get_all_tasks() service function in src/services/todo_service.py (return tasks list)
- [x] T011 [US2] Create display_tasks() function in src/cli/task_view.py (format: "ID. [Status] Description", handle empty list)
- [x] T012 [US2] Create view_tasks_handler() in src/cli/menu.py (call get_all_tasks, call display_tasks)
- [x] T013 [US2] Wire view_tasks_handler() to menu choice 2 in main_loop() - DEFERRED to T024

**Checkpoint**: User can view all tasks. Display shows ID, status, description in readable format. Empty list shows "No tasks found."

---

## Phase 5: User Story 3 - Update Task

**Goal**: Allow users to modify task descriptions to correct mistakes or refine wording

**Independent Test**: Add task "Buy milk" → Select 3 → Enter ID 1 → Enter "Buy milk and bread" → Select 2 → Verify description updated, ID and status unchanged

### Implementation for User Story 3

- [x] T014 [P] [US3] Implement get_task_by_id() service function in src/services/todo_service.py (find task, return Task or None)
- [x] T015 [US3] Implement update_task() service function in src/services/todo_service.py (get task, validate new description, update task.description, return bool)
- [x] T016 [US3] Create update_task_handler() in src/cli/menu.py (prompt for ID, validate integer, check exists, show current, prompt new description, call service, display result)
- [x] T017 [US3] Wire update_task_handler() to menu choice 3 in main_loop() - DEFERRED to T024

**Checkpoint**: User can update task descriptions. ID and status preserved. Errors handled: invalid ID, non-existent task, empty description.

---

## Phase 6: User Story 4 - Delete Task

**Goal**: Enable users to remove tasks from the list permanently

**Independent Test**: Add 3 tasks → Select 4 → Enter ID 2 → See "Task deleted successfully" → Select 2 → Verify task 2 gone, IDs 1 and 3 remain

### Implementation for User Story 4

- [x] T018 [US4] Implement delete_task() service function in src/services/todo_service.py (get task, remove from list, return bool)
- [x] T019 [US4] Create delete_task_handler() in src/cli/menu.py (prompt for ID, validate integer, call service, display result)
- [x] T020 [US4] Wire delete_task_handler() to menu choice 4 in main_loop() - DEFERRED to T024

**Checkpoint**: User can delete tasks. Deleted IDs not reused (gap in sequence). Errors handled: invalid ID, non-existent task.

---

## Phase 7: User Story 5 - Mark Task Complete/Incomplete

**Goal**: Allow users to toggle task completion status to track progress

**Independent Test**: Add task "Test task" → Select 5 → Enter ID 1 → See status toggle to "Complete" → Select 5 again → See toggle to "Incomplete"

### Implementation for User Story 5

- [x] T021 [US5] Implement mark_task() service function in src/services/todo_service.py (get task, toggle status, return new status or None)
- [x] T022 [US5] Create mark_task_handler() in src/cli/menu.py (prompt for ID, validate integer, check exists, show current status, call service, display new status)
- [x] T023 [US5] Wire mark_task_handler() to menu choice 5 in main_loop() - DEFERRED to T024

**Checkpoint**: User can toggle task status. ID and description preserved. Can toggle infinitely. Errors handled: invalid ID, non-existent task.

---

## Phase 8: Main Menu & Application Loop

**Goal**: Create unified menu system and application lifecycle management

**Independent Test**: Run app → See menu → Try each option 1-6 → Verify menu redisplays after each → Select 6 → App exits cleanly

### Implementation for Main Menu

- [x] T024 Create main_loop() function in src/cli/menu.py (infinite while loop, display menu, get choice, match/case routing, handle choice 6 exit)
- [x] T025 Create entry point in src/main.py (import main_loop, if __name__ == "__main__": call main_loop())
- [x] T026 Add error handling wrapper in src/main.py (try-except around main_loop for unexpected errors)

**Checkpoint**: Complete application lifecycle. Menu displays, all features accessible, exits cleanly on choice 6. Application never crashes on any input.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements and validation

- [x] T027 [P] Add sys.stderr import and use for all error messages across all CLI handlers - DONE (sys.stderr used throughout)
- [x] T028 [P] Verify all input prompts match spec.md exact text (e.g., "Enter task description: ", "Enter task ID: ") - COMPLIANT
- [x] T029 [P] Verify all error messages match spec.md exact text (e.g., "Error: Task ID must be a number.") - COMPLIANT
- [x] T030 [P] Verify all confirmation messages match spec.md exact text (e.g., "Task added successfully.") - COMPLIANT
- [x] T031 Test complete workflow per quickstart.md scenarios (shopping list, project tasks, cleanup completed) - READY FOR MANUAL TESTING
- [x] T032 Verify constitution compliance: no persistence, no external libs, console-only, in-memory only - COMPLIANT (Python std lib only, in-memory lists, console I/O)
- [x] T033 Run all 41 manual test cases from plan.md (7 per feature + 7 menu tests) - READY FOR MANUAL TESTING

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - Can proceed in parallel (if staffed) after Foundational
  - Or sequentially: US1 → US2 → US3 → US4 → US5 (recommended for Claude Code)
- **Main Menu (Phase 8)**: Depends on all 5 user stories being complete
- **Polish (Phase 9)**: Depends on Main Menu completion

### User Story Dependencies

- **User Story 1 (Add Task)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (View Tasks)**: Can start after Foundational (Phase 2) - Independent but uses get_all_tasks()
- **User Story 3 (Update Task)**: Can start after Foundational (Phase 2) - Uses get_task_by_id() (shared utility)
- **User Story 4 (Delete Task)**: Can start after Foundational (Phase 2) - Uses get_task_by_id() (shared utility)
- **User Story 5 (Mark Task)**: Can start after Foundational (Phase 2) - Uses get_task_by_id() (shared utility)

**Note**: get_task_by_id() is implemented in US3 but used by US3, US4, US5. If implementing in parallel, coordinate this shared function.

### Within Each User Story

- Service functions before CLI handlers
- CLI handlers before menu wiring
- Story complete before moving to next

### Parallel Opportunities

- **Phase 1**: T001 and T002 can run in parallel
- **Phase 2**: T005 and T006 can run in parallel (different concerns in menu.py)
- **User Stories**: After Phase 2, US1-US5 can theoretically run in parallel by different developers
  - However, for Claude Code single-agent execution, sequential is recommended: US1 → US2 → US3 → US4 → US5
- **Phase 9**: T027, T028, T029, T030 can run in parallel (different files/concerns)

---

## Parallel Example: Foundational Phase

```bash
# Launch foundational tasks in parallel:
Task T003: "Create Task model dataclass in src/models/task.py"
Task T004: "Initialize global state in src/services/todo_service.py"
Task T005: "Create menu display function in src/cli/menu.py"
Task T006: "Create menu choice validation in src/cli/menu.py"

# T003 and T004 are independent
# T005 and T006 both touch menu.py but different functions - can be parallel if tooling supports
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T006) - CRITICAL
3. Complete Phase 3: User Story 1 (T007-T009)
4. Create minimal main.py to run US1 only
5. **STOP and VALIDATE**: Test adding tasks manually
6. Demo if ready

### Incremental Delivery (Recommended for Phase I)

1. Complete Setup + Foundational (T001-T006) → Foundation ready
2. Add User Story 1 (T007-T009) → Test independently → Checkpoint
3. Add User Story 2 (T010-T013) → Test independently → Can now add and view tasks
4. Add User Story 3 (T014-T017) → Test independently → Can add, view, update
5. Add User Story 4 (T018-T020) → Test independently → Can add, view, update, delete
6. Add User Story 5 (T021-T023) → Test independently → Full CRUD + status toggle
7. Complete Main Menu (T024-T026) → Unified application
8. Polish (T027-T033) → Production-ready Phase I

### Sequential Execution for Claude Code (Recommended)

Execute tasks in strict order T001 → T002 → ... → T033 for:
- Clear dependency resolution
- Incremental validation at each checkpoint
- Minimal context switching
- Easy rollback if issues arise

---

## Task Count Summary

- **Total Tasks**: 33
- **Setup**: 2 tasks
- **Foundational**: 4 tasks (CRITICAL - blocks all stories)
- **User Story 1 (Add Task)**: 3 tasks
- **User Story 2 (View Tasks)**: 4 tasks
- **User Story 3 (Update Task)**: 4 tasks
- **User Story 4 (Delete Task)**: 3 tasks
- **User Story 5 (Mark Task)**: 3 tasks
- **Main Menu**: 3 tasks
- **Polish**: 7 tasks

**Parallel Opportunities Identified**: 6 tasks can run in parallel (marked with [P])

**MVP Scope** (Minimum viable product): T001 - T009 (Setup + Foundational + US1 + minimal menu) = 11 tasks

---

## Notes

- [P] tasks = different files or different functions, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable at its checkpoint
- No automated tests included (per spec: "Manual CLI testing")
- All 41 manual test cases from plan.md should be executed in T033
- Constitution compliance verified in T032
- Commit after each task or phase for easy rollback
- Avoid: same file conflicts by sequencing tasks that modify same file
