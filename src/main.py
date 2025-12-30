import sys
from src.services import TodoService
from src.utils import (
    clear_screen,
    print_success,
    print_error,
    validate_title,
    validate_description,
    format_task_table,
    get_confirmation
)

def print_menu():
    """Display the main menu."""
    print("=== TODO APPLICATION PHASE I ===")
    print("1. Add Task")
    print("2. List All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete/Incomplete")
    print("6. Exit")
    print("================================")

def handle_add_task(service: TodoService):
    """Handle the add task UI flow."""
    print("\n--- Add New Task ---")

    while True:
        title = input("Enter Title (3-100 chars): ").strip()
        if validate_title(title):
            break
        print_error("Invalid title length.")

    while True:
        description = input("Enter Description (5-500 chars): ").strip()
        if validate_description(description):
            break
        print_error("Invalid description length.")

    try:
        task = service.add_task(title, description)
        print_success(f"Task added successfully! ID: {str(task.id)[:8]}")
    except ValueError as e:
        print_error(f"Error: {e}")

def handle_list_tasks(service: TodoService):
    """Handle the list tasks UI flow."""
    tasks = service.get_all_tasks()
    stats = service.get_stats()
    format_task_table(tasks, stats)
    input("\nPress Enter to return to menu...")

def handle_update_task(service: TodoService):
    """Handle the update task UI flow."""
    id_prefix = input("Enter Task ID (first 8 chars): ").strip()
    task = service.find_task_by_prefix(id_prefix)

    if not task:
        print_error(f"Task with ID prefix '{id_prefix}' not found.")
        return

    print(f"Updating Task: {task.title}")
    title = input("Enter new Title (leave blank to keep current): ").strip()
    description = input("Enter new Description (leave blank to keep current): ").strip()

    try:
        service.update_task(
            id_prefix,
            title=title if title else None,
            description=description if description else None
        )
        print_success("Task updated successfully!")
    except ValueError as e:
        print_error(f"Error: {e}")

def handle_delete_task(service: TodoService):
    """Handle the delete task UI flow."""
    id_prefix = input("Enter Task ID (first 8 chars) to delete: ").strip()
    task = service.find_task_by_prefix(id_prefix)

    if not task:
        print_error(f"Task with ID prefix '{id_prefix}' not found.")
        return

    if get_confirmation(f"Are you sure you want to delete task '{task.title}'?"):
        if service.delete_task(id_prefix):
            print_success("Task deleted successfully!")
        else:
            print_error("Failed to delete task.")

def handle_toggle_complete(service: TodoService):
    """Handle the toggle completion UI flow."""
    id_prefix = input("Enter Task ID (first 8 chars) to toggle status: ").strip()
    task = service.toggle_task_status(id_prefix)

    if task:
        status = "Completed" if task.completed else "Incomplete"
        print_success(f"Task status updated to: {status}")
    else:
        print_error(f"Task with ID prefix '{id_prefix}' not found.")

def main():
    """Main application loop."""
    service = TodoService()

    while True:
        clear_screen()
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            handle_add_task(service)
            input("\nPress Enter to continue...")
        elif choice == "2":
            handle_list_tasks(service)
        elif choice == "3":
            handle_update_task(service)
            input("\nPress Enter to continue...")
        elif choice == "4":
            handle_delete_task(service)
            input("\nPress Enter to continue...")
        elif choice == "5":
            handle_toggle_complete(service)
            input("\nPress Enter to continue...")
        elif choice == "6":
            print_success("Goodbye!")
            sys.exit(0)
        else:
            print_error("Invalid choice. Please enter a number between 1 and 6.")
            input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    main()
