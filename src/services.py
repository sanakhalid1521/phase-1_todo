from typing import List, Optional
from src.models import Task

class TodoService:
    """Service layer for managing tasks in-memory."""

    def __init__(self):
        self._tasks: List[Task] = []
        self._counter = 0

    def add_task(self, title: str, description: str) -> Task:
        """Create and add a new task with sequential ID."""
        self._counter += 1
        new_id = f"{self._counter:03}"  # Generates "001", "002"...
        task = Task(id=new_id, title=title, description=description)
        self._tasks.append(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks."""
        return self._tasks

    def find_task_by_prefix(self, id_prefix: str) -> Optional[Task]:
        """Find a task by the first few characters of its ID."""
        matches = [t for t in self._tasks if str(t.id).startswith(id_prefix)]
        if len(matches) == 1:
            return matches[0]
        return None

    def update_task(self, id_prefix: str, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """Update an existing task if found."""
        task = self.find_task_by_prefix(id_prefix)
        if task:
            task.update(title=title, description=description)
            return task
        return None

    def delete_task(self, id_prefix: str) -> bool:
        """Delete a task by ID prefix."""
        task = self.find_task_by_prefix(id_prefix)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def toggle_task_status(self, id_prefix: str) -> Optional[Task]:
        """Toggle the completion status of a task."""
        task = self.find_task_by_prefix(id_prefix)
        if task:
            task.toggle_status()
            return task
        return None

    def get_stats(self):
        """Get summary statistics for all tasks."""
        total = len(self._tasks)
        completed = len([t for t in self._tasks if t.completed])
        pending = total - completed
        return {
            "total": total,
            "completed": completed,
            "pending": pending
        }
