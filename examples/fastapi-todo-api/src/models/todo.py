"""Pydantic models for Todo API.

This module defines the Pydantic schemas used for API request/response
validation and serialization. These are separate from the SQLAlchemy
database models.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum
from uuid import UUID


class Priority(str, Enum):
    """Priority levels for todos.

    Values:
        low: Low priority task
        medium: Medium priority task (default)
        high: High priority task
    """
    low = "low"
    medium = "medium"
    high = "high"


class TodoBase(BaseModel):
    """Base todo schema with common fields.

    This is the base class for create and update schemas.
    Contains all user-editable fields.
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Todo title (required)",
        examples=["Buy groceries"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Todo description (optional)",
        examples=["Milk, eggs, bread"]
    )
    priority: Priority = Field(
        default=Priority.medium,
        description="Priority level",
        examples=["medium"]
    )


class TodoCreate(TodoBase):
    """Schema for creating a new todo.

    Inherits all fields from TodoBase. The completed field is
    not accepted in create requests - it defaults to False.

    Example:
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "priority": "high"
        }
    """
    pass


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo.

    All fields are optional to support partial updates.
    Only provided fields will be updated.

    Example (partial update):
        {"completed": true}

    Example (multiple fields):
        {
            "title": "Buy groceries and supplies",
            "completed": true,
            "priority": "low"
        }
    """
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Todo title"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Todo description"
    )
    completed: Optional[bool] = Field(
        default=None,
        description="Completion status"
    )
    priority: Optional[Priority] = Field(
        default=None,
        description="Priority level"
    )


class TodoResponse(TodoBase):
    """Schema for todo responses.

    This is the complete todo object returned by the API,
    including auto-generated fields like ID and timestamps.

    Example:
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false,
            "priority": "medium",
            "created_at": "2026-01-18T10:00:00Z",
            "updated_at": "2026-01-18T10:00:00Z"
        }
    """
    id: UUID = Field(
        ...,
        description="Unique identifier",
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )
    completed: bool = Field(
        ...,
        description="Completion status",
        examples=[False]
    )
    created_at: datetime = Field(
        ...,
        description="Creation timestamp",
        examples=["2026-01-18T10:00:00Z"]
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp",
        examples=["2026-01-18T10:00:00Z"]
    )

    model_config = ConfigDict(from_attributes=True)
