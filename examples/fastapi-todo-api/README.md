# FastAPI Todo API - Spec-Driven Development Example

A production-ready Todo CRUD API built with FastAPI, demonstrating **spec-driven development** using [spec-kit](https://github.com/your-org/spec-kit).

This example shows the complete workflow from writing specifications to implementing and testing a real API, following spec-kit methodology.

## What This Example Demonstrates

- **Specification-First Development**: Feature specs written before code
- **Complete CRUD API**: Create, Read, Update, Delete operations
- **Production-Ready Code**: Error handling, validation, logging
- **Comprehensive Testing**: >80% coverage with pytest
- **OpenAPI Documentation**: Auto-generated interactive API docs
- **Spec-Kit Integration**: Using the api-development plugin

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Spec-Driven Workflow](#spec-driven-workflow)
- [Development](#development)
- [Next Steps](#next-steps)

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Basic knowledge of REST APIs

## Quick Start

### 1. Clone and Navigate

```bash
cd examples/fastapi-todo-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn src.main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000)

### 5. Explore API Documentation

Open your browser and visit:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Try out the endpoints directly in the interactive documentation!

## Project Structure

```
examples/fastapi-todo-api/
├── CLAUDE.md                      # Spec-kit constitution
├── README.md                      # This file
├── .claude/
│   └── skills/
│       └── api-development/       # API development plugin
├── specs/
│   ├── SPECIFICATIONS_SUMMARY.md  # Tracking all specs
│   ├── features/
│   │   ├── create-todo.md         # Spec for creating todos
│   │   ├── list-todos.md          # Spec for listing/filtering
│   │   ├── update-todo.md         # Spec for updating todos
│   │   └── delete-todo.md         # Spec for deleting todos
│   └── api/
│       └── todo-api.yaml          # OpenAPI 3.0 specification
├── src/
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration management
│   ├── database.py                # Database connection
│   ├── api/
│   │   └── todos.py               # Todo CRUD endpoints
│   └── models/
│       ├── todo.py                # Pydantic models
│       └── database.py            # SQLAlchemy models
├── tests/
│   ├── conftest.py                # Pytest fixtures
│   ├── test_create_todo.py       # Create endpoint tests
│   ├── test_list_todos.py        # List endpoint tests
│   ├── test_update_todo.py       # Update endpoint tests
│   └── test_delete_todo.py       # Delete endpoint tests
├── .env.example                   # Environment variables template
├── requirements.txt               # Python dependencies
└── pytest.ini                     # Pytest configuration
```

## API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "healthy"}
```

### Create Todo

```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "high"
  }'
```

Response (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": "high",
  "created_at": "2026-01-18T10:00:00Z",
  "updated_at": "2026-01-18T10:00:00Z"
}
```

### List Todos

```bash
# List all todos
curl http://localhost:8000/api/v1/todos

# Filter by completion status
curl http://localhost:8000/api/v1/todos?completed=false

# Filter by priority
curl http://localhost:8000/api/v1/todos?priority=high

# Combine filters
curl http://localhost:8000/api/v1/todos?completed=false&priority=high

# Pagination
curl http://localhost:8000/api/v1/todos?skip=0&limit=20
```

### Get Single Todo

```bash
curl http://localhost:8000/api/v1/todos/{id}
```

### Update Todo

```bash
# Update single field
curl -X PUT http://localhost:8000/api/v1/todos/{id} \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Update multiple fields
curl -X PUT http://localhost:8000/api/v1/todos/{id} \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries and supplies",
    "completed": true,
    "priority": "low"
  }'
```

### Delete Todo

```bash
curl -X DELETE http://localhost:8000/api/v1/todos/{id}
```

Response: 204 No Content (empty body)

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run with Coverage Report

```bash
pytest tests/ --cov=src --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Run Specific Test File

```bash
pytest tests/test_create_todo.py -v
```

### Run Specific Test

```bash
pytest tests/test_create_todo.py::TestCreateTodo::test_create_todo_with_all_fields -v
```

**Expected Results**: All tests pass with >80% coverage

## Spec-Driven Workflow

This project was built using spec-driven development. Here's how:

### 1. Read the Specifications

Before writing any code, we wrote detailed specifications:

```bash
# Read feature specs
cat specs/features/create-todo.md
cat specs/features/list-todos.md
cat specs/features/update-todo.md
cat specs/features/delete-todo.md

# Review API spec
cat specs/api/todo-api.yaml
```

Each specification includes:
- **Purpose**: Why this feature exists
- **Requirements**: What needs to be implemented
- **Acceptance Criteria**: How to validate it works (in Given/When/Then format)
- **Technical Details**: API contracts, data models
- **Edge Cases**: Error handling scenarios

### 2. Implement Following the Spec

Implementation follows the spec exactly:

- **[specs/features/create-todo.md](specs/features/create-todo.md)** → `src/api/todos.py:create_todo()`
- **[specs/features/list-todos.md](specs/features/list-todos.md)** → `src/api/todos.py:list_todos()`
- **[specs/features/update-todo.md](specs/features/update-todo.md)** → `src/api/todos.py:update_todo()`
- **[specs/features/delete-todo.md](specs/features/delete-todo.md)** → `src/api/todos.py:delete_todo()`

### 3. Validate with Tests

Acceptance criteria from specs become test cases:

**Example from [specs/features/create-todo.md](specs/features/create-todo.md)**:

> **Acceptance Criteria 1**: Given I POST valid todo data, When title is "Buy groceries", Then todo is created with 201 status

Becomes test in [tests/test_create_todo.py](tests/test_create_todo.py):

```python
def test_create_todo_with_all_fields(self, client: TestClient):
    """Test creating todo with all fields provided.

    Acceptance Criteria 1: Create with title and priority.
    """
    response = client.post("/api/v1/todos", json={
        "title": "Buy groceries",
        "priority": "high"
    })

    assert response.status_code == 201
    # ... more assertions
```

### 4. Update Spec Status

After implementation and testing, update spec status from "Draft" to "Implemented".

## Development

### Environment Variables

Copy [.env.example](.env.example) to `.env` and configure:

```bash
cp .env.example .env
```

Available settings:
- `DATABASE_URL`: Database connection (default: `sqlite:///./todos.db`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `CORS_ORIGINS`: Allowed CORS origins (default: all)

### Database

This example uses SQLite for simplicity (no setup required).

**Database file**: `todos.db` (created automatically)

**Tables**: Initialized automatically on startup

For production, you would:
- Use PostgreSQL or MySQL
- Add database migrations with Alembic
- Implement connection pooling

### Code Structure

**Separation of Concerns**:
- **Pydantic models** (`src/models/todo.py`): API request/response validation
- **SQLAlchemy models** (`src/models/database.py`): Database persistence
- **API routes** (`src/api/todos.py`): HTTP endpoint handlers
- **Configuration** (`src/config.py`): Environment management

**Why separate Pydantic and SQLAlchemy models?**
- Pydantic: Validates external data, auto-generates API docs
- SQLAlchemy: Handles database operations, relationships
- Separation prevents leaking database details into API

### Adding a New Feature

Follow the spec-driven workflow:

1. **Write the spec**: Create `specs/features/your-feature.md`
2. **Update API spec**: Add endpoint to `specs/api/todo-api.yaml`
3. **Implement**: Add code following the spec
4. **Test**: Write tests validating acceptance criteria
5. **Update spec**: Mark status as "Implemented"

## Next Steps

### Extend This Example

**Add New Features**:
- [ ] Tags for todos (many-to-many relationship)
- [ ] Due dates with reminder notifications
- [ ] User authentication (multi-tenancy)
- [ ] Search functionality (full-text search)

**Improve Infrastructure**:
- [ ] Add database migrations with Alembic
- [ ] Implement async database driver
- [ ] Add caching with Redis
- [ ] Deploy to cloud (AWS, GCP, Azure)

**Enhance Quality**:
- [ ] Add integration tests
- [ ] Implement rate limiting
- [ ] Add monitoring and metrics
- [ ] Set up CI/CD pipeline

### Learn More

**Spec-Kit Resources**:
- [CLAUDE.md](CLAUDE.md): Constitution for this project
- [Main Spec-Kit Repo](../../README.md): Full documentation
- [API Development Plugin](../../plugins/api-development/): Patterns and templates

**FastAPI Resources**:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## Troubleshooting

**Port 8000 already in use**:
```bash
uvicorn src.main:app --reload --port 8001
```

**Database locked error**:
- Close other connections to `todos.db`
- Delete `todos.db` and restart (data will be lost)

**Import errors**:
```bash
# Ensure you're in the project directory
cd examples/fastapi-todo-api

# Reinstall dependencies
pip install -r requirements.txt
```

**Tests failing**:
```bash
# Run tests with verbose output
pytest tests/ -vv

# Check test coverage
pytest tests/ --cov=src --cov-report=term-missing
```

## License

This example is part of spec-kit and is licensed under the MIT License.

---

**Built with spec-driven development using [spec-kit](https://github.com/your-org/spec-kit)**

Questions? Issues? Open an issue on the spec-kit repository!
