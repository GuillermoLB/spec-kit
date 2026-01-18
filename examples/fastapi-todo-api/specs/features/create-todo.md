# Feature: Create Todo

**Status**: Implemented
**Owner**: Example Team
**Last Updated**: 2026-01-18
**Priority**: High

## Purpose

Allow users to create new todo items via the API so they can track tasks and manage their work.

## Requirements

- [ ] Accept POST requests to `/api/v1/todos`
- [ ] Validate title is required (1-200 characters)
- [ ] Validate description is optional (max 1000 characters)
- [ ] Validate priority is one of: low, medium, high (default: medium)
- [ ] Set `completed` to false by default
- [ ] Generate UUID for new todo
- [ ] Set `created_at` and `updated_at` timestamps automatically
- [ ] Return 201 Created status with todo object
- [ ] Return 422 Unprocessable Entity for validation errors
- [ ] Store todo in database with transaction support

## User Stories

**As a** user
**I want** to create new todo items
**So that** I can track tasks I need to complete

## Acceptance Criteria

1. **Given** I send POST `/api/v1/todos` with valid data
   **When** title is "Buy groceries" and priority is "high"
   **Then** todo is created with 201 status, includes id and timestamps

2. **Given** I send POST `/api/v1/todos` without title
   **When** request body is `{"description": "test"}`
   **Then** I receive 422 status with error "Field required" for title

3. **Given** I send POST `/api/v1/todos` with invalid priority
   **When** priority is "urgent" (not in enum)
   **Then** I receive 422 status with validation error

4. **Given** I send POST `/api/v1/todos` with title too long
   **When** title exceeds 200 characters
   **Then** I receive 422 status with error about maximum length

5. **Given** I send POST `/api/v1/todos` with minimal data
   **When** request body is `{"title": "Task"}`
   **Then** todo is created with default priority "medium" and completed false

## Technical Details

### API Endpoint

**Endpoint**: `POST /api/v1/todos`

**Request Body** (application/json):
```json
{
  "title": "string (required, 1-200 chars)",
  "description": "string (optional, max 1000 chars)",
  "priority": "low|medium|high (optional, default: medium)"
}
```

**Response** (201 Created):
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string|null",
  "completed": false,
  "priority": "low|medium|high",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Error Response** (422 Unprocessable Entity):
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

### Validation Rules

- **title**: Required, 1-200 characters
- **description**: Optional, max 1000 characters, nullable
- **priority**: Optional, must be one of: low, medium, high
- **completed**: Auto-set to false, not accepted in create request
- **id**: Auto-generated UUID4
- **timestamps**: Auto-set to current UTC time

### Database Schema

See [specs/api/todo-api.yaml](../api/todo-api.yaml) for complete schema.

## Edge Cases & Error Handling

1. **Edge case**: Title with only whitespace
   - **Handling**: Pydantic validation rejects empty/whitespace-only strings
   - **Message**: "String should have at least 1 character"

2. **Edge case**: Description is null vs empty string
   - **Handling**: Both treated as no description (nullable field)
   - **Response**: Returns `"description": null` in both cases

3. **Edge case**: Priority not provided
   - **Handling**: Default to "medium"
   - **Response**: Todo created with priority "medium"

4. **Error**: Database connection failure
   - **Message**: "503 Service Unavailable: Database connection error"
   - **Recovery**: Client retries after delay

5. **Error**: Duplicate UUID (extremely rare)
   - **Handling**: Database unique constraint prevents duplicate
   - **Recovery**: Retry with new UUID automatically

## Testing Strategy

### Unit Tests

- [ ] Test Pydantic TodoCreate model validation
- [ ] Test title length validation (1-200 chars)
- [ ] Test description length validation (max 1000 chars)
- [ ] Test priority enum validation
- [ ] Test default values (completed, priority)

### Integration Tests

- [ ] Test successful todo creation with all fields
- [ ] Test successful todo creation with minimal fields (title only)
- [ ] Test validation error for missing title
- [ ] Test validation error for invalid priority
- [ ] Test validation error for title too long
- [ ] Test validation error for description too long
- [ ] Test UUID is generated correctly
- [ ] Test timestamps are set correctly
- [ ] Test database persistence

### Test Coverage Goal

- 100% coverage on create_todo endpoint
- All validation paths tested
- All error responses tested

## Dependencies

- **Blocked by**: None
- **Blocks**: None
- **Related**: list-todos.md, update-todo.md, delete-todo.md

## Implementation Notes

### Decisions Made

- 2026-01-18: Use Pydantic v2 for validation (better error messages)
- 2026-01-18: Use UUID4 for IDs (better than auto-increment for distributed systems)
- 2026-01-18: Default priority to "medium" (most tasks are medium priority)
- 2026-01-18: Auto-set timestamps server-side (prevent client time manipulation)

### Implementation

See: [src/api/todos.py](../../src/api/todos.py)

---

**Template Version**: 1.0
**Last Updated**: 2026-01-18
