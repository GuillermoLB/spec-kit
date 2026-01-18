"""Pytest fixtures for Todo API tests.

This module provides reusable test fixtures for database and API testing.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from typing import Generator

from src.main import app
from src.database import Base, get_db
from src.models.database import TodoModel


# Use in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_engine():
    """Create test database engine.

    Uses in-memory SQLite database that is recreated for each test.

    Yields:
        SQLAlchemy engine
    """
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)

    yield engine

    # Drop all tables after test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create test database session.

    Creates a new session for each test, providing isolation.

    Args:
        db_engine: Database engine fixture

    Yields:
        SQLAlchemy session
    """
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine
    )

    session = TestingSessionLocal()

    yield session

    session.close()


@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    """Create FastAPI test client.

    Overrides the get_db dependency to use the test database.

    Args:
        db_session: Database session fixture

    Yields:
        FastAPI TestClient
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def sample_todo(db_session) -> TodoModel:
    """Create a sample todo in the database.

    Useful for testing update and delete operations.

    Args:
        db_session: Database session fixture

    Returns:
        Created TodoModel instance
    """
    todo = TodoModel(
        title="Sample Todo",
        description="This is a sample todo for testing",
        completed=False,
        priority="medium"
    )

    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    return todo


@pytest.fixture(scope="function")
def sample_todos(db_session) -> list[TodoModel]:
    """Create multiple sample todos with varying properties.

    Useful for testing list and filter operations.

    Args:
        db_session: Database session fixture

    Returns:
        List of created TodoModel instances
    """
    todos = [
        TodoModel(
            title="High priority task",
            description="Important task",
            completed=False,
            priority="high"
        ),
        TodoModel(
            title="Completed task",
            description="Already done",
            completed=True,
            priority="medium"
        ),
        TodoModel(
            title="Low priority task",
            description="Can wait",
            completed=False,
            priority="low"
        ),
        TodoModel(
            title="Another high priority",
            description="Also important",
            completed=False,
            priority="high"
        ),
        TodoModel(
            title="Completed low priority",
            description="Done, was not urgent",
            completed=True,
            priority="low"
        ),
    ]

    for todo in todos:
        db_session.add(todo)

    db_session.commit()

    for todo in todos:
        db_session.refresh(todo)

    return todos
