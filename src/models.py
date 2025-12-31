from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """Represents a single task in the Todo application."""
    id: str  # Format: "001", "002", etc.
    title: str
    description: str
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Perform validation and normalization after initialization."""
        self.title = self.title.strip()
        self.description = self.description.strip()

        if len(self.title) < 3 or len(self.title) > 100:
            raise ValueError("Title must be between 3 and 100 characters.")

        if len(self.description) < 5 or len(self.description) > 500:
            raise ValueError("Description must be between 5 and 500 characters.")

    def update(self, title: Optional[str] = None, description: Optional[str] = None):
        """Update task details and refresh the updated_at timestamp."""
        if title is not None:
            self.title = title.strip()
            if len(self.title) < 3 or len(self.title) > 100:
                raise ValueError("Title must be between 3 and 100 characters.")

        if description is not None:
            self.description = description.strip()
            if len(self.description) < 5 or len(self.description) > 500:
                raise ValueError("Description must be between 5 and 500 characters.")

        self.updated_at = datetime.now()

    def toggle_status(self):
        """Toggle the completion status of the task."""
        self.completed = not self.completed
        self.updated_at = datetime.now()
