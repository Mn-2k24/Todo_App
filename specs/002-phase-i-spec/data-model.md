# Data Model: Phase I Todo App

**Branch**: `002-phase-i-spec` | **Date**: 2025-12-31 | **Plan**: [plan.md](plan.md)

## Purpose

This document defines the complete data model for Phase I, including entity definitions, validation rules, and relationships.

---

## Core Entities

### 1. Task

**Description**: Represents a single todo item with description and completion status.

**Attributes**:

| Attribute | Type | Constraints | Mutability | Default |
|-----------|------|-------------|------------|---------|
| `id` | `int` | Unique, positive integer, sequential (1, 2, 3, ...) | Immutable | Assigned by system |
| `description` | `str` | 1-200 chars after trimming, non-empty | Mutable | None (required) |
| `status` | `str` | Exactly "Complete" or "Incomplete" | Mutable | "Incomplete" |

**Implementation**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    description: str
    status: str  # "Complete" or "Incomplete"
```

**Validation Rules**:
- `id` must be positive integer (> 0)
- `description` must be non-empty after `strip()`
- `description` length must be ≤ 200 characters after trimming
- `status` must be exactly "Complete" or "Incomplete" (case-sensitive)

**Lifecycle**:
1. **Creation**: Task created with auto-assigned ID, user-provided description, status = "Incomplete"
2. **Update**: Description can be modified, ID and status preserved
3. **Mark**: Status toggled between "Complete" and "Incomplete", ID and description preserved
4. **Deletion**: Task removed from storage, ID never reused

---

### 2. TaskList (Global State)

**Description**: Application-wide storage for all tasks and ID counter.

**Attributes**:

| Attribute | Type | Constraints | Scope | Initial Value |
|-----------|------|-------------|-------|---------------|
| `tasks` | `List[Task]` | Ordered list, no duplicates by ID | Global module variable | `[]` (empty list) |
| `next_task_id` | `int` | Always > max(task.id), increments on add | Global module variable | `1` |

**Implementation**:
```python
# In src/services/todo_service.py
tasks: List[Task] = []
next_task_id: int = 1
```

**Invariants**:
- `tasks` list maintains insertion order (chronological by creation)
- Task IDs in `tasks` list are unique
- `next_task_id` is always greater than any existing task ID
- Deleted task IDs leave gaps (e.g., after deleting ID 2: tasks = [1, 3, 4, ...])
- `next_task_id` never decrements (monotonically increasing)

---

## Relationships

**Type**: None (single entity model)

Phase I has only one entity (`Task`) with no relationships. All tasks are independent.

---

## Data Flow

### Add Task
```
User Input (description)
  → Trim whitespace
  → Validate (non-empty)
  → Create Task(id=next_task_id, description, status="Incomplete")
  → Append to tasks list
  → Increment next_task_id
```

### View Tasks
```
tasks list → Return copy or direct reference → Format for display
```

### Update Task
```
User Input (task_id, new_description)
  → Find task by ID
  → Validate new description (non-empty)
  → Update task.description
  → Return success/failure
```

### Delete Task
```
User Input (task_id)
  → Find task by ID
  → Remove from tasks list
  → ID gap preserved (no decrement of next_task_id)
```

### Mark Task
```
User Input (task_id)
  → Find task by ID
  → Toggle status (Incomplete ↔ Complete)
  → Return new status
```

---

## Validation Rules Summary

| Rule ID | Entity | Field | Validation | Error Message |
|---------|--------|-------|------------|---------------|
| VAL-001 | Task | id | Must be positive integer (> 0) | Internal error (not user-facing) |
| VAL-002 | Task | description | Must be non-empty after strip() | "Error: Task description cannot be empty. Please enter a description." |
| VAL-003 | Task | description | Length ≤ 200 chars after trim | "Error: Description too long (max 200 characters)." |
| VAL-004 | Task | status | Must be "Complete" or "Incomplete" | Internal error (not user-facing, status set by system) |
| VAL-005 | Input | task_id | Must be integer | "Error: Task ID must be a number." |
| VAL-006 | Input | task_id | Task with ID must exist | "Error: Task ID {id} not found. Please enter a valid task ID." |

---

## Storage Characteristics

**Type**: In-memory (volatile)
**Data Structure**: Python list (`List[Task]`)
**Persistence**: None (data lost on application exit)
**Concurrency**: Single-threaded (no concurrent access)
**Capacity**: Limited by available RAM (~100 tasks expected, tested up to 1000)

**Access Patterns**:
- **Add**: O(1) - append to list
- **View All**: O(n) - iterate entire list
- **Find by ID**: O(n) - linear search
- **Update**: O(n) - find task + update in place
- **Delete**: O(n) - find task + remove from list
- **Mark**: O(n) - find task + update status

**Performance Budget** (per spec SC-PERF-001):
- All operations must complete in < 1 second for lists up to 100 tasks
- Expected: ~1-10ms per operation on modern hardware

---

## Constraints & Assumptions

**Constraints**:
- ✅ In-memory only (no file I/O, databases, or persistence)
- ✅ Single user, single session
- ✅ No concurrent access (single-threaded)
- ✅ Task IDs never reused (monotonically increasing counter)

**Assumptions**:
- Users will add < 100 tasks per session (O(n) operations acceptable)
- Python 3.13+ available (dataclass support)
- Sufficient RAM for task storage (each task ~100 bytes → 10KB for 100 tasks)

---

## Status

✅ **Data model complete and validated**

All entities defined, validation rules specified, ready for implementation in Phase 1 (Design).
