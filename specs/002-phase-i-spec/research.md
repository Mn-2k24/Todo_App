# Technical Research: Phase I Todo App

**Branch**: `002-phase-i-spec` | **Date**: 2025-12-31 | **Plan**: [plan.md](plan.md)

## Purpose

This document captures all technical decisions made during Phase 0 (Research) of the implementation planning process. Each decision includes the chosen approach, rationale, alternatives considered, and implementation notes.

---

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

---

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

---

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

---

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

---

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

---

## Research Summary

All technical decisions resolved. No external dependencies needed. Implementation uses Python standard library features:
- `dataclasses` for Task model
- `input()` for user input
- `print()` for output, `sys.stderr` for errors
- `match/case` for menu routing (Python 3.10+)
- Simple list for storage, integer counter for IDs

**Total Decisions**: 5 (Data structure, ID assignment, Task model, Menu loop, Error handling)

**Dependencies**: None (Python 3.13+ standard library only)

**Constraints Met**:
- ✅ In-memory only
- ✅ Console/CLI only
- ✅ No external libraries
- ✅ No persistence
- ✅ Phase I scope only

**Status**: ✅ All research complete, ready for design phase
