"""Tests for Delete Todo endpoint.

Validates specification: specs/features/delete-todo.md

Tests cover:
- Successful deletion (204 No Content)
- 404 errors for non-existent todos
- Idempotency (deleting twice)
- Verification that todo is removed
- No response body on success
"""

import pytest
from fastapi.testclient import TestClient
from src.models.database import TodoModel


class TestDeleteTodo:
    """Tests for DELETE /api/v1/todos/{id} endpoint."""

    def test_delete_existing_todo(self, client: TestClient, sample_todo):
        """Test successful deletion of existing todo.

        Acceptance Criteria 1: Delete returns 204 No Content.
        """
        todo_id = str(sample_todo.id)

        response = client.delete(f"/api/v1/todos/{todo_id}")

        assert response.status_code == 204
        assert response.text == ""  # No response body

    def test_delete_nonexistent_todo(self, client: TestClient):
        """Test 404 error when deleting non-existent todo.

        Acceptance Criteria 2: Non-existent todo returns 404.
        """
        fake_id = "550e8400-e29b-41d4-a716-446655440000"

        response = client.delete(f"/api/v1/todos/{fake_id}")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert fake_id in data["detail"]

    def test_deleted_todo_cannot_be_retrieved(self, client: TestClient, sample_todo):
        """Test that deleted todo cannot be retrieved.

        Acceptance Criteria 3: Deleted todo returns 404 on GET.
        """
        todo_id = str(sample_todo.id)

        # Delete the todo
        delete_response = client.delete(f"/api/v1/todos/{todo_id}")
        assert delete_response.status_code == 204

        # Try to retrieve it
        get_response = client.get(f"/api/v1/todos/{todo_id}")
        assert get_response.status_code == 404

    def test_delete_idempotency(self, client: TestClient, sample_todo):
        """Test deleting same todo twice (idempotent behavior).

        Acceptance Criteria 4: Deleting again returns 404.
        """
        todo_id = str(sample_todo.id)

        # First delete
        response1 = client.delete(f"/api/v1/todos/{todo_id}")
        assert response1.status_code == 204

        # Second delete (should return 404, not 204)
        response2 = client.delete(f"/api/v1/todos/{todo_id}")
        assert response2.status_code == 404

    def test_delete_no_response_body(self, client: TestClient, sample_todo):
        """Test that successful deletion has no response body.

        Acceptance Criteria 5: Response has no body.
        """
        todo_id = str(sample_todo.id)

        response = client.delete(f"/api/v1/todos/{todo_id}")

        assert response.status_code == 204
        assert len(response.content) == 0

    def test_delete_removes_from_list(self, client: TestClient, sample_todo):
        """Test that deleted todo is removed from list."""
        todo_id = str(sample_todo.id)

        # Verify todo exists in list
        list_response1 = client.get("/api/v1/todos")
        todos_before = list_response1.json()
        ids_before = [todo["id"] for todo in todos_before]
        assert todo_id in ids_before

        # Delete todo
        client.delete(f"/api/v1/todos/{todo_id}")

        # Verify todo no longer in list
        list_response2 = client.get("/api/v1/todos")
        todos_after = list_response2.json()
        ids_after = [todo["id"] for todo in todos_after]
        assert todo_id not in ids_after

    def test_delete_invalid_uuid(self, client: TestClient):
        """Test validation error for invalid UUID format."""
        response = client.delete("/api/v1/todos/invalid-uuid")

        assert response.status_code == 422

    def test_delete_multiple_todos(self, client: TestClient, sample_todos):
        """Test deleting multiple todos independently."""
        todo_ids = [str(todo.id) for todo in sample_todos[:3]]

        # Delete each todo
        for todo_id in todo_ids:
            response = client.delete(f"/api/v1/todos/{todo_id}")
            assert response.status_code == 204

        # Verify all deleted
        for todo_id in todo_ids:
            get_response = client.get(f"/api/v1/todos/{todo_id}")
            assert get_response.status_code == 404

    def test_delete_does_not_affect_other_todos(self, client: TestClient, sample_todos):
        """Test that deleting one todo doesn't affect others."""
        todo_to_delete_id = str(sample_todos[0].id)
        other_todo_id = str(sample_todos[1].id)

        # Delete first todo
        client.delete(f"/api/v1/todos/{todo_to_delete_id}")

        # Verify other todo still exists
        response = client.get(f"/api/v1/todos/{other_todo_id}")
        assert response.status_code == 200

    def test_delete_is_permanent(self, client: TestClient, sample_todo):
        """Test that deletion is permanent (no soft delete)."""
        todo_id = str(sample_todo.id)
        original_title = sample_todo.title

        # Delete todo
        client.delete(f"/api/v1/todos/{todo_id}")

        # Create new todo with same title
        create_response = client.post(
            "/api/v1/todos",
            json={"title": original_title}
        )
        new_todo_id = create_response.json()["id"]

        # New todo should have different ID
        assert new_todo_id != todo_id

        # Original todo should still be gone
        get_response = client.get(f"/api/v1/todos/{todo_id}")
        assert get_response.status_code == 404
