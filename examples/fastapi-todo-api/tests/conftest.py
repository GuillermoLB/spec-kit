"""Pytest fixtures for Todo API tests.

This module provides reusable test fixtures for database and API testing.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import FastAPI
from typing import Generator

from src.database import Base, get_db
from src.models.database import TodoModel
from src.config import get_settings


# Use file-based SQLite database for tests
# Note: We must use a file-based database instead of :memory: because
# FastAPI's TestClient runs in a different thread, and each :memory: connection
# creates a separate database. Using check_same_thread=False allows sharing
# the database connection across threads.
import tempfile
import os


@pytest.fixture(scope="function")
def db_engine():
    """Create test database engine.

    Uses file-based SQLite database that is created for each test and deleted after.
    We use file-based instead of :memory: because TestClient runs in a different
    thread and :memory: databases aren't shared across threads.

    Yields:
        SQLAlchemy engine
    """
    # Create temp file for this test
    db_file = tempfile.mktemp(suffix=".db")
    db_url = f"sqlite:///{db_file}"

    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False}
    )

    # Import model to ensure it's registered with Base.metadata
    # This import is needed before create_all() so SQLAlchemy knows about the table
    from src.models.database import TodoModel  # noqa: F401

    # Create all tables
    Base.metadata.create_all(bind=engine)

    yield engine

    # Cleanup
    engine.dispose()
    if os.path.exists(db_file):
        os.remove(db_file)


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
def app_for_testing():
    """Create FastAPI app instance for testing.

    Creates app without lifespan to avoid database initialization conflicts.

    Returns:
        FastAPI app instance
    """
    from fastapi.middleware.cors import CORSMiddleware
    from src.api import todos_router

    settings = get_settings()

    # Create app without lifespan for testing
    test_app = FastAPI(
        title="Todo API (Test)",
        description="Testing instance",
        version="1.0.0-test",
    )

    # Configure CORS
    test_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    test_app.include_router(
        todos_router,
        prefix="/api/v1",
        tags=["todos"]
    )

    # Add health check endpoint
    @test_app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "healthy"}

    return test_app


@pytest.fixture(scope="function")
def client(db_session, db_engine, app_for_testing) -> Generator:
    """Create FastAPI test client.

    Overrides the get_db dependency to use the test database.

    Args:
        db_session: Database session fixture
        db_engine: Database engine fixture (ensures tables are created first)
        app_for_testing: Test app instance

    Yields:
        FastAPI TestClient
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app_for_testing.dependency_overrides[get_db] = override_get_db

    with TestClient(app_for_testing, raise_server_exceptions=False) as test_client:
        yield test_client

    app_for_testing.dependency_overrides.clear()


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
