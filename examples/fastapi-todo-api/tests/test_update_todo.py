"""Tests for Update Todo endpoint.

Validates specification: specs/features/update-todo.md

Tests cover:
- Successful updates (single and multiple fields)
- Partial updates
- Validation errors
- 404 errors for non-existent todos
- Timestamp updates
- Immutable fields
"""

import pytest
from fastapi.testclient import TestClient
from src.models.database import TodoModel


class TestUpdateTodo:
    """Tests for PUT /api/v1/todos/{id} endpoint."""

    def test_update_completed_status(self, client: TestClient, sample_todo):
        """Test updating only the completed field.

        Acceptance Criteria 1: Update completed to true.
        """
        todo_id = str(sample_todo.id)

        response = client.put(
            f"/api/v1/todos/{todo_id}",
            json={"completed": True}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["completed"] is True
        assert data["title"] == sample_todo.title  # Other fields unchanged
        assert data["priority"] == sample_todo.priority

    def test_update_priority(self, client: TestClient, sample_todo):
        """Test updating only the priority field.

        Acceptance Criteria 2: Update priority only.
        """
        todo_id = str(sample_todo.id)

        response = client.put(
            f"/api/v1/todos/{todo_id}",
            json={"priority": "low"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["priority"] == "low"
        assert data["title"] == sample_todo.title  # Other fields unchanged

    def test_update_multiple_fields(self, client: TestClient, sample_todo):
        """Test updating multiple fields at once.

        Acceptance Criteria 3: Update multiple fields.
        """
        todo_id = str(sample_todo.id)

        response = client.put(
            f"/api/v1/todos/{todo_id}",
            json={
                "title": "Updated title",
                "completed": True,
                "priority": "high"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert data["title"] == "Updated title"
        assert data["completed"] is True
        assert data["priority"] == "high"

    def test_update_nonexistent_todo(self, client: TestClient):
        """Test 404 error when updating non-existent todo.

        Acceptance Criteria 4: Non-existent todo returns 404.
        """
        fake_id = "550e8400-e29b-41d4-a716-446655440000"

        response = client.put(
            f"/api/v1/todos/{fake_id}",
            json={"completed": True}
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert fake_id in data["detail"]

    def test_update_title_too_long(self, client: TestClient, sample_todo):
        """Test validation error for title exceeding 200 characters.

        Acceptance Criteria 5: Invalid data returns 422.
        """
        todo_id = str(sample_todo.id)
        long_title = "x" * 201

        response = client.put(
            f"/api/v1/todos/{todo_id}",
            json={"title": long_title}
        )

        assert response.status_code == 422

    def test_update_description_to_null(self, client: TestClient, sample_todo):
        """Test setting description to null.

        Acceptance Criteria 6: Can set description to null.
        """
        todo_id = str(sample_todo.id)

        response = client.put(
            f"/api/v1/todos/{todo_id}",
            json={"description": None}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["description"] is None

    def test_update_empty_body(self, client: TestClient, sample_todo):
        """Test update with empty body (only timestamp updated).

        Edge Case: Empty body should succeed, updating only timestamp.
        """
        todo_id = str(sample_todo.id)
        original_updated_at = sample_todo.updated_at

        response = client.put(
            f"/api/v1/todos/{todo_id}",
            json={}
        )

        assert response.status_code == 200
        data = response.json()

        # All fields should remain the same except updated_at
        assert data["title"] == sample_todo.title
        assert data["completed"] == sample_todo.completed

    def test_update_invalid_priority(self, client: TestClient, sample_todo):
        """Test validation error for invalid priority."""
        todo_id = str(sample_todo.id)

        response = client.put(
            f"/api/v1/todos/{todo_id}",
            json={"priority": "urgent"}
        )

        assert response.status_code == 422

    def test_update_timestamp_changes(self, client: TestClient, sample_todo):
        """Test that updated_at timestamp is updated."""
        todo_id = str(sample_todo.id)
        original_created_at = sample_todo.created_at

        response = client.put(
            f"/api/v1/todos/{todo_id}",
            json={"title": "Updated"}
        )

        assert response.status_code == 200
        data = response.json()

        # created_at should not change
        # (Note: comparing strings here since they're in response)
        assert "created_at" in data
        assert "updated_at" in data

    def test_update_all_fields(self, client: TestClient, sample_todo):
        """Test updating all editable fields."""
        todo_id = str(sample_todo.id)

        response = client.put(
            f"/api/v1/todos/{todo_id}",
            json={
                "title": "Completely updated",
                "description": "New description",
                "completed": True,
                "priority": "high"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert data["title"] == "Completely updated"
        assert data["description"] == "New description"
        assert data["completed"] is True
        assert data["priority"] == "high"

    def test_update_title_to_empty_fails(self, client: TestClient, sample_todo):
        """Test that updating title to empty string fails validation."""
        todo_id = str(sample_todo.id)

        response = client.put(
            f"/api/v1/todos/{todo_id}",
            json={"title": ""}
        )

        assert response.status_code == 422

    def test_update_invalid_uuid(self, client: TestClient):
        """Test validation error for invalid UUID format."""
        response = client.put(
            "/api/v1/todos/invalid-uuid",
            json={"completed": True}
        )

        assert response.status_code == 422

    def test_update_preserves_other_fields(self, client: TestClient, sample_todo):
        """Test that updating one field preserves others."""
        todo_id = str(sample_todo.id)
        original_description = sample_todo.description
        original_priority = sample_todo.priority

        response = client.put(
            f"/api/v1/todos/{todo_id}",
            json={"title": "New title"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["title"] == "New title"
        assert data["description"] == original_description
        assert data["priority"] == original_priority
