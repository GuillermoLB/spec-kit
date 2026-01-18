# Feature: Update Todo

**Status**: Implemented
**Owner**: Example Team
**Last Updated**: 2026-01-18
**Priority**: High

## Purpose

Allow users to update existing todo items so they can modify task details, mark items as complete, or change priorities.

## Requirements

- [ ] Accept PUT requests to `/api/v1/todos/{id}`
- [ ] Support partial updates (only provided fields are updated)
- [ ] Validate title if provided (1-200 characters)
- [ ] Validate description if provided (max 1000 characters)
- [ ] Validate priority if provided (low/medium/high)
- [ ] Validate completed if provided (boolean)
- [ ] Update `updated_at` timestamp automatically
- [ ] Do not allow updating `id`, `created_at`
- [ ] Return 200 OK with updated todo object
- [ ] Return 404 Not Found if todo doesn't exist
- [ ] Return 422 Unprocessable Entity for validation errors

## User Stories

**As a** user
**I want** to update todo details
**So that** I can modify tasks as my work changes

**As a** user
**I want** to mark todos as complete
**So that** I can track my progress

**As a** user
**I want** to change todo priority
**So that** I can reprioritize my work

## Acceptance Criteria

1. **Given** I send PUT `/api/v1/todos/{id}` with `{"completed": true}`
   **When** todo exists
   **Then** todo is updated, completed is true, updated_at is current time, 200 status

2. **Given** I send PUT `/api/v1/todos/{id}` with `{"priority": "low"}`
   **When** todo exists
   **Then** only priority is updated, other fields unchanged, 200 status

3. **Given** I send PUT `/api/v1/todos/{id}` with multiple fields
   **When** request has `{"title": "New title", "completed": true, "priority": "high"}`
   **Then** all provided fields are updated, 200 status

4. **Given** I send PUT `/api/v1/todos/{invalid-id}`
   **When** todo doesn't exist
   **Then** I receive 404 status with error message

5. **Given** I send PUT `/api/v1/todos/{id}` with invalid data
   **When** title exceeds 200 characters
   **Then** I receive 422 status with validation error

6. **Given** I send PUT `/api/v1/todos/{id}` with `{"description": null}`
   **When** setting description to null
   **Then** description is cleared, 200 status

## Technical Details

### API Endpoint

**Endpoint**: `PUT /api/v1/todos/{id}`

**Path Parameters**:
- `id`: UUID - Todo identifier

**Request Body** (application/json, all fields optional):
```json
{
  "title": "string (optional, 1-200 chars)",
  "description": "string|null (optional, max 1000 chars)",
  "completed": "boolean (optional)",
  "priority": "low|medium|high (optional)"
}
```

**Response** (200 OK):
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string|null",
  "completed": boolean,
  "priority": "low|medium|high",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Todo with ID {id} not found"
}
```

**Error Response** (422 Unprocessable Entity):
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "String should have at most 200 characters",
      "type": "string_too_long"
    }
  ]
}
```

### Update Logic

**Partial Update Implementation**:
1. Fetch existing todo from database
2. If not found, return 404
3. Validate provided fields
4. Update only fields present in request body
5. Auto-update `updated_at` to current time
6. Save to database
7. Return updated todo

**Fields That Can Be Updated**:
- title
- description (including setting to null)
- completed
- priority

**Fields That Cannot Be Updated**:
- id (immutable)
- created_at (immutable)
- updated_at (auto-managed)

### Validation Rules

- **title**: If provided, must be 1-200 characters
- **description**: If provided, max 1000 characters, nullable
- **completed**: If provided, must be boolean
- **priority**: If provided, must be one of: low, medium, high
- **updated_at**: Auto-set to current UTC time on any update

## Edge Cases & Error Handling

1. **Edge case**: Empty request body `{}`
   - **Handling**: Accept request, only update updated_at timestamp
   - **Response**: 200 OK with todo (only timestamp changed)

2. **Edge case**: Invalid UUID format
   - **Handling**: FastAPI validation rejects invalid UUID
   - **Response**: 422 Unprocessable Entity with validation error

3. **Edge case**: Update description to empty string vs null
   - **Handling**: Empty string "" is valid, null clears description
   - **Response**: 200 OK with description set to "" or null respectively

4. **Edge case**: Update same values (no actual change)
   - **Handling**: Accept request, update updated_at anyway
   - **Response**: 200 OK (idempotent operation)

5. **Error**: Database update fails
   - **Message**: "500 Internal Server Error: Database update failed"
   - **Recovery**: Client retries after delay

6. **Error**: Concurrent updates (race condition)
   - **Handling**: Last write wins (no optimistic locking for simplicity)
   - **Note**: Could add version field for optimistic locking in production

## Testing Strategy

### Unit Tests

- [ ] Test Pydantic TodoUpdate model validation
- [ ] Test partial update logic (only provided fields)
- [ ] Test title validation
- [ ] Test description validation
- [ ] Test priority validation
- [ ] Test completed validation

### Integration Tests

- [ ] Test successful update with single field
- [ ] Test successful update with multiple fields
- [ ] Test successful update with all fields
- [ ] Test empty request body (only timestamp updated)
- [ ] Test 404 error for non-existent todo
- [ ] Test validation error for invalid title
- [ ] Test validation error for invalid priority
- [ ] Test description can be set to null
- [ ] Test updated_at timestamp is updated
- [ ] Test created_at timestamp is not changed
- [ ] Test id cannot be changed

### Test Coverage Goal

- 100% coverage on update_todo endpoint
- All partial update combinations tested
- All error responses tested

## Dependencies

- **Blocked by**: create-todo.md (need todos to update)
- **Blocks**: None
- **Related**: list-todos.md, delete-todo.md

## Implementation Notes

### Decisions Made

- 2026-01-18: Use PUT for updates (full resource representation expected)
- 2026-01-18: Support partial updates (more flexible for clients)
- 2026-01-18: Empty body updates timestamp only (idempotent "touch" operation)
- 2026-01-18: Last write wins for concurrent updates (simplicity over consistency)
- 2026-01-18: Allow setting description to null (clear description)

### Alternative Considered

**PATCH vs PUT**:
- Chose PUT with partial update support
- PATCH is semantically more correct for partial updates
- PUT is more common in REST APIs and simpler to understand

### Implementation

See: [src/api/todos.py](../../src/api/todos.py)

---

**Template Version**: 1.0
**Last Updated**: 2026-01-18
