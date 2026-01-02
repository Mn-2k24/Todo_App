# Quickstart Guide: Phase I Todo App

**Branch**: `002-phase-i-spec` | **Date**: 2025-12-31 | **Plan**: [plan.md](plan.md)

## Overview

Phase I Todo App is a simple, in-memory console application for managing todo tasks. This guide walks you through installation, usage, and common scenarios.

---

## Prerequisites

- **Python**: Version 3.13 or higher
- **Operating System**: Linux, macOS, or Windows
- **Terminal**: Any terminal or command prompt

**Check Python Version**:
```bash
python --version
# or
python3 --version
```

Expected output: `Python 3.13.x` or higher

---

## Installation

No installation required! Phase I is a standalone Python application with no external dependencies.

**Steps**:
1. Ensure you have Python 3.13+ installed
2. Navigate to the project root directory
3. Run the application (see Usage section)

---

## Usage

### Starting the Application

From the project root directory:

```bash
python src/main.py
```

or (if `python` points to Python 2.x):

```bash
python3 src/main.py
```

### Main Menu

Upon launch, you'll see the main menu:

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

Enter a number (1-6) to select an option.

---

## Features

### 1. Add Task

**Purpose**: Create a new todo task with a description.

**Steps**:
1. Select `1` from the main menu
2. Enter task description when prompted
3. Press Enter

**Example**:
```
Enter choice: 1
Enter task description: Buy groceries
Task added successfully.
```

**Notes**:
- Task gets a unique ID (1, 2, 3, ...)
- New tasks start with status "Incomplete"
- Empty descriptions are rejected

---

### 2. View Tasks

**Purpose**: Display all tasks in the list.

**Steps**:
1. Select `2` from the main menu
2. View displayed tasks

**Example (with tasks)**:
```
Enter choice: 2

Tasks:
1. [Incomplete] Buy groceries
2. [Incomplete] Finish homework
3. [Complete] Call dentist
```

**Example (empty list)**:
```
Enter choice: 2

No tasks found.
```

**Notes**:
- Tasks shown in ID order
- Status displayed as [Complete] or [Incomplete]
- Full description shown (no truncation)

---

### 3. Update Task

**Purpose**: Change the description of an existing task.

**Steps**:
1. Select `3` from the main menu
2. Enter the task ID to update
3. Review current description (displayed)
4. Enter new description
5. Press Enter

**Example**:
```
Enter choice: 3
Enter task ID to update: 1
Current: Buy groceries
Enter new description: Buy groceries and milk
Task updated successfully.
```

**Notes**:
- Task ID and status remain unchanged
- Only description is updated
- Empty descriptions are rejected

---

### 4. Delete Task

**Purpose**: Remove a task from the list permanently.

**Steps**:
1. Select `4` from the main menu
2. Enter the task ID to delete
3. Press Enter

**Example**:
```
Enter choice: 4
Enter task ID to delete: 2
Task deleted successfully.
```

**Notes**:
- Deletion is permanent (no undo)
- Deleted task IDs are not reused
- If you delete task 2, next tasks remain 1, 3, 4, ... (gap in IDs)

---

### 5. Mark Task Complete/Incomplete

**Purpose**: Toggle task completion status.

**Steps**:
1. Select `5` from the main menu
2. Enter the task ID to mark
3. Review current status (displayed)
4. Status toggles automatically

**Example (mark as complete)**:
```
Enter choice: 5
Enter task ID: 1
Current status: Incomplete
Task marked as Complete.
```

**Example (mark as incomplete)**:
```
Enter choice: 5
Enter task ID: 1
Current status: Complete
Task marked as Incomplete.
```

**Notes**:
- Status toggles between "Complete" and "Incomplete"
- Can toggle infinitely (no limit)
- Task ID and description remain unchanged

---

### 6. Exit

**Purpose**: Quit the application.

**Steps**:
1. Select `6` from the main menu
2. Application terminates

**Example**:
```
Enter choice: 6
Goodbye!
```

**Notes**:
- All tasks are lost when you exit (in-memory only)
- No data is saved to disk

---

## Error Handling

### Invalid Menu Choice

**Input**: Non-numeric or out-of-range choice

**Example**:
```
Enter choice: abc
Error: Please enter a number between 1 and 6.
```

**Action**: Menu redisplays, try again

---

### Invalid Task ID (Non-Integer)

**Input**: Non-numeric task ID

**Example**:
```
Enter task ID to update: xyz
Error: Task ID must be a number.
```

**Action**: Returns to main menu

---

### Task Not Found

**Input**: Task ID that doesn't exist

**Example**:
```
Enter task ID to delete: 99
Error: Task ID 99 not found. No task deleted.
```

**Action**: Returns to main menu, no changes made

---

### Empty Task Description

**Input**: Empty or whitespace-only description

**Example**:
```
Enter task description:
Error: Task description cannot be empty. Please enter a description.
```

**Action**: Returns to main menu, no task created

---

## Common Scenarios

### Scenario 1: Create a Shopping List

```
1. Add Task → "Buy milk"
2. Add Task → "Buy eggs"
3. Add Task → "Buy bread"
4. View Tasks → See all 3 items
5. Mark Task Complete/Incomplete → Mark "Buy milk" as Complete (ID 1)
6. View Tasks → See milk marked as [Complete]
```

---

### Scenario 2: Track Project Tasks

```
1. Add Task → "Write introduction"
2. Add Task → "Conduct research"
3. Add Task → "Write conclusion"
4. Update Task → Change task 2 to "Conduct background research"
5. Mark Task Complete/Incomplete → Mark task 1 as Complete
6. View Tasks → See updated list
```

---

### Scenario 3: Clean Up Completed Tasks

```
1. View Tasks → Identify completed tasks (e.g., IDs 2, 5)
2. Delete Task → Delete task 2
3. Delete Task → Delete task 5
4. View Tasks → Only incomplete tasks remain
```

---

## Limitations & Constraints

### Phase I Constraints

- ✅ **In-Memory Only**: Tasks are lost when you exit the app (no persistence)
- ✅ **Console-Only**: Text-based interface (no GUI or web interface)
- ✅ **Single Session**: No multi-user support, no networking
- ✅ **No Advanced Features**: No priorities, due dates, tags, categories, search, or filtering

### Performance

- Supports up to 100 tasks comfortably
- All operations complete in < 1 second

---

## Troubleshooting

### Problem: "python: command not found"

**Solution**: Try `python3` instead of `python`, or install Python 3.13+

---

### Problem: "ImportError: No module named dataclasses"

**Solution**: Upgrade to Python 3.13+ (dataclasses are standard library in Python 3.7+)

---

### Problem: Application crashes on input

**Solution**: Ensure you're running Python 3.13+ (not Python 2.x). Check version with `python --version`

---

### Problem: Tasks disappear after closing app

**Expected Behavior**: Phase I is in-memory only. Tasks are intentionally not saved. This is by design for Phase I.

---

## Next Steps

After using the Phase I app:

1. **Provide Feedback**: Report bugs or usability issues
2. **Test Edge Cases**: Try unusual inputs to verify error handling
3. **Prepare for Phase II**: Future phases will add persistence, search, and advanced features

---

## Support

For issues or questions:

1. Check error messages displayed by the app
2. Review this Quickstart Guide
3. Consult the full specification: [spec.md](spec.md)
4. Review the implementation plan: [plan.md](plan.md)

---

## Status

✅ **Quickstart guide complete**

This guide covers all Phase I features with examples, error scenarios, and troubleshooting steps.
