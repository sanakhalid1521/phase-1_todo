"""Tests for Todo API endpoints."""
from fastapi.testclient import TestClient


class TestCreateTodo:
    """Tests for POST /todos endpoint."""

    def test_create_todo_success(self, client: TestClient, sample_todo_data: dict):
        """Test creating a todo successfully returns 201."""
        response = client.post("/todos", json=sample_todo_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_todo_data["title"]
        assert data["description"] == sample_todo_data["description"]
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_todo_empty_title(self, client: TestClient):
        """Test creating todo with empty title returns 422."""
        response = client.post("/todos", json={"title": "", "description": "Valid description"})

        assert response.status_code == 422

    def test_create_todo_title_too_short(self, client: TestClient):
        """Test creating todo with title < 3 chars returns 422."""
        response = client.post("/todos", json={"title": "AB", "description": "Valid description"})

        assert response.status_code == 422

    def test_create_todo_title_too_long(self, client: TestClient):
        """Test creating todo with title > 100 chars returns 422."""
        response = client.post("/todos", json={"title": "A" * 101, "description": "Valid description"})

        assert response.status_code == 422

    def test_create_todo_empty_description(self, client: TestClient):
        """Test creating todo with empty description returns 422."""
        response = client.post("/todos", json={"title": "Valid Title", "description": ""})

        assert response.status_code == 422

    def test_create_todo_description_too_short(self, client: TestClient):
        """Test creating todo with description < 5 chars returns 422."""
        response = client.post("/todos", json={"title": "Valid Title", "description": "ABC"})

        assert response.status_code == 422

    def test_create_todo_description_too_long(self, client: TestClient):
        """Test creating todo with description > 500 chars returns 422."""
        response = client.post("/todos", json={"title": "Valid Title", "description": "A" * 501})

        assert response.status_code == 422


class TestGetTodos:
    """Tests for GET /todos endpoint."""

    def test_get_empty_todos(self, client: TestClient):
        """Test getting todos when none exist returns empty list."""
        response = client.get("/todos")

        assert response.status_code == 200
        data = response.json()
        assert data["todos"] == []
        assert data["total"] == 0
        assert data["completed"] == 0
        assert data["pending"] == 0

    def test_get_todos_with_data(self, client: TestClient, sample_todo_data: dict):
        """Test getting todos returns created todos."""
        # Create a todo first
        client.post("/todos", json=sample_todo_data)

        response = client.get("/todos")

        assert response.status_code == 200
        data = response.json()
        assert len(data["todos"]) == 1
        assert data["total"] == 1
        assert data["pending"] == 1
        assert data["completed"] == 0

    def test_get_todos_filter_completed(self, client: TestClient, sample_todo_data: dict):
        """Test filtering todos by completed status."""
        # Create a todo
        client.post("/todos", json=sample_todo_data)

        response = client.get("/todos?completed=true")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0

    def test_get_todos_filter_pending(self, client: TestClient, sample_todo_data: dict):
        """Test filtering todos by pending status."""
        # Create a todo
        client.post("/todos", json=sample_todo_data)

        response = client.get("/todos?completed=false")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1


class TestGetSingleTodo:
    """Tests for GET /todos/{id} endpoint."""

    def test_get_single_todo_success(self, client: TestClient, sample_todo_data: dict):
        """Test getting a single todo by ID."""
        # Create a todo first
        create_resp = client.post("/todos", json=sample_todo_data)
        todo_id = create_resp.json()["id"]

        response = client.get(f"/todos/{todo_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == sample_todo_data["title"]

    def test_get_single_todo_not_found(self, client: TestClient):
        """Test getting non-existent todo returns 404."""
        response = client.get("/todos/non-existent-id")

        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"


class TestUpdateTodo:
    """Tests for PUT /todos/{id} endpoint."""

    def test_update_todo_success(self, client: TestClient, sample_todo_data: dict):
        """Test updating a todo successfully."""
        # Create a todo first
        create_resp = client.post("/todos", json=sample_todo_data)
        todo_id = create_resp.json()["id"]

        update_data = {"title": "Updated Title", "description": "Updated description"}
        response = client.put(f"/todos/{todo_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated description"

    def test_update_todo_partial(self, client: TestClient, sample_todo_data: dict):
        """Test partial update of a todo."""
        # Create a todo first
        create_resp = client.post("/todos", json=sample_todo_data)
        todo_id = create_resp.json()["id"]

        update_data = {"title": "Only Title Updated"}
        response = client.put(f"/todos/{todo_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Only Title Updated"
        # Description should remain unchanged
        assert data["description"] == sample_todo_data["description"]

    def test_update_todo_not_found(self, client: TestClient):
        """Test updating non-existent todo returns 404."""
        response = client.put("/todos/non-existent-id", json={"title": "New Title"})

        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_update_todo_invalid_title(self, client: TestClient, sample_todo_data: dict):
        """Test updating with invalid title returns 422."""
        # Create a todo first
        create_resp = client.post("/todos", json=sample_todo_data)
        todo_id = create_resp.json()["id"]

        response = client.put(f"/todos/{todo_id}", json={"title": "AB"})

        assert response.status_code == 422


class TestDeleteTodo:
    """Tests for DELETE /todos/{id} endpoint."""

    def test_delete_todo_success(self, client: TestClient, sample_todo_data: dict):
        """Test deleting a todo successfully returns 204."""
        # Create a todo first
        create_resp = client.post("/todos", json=sample_todo_data)
        todo_id = create_resp.json()["id"]

        response = client.delete(f"/todos/{todo_id}")

        assert response.status_code == 204

        # Verify todo is deleted
        get_resp = client.get(f"/todos/{todo_id}")
        assert get_resp.status_code == 404

    def test_delete_todo_not_found(self, client: TestClient):
        """Test deleting non-existent todo returns 404."""
        response = client.delete("/todos/non-existent-id")

        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"


class TestToggleTodo:
    """Tests for POST /todos/{id}/toggle endpoint."""

    def test_toggle_todo_incomplete_to_complete(self, client: TestClient, sample_todo_data: dict):
        """Test toggling incomplete todo to complete."""
        # Create a todo first
        create_resp = client.post("/todos", json=sample_todo_data)
        todo_id = create_resp.json()["id"]

        response = client.post(f"/todos/{todo_id}/toggle")

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

    def test_toggle_todo_complete_to_incomplete(self, client: TestClient, sample_todo_data: dict):
        """Test toggling complete todo back to incomplete."""
        # Create a todo first
        create_resp = client.post("/todos", json=sample_todo_data)
        todo_id = create_resp.json()["id"]

        # Toggle twice
        client.post(f"/todos/{todo_id}/toggle")
        response = client.post(f"/todos/{todo_id}/toggle")

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is False

    def test_toggle_todo_not_found(self, client: TestClient):
        """Test toggling non-existent todo returns 404."""
        response = client.post("/todos/non-existent-id/toggle")

        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"


class TestRootEndpoints:
    """Tests for root and health endpoints."""

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns welcome message."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data

    def test_health_endpoint(self, client: TestClient):
        """Test health check endpoint returns healthy status."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
