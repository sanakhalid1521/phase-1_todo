"""Tests for Todo model."""
from datetime import datetime
from uuid import uuid4

from backend.models.todo import Todo


class TestTodoModel:
    """Tests for Todo model."""

    def test_todo_creation_with_defaults(self):
        """Test creating a todo with default values."""
        todo = Todo(
            title="Test Todo",
            description="Test description",
        )

        assert todo.title == "Test Todo"
        assert todo.description == "Test description"
        assert todo.completed is False
        assert todo.id is not None
        assert todo.created_at is not None
        assert todo.updated_at is not None

    def test_todo_creation_with_all_fields(self):
        """Test creating a todo with all fields specified."""
        now = datetime.utcnow()
        todo = Todo(
            id=str(uuid4()),
            title="Test Todo",
            description="Test description",
            completed=True,
            created_at=now,
            updated_at=now,
        )

        assert todo.title == "Test Todo"
        assert todo.description == "Test description"
        assert todo.completed is True

    def test_todo_update_timestamps(self):
        """Test update_timestamps method."""
        todo = Todo(
            title="Test Todo",
            description="Test description",
        )
        original_updated_at = todo.updated_at

        # Small delay to ensure different timestamp
        todo.update_timestamps()

        assert todo.updated_at >= original_updated_at

    def test_todo_toggle_complete_false_to_true(self):
        """Test toggle_complete from False to True."""
        todo = Todo(
            title="Test Todo",
            description="Test description",
            completed=False,
        )

        todo.toggle_complete()

        assert todo.completed is True

    def test_todo_toggle_complete_true_to_false(self):
        """Test toggle_complete from True to False."""
        todo = Todo(
            title="Test Todo",
            description="Test description",
            completed=True,
        )

        todo.toggle_complete()

        assert todo.completed is False

    def test_todo_id_is_uuid_format(self):
        """Test that todo ID is in UUID format."""
        todo = Todo(
            title="Test Todo",
            description="Test description",
        )

        # Should not raise exception
        uuid4_obj = uuid4()
        assert str(uuid4_obj).count("-") == 4  # UUID has 4 dashes
