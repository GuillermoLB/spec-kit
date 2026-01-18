"""SQLAlchemy database models.

This module defines the database schema for todos using SQLAlchemy ORM.
"""

from sqlalchemy import Boolean, Column, DateTime, Enum, String
from sqlalchemy.types import TypeDecorator, CHAR
from datetime import datetime
import uuid
import enum

from src.database import Base


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type when available, otherwise uses
    CHAR(36), storing as stringified hex values.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            from sqlalchemy.dialects.postgresql import UUID
            return dialect.type_descriptor(UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if isinstance(value, uuid.UUID):
                return str(value)
            else:
                return str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if isinstance(value, uuid.UUID):
                return value
            else:
                return uuid.UUID(value)


class PriorityEnum(str, enum.Enum):
    """Priority levels for todos."""
    low = "low"
    medium = "medium"
    high = "high"


class TodoModel(Base):
    """Todo database model.

    Represents a todo item in the database with all fields including
    auto-generated ID and timestamps.

    Attributes:
        id: Unique identifier (UUID)
        title: Todo title (required, max 200 chars)
        description: Todo description (optional, max 1000 chars)
        completed: Completion status (default False)
        priority: Priority level (default medium)
        created_at: Creation timestamp (auto-set)
        updated_at: Last update timestamp (auto-updated)
    """
    __tablename__ = "todos"

    # Primary key - UUID for better distribution and uniqueness
    id = Column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    # Todo fields
    title = Column(String(200), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    completed = Column(Boolean, default=False, nullable=False, index=True)
    priority = Column(
        Enum(PriorityEnum),
        default=PriorityEnum.medium,
        nullable=False,
        index=True
    )

    # Timestamps - auto-managed
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def __repr__(self) -> str:
        """String representation for debugging."""
        priority_str = self.priority.value if self.priority else "unset"
        return f"<Todo {self.id}: {self.title} ({priority_str})>"
