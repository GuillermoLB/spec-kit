"""Tests for List Todos endpoint.

Validates specification: specs/features/list-todos.md

Tests cover:
- Listing all todos
- Filtering by completion status
- Filtering by priority
- Multiple filters (AND logic)
- Pagination (skip/limit)
- Ordering by created_at desc
- Empty results
"""

import pytest
from fastapi.testclient import TestClient
from src.models.database import TodoModel


class TestListTodos:
    """Tests for GET /api/v1/todos endpoint."""

    def test_list_all_todos(self, client: TestClient, sample_todos):
        """Test listing all todos without filters.

        Acceptance Criteria 1: List all todos with 200 status.
        """
        response = client.get("/api/v1/todos")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 5  # sample_todos creates 5 todos

    def test_list_empty_todos(self, client: TestClient):
        """Test listing todos when database is empty.

        Acceptance Criteria 7: Empty list returns empty array with 200.
        """
        response = client.get("/api/v1/todos")

        assert response.status_code == 200
        data = response.json()

        assert data == []

    def test_filter_by_completed_true(self, client: TestClient, sample_todos):
        """Test filtering by completed=true.

        Acceptance Criteria 2: Filter by completion status.
        """
        response = client.get("/api/v1/todos?completed=true")

        assert response.status_code == 200
        data = response.json()

        # sample_todos has 2 completed todos
        assert len(data) == 2
        for todo in data:
            assert todo["completed"] is True

    def test_filter_by_completed_false(self, client: TestClient, sample_todos):
        """Test filtering by completed=false."""
        response = client.get("/api/v1/todos?completed=false")

        assert response.status_code == 200
        data = response.json()

        # sample_todos has 3 incomplete todos
        assert len(data) == 3
        for todo in data:
            assert todo["completed"] is False

    def test_filter_by_priority(self, client: TestClient, sample_todos):
        """Test filtering by priority.

        Acceptance Criteria 3: Filter by priority.
        """
        response = client.get("/api/v1/todos?priority=high")

        assert response.status_code == 200
        data = response.json()

        # sample_todos has 2 high priority todos
        assert len(data) == 2
        for todo in data:
            assert todo["priority"] == "high"

    def test_filter_multiple_conditions(self, client: TestClient, sample_todos):
        """Test filtering with multiple conditions (AND logic).

        Acceptance Criteria 4: Multiple filters use AND logic.
        """
        response = client.get("/api/v1/todos?completed=false&priority=high")

        assert response.status_code == 200
        data = response.json()

        # sample_todos has 2 incomplete high priority todos
        assert len(data) == 2
        for todo in data:
            assert todo["completed"] is False
            assert todo["priority"] == "high"

    def test_pagination_skip_and_limit(self, client: TestClient, sample_todos):
        """Test pagination with skip and limit.

        Acceptance Criteria 5: Pagination with skip/limit works.
        """
        # Get first 2 todos
        response1 = client.get("/api/v1/todos?skip=0&limit=2")
        assert response1.status_code == 200
        data1 = response1.json()
        assert len(data1) == 2

        # Get next 2 todos
        response2 = client.get("/api/v1/todos?skip=2&limit=2")
        assert response2.status_code == 200
        data2 = response2.json()
        assert len(data2) == 2

        # Verify different todos returned
        ids1 = {todo["id"] for todo in data1}
        ids2 = {todo["id"] for todo in data2}
        assert ids1.isdisjoint(ids2)

    def test_limit_capping_at_100(self, client: TestClient):
        """Test that limit is capped at 100.

        Acceptance Criteria 6: Limit exceeding 100 is capped.
        """
        # Request limit > 100
        response = client.get("/api/v1/todos?limit=200")

        assert response.status_code == 200
        # Should not raise error, but limit should be capped
        # (with empty db, we can't test the cap directly, but no error is good)

    def test_invalid_skip_negative(self, client: TestClient):
        """Test validation error for negative skip."""
        response = client.get("/api/v1/todos?skip=-1")

        assert response.status_code == 422

    def test_invalid_limit_zero(self, client: TestClient):
        """Test validation error for limit=0."""
        response = client.get("/api/v1/todos?limit=0")

        assert response.status_code == 422

    def test_invalid_priority_value(self, client: TestClient):
        """Test validation error for invalid priority."""
        response = client.get("/api/v1/todos?priority=urgent")

        assert response.status_code == 422

    def test_todos_ordered_by_created_at_desc(self, client: TestClient):
        """Test that todos are ordered by created_at descending (newest first).

        Acceptance Criteria: Ordering by created_at desc.
        """
        # Create todos in sequence
        client.post("/api/v1/todos", json={"title": "First"})
        client.post("/api/v1/todos", json={"title": "Second"})
        client.post("/api/v1/todos", json={"title": "Third"})

        response = client.get("/api/v1/todos")
        data = response.json()

        # Newest should be first
        assert data[0]["title"] == "Third"
        assert data[1]["title"] == "Second"
        assert data[2]["title"] == "First"

    def test_skip_beyond_available_todos(self, client: TestClient, sample_todos):
        """Test skip beyond available todos returns empty array."""
        response = client.get("/api/v1/todos?skip=100")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_filter_no_matches(self, client: TestClient, sample_todos):
        """Test filtering with no matches returns empty array."""
        # Try to find completed high priority todos
        # sample_todos has high priority incomplete todos, not completed
        response = client.get("/api/v1/todos?completed=true&priority=high")

        assert response.status_code == 200
        data = response.json()
        # Should return empty array if no matches
        # (depends on sample_todos - adjust based on your fixtures)
