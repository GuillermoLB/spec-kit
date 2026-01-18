"""Tests for Create Todo endpoint.

Validates specification: specs/features/create-todo.md

Tests cover:
- Successful creation with all fields
- Successful creation with minimal fields
- Validation errors for invalid data
- Default values
- Timestamp generation
"""

import pytest
from fastapi.testclient import TestClient


class TestCreateTodo:
    """Tests for POST /api/v1/todos endpoint."""

    def test_create_todo_with_all_fields(self, client: TestClient):
        """Test creating todo with all fields provided.

        Acceptance Criteria 1: Create with title and priority.
        """
        response = client.post(
            "/api/v1/todos",
            json={
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "priority": "high"
            }
        )

        assert response.status_code == 201
        data = response.json()

        assert data["title"] == "Buy groceries"
        assert data["description"] == "Milk, eggs, bread"
        assert data["priority"] == "high"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_todo_with_minimal_fields(self, client: TestClient):
        """Test creating todo with only required title field.

        Acceptance Criteria 5: Minimal data with defaults.
        """
        response = client.post(
            "/api/v1/todos",
            json={"title": "Simple task"}
        )

        assert response.status_code == 201
        data = response.json()

        assert data["title"] == "Simple task"
        assert data["description"] is None
        assert data["priority"] == "medium"  # Default
        assert data["completed"] is False  # Default

    def test_create_todo_missing_title(self, client: TestClient):
        """Test validation error when title is missing.

        Acceptance Criteria 2: Missing title returns 422.
        """
        response = client.post(
            "/api/v1/todos",
            json={"description": "test"}
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_create_todo_invalid_priority(self, client: TestClient):
        """Test validation error for invalid priority value.

        Acceptance Criteria 3: Invalid priority returns 422.
        """
        response = client.post(
            "/api/v1/todos",
            json={
                "title": "Task",
                "priority": "urgent"  # Not a valid enum value
            }
        )

        assert response.status_code == 422

    def test_create_todo_title_too_long(self, client: TestClient):
        """Test validation error for title exceeding 200 characters.

        Acceptance Criteria 4: Title too long returns 422.
        """
        long_title = "x" * 201  # Exceeds 200 char limit

        response = client.post(
            "/api/v1/todos",
            json={"title": long_title}
        )

        assert response.status_code == 422

    def test_create_todo_description_too_long(self, client: TestClient):
        """Test validation error for description exceeding 1000 characters."""
        long_description = "x" * 1001  # Exceeds 1000 char limit

        response = client.post(
            "/api/v1/todos",
            json={
                "title": "Task",
                "description": long_description
            }
        )

        assert response.status_code == 422

    def test_create_todo_empty_title(self, client: TestClient):
        """Test validation error for empty title."""
        response = client.post(
            "/api/v1/todos",
            json={"title": ""}
        )

        assert response.status_code == 422

    def test_create_todo_all_priorities(self, client: TestClient):
        """Test creating todos with each priority level."""
        for priority in ["low", "medium", "high"]:
            response = client.post(
                "/api/v1/todos",
                json={
                    "title": f"Task with {priority} priority",
                    "priority": priority
                }
            )

            assert response.status_code == 201
            data = response.json()
            assert data["priority"] == priority

    def test_create_todo_null_description(self, client: TestClient):
        """Test creating todo with explicitly null description."""
        response = client.post(
            "/api/v1/todos",
            json={
                "title": "Task",
                "description": None
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["description"] is None

    def test_create_todo_generates_unique_ids(self, client: TestClient):
        """Test that each created todo gets a unique ID."""
        response1 = client.post("/api/v1/todos", json={"title": "Task 1"})
        response2 = client.post("/api/v1/todos", json={"title": "Task 2"})

        assert response1.status_code == 201
        assert response2.status_code == 201

        id1 = response1.json()["id"]
        id2 = response2.json()["id"]

        assert id1 != id2

    def test_create_todo_timestamps(self, client: TestClient):
        """Test that created_at and updated_at are set correctly."""
        response = client.post(
            "/api/v1/todos",
            json={"title": "Task"}
        )

        assert response.status_code == 201
        data = response.json()

        assert "created_at" in data
        assert "updated_at" in data
        # For new todos, created_at and updated_at should be very close
        assert data["created_at"] is not None
        assert data["updated_at"] is not None
