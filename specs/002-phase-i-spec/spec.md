# Phase I Complete Specification: Todo In-Memory Python Console App

**Feature Branch**: `002-phase-i-spec`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User description: "Complete Phase I specification for all 5 features"

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Feature 1: Add Task](#feature-1-add-task)
3. [Feature 2: View Task List](#feature-2-view-task-list)
4. [Feature 3: Update Task](#feature-3-update-task)
5. [Feature 4: Delete Task](#feature-4-delete-task)
6. [Feature 5: Mark Task Complete/Incomplete](#feature-5-mark-task-completein complete)
7. [Shared Requirements](#shared-requirements)
8. [Global Success Criteria](#global-success-criteria)

---

## Project Overview

**Purpose**: Create a minimal, functional, console-based Todo application in Python that operates entirely in memory.

**Phase I Vision**: Deliver a working prototype demonstrating core CRUD operations for todo tasks through a text-based terminal interface without persistence, web interfaces, or advanced features.

**Key Constraints**:
- In-memory only (no databases or file persistence)
- Console/CLI only (text-based menu interaction)
- Python 3.13+ standard library only
- No web, GUI, AI, or advanced features

**Core Entities**:
- **Task**: A todo item with unique ID, description (text), and status (Complete/Incomplete)
- **Task List**: In-memory collection of all tasks (list or dictionary)

---

# Feature 1: Add Task

## Feature Overview

The Add Task feature enables users to create new todo items by entering a text description. This is the foundational feature that allows users to capture tasks they need to accomplish.

**User Value**: Users can quickly record tasks as they think of them, building their personal todo list.

## User Story

**As a** user of the todo application,
**I want to** add a new task with a description,
**So that** I can track what I need to do.

## Functional Requirements

- **FR-ADD-001**: System MUST provide a "Add Task" menu option in the main menu
- **FR-ADD-002**: System MUST prompt user with "Enter task description: " when Add Task is selected
- **FR-ADD-003**: System MUST accept task descriptions containing letters, numbers, spaces, and common punctuation
- **FR-ADD-004**: System MUST create a new task with the provided description and status "Incomplete"
- **FR-ADD-005**: System MUST assign a unique sequential identifier to each new task
- **FR-ADD-006**: System MUST store the task in the in-memory task list
- **FR-ADD-007**: System MUST trim leading and trailing whitespace from descriptions
- **FR-ADD-008**: System MUST reject empty descriptions (zero-length or whitespace-only)
- **FR-ADD-009**: System MUST display confirmation "Task added successfully" after creation
- **FR-ADD-010**: System MUST return to main menu after adding task

## Acceptance Criteria

- [ ] **AC-ADD-001**: User can select "Add Task" from main menu
- [ ] **AC-ADD-002**: System displays prompt "Enter task description: "
- [ ] **AC-ADD-003**: User can enter multi-word description and press Enter
- [ ] **AC-ADD-004**: Task is created with status "Incomplete" and unique ID
- [ ] **AC-ADD-005**: Confirmation message "Task added successfully" appears
- [ ] **AC-ADD-006**: System returns to main menu
- [ ] **AC-ADD-007**: Empty descriptions are rejected with error
- [ ] **AC-ADD-008**: Whitespace-only descriptions are rejected with error
- [ ] **AC-ADD-009**: Leading/trailing whitespace is removed from stored description
- [ ] **AC-ADD-010**: Task appears in list when user views tasks

## Validation Rules

- **VR-ADD-001**: Description MUST NOT be empty after trimming whitespace
- **VR-ADD-002**: Description length after trimming MUST be at least 1 character
- **VR-ADD-003**: Task ID MUST be unique within current application session

## Error Handling

**Error: Empty Description**
- **Trigger**: User presses Enter without text, or enters only spaces/tabs
- **Message**: "Error: Task description cannot be empty. Please enter a description."
- **Behavior**: Return to main menu; do not create task; do not crash

## Notes / Constraints

- ✅ In-memory only (task lost on exit)
- ✅ Console/CLI interaction via `input()` and `print()`
- ✅ No database, web, GUI, or AI features
- ✅ Python 3.13+ standard library
- Task IDs assigned sequentially starting from 1
- Maximum description length: Limited only by memory (no enforced cap)

---

# Feature 2: View Task List

## Feature Overview

The View Task List feature displays all current tasks in a readable format, showing task IDs, descriptions, and completion status. This allows users to see what tasks they have and their current state.

**User Value**: Users can review their entire todo list at a glance to plan their work and track progress.

## User Story

**As a** user of the todo application,
**I want to** view all my tasks in a list format,
**So that** I can see what I need to do and what I've completed.

## Functional Requirements

- **FR-VIEW-001**: System MUST provide a "View Tasks" menu option in the main menu
- **FR-VIEW-002**: System MUST display all tasks currently stored in memory
- **FR-VIEW-003**: System MUST show task ID, status, and description for each task
- **FR-VIEW-004**: System MUST format status as "[Complete]" or "[Incomplete]"
- **FR-VIEW-005**: System MUST display tasks in ascending order by ID
- **FR-VIEW-006**: System MUST display "No tasks found" when task list is empty
- **FR-VIEW-007**: System MUST use clear, human-readable format (not technical dump)
- **FR-VIEW-008**: System MUST return to main menu after displaying tasks

## Acceptance Criteria

- [ ] **AC-VIEW-001**: User can select "View Tasks" from main menu
- [ ] **AC-VIEW-002**: All tasks are displayed in a numbered list
- [ ] **AC-VIEW-003**: Each task shows: ID, status marker, and description
- [ ] **AC-VIEW-004**: Status is shown as "[Complete]" or "[Incomplete]"
- [ ] **AC-VIEW-005**: Tasks appear in order by ID (1, 2, 3, ...)
- [ ] **AC-VIEW-006**: Empty list shows "No tasks found" message
- [ ] **AC-VIEW-007**: Display is easy to read (aligned, clear formatting)
- [ ] **AC-VIEW-008**: System returns to main menu after display
- [ ] **AC-VIEW-009**: Long descriptions are displayed without truncation
- [ ] **AC-VIEW-010**: Special characters in descriptions display correctly

## Validation Rules

- **VR-VIEW-001**: Display MUST show all tasks in task list (no filtering or hiding)
- **VR-VIEW-002**: Task order MUST be ascending by task ID

## Error Handling

**No Error Scenarios** (viewing is read-only and always succeeds)
- If task list is empty, display "No tasks found" (not an error condition)
- If task data is corrupted (edge case), display error and return to menu

## Notes / Constraints

- ✅ In-memory only (displays current session tasks)
- ✅ Console/CLI output via `print()`
- ✅ No database, web, GUI, or AI features
- ✅ Python 3.13+ standard library
- Display format example:
  ```
  Tasks:
  1. [Incomplete] Buy groceries
  2. [Complete] Finish homework
  3. [Incomplete] Call dentist
  ```
- No pagination (display all tasks regardless of count)

---

# Feature 3: Update Task

## Feature Overview

The Update Task feature allows users to modify the description of an existing task. This enables users to correct mistakes, add clarification, or refine task wording.

**User Value**: Users can edit tasks to fix typos, update requirements, or add more detail without deleting and recreating.

## User Story

**As a** user of the todo application,
**I want to** update the description of an existing task,
**So that** I can correct mistakes or refine task details.

## Functional Requirements

- **FR-UPDATE-001**: System MUST provide an "Update Task" menu option in the main menu
- **FR-UPDATE-002**: System MUST prompt user for task ID to update
- **FR-UPDATE-003**: System MUST validate that the provided task ID exists
- **FR-UPDATE-004**: System MUST display current task description before update
- **FR-UPDATE-005**: System MUST prompt user for new task description
- **FR-UPDATE-006**: System MUST accept new descriptions following same rules as Add Task
- **FR-UPDATE-007**: System MUST replace old description with new description
- **FR-UPDATE-008**: System MUST preserve task ID and status during update (only description changes)
- **FR-UPDATE-009**: System MUST trim leading/trailing whitespace from new description
- **FR-UPDATE-010**: System MUST reject empty new descriptions
- **FR-UPDATE-011**: System MUST display confirmation "Task updated successfully"
- **FR-UPDATE-012**: System MUST return to main menu after update

## Acceptance Criteria

- [ ] **AC-UPDATE-001**: User can select "Update Task" from main menu
- [ ] **AC-UPDATE-002**: System prompts "Enter task ID to update: "
- [ ] **AC-UPDATE-003**: User can enter task ID number
- [ ] **AC-UPDATE-004**: System displays current description "Current: [description]"
- [ ] **AC-UPDATE-005**: System prompts "Enter new description: "
- [ ] **AC-UPDATE-006**: User can enter new description
- [ ] **AC-UPDATE-007**: Task description is updated in memory
- [ ] **AC-UPDATE-008**: Task ID and status remain unchanged
- [ ] **AC-UPDATE-009**: Confirmation "Task updated successfully" appears
- [ ] **AC-UPDATE-010**: Non-existent task ID shows error message
- [ ] **AC-UPDATE-011**: Empty new description is rejected with error
- [ ] **AC-UPDATE-012**: System returns to main menu

## Validation Rules

- **VR-UPDATE-001**: Task ID MUST exist in current task list
- **VR-UPDATE-002**: Task ID MUST be a valid integer
- **VR-UPDATE-003**: New description MUST NOT be empty after trimming
- **VR-UPDATE-004**: New description length MUST be at least 1 character after trimming

## Error Handling

**Error: Task Not Found**
- **Trigger**: User enters task ID that doesn't exist
- **Message**: "Error: Task ID [ID] not found. Please enter a valid task ID."
- **Behavior**: Return to main menu; do not crash

**Error: Invalid Task ID Format**
- **Trigger**: User enters non-numeric value for task ID
- **Message**: "Error: Task ID must be a number."
- **Behavior**: Return to main menu; do not crash

**Error: Empty New Description**
- **Trigger**: User enters empty or whitespace-only new description
- **Message**: "Error: Task description cannot be empty. Task not updated."
- **Behavior**: Return to main menu; original description preserved; do not crash

## Notes / Constraints

- ✅ In-memory only (changes lost on exit)
- ✅ Console/CLI interaction
- ✅ No database, web, GUI, or AI features
- ✅ Python 3.13+ standard library
- Task ID and status are immutable (only description can change)
- Users cannot update non-existent tasks
- Users cannot change task ID during update

---

# Feature 4: Delete Task

## Feature Overview

The Delete Task feature allows users to remove tasks from the list. This enables users to clean up completed tasks or remove tasks that are no longer relevant.

**User Value**: Users can maintain a clean, focused task list by removing items they no longer need to track.

## User Story

**As a** user of the todo application,
**I want to** delete a task from my list,
**So that** I can remove completed or irrelevant tasks.

## Functional Requirements

- **FR-DELETE-001**: System MUST provide a "Delete Task" menu option in the main menu
- **FR-DELETE-002**: System MUST prompt user for task ID to delete
- **FR-DELETE-003**: System MUST validate that the provided task ID exists
- **FR-DELETE-004**: System MUST display task description before deletion (for confirmation context)
- **FR-DELETE-005**: System MUST remove the task from the in-memory task list
- **FR-DELETE-006**: System MUST display confirmation "Task deleted successfully"
- **FR-DELETE-007**: System MUST return to main menu after deletion
- **FR-DELETE-008**: System MUST handle deletion of any task regardless of status (Complete or Incomplete)

## Acceptance Criteria

- [ ] **AC-DELETE-001**: User can select "Delete Task" from main menu
- [ ] **AC-DELETE-002**: System prompts "Enter task ID to delete: "
- [ ] **AC-DELETE-003**: User can enter task ID number
- [ ] **AC-DELETE-004**: Task is removed from in-memory list
- [ ] **AC-DELETE-005**: Confirmation "Task deleted successfully" appears
- [ ] **AC-DELETE-006**: Deleted task no longer appears in View Tasks
- [ ] **AC-DELETE-007**: System returns to main menu
- [ ] **AC-DELETE-008**: Non-existent task ID shows error message
- [ ] **AC-DELETE-009**: Application does not crash on invalid input
- [ ] **AC-DELETE-010**: Both Complete and Incomplete tasks can be deleted

## Validation Rules

- **VR-DELETE-001**: Task ID MUST exist in current task list
- **VR-DELETE-002**: Task ID MUST be a valid integer

## Error Handling

**Error: Task Not Found**
- **Trigger**: User enters task ID that doesn't exist
- **Message**: "Error: Task ID [ID] not found. No task deleted."
- **Behavior**: Return to main menu; task list unchanged; do not crash

**Error: Invalid Task ID Format**
- **Trigger**: User enters non-numeric value for task ID
- **Message**: "Error: Task ID must be a number."
- **Behavior**: Return to main menu; task list unchanged; do not crash

## Notes / Constraints

- ✅ In-memory only (deletion is permanent within session, no undo)
- ✅ Console/CLI interaction
- ✅ No database, web, GUI, or AI features
- ✅ Python 3.13+ standard library
- Deletion is immediate (no confirmation prompt "Are you sure?")
- Deleted task IDs are not reused (gap in sequence after deletion)
- Example: After deleting task 2, task list shows IDs 1, 3, 4, ... (ID 2 doesn't get reassigned)

---

# Feature 5: Mark Task Complete/Incomplete

## Feature Overview

The Mark Task Complete/Incomplete feature allows users to toggle the completion status of tasks. This enables users to track their progress and distinguish between finished and pending work.

**User Value**: Users can mark tasks as done when completed, providing a sense of accomplishment and clear visibility into what remains.

## User Story

**As a** user of the todo application,
**I want to** mark a task as complete or incomplete,
**So that** I can track my progress and see which tasks are finished.

## Functional Requirements

- **FR-MARK-001**: System MUST provide a "Mark Task Complete/Incomplete" menu option in the main menu
- **FR-MARK-002**: System MUST prompt user for task ID to update
- **FR-MARK-003**: System MUST validate that the provided task ID exists
- **FR-MARK-004**: System MUST display current task status before update
- **FR-MARK-005**: System MUST toggle status: Incomplete → Complete, Complete → Incomplete
- **FR-MARK-006**: System MUST preserve task ID and description during status update
- **FR-MARK-007**: System MUST display confirmation showing new status (e.g., "Task marked as Complete")
- **FR-MARK-008**: System MUST return to main menu after status update

## Acceptance Criteria

- [ ] **AC-MARK-001**: User can select "Mark Task Complete/Incomplete" from main menu
- [ ] **AC-MARK-002**: System prompts "Enter task ID: "
- [ ] **AC-MARK-003**: User can enter task ID number
- [ ] **AC-MARK-004**: System shows current status "Current status: [Complete/Incomplete]"
- [ ] **AC-MARK-005**: Task status toggles to opposite value
- [ ] **AC-MARK-006**: Confirmation shows new status "Task marked as [Complete/Incomplete]"
- [ ] **AC-MARK-007**: Task ID and description remain unchanged
- [ ] **AC-MARK-008**: Updated status appears in View Tasks
- [ ] **AC-MARK-009**: System returns to main menu
- [ ] **AC-MARK-010**: Non-existent task ID shows error message
- [ ] **AC-MARK-011**: Status can be toggled multiple times (Complete → Incomplete → Complete ...)

## Validation Rules

- **VR-MARK-001**: Task ID MUST exist in current task list
- **VR-MARK-002**: Task ID MUST be a valid integer
- **VR-MARK-003**: Status MUST be either "Complete" or "Incomplete" (no other values)

## Error Handling

**Error: Task Not Found**
- **Trigger**: User enters task ID that doesn't exist
- **Message**: "Error: Task ID [ID] not found. Status not changed."
- **Behavior**: Return to main menu; task list unchanged; do not crash

**Error: Invalid Task ID Format**
- **Trigger**: User enters non-numeric value for task ID
- **Message**: "Error: Task ID must be a number."
- **Behavior**: Return to main menu; task list unchanged; do not crash

## Notes / Constraints

- ✅ In-memory only (status changes lost on exit)
- ✅ Console/CLI interaction
- ✅ No database, web, GUI, or AI features
- ✅ Python 3.13+ standard library
- Status toggle is automatic (no separate "Mark Complete" and "Mark Incomplete" options)
- Users can toggle status as many times as needed
- No partial completion states (only Complete or Incomplete, no percentages or "In Progress")

---

# Shared Requirements

## Main Menu Specification

All features are accessed through a unified main menu that displays on application startup and after each operation completes.

**Menu Structure**:
```
=== Todo App ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit
Enter choice:
```

**Menu Requirements**:
- **FR-MENU-001**: Main menu MUST display all 6 options numbered 1-6
- **FR-MENU-002**: User input MUST be validated (choices 1-6 only)
- **FR-MENU-003**: Invalid choices MUST show error "Error: Please enter a number between 1 and 6"
- **FR-MENU-004**: Menu MUST redisplay after each operation completes
- **FR-MENU-005**: Option 6 (Exit) MUST terminate application with exit code 0
- **FR-MENU-006**: Menu text MUST be clear and consistent across all displays

## Data Model Requirements

**Task Entity**:
- **Attributes**:
  - `id` (integer): Unique identifier, assigned sequentially
  - `description` (string): Task text, 1-200 characters after trimming
  - `status` (string): Either "Complete" or "Incomplete"
- **Invariants**:
  - Task ID is immutable after creation
  - Task ID is unique within session
  - Status can only be "Complete" or "Incomplete"
  - Description cannot be empty after trimming

**Task List**:
- In-memory storage (Python list or dictionary)
- Persists only during application runtime
- Lost when application exits

## Input/Output Requirements

**Input Handling**:
- **FR-IO-001**: All user input captured via `input()` function
- **FR-IO-002**: Input prompts MUST be clear and specific
- **FR-IO-003**: Input validation MUST occur before processing
- **FR-IO-004**: Invalid input MUST NOT crash application

**Output Handling**:
- **FR-IO-005**: Normal messages displayed via `print()` to stdout
- **FR-IO-006**: Error messages displayed via `print(..., file=sys.stderr)` to stderr
- **FR-IO-007**: Success confirmations MUST be displayed after state changes
- **FR-IO-008**: Output MUST be human-readable (no JSON, XML, or technical dumps)

## Error Handling Principles

**Global Error Standards**:
- **FR-ERR-001**: Application MUST NEVER crash on user input
- **FR-ERR-002**: All errors MUST display user-friendly messages
- **FR-ERR-003**: Error messages MUST explain what went wrong
- **FR-ERR-004**: Error messages MUST be written to stderr
- **FR-ERR-005**: After error, application MUST return to main menu
- **FR-ERR-006**: No stack traces, exception names, or technical jargon in user-facing errors

---

# Global Success Criteria

## Functional Completeness

- **SC-FUNC-001**: All 5 Phase I features work correctly (Add, View, Update, Delete, Mark)
- **SC-FUNC-002**: User can perform complete workflow: add → view → update → mark → delete
- **SC-FUNC-003**: Application runs from command line: `python src/main.py`
- **SC-FUNC-004**: Main menu displays and accepts user choices correctly
- **SC-FUNC-005**: Application exits cleanly when user selects Exit

## Performance & Usability

- **SC-PERF-001**: Each operation completes in under 1 second for lists up to 100 tasks
- **SC-PERF-002**: User can add a task in under 10 seconds from menu to confirmation
- **SC-PERF-003**: Viewing tasks displays all items immediately (< 1 second for 100 tasks)
- **SC-PERF-004**: Application supports at least 100 tasks without degradation

## Quality & Reliability

- **SC-QUAL-001**: Zero crashes during normal operation (all valid and invalid inputs handled)
- **SC-QUAL-002**: 100% of empty description submissions are rejected with clear error
- **SC-QUAL-003**: 100% of invalid task IDs are rejected with clear error
- **SC-QUAL-004**: All success operations display confirmation messages
- **SC-QUAL-005**: All tasks added appear in View Tasks display

## Phase I Compliance

- **SC-COMP-001**: No persistence (data lost on exit - verified)
- **SC-COMP-002**: No database, web, GUI, or AI features present
- **SC-COMP-003**: All code generated via Claude Code (no manual edits)
- **SC-COMP-004**: Python 3.13+ standard library only (no external dependencies)
- **SC-COMP-005**: Console-only interface (text-based interaction)

---

## Assumptions

1. **Single User**: Application serves one user at a time (no concurrent access)
2. **Session Scope**: Data lifetime is one application execution (start to exit)
3. **Sequential IDs**: Task IDs assigned as 1, 2, 3, ... in order of creation
4. **ID Persistence**: Task IDs do not change after creation, even after deletions
5. **String Status**: Status values are strings "Complete" and "Incomplete" (not booleans or enums)
6. **UTF-8 Support**: Descriptions support UTF-8 characters (emojis, international characters)
7. **No Confirmation Dialogs**: Operations execute immediately (no "Are you sure?" prompts)
8. **Input Method**: User input is keyboard-based (no voice, touch, or alternative input)
9. **Display Capacity**: Terminal can display at least 50 lines (for viewing many tasks)
10. **Whitespace Handling**: Leading/trailing whitespace automatically trimmed from descriptions

---

## Scope Boundaries

### Explicitly In-Scope (Phase I)

- Adding, viewing, updating, deleting, and marking tasks
- Menu-driven console interface
- In-memory task storage
- Input validation and error handling
- Task ID assignment and management

### Explicitly Out-of-Scope (Phase I)

Per constitution, these features are PROHIBITED:

- Persistence (files, databases, cloud storage)
- Web or GUI interfaces
- User authentication or multi-user support
- Task priorities, due dates, or timestamps
- Categories, tags, or task organization
- Search, filter, or sort capabilities
- Undo/redo functionality
- Import/export features
- Notifications or reminders
- AI features or natural language processing
- Configuration files or settings
- Logging beyond stderr error messages

---

## Dependencies

**Prerequisites for Implementation**:
1. Python 3.13+ installed
2. Terminal/console environment
3. No external libraries (standard library only)

**Feature Dependencies**:
- View Tasks depends on Add Task (need tasks to view)
- Update, Delete, Mark depend on Add Task and View Tasks (need tasks and IDs)
- All features depend on Main Menu system

**Development Dependencies**:
1. Constitution created (defines rules)
2. This specification validated (quality gates passed)
3. Implementation plan created (`/sp.plan`)
4. Task breakdown created (`/sp.tasks`)

---

**Specification Status**: Ready for Validation
**Next Steps**:
1. Run quality validation checklist
2. Create plan.md with `/sp.plan`
3. Create tasks.md with `/sp.tasks`
4. Begin implementation with `/sp.implement`
