"""
FastAPI Endpoint Template

Replace placeholders:
- ResourceName: Your resource name (e.g., User, Product)
- resource_name: Lowercase version (e.g., user, product)
- RESOURCE_TABLE: DynamoDB table name (if using DynamoDB)
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)

# Router configuration
router = APIRouter(
    prefix="/api/v1/resources",
    tags=["resources"]
)

# ============================================================================
# Pydantic Models
# ============================================================================

class ResourceBase(BaseModel):
    """Base model with common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="Resource name")
    description: Optional[str] = Field(None, max_length=500, description="Optional description")


class ResourceCreate(ResourceBase):
    """Model for creating a new resource."""
    pass


class ResourceUpdate(BaseModel):
    """Model for updating an existing resource."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ResourceResponse(ResourceBase):
    """Model for resource responses."""
    id: str = Field(..., description="Unique resource ID")
    created_at: str = Field(..., description="ISO 8601 timestamp")
    updated_at: str = Field(..., description="ISO 8601 timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Example Resource",
                "description": "This is an example",
                "created_at": "2024-01-17T10:00:00Z",
                "updated_at": "2024-01-17T10:00:00Z"
            }
        }


# ============================================================================
# Endpoints
# ============================================================================

@router.post(
    "",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new resource",
    description="Creates a new resource with the provided data"
)
async def create_resource(resource: ResourceCreate) -> ResourceResponse:
    """
    Create a new resource.

    Args:
        resource: Resource data

    Returns:
        The created resource

    Raises:
        HTTPException: 400 if validation fails, 500 if server error
    """
    try:
        now = datetime.utcnow().isoformat() + "Z"
        resource_id = str(uuid.uuid4())

        # TODO: Save to database
        # Example: await db.save(resource_id, resource.dict())

        logger.info(f"Created resource: {resource_id}")

        return ResourceResponse(
            id=resource_id,
            name=resource.name,
            description=resource.description,
            created_at=now,
            updated_at=now
        )

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error creating resource: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get(
    "/{resource_id}",
    response_model=ResourceResponse,
    summary="Get a resource by ID",
    description="Retrieves a single resource by its unique ID"
)
async def get_resource(resource_id: str) -> ResourceResponse:
    """
    Get a resource by ID.

    Args:
        resource_id: The resource ID

    Returns:
        The requested resource

    Raises:
        HTTPException: 404 if not found, 500 if server error
    """
    try:
        # TODO: Fetch from database
        # Example: resource = await db.get(resource_id)

        # Placeholder - replace with actual database query
        resource = None

        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource {resource_id} not found"
            )

        return resource

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching resource: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get(
    "",
    response_model=List[ResourceResponse],
    summary="List all resources",
    description="Retrieves a paginated list of resources"
)
async def list_resources(
    skip: int = 0,
    limit: int = 10
) -> List[ResourceResponse]:
    """
    List resources with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of resources

    Raises:
        HTTPException: 500 if server error
    """
    try:
        # TODO: Fetch from database with pagination
        # Example: resources = await db.list(skip=skip, limit=limit)

        logger.info(f"Listing resources: skip={skip}, limit={limit}")

        return []  # Replace with actual data

    except Exception as e:
        logger.error(f"Unexpected error listing resources: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put(
    "/{resource_id}",
    response_model=ResourceResponse,
    summary="Update a resource",
    description="Updates an existing resource with new data"
)
async def update_resource(
    resource_id: str,
    resource: ResourceUpdate
) -> ResourceResponse:
    """
    Update a resource.

    Args:
        resource_id: The resource ID
        resource: Updated resource data

    Returns:
        The updated resource

    Raises:
        HTTPException: 404 if not found, 400 if validation fails, 500 if server error
    """
    try:
        # TODO: Update in database
        # Example: updated = await db.update(resource_id, resource.dict(exclude_unset=True))

        # Check if resource exists
        # if not updated:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"Resource {resource_id} not found"
        #     )

        logger.info(f"Updated resource: {resource_id}")

        # Return updated resource (placeholder)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource {resource_id} not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating resource: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete(
    "/{resource_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a resource",
    description="Permanently deletes a resource"
)
async def delete_resource(resource_id: str) -> None:
    """
    Delete a resource.

    Args:
        resource_id: The resource ID

    Raises:
        HTTPException: 404 if not found, 500 if server error
    """
    try:
        # TODO: Delete from database
        # Example: deleted = await db.delete(resource_id)

        # if not deleted:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"Resource {resource_id} not found"
        #     )

        logger.info(f"Deleted resource: {resource_id}")

        # Placeholder
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource {resource_id} not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting resource: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
