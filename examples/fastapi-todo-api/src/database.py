"""Database configuration and session management.

This module provides SQLAlchemy database setup for the Todo API.
Uses SQLite for simplicity in this example.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

from src.config import get_settings

# Get database URL from configuration
settings = get_settings()

# Create SQLAlchemy engine
# connect_args={"check_same_thread": False} is needed for SQLite
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()


def get_db() -> Generator:
    """Get database session.

    This is a FastAPI dependency that provides a database session
    for each request. The session is automatically closed when the
    request is complete.

    Yields:
        SQLAlchemy database session

    Example:
        @app.get("/todos")
        def list_todos(db: Session = Depends(get_db)):
            return db.query(TodoModel).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables.

    Creates all tables defined in SQLAlchemy models.
    This is called when the application starts.

    In production, you would use migrations (Alembic) instead
    of creating tables directly.
    """
    from src.models.database import TodoModel  # Import models to register them
    Base.metadata.create_all(bind=engine)
