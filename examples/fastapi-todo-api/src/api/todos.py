"""Todo CRUD API endpoints.

This module implements all Todo CRUD operations following the specifications
in specs/features/. Each endpoint corresponds to a feature spec.

Specifications:
- create-todo.md: POST /api/v1/todos
- list-todos.md: GET /api/v1/todos
- update-todo.md: PUT /api/v1/todos/{id}
- delete-todo.md: DELETE /api/v1/todos/{id}
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import logging

from src.database import get_db
from src.models import TodoCreate, TodoUpdate, TodoResponse, TodoModel, Priority

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()


@router.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create todo",
    description="Create a new todo item",
)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db)
) -> TodoResponse:
    """Create a new todo.

    Specification: specs/features/create-todo.md

    Args:
        todo: Todo creation data (title, description, priority)
        db: Database session (injected)

    Returns:
        Created todo with auto-generated ID and timestamps

    Raises:
        HTTPException 422: Validation error (Pydantic handles this)

    Example:
        POST /api/v1/todos
        Body: {"title": "Buy groceries", "priority": "high"}
        Response: {
            "id": "uuid",
            "title": "Buy groceries",
            "completed": false,
            "priority": "high",
            ...
        }
    """
    logger.info(f"Creating todo: {todo.title}")

    # Create database model from Pydantic model
    db_todo = TodoModel(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        completed=False,  # Always false on creation
    )

    # Add to database
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    logger.info(f"Todo created successfully: {db_todo.id}")
    return TodoResponse.model_validate(db_todo)


@router.get(
    "/todos",
    response_model=List[TodoResponse],
    summary="List todos",
    description="Retrieve list of todos with optional filtering and pagination",
)
def list_todos(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[Priority] = Query(None, description="Filter by priority level"),
    skip: int = Query(0, ge=0, description="Number of items to skip (pagination)"),
    limit: int = Query(50, ge=1, le=100, description="Maximum items to return (max 100)"),
    db: Session = Depends(get_db)
) -> List[TodoResponse]:
    """List todos with filtering and pagination.

    Specification: specs/features/list-todos.md

    Args:
        completed: Filter by completion status (optional)
        priority: Filter by priority level (optional)
        skip: Pagination offset (default 0)
        limit: Max items to return (default 50, max 100)
        db: Database session (injected)

    Returns:
        List of todos matching filters, ordered by created_at desc

    Example:
        GET /api/v1/todos?completed=false&priority=high&skip=0&limit=20
        Response: [{todo1}, {todo2}, ...]
    """
    logger.info(
        f"Listing todos: completed={completed}, priority={priority}, "
        f"skip={skip}, limit={limit}"
    )

    # Build query with filters
    query = db.query(TodoModel)

    if completed is not None:
        query = query.filter(TodoModel.completed == completed)

    if priority is not None:
        query = query.filter(TodoModel.priority == priority)

    # Order by created_at descending (newest first)
    query = query.order_by(TodoModel.created_at.desc())

    # Apply pagination
    query = query.offset(skip).limit(limit)

    # Execute query
    todos = query.all()

    logger.info(f"Found {len(todos)} todos")
    return [TodoResponse.model_validate(todo) for todo in todos]


@router.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    summary="Get todo",
    description="Retrieve a specific todo by ID",
)
def get_todo(
    todo_id: UUID,
    db: Session = Depends(get_db)
) -> TodoResponse:
    """Get a single todo by ID.

    Args:
        todo_id: Todo UUID
        db: Database session (injected)

    Returns:
        Todo object

    Raises:
        HTTPException 404: Todo not found

    Example:
        GET /api/v1/todos/550e8400-e29b-41d4-a716-446655440000
        Response: {todo object}
    """
    logger.info(f"Getting todo: {todo_id}")

    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()

    if not todo:
        logger.warning(f"Todo not found: {todo_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )

    return TodoResponse.model_validate(todo)


@router.put(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    summary="Update todo",
    description="Update an existing todo (partial updates supported)",
)
def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db)
) -> TodoResponse:
    """Update an existing todo.

    Specification: specs/features/update-todo.md

    Supports partial updates - only provided fields are updated.
    The updated_at timestamp is automatically updated.

    Args:
        todo_id: Todo UUID
        todo_update: Fields to update (all optional)
        db: Database session (injected)

    Returns:
        Updated todo object

    Raises:
        HTTPException 404: Todo not found
        HTTPException 422: Validation error

    Example:
        PUT /api/v1/todos/uuid
        Body: {"completed": true, "priority": "low"}
        Response: {updated todo}
    """
    logger.info(f"Updating todo: {todo_id}")

    # Find existing todo
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()

    if not db_todo:
        logger.warning(f"Todo not found: {todo_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )

    # Update only provided fields (partial update)
    update_data = todo_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_todo, field, value)

    # Commit changes (updated_at will be auto-updated by SQLAlchemy)
    db.commit()
    db.refresh(db_todo)

    logger.info(f"Todo updated successfully: {todo_id}")
    return TodoResponse.model_validate(db_todo)


@router.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete todo",
    description="Delete a todo by ID",
)
def delete_todo(
    todo_id: UUID,
    db: Session = Depends(get_db)
) -> None:
    """Delete a todo.

    Specification: specs/features/delete-todo.md

    Permanently removes the todo from the database.
    Returns 204 No Content on success (no response body).

    Args:
        todo_id: Todo UUID
        db: Database session (injected)

    Returns:
        None (204 No Content)

    Raises:
        HTTPException 404: Todo not found

    Example:
        DELETE /api/v1/todos/uuid
        Response: 204 No Content (empty body)
    """
    logger.info(f"Deleting todo: {todo_id}")

    # Find and delete todo
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()

    if not db_todo:
        logger.warning(f"Todo not found: {todo_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )

    db.delete(db_todo)
    db.commit()

    logger.info(f"Todo deleted successfully: {todo_id}")
    # No return value for 204 No Content
