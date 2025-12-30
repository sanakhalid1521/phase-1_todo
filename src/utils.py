import os
import platform
import sys
from typing import List
from src.models import Task

def clear_screen():
    """Clear the terminal screen based on the OS."""
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")

def print_success(message: str):
    """Print success message in green."""
    print(f"\033[92m{message}\033[0m")

def print_error(message: str):
    """Print error message in red."""
    print(f"\033[91m{message}\033[0m")

def validate_title(title: str) -> bool:
    """Check if title length is within boundaries."""
    return 3 <= len(title.strip()) <= 100

def validate_description(description: str) -> bool:
    """Check if description length is within boundaries."""
    return 5 <= len(description.strip()) <= 500

def get_confirmation(prompt: str) -> bool:
    """Ask user for y/n confirmation."""
    while True:
        choice = input(f"{prompt} (y/n): ").strip().lower()
        if choice in ('y', 'yes'):
            return True
        if choice in ('n', 'no'):
            return False
        print_error("Please enter 'y' or 'n'.")

def format_task_table(tasks: List[Task], stats: dict):
    """Render a formatted ASCII table of tasks."""
    if not tasks:
        print("\nNo tasks found. Get started by adding your first task!")
        return

    # ID Title Status Created
    header = f"{'ID':<10} | {'Title':<40} | {'Status':<10} | {'Created':<20}"
    separator = "-" * len(header)

    print(f"\n{separator}")
    print(header)
    print(separator)

    for task in tasks:
        # Use simple ASCII for status if Unicode is not supported
        try:
            status_icon = "✓" if task.completed else "○"
            f"{status_icon}".encode(sys.stdout.encoding)
        except (UnicodeEncodeError, AttributeError):
            status_icon = "[x]" if task.completed else "[ ]"

        created_str = task.created_at.strftime("%Y-%m-%d %H:%M")
        short_id = str(task.id)[:8]

        # Truncate title for display if needed
        title_display = task.title if len(task.title) <= 37 else task.title[:37] + "..."

        print(f"{short_id:<10} | {title_display:<40} | {status_icon:<10} | {created_str:<20}")

    print(separator)
    print(f"SUMMARY: Total: {stats['total']} | Completed: {stats['completed']} | Pending: {stats['pending']}")
    print(f"{separator}\n")
