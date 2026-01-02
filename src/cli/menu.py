"""Menu system for Phase I Todo App.

This module handles the main menu display, user choice validation,
and routing to feature handlers.
"""

import sys
from src.services import todo_service
from src.cli import task_view


def display_menu() -> None:
    """Display the main menu with all available options.

    Prints the menu header and 6 numbered options to stdout.
    """
    print("=== Todo App ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete/Incomplete")
    print("6. Exit")
    print("Enter choice: ", end="")


def get_user_choice() -> int:
    """Get and validate user menu choice.

    Returns:
        int: Valid choice (1-6), or 0 for invalid input

    Validates that input is:
    - An integer
    - In range 1-6
    - Returns 0 if validation fails (triggers menu redisplay)
    """
    choice_str = input()

    try:
        choice = int(choice_str)
    except ValueError:
        print("Error: Please enter a number between 1 and 6.", file=sys.stderr)
        return 0

    if choice < 1 or choice > 6:
        print("Error: Please enter a number between 1 and 6.", file=sys.stderr)
        return 0

    return choice


def add_task_handler() -> None:
    """Handle the Add Task menu option (choice 1).

    Prompts user for task description, calls service to create task,
    displays confirmation or error message.
    """
    print("Enter task description: ", end="")
    description = input()

    # Call service to create task
    task = todo_service.add_task(description)

    if task is None:
        # Error: empty description
        print("Error: Task description cannot be empty. Please enter a description.", file=sys.stderr)
    else:
        # Success
        print("Task added successfully.")


def view_tasks_handler() -> None:
    """Handle the View Tasks menu option (choice 2).

    Retrieves all tasks from service and displays them in formatted list.
    """
    tasks = todo_service.get_all_tasks()
    task_view.display_tasks(tasks)


def update_task_handler() -> None:
    """Handle the Update Task menu option (choice 3).

    Prompts for task ID, validates, displays current description,
    prompts for new description, calls service to update.
    """
    print("Enter task ID to update: ", end="")
    task_id_str = input()

    # Validate task ID is integer
    try:
        task_id = int(task_id_str)
    except ValueError:
        print("Error: Task ID must be a number.", file=sys.stderr)
        return

    # Check task exists
    task = todo_service.get_task_by_id(task_id)
    if task is None:
        print(f"Error: Task ID {task_id} not found. Please enter a valid task ID.", file=sys.stderr)
        return

    # Show current description
    print(f"Current: {task.description}")

    # Prompt for new description
    print("Enter new description: ", end="")
    new_description = input()

    # Call service to update
    success = todo_service.update_task(task_id, new_description)

    if success:
        print("Task updated successfully.")
    else:
        print("Error: Task description cannot be empty. Task not updated.", file=sys.stderr)


def delete_task_handler() -> None:
    """Handle the Delete Task menu option (choice 4).

    Prompts for task ID, validates, calls service to delete.
    """
    print("Enter task ID to delete: ", end="")
    task_id_str = input()

    # Validate task ID is integer
    try:
        task_id = int(task_id_str)
    except ValueError:
        print("Error: Task ID must be a number.", file=sys.stderr)
        return

    # Call service to delete
    success = todo_service.delete_task(task_id)

    if success:
        print("Task deleted successfully.")
    else:
        print(f"Error: Task ID {task_id} not found. No task deleted.", file=sys.stderr)


def mark_task_handler() -> None:
    """Handle the Mark Task Complete/Incomplete menu option (choice 5).

    Prompts for task ID, validates, shows current status, toggles status.
    """
    print("Enter task ID: ", end="")
    task_id_str = input()

    # Validate task ID is integer
    try:
        task_id = int(task_id_str)
    except ValueError:
        print("Error: Task ID must be a number.", file=sys.stderr)
        return

    # Get task to show current status
    task = todo_service.get_task_by_id(task_id)
    if task is None:
        print(f"Error: Task ID {task_id} not found. Status not changed.", file=sys.stderr)
        return

    # Show current status
    print(f"Current status: {task.status}")

    # Toggle status
    new_status = todo_service.mark_task(task_id)

    if new_status:
        print(f"Task marked as {new_status}.")
    else:
        print("Error: Unable to update task status.", file=sys.stderr)


def main_loop() -> None:
    """Main application loop.

    Displays menu, gets user choice, routes to handlers, repeats until exit.
    Implements infinite loop with match/case routing for all 6 menu options.
    """
    while True:
        display_menu()
        choice = get_user_choice()

        if choice == 0:
            # Invalid input, menu will redisplay
            continue

        match choice:
            case 1:
                add_task_handler()
            case 2:
                view_tasks_handler()
            case 3:
                update_task_handler()
            case 4:
                delete_task_handler()
            case 5:
                mark_task_handler()
            case 6:
                # Exit
                print("Goodbye!")
                break

        # Print newline for spacing between operations
        print()
