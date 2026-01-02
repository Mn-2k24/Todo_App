# Implementation Plan: Phase I Todo App

**Branch**: `002-phase-i-spec` | **Date**: 2025-12-31 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-phase-i-spec/spec.md`

## Summary

Phase I delivers a minimal, functional, console-based Todo application in Python operating entirely in memory. The application provides 5 core CRUD operations (Add, View, Update, Delete, Mark Complete/Incomplete) through a text-based menu interface. Implementation follows strict Spec-Driven Development principles with all code generated via Claude Code, no persistence, and Python 3.13+ standard library only.

**Technical Approach**: Single-module Python application using simple data structures (list/dict for task storage), menu-driven CLI with `input()`/`print()`, and comprehensive error handling to prevent crashes.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory (Python list or dictionary)
**Testing**: Manual CLI testing (automated tests optional per spec)
**Target Platform**: Any OS with Python 3.13+ (Linux, macOS, Windows)
**Project Type**: Single project (console application)
**Performance Goals**: <1 second per operation for lists up to 100 tasks
**Constraints**: No persistence, no external libraries, console-only, in-memory only
**Scale/Scope**: Single-user, single-session, up to 100 tasks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Scope Compliance

✅ **In-Scope Features** (All 5 Required):
1. Add Task - ✅ Specified
2. Delete Task - ✅ Specified
3. Update Task - ✅ Specified
4. View Tasks - ✅ Specified
5. Mark Task Complete/Incomplete - ✅ Specified

✅ **Out-of-Scope Enforcement** (No Prohibited Features):
- ❌ Databases or persistence - Not in plan
- ❌ Web or GUI interfaces - Not in plan
- ❌ AI features - Not in plan
- ❌ Advanced features (priorities, search, filtering, tags, due dates) - Not in plan

### SDD Compliance

✅ **Specification First**: Complete spec.md exists with all requirements
✅ **No Manual Code**: Implementation via Claude Code only
✅ **Spec Refinement**: Plan follows spec requirements precisely
✅ **Validation Gates**: Quality checklist passed (see checklists/requirements.md)
✅ **Traceability**: All plan elements trace to spec requirements

### Python Coding Standards

✅ **Python 3.13+**: Confirmed
✅ **Standard Library Only**: No external dependencies
✅ **Clean Code**: Modular structure, clear naming, small functions planned
✅ **In-Memory Data**: Using Python list/dict
✅ **Console-Only**: Text-based menu via input()/print()

### Error Handling & Validation

✅ **Graceful Errors**: All invalid inputs handled without crashes
✅ **User-Friendly Messages**: Error messages from spec (e.g., "Error: Task ID must be a number")
✅ **Validation**: Input validation planned for all user inputs
✅ **Recovery**: Return to menu after errors

**GATE RESULT**: ✅ **PASS** - All constitution requirements met, no violations

## Project Structure

### Documentation (this feature)

```text
specs/002-phase-i-spec/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technical decisions)
├── data-model.md        # Phase 1 output (Task entity design)
├── quickstart.md        # Phase 1 output (user guide)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py          # Task class definition
├── services/
│   └── todo_service.py  # Business logic (add, update, delete, mark)
├── cli/
│   ├── menu.py          # Main menu display and input handling
│   └── task_view.py     # Task list display formatting
└── main.py              # Application entry point

tests/                   # Optional (per spec, tests not required)
└── manual_test_plan.md  # Manual testing checklist
```

**Structure Decision**: Single project structure selected because:
- Console-only application (no web frontend/backend split needed)
- Single user, single session (no multi-tier architecture)
- Minimal complexity (no separate API layer)
- All features interact with same in-memory task list

## Complexity Tracking

> No violations detected. All constitution principles followed.

---

# Phase 0: Research & Technical Decisions

## Research Topics

### 1. Data Structure Selection for Task Storage

**Decision**: Use Python list for task storage

**Rationale**:
- Simple sequential access for viewing all tasks (O(n) acceptable for <100 tasks)
- Tasks have sequential integer IDs (1, 2, 3, ...) matching list indices
- Easy iteration for display and search by ID
- No need for complex lookups (dictionary) given small scale

**Alternatives Considered**:
- **Dictionary `{id: Task}`**: Better for O(1) lookup by ID, but adds complexity for sequential ID assignment and ordering. Rejected due to YAGNI (You Aren't Gonna Need It) - list is simpler.
- **Set**: No ordering, IDs would need separate tracking. Rejected.

**Implementation**: Global `tasks = []` list containing Task objects

### 2. Task ID Assignment Strategy

**Decision**: Use incrementing counter starting from 1

**Rationale**:
- Simple, predictable IDs (1, 2, 3, ...)
- Easy to display and reference for users
- No reuse of deleted IDs (gap in sequence after deletion) per spec requirement
- Counter tracks next available ID

**Alternatives Considered**:
- **List index as ID**: Problem - indices change when tasks are deleted. Rejected.
- **UUID**: Overkill for in-memory single-session app. Not user-friendly. Rejected.

**Implementation**: Global `next_task_id = 1` counter, incremented on each add

### 3. Task Class Design

**Decision**: Simple dataclass with id, description, status attributes

**Rationale**:
- Python dataclasses provide automatic __init__, __repr__, __eq__
- Immutable ID (set once in constructor)
- Mutable description and status (for updates)
- No methods (business logic in TodoService, not in model)

**Alternatives Considered**:
- **Plain dict**: Less type safety, no attribute access. Rejected.
- **Named tuple**: Immutable, can't update description/status. Rejected.

**Implementation**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    description: str
    status: str  # "Complete" or "Incomplete"
```

### 4. Menu Loop Structure

**Decision**: Infinite while loop with switch-case (match statement) for menu choices

**Rationale**:
- Continuously redisplays menu after each operation (per spec FR-MENU-004)
- Python 3.10+ match/case statement provides clean routing
- Easy to add new menu options
- Exit condition (choice 6) breaks loop

**Alternatives Considered**:
- **Recursive function calls**: Stack overflow risk if user runs app for long time. Rejected.
- **if-elif chain**: Works but less readable than match/case. Acceptable fallback if match unavailable.

**Implementation**: Main loop in main.py calls menu functions based on user choice

### 5. Error Handling Strategy

**Decision**: Try-except blocks at menu choice level, validate inputs before processing

**Rationale**:
- Prevents crashes from invalid user input (per FR-ERR-001)
- Errors caught, message printed to stderr, return to menu
- Input validation (e.g., task ID is integer, description not empty) prevents errors early

**Alternatives Considered**:
- **Validate everywhere**: Redundant, adds complexity. Single validation point preferred.
- **No try-except**: App would crash. Violates spec. Rejected.

**Implementation**: Validation functions (e.g., `validate_task_id()`, `validate_description()`)

## Research Summary

All technical decisions resolved. No external dependencies needed. Implementation uses Python standard library features:
- `dataclasses` for Task model
- `input()` for user input
- `print()` for output, `sys.stderr` for errors
- `match/case` for menu routing (Python 3.10+)
- Simple list for storage, integer counter for IDs

---

# Phase 1: Design & Contracts

## Data Model

(See `data-model.md` for complete entity definitions)

**Core Entities**:

1. **Task**
   - `id`: int (unique, immutable, sequential)
   - `description`: str (1-200 chars after trim, mutable)
   - `status`: str ("Complete" | "Incomplete", mutable)

2. **TaskList** (Global State)
   - `tasks`: List[Task] (in-memory storage)
   - `next_task_id`: int (counter for ID assignment)

**Relationships**: None (single entity model)

**Validation Rules**:
- Task ID must be positive integer
- Description must be non-empty after trimming
- Status must be exactly "Complete" or "Incomplete"

## Module Structure & Responsibilities

### `src/models/task.py`
**Purpose**: Task entity definition
**Responsibilities**:
- Define Task dataclass
- No business logic (data container only)

### `src/services/todo_service.py`
**Purpose**: Business logic for all CRUD operations
**Responsibilities**:
- `add_task(description: str) -> Task`: Create and store task
- `get_all_tasks() -> List[Task]`: Retrieve all tasks
- `get_task_by_id(task_id: int) -> Task | None`: Find task by ID
- `update_task(task_id: int, new_description: str) -> bool`: Update description
- `delete_task(task_id: int) -> bool`: Remove task
- `mark_task(task_id: int) -> bool`: Toggle status
- Manage global `tasks` list and `next_task_id` counter

### `src/cli/menu.py`
**Purpose**: Main menu display and user choice handling
**Responsibilities**:
- `display_menu()`: Print menu options
- `get_user_choice() -> int`: Get and validate menu choice (1-6)
- `main_loop()`: Infinite loop calling menu and routing to features

### `src/cli/task_view.py`
**Purpose**: Task display formatting
**Responsibilities**:
- `display_tasks(tasks: List[Task])`: Format and print task list
- `display_empty_message()`: Print "No tasks found"

### `src/main.py`
**Purpose**: Application entry point
**Responsibilities**:
- Import and call `main_loop()` from cli/menu.py
- Handle global exception (last resort error handling)

## Quickstart Guide

(See `quickstart.md` for detailed usage instructions)

**Quick Start Steps**:
1. Ensure Python 3.13+ installed: `python --version`
2. Navigate to project root
3. Run application: `python src/main.py`
4. Follow on-screen menu prompts

**Example Session**:
```
=== Todo App ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit
Enter choice: 1

Enter task description: Buy groceries
Task added successfully.

=== Todo App ===
...
Enter choice: 2

Tasks:
1. [Incomplete] Buy groceries

=== Todo App ===
...
Enter choice: 6
```

---

# Implementation Plan by Feature

## Feature 1: Add Task

### Implementation Steps

1. **Create Task Model** (`src/models/task.py`)
   - Import dataclass
   - Define Task class with id, description, status fields
   - No validation in model (handled by service)

2. **Initialize Global State** (`src/services/todo_service.py`)
   - Create global `tasks: List[Task] = []`
   - Create global `next_task_id: int = 1`

3. **Implement `add_task()` Function** (`src/services/todo_service.py`)
   ```
   Steps:
   a. Accept description parameter (str)
   b. Trim whitespace: description = description.strip()
   c. Validate: if len(description) == 0, return None (error case)
   d. Create Task: task = Task(id=next_task_id, description=description, status="Incomplete")
   e. Append to list: tasks.append(task)
   f. Increment counter: next_task_id += 1
   g. Return task (success case)
   ```

4. **Create CLI Handler** (`src/cli/menu.py` - add_task_handler)
   ```
   Steps:
   a. Print prompt: "Enter task description: "
   b. Get input: description = input()
   c. Call service: task = add_task(description)
   d. If task is None:
      - Print to stderr: "Error: Task description cannot be empty. Please enter a description."
   e. Else:
      - Print to stdout: "Task added successfully."
   ```

5. **Wire to Main Menu**
   - In `main_loop()`, add case for choice 1 that calls `add_task_handler()`

### Dependencies

- None (foundational feature)
- Requires: Task model, TodoService, Menu system

### Testing & Verification

**Test Cases**:
1. **Happy Path**: Enter "Buy groceries" → Task added, ID 1, status Incomplete
2. **Empty Input**: Press Enter without text → Error message, no task created
3. **Whitespace Only**: Enter "   " → Error message, no task created
4. **Multi-Word**: Enter "Finish project documentation" → Full description stored
5. **Special Characters**: Enter "Call John @ 555-1234" → Stored as-is
6. **Leading/Trailing Spaces**: Enter "  Task  " → Stored as "Task" (trimmed)
7. **Sequential IDs**: Add 3 tasks → IDs are 1, 2, 3

**Expected CLI Output**:
```
Enter choice: 1
Enter task description: Buy groceries
Task added successfully.
```

**Error Case**:
```
Enter choice: 1
Enter task description:
Error: Task description cannot be empty. Please enter a description.
```

### Notes / Constraints

- ✅ Phase I only (no priorities, dates, categories)
- ✅ Console/CLI via input()/print()
- ✅ In-memory only (tasks list in RAM)
- ✅ No database or file I/O
- ✅ Python standard library (dataclasses, sys)
- ✅ Code generated via Claude Code

---

## Feature 2: View Tasks

### Implementation Steps

1. **Implement `get_all_tasks()` Function** (`src/services/todo_service.py`)
   ```
   Steps:
   a. Return copy of tasks list: return tasks[:]
   b. Or return tasks directly (safe since we control mutations)
   ```

2. **Create Display Function** (`src/cli/task_view.py`)
   ```
   display_tasks(tasks: List[Task]):
   Steps:
   a. If len(tasks) == 0:
      - Print "No tasks found."
      - Return
   b. Print header: "Tasks:"
   c. For each task in tasks (ordered by ID):
      - Format: f"{task.id}. [{task.status}] {task.description}"
      - Print formatted line
   ```

3. **Create CLI Handler** (`src/cli/menu.py` - view_tasks_handler)
   ```
   Steps:
   a. Call service: tasks = get_all_tasks()
   b. Call display: display_tasks(tasks)
   ```

4. **Wire to Main Menu**
   - In `main_loop()`, add case for choice 2 that calls `view_tasks_handler()`

### Dependencies

- **Depends On**: Add Task feature (need tasks to view)
- **Requires**: TodoService.get_all_tasks(), task_view.display_tasks()

### Testing & Verification

**Test Cases**:
1. **Empty List**: View with no tasks → "No tasks found."
2. **Single Task**: Add 1 task, view → ID, status, description displayed
3. **Multiple Tasks**: Add 3 tasks, view → All 3 displayed in ID order
4. **Complete vs Incomplete**: Add task, mark complete, view → "[Complete]" shown
5. **Long Description**: Add task with 100-char description → Displayed without truncation
6. **After Delete**: Delete task 2, view → Tasks 1, 3 shown (gap in IDs)

**Expected CLI Output**:
```
Enter choice: 2

Tasks:
1. [Incomplete] Buy groceries
2. [Incomplete] Finish homework
3. [Complete] Call dentist
```

**Empty Case**:
```
Enter choice: 2

No tasks found.
```

### Notes / Constraints

- ✅ Phase I only (no filtering, sorting, search)
- ✅ Display all tasks (no pagination)
- ✅ Read-only operation (no state changes)
- ✅ Simple list format (no table formatting)

---

## Feature 3: Update Task

### Implementation Steps

1. **Implement `get_task_by_id()` Function** (`src/services/todo_service.py`)
   ```
   Steps:
   a. For each task in tasks:
      - If task.id == task_id: return task
   b. Return None (not found)
   ```

2. **Implement `update_task()` Function** (`src/services/todo_service.py`)
   ```
   Steps:
   a. Find task: task = get_task_by_id(task_id)
   b. If task is None: return False (not found)
   c. Trim new description: new_description = new_description.strip()
   d. Validate: if len(new_description) == 0: return False (invalid)
   e. Update: task.description = new_description
   f. Return True (success)
   ```

3. **Create CLI Handler** (`src/cli/menu.py` - update_task_handler)
   ```
   Steps:
   a. Print prompt: "Enter task ID to update: "
   b. Get input: task_id_str = input()
   c. Validate integer:
      - Try: task_id = int(task_id_str)
      - Except ValueError:
        - Print to stderr: "Error: Task ID must be a number."
        - Return
   d. Get current task: task = get_task_by_id(task_id)
   e. If task is None:
      - Print to stderr: f"Error: Task ID {task_id} not found. Please enter a valid task ID."
      - Return
   f. Display current: print(f"Current: {task.description}")
   g. Print prompt: "Enter new description: "
   h. Get input: new_description = input()
   i. Call service: success = update_task(task_id, new_description)
   j. If success:
      - Print: "Task updated successfully."
   k. Else:
      - Print to stderr: "Error: Task description cannot be empty. Task not updated."
   ```

4. **Wire to Main Menu**
   - In `main_loop()`, add case for choice 3 that calls `update_task_handler()`

### Dependencies

- **Depends On**: Add Task, View Tasks (need tasks to update, need IDs)
- **Requires**: TodoService.get_task_by_id(), TodoService.update_task()

### Testing & Verification

**Test Cases**:
1. **Valid Update**: Add task 1, update to "New description" → Description changed
2. **Non-Existent ID**: Try to update task 99 → "Task ID 99 not found" error
3. **Invalid ID Format**: Enter "abc" as ID → "Task ID must be a number" error
4. **Empty New Description**: Enter "" as new description → "cannot be empty" error
5. **Whitespace Trimming**: Update to "  New  " → Stored as "New"
6. **ID Preserved**: Update task 2 → ID remains 2, status unchanged
7. **Status Preserved**: Update complete task → Remains complete

**Expected CLI Output**:
```
Enter choice: 3
Enter task ID to update: 1
Current: Buy groceries
Enter new description: Buy groceries and milk
Task updated successfully.
```

**Error Cases**:
```
Enter choice: 3
Enter task ID to update: 99
Error: Task ID 99 not found. Please enter a valid task ID.
```

### Notes / Constraints

- ✅ Only description changes (ID and status immutable during update)
- ✅ No batch updates (one task at a time)
- ✅ Validation before update (prevents empty descriptions)

---

## Feature 4: Delete Task

### Implementation Steps

1. **Implement `delete_task()` Function** (`src/services/todo_service.py`)
   ```
   Steps:
   a. Find task: task = get_task_by_id(task_id)
   b. If task is None: return False (not found)
   c. Remove from list: tasks.remove(task)
   d. Return True (success)
   ```

2. **Create CLI Handler** (`src/cli/menu.py` - delete_task_handler)
   ```
   Steps:
   a. Print prompt: "Enter task ID to delete: "
   b. Get input: task_id_str = input()
   c. Validate integer:
      - Try: task_id = int(task_id_str)
      - Except ValueError:
        - Print to stderr: "Error: Task ID must be a number."
        - Return
   d. Call service: success = delete_task(task_id)
   e. If success:
      - Print: "Task deleted successfully."
   f. Else:
      - Print to stderr: f"Error: Task ID {task_id} not found. No task deleted."
   ```

3. **Wire to Main Menu**
   - In `main_loop()`, add case for choice 4 that calls `delete_task_handler()`

### Dependencies

- **Depends On**: Add Task, View Tasks (need tasks to delete, need IDs)
- **Requires**: TodoService.get_task_by_id(), TodoService.delete_task()

### Testing & Verification

**Test Cases**:
1. **Valid Delete**: Add 3 tasks, delete task 2 → Task removed, IDs 1,3 remain
2. **Non-Existent ID**: Try to delete task 99 → "Task ID 99 not found" error
3. **Invalid ID Format**: Enter "xyz" as ID → "Task ID must be a number" error
4. **Delete Complete Task**: Add and complete task, delete → Removed successfully
5. **Delete Incomplete Task**: Add task, delete → Removed successfully
6. **ID Gap Preserved**: Delete task 2 → Next added task gets ID 4 (not 2)
7. **View After Delete**: Delete task, view list → Deleted task not shown

**Expected CLI Output**:
```
Enter choice: 4
Enter task ID to delete: 2
Task deleted successfully.
```

**Error Case**:
```
Enter choice: 4
Enter task ID to delete: 99
Error: Task ID 99 not found. No task deleted.
```

### Notes / Constraints

- ✅ Permanent deletion (no undo within session)
- ✅ No confirmation prompt ("Are you sure?") per spec
- ✅ Deleted IDs not reused (gap in sequence)
- ✅ No cascade effects (standalone operation)

---

## Feature 5: Mark Task Complete/Incomplete

### Implementation Steps

1. **Implement `mark_task()` Function** (`src/services/todo_service.py`)
   ```
   Steps:
   a. Find task: task = get_task_by_id(task_id)
   b. If task is None: return None (not found)
   c. Toggle status:
      - If task.status == "Incomplete":
        - task.status = "Complete"
      - Else:
        - task.status = "Incomplete"
   d. Return task.status (new status)
   ```

2. **Create CLI Handler** (`src/cli/menu.py` - mark_task_handler)
   ```
   Steps:
   a. Print prompt: "Enter task ID: "
   b. Get input: task_id_str = input()
   c. Validate integer:
      - Try: task_id = int(task_id_str)
      - Except ValueError:
        - Print to stderr: "Error: Task ID must be a number."
        - Return
   d. Get current task: task = get_task_by_id(task_id)
   e. If task is None:
      - Print to stderr: f"Error: Task ID {task_id} not found. Status not changed."
      - Return
   f. Display current: print(f"Current status: {task.status}")
   g. Call service: new_status = mark_task(task_id)
   h. If new_status:
      - Print: f"Task marked as {new_status}."
   i. Else:
      - Print to stderr: "Error: Unable to update task status."
   ```

3. **Wire to Main Menu**
   - In `main_loop()`, add case for choice 5 that calls `mark_task_handler()`

### Dependencies

- **Depends On**: Add Task, View Tasks (need tasks to mark, need IDs)
- **Requires**: TodoService.get_task_by_id(), TodoService.mark_task()

### Testing & Verification

**Test Cases**:
1. **Mark Incomplete → Complete**: Add task, mark → Status changes to "Complete"
2. **Mark Complete → Incomplete**: Mark complete task again → Toggles back to "Incomplete"
3. **Multiple Toggles**: Mark → Unmark → Mark → Status cycles correctly
4. **Non-Existent ID**: Try to mark task 99 → "Task ID 99 not found" error
5. **Invalid ID Format**: Enter "abc" as ID → "Task ID must be a number" error
6. **ID Preserved**: Mark task 2 → ID remains 2, description unchanged
7. **Description Preserved**: Mark task → Description unchanged

**Expected CLI Output**:
```
Enter choice: 5
Enter task ID: 1
Current status: Incomplete
Task marked as Complete.
```

**Toggle Example**:
```
Enter choice: 5
Enter task ID: 1
Current status: Complete
Task marked as Incomplete.
```

**Error Case**:
```
Enter choice: 5
Enter task ID: 99
Error: Task ID 99 not found. Status not changed.
```

### Notes / Constraints

- ✅ Single toggle operation (no separate "mark complete" and "mark incomplete")
- ✅ Can toggle infinitely (no limit on status changes)
- ✅ Only status changes (ID and description immutable)
- ✅ No partial states (only "Complete" or "Incomplete")

---

## Feature 6: Main Menu & Application Loop

### Implementation Steps

1. **Create Menu Display** (`src/cli/menu.py`)
   ```
   display_menu():
   Steps:
   a. Print header: "=== Todo App ==="
   b. Print options:
      "1. Add Task"
      "2. View Tasks"
      "3. Update Task"
      "4. Delete Task"
      "5. Mark Task Complete/Incomplete"
      "6. Exit"
   c. Print prompt: "Enter choice: "
   ```

2. **Create Choice Handler** (`src/cli/menu.py`)
   ```
   get_user_choice() -> int:
   Steps:
   a. Get input: choice_str = input()
   b. Validate integer:
      - Try: choice = int(choice_str)
      - Except ValueError:
        - Print to stderr: "Error: Please enter a number between 1 and 6."
        - Return 0 (invalid)
   c. Validate range:
      - If choice < 1 or choice > 6:
        - Print to stderr: "Error: Please enter a number between 1 and 6."
        - Return 0 (invalid)
   d. Return choice
   ```

3. **Create Main Loop** (`src/cli/menu.py`)
   ```
   main_loop():
   Steps:
   a. While True:
      b. Call display_menu()
      c. Get choice: choice = get_user_choice()
      d. If choice == 0: continue (invalid, re-display menu)
      e. Match choice:
         - Case 1: add_task_handler()
         - Case 2: view_tasks_handler()
         - Case 3: update_task_handler()
         - Case 4: delete_task_handler()
         - Case 5: mark_task_handler()
         - Case 6: break (exit loop)
      f. Print newline for spacing
   g. After loop: print "Goodbye!" and exit
   ```

4. **Create Entry Point** (`src/main.py`)
   ```
   Steps:
   a. Import main_loop from cli.menu
   b. Add main guard: if __name__ == "__main__":
   c. Call main_loop()
   ```

### Dependencies

- **Depends On**: All 5 features (menu routes to feature handlers)
- **Requires**: All CLI handlers, menu display functions

### Testing & Verification

**Test Cases**:
1. **Menu Display**: Run app → Menu shows all 6 options correctly
2. **Valid Choices**: Enter 1-6 → Corresponding feature executes
3. **Invalid Choice (Non-Integer)**: Enter "abc" → Error message, re-display menu
4. **Invalid Choice (Out of Range)**: Enter 7 → Error message, re-display menu
5. **Exit**: Enter 6 → App terminates with exit code 0
6. **Menu Redisplay**: Complete any operation → Menu redisplays
7. **Continuous Loop**: Perform 10 operations → App doesn't crash or exit unexpectedly

**Expected CLI Output**:
```
=== Todo App ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit
Enter choice: 1

[Add task operation]

=== Todo App ===
...
Enter choice: 6
Goodbye!
```

**Error Case**:
```
Enter choice: abc
Error: Please enter a number between 1 and 6.

=== Todo App ===
...
```

### Notes / Constraints

- ✅ Infinite loop until user selects Exit
- ✅ Menu redisplays after each operation
- ✅ Invalid input handled gracefully (no crash)
- ✅ Exit terminates cleanly (exit code 0)

---

# Summary & Next Steps

## Implementation Summary

**Total Features**: 5 core CRUD operations + Main Menu system
**Total Modules**: 5 files (task.py, todo_service.py, menu.py, task_view.py, main.py)
**Total Functions**: ~15 functions across all modules
**Lines of Code (Estimated)**: ~300-400 lines (simple, focused implementation)

**Key Design Decisions**:
1. List-based storage (simple, sufficient for <100 tasks)
2. Sequential integer IDs (user-friendly, predictable)
3. Dataclass Task model (clean, pythonic)
4. Modular structure (separation of concerns: models, services, CLI)
5. Comprehensive error handling (no crashes on invalid input)

## Phase 2: Task Generation

**Next Command**: `/sp.tasks`

This will generate `tasks.md` with:
- Granular, testable tasks for implementation
- Dependency ordering
- Test cases for each task
- Acceptance criteria

## Phase 3: Implementation

**Next Command**: `/sp.implement`

This will execute tasks from `tasks.md`:
- Generate Python code via Claude Code
- Create all source files in `src/` directory
- Validate against spec requirements
- Run manual tests

## Readiness Checklist

- [x] Technical Context defined
- [x] Constitution Check passed
- [x] Research complete (all technical decisions made)
- [x] Data model designed
- [x] Module structure defined
- [x] Implementation steps detailed for all features
- [x] Test cases specified
- [x] Ready for task breakdown (`/sp.tasks`)

**Status**: ✅ **READY FOR TASK GENERATION**

The plan is complete and validated. Proceed with `/sp.tasks` to create actionable implementation tasks.
