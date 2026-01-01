"""Tests for Todo schemas."""
from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from backend.schemas.todo import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse


class TestTodoCreate:
    """Tests for TodoCreate schema."""

    def test_valid_todo_create(self):
        """Test creating TodoCreate with valid data."""
        data = TodoCreate(
            title="Buy Milk",
            description="Whole milk, 2 liters from the store",
        )

        assert data.title == "Buy Milk"
        assert data.description == "Whole milk, 2 liters from the store"

    def test_todo_create_title_too_short(self):
        """Test TodoCreate with title < 3 chars raises error."""
        with pytest.raises(ValidationError):
            TodoCreate(
                title="AB",
                description="Valid description",
            )

    def test_todo_create_title_too_long(self):
        """Test TodoCreate with title > 100 chars raises error."""
        with pytest.raises(ValidationError):
            TodoCreate(
                title="A" * 101,
                description="Valid description",
            )

    def test_todo_create_description_too_short(self):
        """Test TodoCreate with description < 5 chars raises error."""
        with pytest.raises(ValidationError):
            TodoCreate(
                title="Valid Title",
                description="ABC",
            )

    def test_todo_create_description_too_long(self):
        """Test TodoCreate with description > 500 chars raises error."""
        with pytest.raises(ValidationError):
            TodoCreate(
                title="Valid Title",
                description="A" * 501,
            )

    def test_todo_create_empty_title(self):
        """Test TodoCreate with empty title raises error."""
        with pytest.raises(ValidationError):
            TodoCreate(
                title="",
                description="Valid description",
            )


class TestTodoUpdate:
    """Tests for TodoUpdate schema."""

    def test_todo_update_partial(self):
        """Test TodoUpdate with partial data."""
        data = TodoUpdate(title="Updated Title")

        assert data.title == "Updated Title"
        assert data.description is None
        assert data.completed is None

    def test_todo_update_all_fields(self):
        """Test TodoUpdate with all fields."""
        data = TodoUpdate(
            title="Updated Title",
            description="Updated description",
            completed=True,
        )

        assert data.title == "Updated Title"
        assert data.description == "Updated description"
        assert data.completed is True

    def test_todo_update_empty(self):
        """Test TodoUpdate with no data."""
        data = TodoUpdate()

        assert data.title is None
        assert data.description is None
        assert data.completed is None


class TestTodoResponse:
    """Tests for TodoResponse schema."""

    def test_todo_response_creation(self):
        """Test creating TodoResponse."""
        now = datetime.utcnow()
        data = TodoResponse(
            id=str(uuid4()),
            title="Buy Milk",
            description="Whole milk",
            completed=False,
            created_at=now,
            updated_at=now,
        )

        assert data.title == "Buy Milk"
        assert data.completed is False

    def test_todo_response_from_attributes(self):
        """Test TodoResponse with from_attributes."""
        from backend.models.todo import Todo

        todo = Todo(
            id=str(uuid4()),
            title="Test Todo",
            description="Test description",
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        data = TodoResponse.model_validate(todo)

        assert data.title == todo.title
        assert data.description == todo.description


class TestTodoListResponse:
    """Tests for TodoListResponse schema."""

    def test_todo_list_response_empty(self):
        """Test TodoListResponse with empty list."""
        data = TodoListResponse(
            todos=[],
            total=0,
            completed=0,
            pending=0,
        )

        assert data.todos == []
        assert data.total == 0
        assert data.completed == 0
        assert data.pending == 0

    def test_todo_list_response_with_data(self):
        """Test TodoListResponse with todos."""
        now = datetime.utcnow()
        todo = TodoResponse(
            id=str(uuid4()),
            title="Test Todo",
            description="Test description",
            completed=False,
            created_at=now,
            updated_at=now,
        )

        data = TodoListResponse(
            todos=[todo],
            total=1,
            completed=0,
            pending=1,
        )

        assert len(data.todos) == 1
        assert data.total == 1
        assert data.pending == 1
