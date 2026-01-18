---
name: api-development
description: FastAPI and AWS SAM/Lambda patterns for building production-ready REST APIs. Use when creating API endpoints, implementing serverless functions (Lambda), configuring API Gateway, designing REST APIs, adding error handling, writing API tests, or working with OpenAPI specifications. Includes Pydantic models, CloudWatch logging, and pytest patterns.
---

# API Development Plugin

This skill provides patterns and best practices for building APIs with FastAPI and AWS SAM/Lambda.

## FastAPI Best Practices

### 1. Endpoint Structure

```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["resource"])

class ResourceCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ResourceResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: str

@router.post("/resources", response_model=ResourceResponse, status_code=201)
async def create_resource(resource: ResourceCreate):
    """
    Create a new resource.

    Returns:
        ResourceResponse: The created resource
    """
    # Implementation here
    pass
```

### 2. Error Handling

Always use proper HTTP status codes and structured error responses:

```python
from fastapi import HTTPException, status

# 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid input data"
)

# 404 Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Resource {resource_id} not found"
)

# 500 Internal Server Error (catch unexpected errors)
try:
    # risky operation
    pass
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
    )
```

### 3. Dependency Injection

Use FastAPI's dependency injection for shared logic:

```python
from fastapi import Depends

def get_db():
    # Database connection logic
    pass

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Auth logic
    pass

@router.get("/protected")
async def protected_endpoint(
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    pass
```

## AWS SAM/Lambda Patterns

### 1. Lambda Handler Structure

```python
import json
import logging
from typing import Dict, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        API Gateway response
    """
    try:
        # Parse request
        body = json.loads(event.get('body', '{}'))

        # Business logic
        result = process_request(body)

        # Success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return error_response(400, str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return error_response(500, "Internal server error")

def error_response(status_code: int, message: str) -> Dict[str, Any]:
    """Standard error response format."""
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': message})
    }
```

### 2. SAM Template Pattern

See `templates/sam-template.yaml` for a complete SAM configuration.

Key patterns:
- Use environment variables for configuration
- Enable CloudWatch Logs for all functions
- Set appropriate timeout and memory limits
- Use IAM roles with least privilege

### 3. API Gateway Integration

```yaml
Events:
  ApiEvent:
    Type: Api
    Properties:
      Path: /resource/{id}
      Method: get
      RestApiId: !Ref MyApi
```

## Testing Patterns

### 1. pytest for API Testing

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_resource():
    response = client.post(
        "/api/v1/resources",
        json={"name": "Test Resource"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Resource"
    assert "id" in data

def test_get_resource_not_found():
    response = client.get("/api/v1/resources/nonexistent")
    assert response.status_code == 404
```

### 2. Mocking External Services

```python
from unittest.mock import Mock, patch

@patch('app.services.external_api_call')
def test_with_mock(mock_api):
    mock_api.return_value = {"data": "mocked"}
    response = client.get("/api/v1/data")
    assert response.status_code == 200
```

## OpenAPI/Documentation

FastAPI automatically generates OpenAPI docs. Enhance them with:

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API for managing resources",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@router.post(
    "/resources",
    summary="Create a resource",
    description="Creates a new resource with the provided data",
    response_description="The created resource",
    responses={
        201: {"description": "Resource created successfully"},
        400: {"description": "Invalid input data"},
        500: {"description": "Internal server error"}
    }
)
async def create_resource(resource: ResourceCreate):
    pass
```

## Environment Variables

Use `.env` for local development, AWS Systems Manager Parameter Store for production:

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    api_key: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

## Logging (CloudWatch)

```python
import logging
import json

# Structured logging for CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def log_event(event_type: str, data: dict):
    """Log structured events for CloudWatch Insights."""
    logger.info(json.dumps({
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        **data
    }))
```

## Checklist for New Endpoints

When creating a new API endpoint:

- [ ] Define Pydantic models for request/response
- [ ] Implement proper error handling
- [ ] Add OpenAPI documentation
- [ ] Write unit tests
- [ ] Add integration tests
- [ ] Configure CORS if needed
- [ ] Set up authentication/authorization
- [ ] Add logging
- [ ] Update SAM template if serverless
- [ ] Update API specification in `specs/`

## Common Patterns

### Pagination

```python
from fastapi import Query

@router.get("/resources")
async def list_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    # Return paginated results
    pass
```

### Request Validation

```python
from pydantic import BaseModel, validator, Field

class ResourceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()
```

---

*Use this skill to ensure consistent, production-ready API development patterns across your projects.*
