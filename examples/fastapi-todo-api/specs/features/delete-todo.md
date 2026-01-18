# Feature: Delete Todo

**Status**: Implemented
**Owner**: Example Team
**Last Updated**: 2026-01-18
**Priority**: High

## Purpose

Allow users to delete todo items so they can remove completed or unwanted tasks from their list.

## Requirements

- [ ] Accept DELETE requests to `/api/v1/todos/{id}`
- [ ] Remove todo from database permanently
- [ ] Return 204 No Content on successful deletion
- [ ] Return 404 Not Found if todo doesn't exist
- [ ] Operation is idempotent (deleting already-deleted todo returns 404)
- [ ] No request body required
- [ ] No response body on success

## User Stories

**As a** user
**I want** to delete completed todos
**So that** I can keep my todo list clean and focused

**As a** user
**I want** to remove unwanted todos
**So that** I can fix mistakes or remove tasks that are no longer relevant

## Acceptance Criteria

1. **Given** I send DELETE `/api/v1/todos/{id}`
   **When** todo exists
   **Then** todo is permanently deleted and I receive 204 No Content

2. **Given** I send DELETE `/api/v1/todos/{invalid-id}`
   **When** todo doesn't exist
   **Then** I receive 404 Not Found with error message

3. **Given** I delete a todo successfully
   **When** I try to retrieve it with GET `/api/v1/todos/{id}`
   **Then** I receive 404 Not Found

4. **Given** I delete a todo successfully
   **When** I try to delete it again
   **Then** I receive 404 Not Found (idempotent behavior)

5. **Given** I send DELETE `/api/v1/todos/{id}`
   **When** todo exists
   **Then** response has no body, only 204 status code

## Technical Details

### API Endpoint

**Endpoint**: `DELETE /api/v1/todos/{id}`

**Path Parameters**:
- `id`: UUID - Todo identifier

**Request**: No body required

**Response** (204 No Content):
- No response body
- Status code: 204

**Error Response** (404 Not Found):
```json
{
  "detail": "Todo with ID {id} not found"
}
```

### Delete Logic

**Implementation**:
1. Receive DELETE request with todo ID
2. Attempt to find todo in database
3. If not found, return 404 Not Found
4. If found, delete from database
5. Commit transaction
6. Return 204 No Content (no body)

**Database Operation**:
- Use DELETE SQL statement
- Check affected rows count
- If 0 rows affected, todo didn't exist → 404
- If 1 row affected, deletion successful → 204

### Idempotency

**Idempotent Behavior**:
- First DELETE: Returns 204 (todo deleted)
- Second DELETE: Returns 404 (todo doesn't exist)
- This is correct idempotent behavior for DELETE

**Rationale**:
- HTTP DELETE is idempotent: multiple identical requests have same effect
- After first delete, resource no longer exists
- Subsequent deletes confirm resource doesn't exist (404)

## Edge Cases & Error Handling

1. **Edge case**: Delete non-existent todo
   - **Handling**: Return 404 Not Found
   - **Message**: "Todo with ID {id} not found"

2. **Edge case**: Invalid UUID format
   - **Handling**: FastAPI validation rejects invalid UUID
   - **Response**: 422 Unprocessable Entity

3. **Edge case**: Delete then immediately create with same ID
   - **Handling**: UUIDs should be unique, extremely unlikely
   - **Recovery**: If it happens, new todo is created normally

4. **Error**: Database connection fails during delete
   - **Message**: "500 Internal Server Error: Database connection error"
   - **Recovery**: Client retries after delay

5. **Error**: Transaction fails after delete
   - **Handling**: Rollback transaction, todo remains in database
   - **Response**: 500 Internal Server Error
   - **Recovery**: Client retries delete

## Testing Strategy

### Unit Tests

- [ ] Test database delete operation
- [ ] Test affected rows count check
- [ ] Test UUID validation

### Integration Tests

- [ ] Test successful deletion returns 204
- [ ] Test successful deletion removes todo from database
- [ ] Test 404 error for non-existent todo
- [ ] Test deleted todo cannot be retrieved
- [ ] Test deleted todo cannot be deleted again (404)
- [ ] Test deletion is permanent (verify with list endpoint)
- [ ] Test no response body on successful delete
- [ ] Test invalid UUID format rejected

### Test Coverage Goal

- 100% coverage on delete_todo endpoint
- All error paths tested
- Idempotency verified

## Dependencies

- **Blocked by**: create-todo.md (need todos to delete)
- **Blocks**: None
- **Related**: list-todos.md, update-todo.md

## Implementation Notes

### Decisions Made

- 2026-01-18: Return 204 No Content on success (REST best practice)
- 2026-01-18: Return 404 on non-existent todo (correct idempotent behavior)
- 2026-01-18: Permanent deletion (no soft delete for simplicity)
- 2026-01-18: No undo mechanism (keep example simple)

### Alternative Considered

**Soft Delete vs Hard Delete**:
- **Chose**: Hard delete (permanent removal)
- **Alternative**: Soft delete (mark as deleted, keep in DB)
- **Rationale**: Keep example simple, hard delete is easier to understand
- **Production Note**: Many production systems use soft delete for audit trails

**204 vs 200 for Success**:
- **Chose**: 204 No Content (no response body)
- **Alternative**: 200 OK with success message
- **Rationale**: 204 is correct REST status for successful delete with no body

### Security Considerations

- Only allow deleting todos owned by authenticated user (if auth added later)
- Validate UUID format to prevent SQL injection (Pydantic handles this)
- Use parameterized queries (SQLAlchemy handles this)

### Implementation

See: [src/api/todos.py](../../src/api/todos.py)

---

**Template Version**: 1.0
**Last Updated**: 2026-01-18
