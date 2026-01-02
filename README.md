# Todo App - Phase I

A minimal, functional, console-based Todo application in Python operating entirely in memory.

## Overview

Phase I delivers core CRUD operations for managing todo tasks through a text-based terminal interface:
- ✅ Add tasks with descriptions
- ✅ View all tasks with status
- ✅ Update task descriptions
- ✅ Delete tasks
- ✅ Mark tasks complete/incomplete

**Key Constraints:**
- In-memory only (no persistence)
- Console-only interface
- Python 3.13+ standard library
- No external dependencies

## Prerequisites

- Python 3.13 or higher
- UV package manager (recommended) or pip

## Installation

### Using UV (Recommended)

```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/Mn-2k24/Todo_App.git
cd Todo_App

# No dependencies to install for Phase I (standard library only)
```

### Using Python directly

```bash
# Clone the repository
git clone https://github.com/Mn-2k24/Todo_App.git
cd Todo_App

# Verify Python version
python --version  # Should be 3.13+
```

## Running the Application

```bash
python src/main.py
```

## Usage

The application presents a menu-driven interface:

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

### Example Session

```
1. Add a task:
   Choice: 1
   Enter task description: Buy groceries
   → Task added successfully

2. View tasks:
   Choice: 2
   → Tasks:
     1. [Incomplete] Buy groceries

3. Mark complete:
   Choice: 5
   Enter task ID: 1
   → Task marked complete

4. View tasks:
   Choice: 2
   → Tasks:
     1. [Complete] Buy groceries
```

## Project Structure

```
src/
├── main.py              # Application entry point
├── models/
│   └── task.py         # Task data model
├── services/
│   └── todo_service.py # Business logic
└── cli/
    ├── menu.py         # Menu interface
    └── task_view.py    # Task display
```

## Development Approach

This project follows **Spec-Driven Development (SDD)** principles:
- All code generated via Claude Code
- No manual source code edits
- Specification-first workflow
- See `CLAUDE.md` for details

## Documentation

- `constitution.md` - Phase I project principles and constraints
- `specs/002-phase-i-spec/spec.md` - Complete feature specifications
- `specs/002-phase-i-spec/plan.md` - Implementation plan
- `CLAUDE.md` - SDD workflow and Claude Code usage

## Phase I Scope

**In Scope:**
- Five core CRUD features (listed above)
- Console menu interface
- In-memory storage
- Input validation and error handling

**Out of Scope (Future Phases):**
- Persistence (database, file storage)
- Web or GUI interfaces
- Advanced features (priorities, search, due dates, tags)
- Multi-user support

## License

MIT License - See LICENSE file

## Contact

GitHub: [@Mn-2k24](https://github.com/Mn-2k24)
