# Feature: FastAPI Todo API Example

**Status**: Implemented
**Owner**: spec-kit development team
**Last Updated**: 2026-01-18
**Priority**: High

## Purpose

Create a complete, production-ready FastAPI Todo API example project that demonstrates spec-kit's spec-driven development workflow in practice. This example serves as a reference implementation showing how to use spec-kit with the api-development plugin, write specifications, and build a real application.

## Requirements

- [ ] Complete FastAPI application with CRUD operations for todos
- [ ] Follows spec-kit directory structure with CLAUDE.md, .claude/skills/, specs/
- [ ] Includes feature specifications for each major capability (create, list, update, delete todos)
- [ ] Includes OpenAPI specification in specs/api/todo-api.yaml
- [ ] Production-ready code with error handling, validation, logging
- [ ] Comprehensive pytest test suite with >80% coverage
- [ ] README explaining the example and how to run it
- [ ] Requirements.txt with all dependencies
- [ ] Environment variable configuration
- [ ] Demonstrates spec-driven workflow from spec to implementation

## User Stories

**As a** developer learning spec-kit
**I want** a complete example project
**So that** I can see how spec-driven development works in practice

**As a** new spec-kit user
**I want** a reference implementation using the api-development plugin
**So that** I can model my own projects after it

**As a** potential spec-kit adopter
**I want** to see real specifications and their implementations
**So that** I can evaluate if spec-kit fits my workflow

## Acceptance Criteria

1. **Given** I clone the spec-kit repository
   **When** I navigate to examples/fastapi-todo-api/
   **Then** I see a complete project structure with all necessary files

2. **Given** I read the example README
   **When** I follow the setup instructions
   **Then** I can run the API locally and make requests to all endpoints

3. **Given** I examine the specs/features/ directory
   **When** I read the feature specifications
   **Then** each spec clearly describes a feature with acceptance criteria

4. **Given** I compare specs to implementation
   **When** I review the code
   **Then** the implementation matches the specifications

5. **Given** I run the test suite
   **When** I execute pytest
   **Then** all tests pass with >80% coverage

6. **Given** I want to extend the example
   **When** I follow the spec-driven workflow shown
   **Then** I can add new features following the same pattern

## Technical Details

### Architecture

**FastAPI Todo API with SQLite database:**

```
examples/fastapi-todo-api/
├── CLAUDE.md                      # Spec-kit constitution
├── README.md                      # Example documentation
├── .claude/
│   └── skills/
│       └── api-development/       # API plugin (copied from spec-kit)
│           ├── SKILL.md
│           └── references/
│               ├── fastapi-endpoint.py
│               └── sam-template.yaml
├── specs/
│   ├── features/
│   │   ├── create-todo.md         # Spec for creating todos
│   │   ├── list-todos.md          # Spec for listing/filtering todos
│   │   ├── update-todo.md         # Spec for updating todos
│   │   └── delete-todo.md         # Spec for deleting todos
│   └── api/
│       └── todo-api.yaml          # OpenAPI 3.0 specification
├── src/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration management
│   ├── database.py                # Database connection
│   ├── api/
│   │   ├── __init__.py
│   │   └── todos.py               # Todo endpoints
│   └── models/
│       ├── __init__.py
│       ├── todo.py                # Pydantic models
│       └── database.py            # SQLAlchemy models
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── test_create_todo.py
│   ├── test_list_todos.py
│   ├── test_update_todo.py
│   └── test_delete_todo.py
├── .env.example                   # Environment variables template
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
└── .gitignore
```

### API Endpoints

**Todo CRUD Operations:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/todos | Create new todo |
| GET | /api/v1/todos | List all todos (with filtering) |
| GET | /api/v1/todos/{id} | Get single todo |
| PUT | /api/v1/todos/{id} | Update todo |
| DELETE | /api/v1/todos/{id} | Delete todo |
| GET | /health | Health check endpoint |

### Data Model

**Todo Schema:**

```python
{
    "id": "uuid",
    "title": "string (required, max 200 chars)",
    "description": "string (optional, max 1000 chars)",
    "completed": "boolean (default: false)",
    "priority": "string (enum: low, medium, high)",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### Technology Stack

- **Framework**: FastAPI 0.104+
- **Database**: SQLite (development), SQLAlchemy ORM
- **Validation**: Pydantic v2
- **Testing**: pytest, pytest-asyncio, httpx
- **Documentation**: Auto-generated OpenAPI/Swagger

### Feature Specifications

**Each spec follows this pattern:**

```markdown
# Feature: Create Todo

**Status**: Implemented
**Owner**: Example team
**Last Updated**: 2026-01-17

## Purpose
Allow users to create new todo items via API.

## Requirements
- [ ] Accept POST requests to /api/v1/todos
- [ ] Validate title is required and ≤200 chars
- [ ] Default completed to false
- [ ] Return 201 Created with todo object

## Acceptance Criteria
1. Given I POST valid todo data
   When request includes title
   Then todo is created and returned with 201 status

2. Given I POST invalid data
   When title is missing
   Then I receive 422 Unprocessable Entity with error details
```

### README Content

The example README should include:

1. **Overview** - What this example demonstrates
2. **Prerequisites** - Python 3.11+, pip
3. **Setup Instructions** - Virtual env, install deps, run app
4. **API Usage** - Example curl commands for each endpoint
5. **Running Tests** - How to execute test suite
6. **Spec-Driven Workflow** - How specs were used to build this
7. **Project Structure** - Explanation of directory layout
8. **Next Steps** - How to extend the example

### Security Considerations

- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (via SQLAlchemy ORM)
- [ ] CORS configuration for production
- [ ] Rate limiting recommendations in README
- [ ] Environment variables for sensitive config
- [ ] No hardcoded secrets

## Edge Cases & Error Handling

1. **Edge case**: Create todo with duplicate title
   - **Handling**: Allow duplicates (titles don't need to be unique)

2. **Edge case**: Update non-existent todo
   - **Message**: "404 Not Found: Todo with ID {id} not found"
   - **Recovery**: Client checks ID and retries

3. **Error**: Database connection fails
   - **Message**: "503 Service Unavailable: Database connection error"
   - **Recovery**: Retry after delay, check database status

4. **Edge case**: List todos with invalid filter parameters
   - **Handling**: Ignore invalid filters, return all todos with warning in logs

5. **Edge case**: Delete todo that's already deleted
   - **Handling**: Return 404 Not Found (idempotent behavior)

## Testing Strategy

### Unit Tests

- [ ] Test Pydantic model validation
- [ ] Test database model relationships
- [ ] Test individual endpoint functions
- [ ] Test error handling for each endpoint

### Integration Tests

- [ ] Test full CRUD workflow (create → read → update → delete)
- [ ] Test filtering and pagination
- [ ] Test error responses (400, 404, 422, 500)
- [ ] Test concurrent requests
- [ ] Test database transactions

### Test Coverage Goals

- Minimum 80% code coverage
- 100% coverage on API endpoints
- All error paths tested

### Manual Testing Checklist

- [ ] Create todo via Swagger UI
- [ ] List todos with different filters
- [ ] Update todo fields individually
- [ ] Delete todo and verify removal
- [ ] Test with invalid data
- [ ] Check OpenAPI docs are accurate

## Dependencies

- **Blocked by**: documentation-improvements (README template)
- **Blocks**: None (but helps validate api-development plugin)
- **Related**: testing-infrastructure (can use tests as examples)

## Implementation Notes

### Decisions Made

- 2026-01-17 - Use SQLite for simplicity (easy to run example without setup)
- 2026-01-17 - Include UUID for IDs (more realistic than auto-increment)
- 2026-01-17 - Priority enum limited to low/medium/high (KISS principle)
- 2026-01-17 - No authentication (keeps example focused on spec-driven workflow)

### Example Spec: Create Todo

Show one complete specification in the example to demonstrate format:

```markdown
# Feature: Create Todo

**Status**: Implemented
**Owner**: Example Team
**Last Updated**: 2026-01-17
**Priority**: High

## Purpose

Allow users to create new todo items via the API so they can track tasks.

## Requirements

- [ ] Accept POST requests to /api/v1/todos
- [ ] Validate title is required (max 200 characters)
- [ ] Validate description is optional (max 1000 characters)
- [ ] Validate priority is one of: low, medium, high (default: medium)
- [ ] Set completed to false by default
- [ ] Generate UUID for new todo
- [ ] Set created_at and updated_at timestamps
- [ ] Return 201 Created with todo object
- [ ] Return 422 Unprocessable Entity for validation errors

## Acceptance Criteria

1. **Given** I send POST /api/v1/todos with valid data
   **When** title is "Buy groceries"
   **Then** todo is created with 201 status and includes id, timestamps

2. **Given** I send POST /api/v1/todos without title
   **When** request body is {"description": "test"}
   **Then** I receive 422 status with error "title is required"

3. **Given** I send POST /api/v1/todos with invalid priority
   **When** priority is "urgent" (not in enum)
   **Then** I receive 422 status with error "priority must be low, medium, or high"

## Implementation

See: `src/api/todos.py:create_todo()`
```

### Development Workflow Example

The README should show this workflow:

```bash
# 1. Read the spec
cat specs/features/create-todo.md

# 2. Start Claude Code
claude

# 3. Ask Claude to implement
> "Implement the create todo feature from specs/features/create-todo.md using the api-development plugin"

# 4. Claude reads spec, asks clarifying questions, implements

# 5. Run tests to validate
pytest tests/test_create_todo.py -v

# 6. Update spec status to "Implemented"
```

## Verification

### Setup Verification

```bash
cd examples/fastapi-todo-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### API Verification

```bash
# Health check
curl http://localhost:8000/health

# Create todo
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Test todo","priority":"high"}'

# List todos
curl http://localhost:8000/api/v1/todos
```

### Test Verification

```bash
pytest -v --cov=src --cov-report=term-missing
# Should show >80% coverage
```

### Documentation Verification

```bash
# Open auto-generated docs
open http://localhost:8000/docs
# Should see all endpoints documented
```

## References

- API development plugin: [plugins/api-development/](../../plugins/api-development/)
- FastAPI template: [plugins/api-development/templates/fastapi-endpoint.py](../../plugins/api-development/templates/fastapi-endpoint.py)
- Feature template: [templates/specs/feature.template.md](../../templates/specs/feature.template.md)
- API spec template: [templates/specs/api.template.yaml](../../templates/specs/api.template.yaml)

---

**Template Version**: 1.0
**Last Updated**: 2026-01-17
