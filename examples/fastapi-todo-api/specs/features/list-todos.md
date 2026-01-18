# Feature: List Todos

**Status**: Implemented
**Owner**: Example Team
**Last Updated**: 2026-01-18
**Priority**: High

## Purpose

Allow users to retrieve a list of todos with filtering and pagination so they can view and manage their tasks efficiently.

## Requirements

- [ ] Accept GET requests to `/api/v1/todos`
- [ ] Support filtering by `completed` status (true/false)
- [ ] Support filtering by `priority` (low/medium/high)
- [ ] Support pagination with `skip` and `limit` parameters
- [ ] Default `skip` to 0, `limit` to 50
- [ ] Maximum `limit` of 100 items
- [ ] Return 200 OK with array of todos
- [ ] Return empty array if no todos match filters
- [ ] Order todos by `created_at` descending (newest first)

## User Stories

**As a** user
**I want** to view my todo list with filters
**So that** I can focus on specific types of tasks

**As a** user
**I want** to paginate through many todos
**So that** the API responds quickly even with many items

## Acceptance Criteria

1. **Given** I send GET `/api/v1/todos`
   **When** no filters are provided
   **Then** I receive all todos ordered by created_at desc with 200 status

2. **Given** I send GET `/api/v1/todos?completed=true`
   **When** filtering by completion status
   **Then** I receive only completed todos

3. **Given** I send GET `/api/v1/todos?priority=high`
   **When** filtering by priority
   **Then** I receive only high priority todos

4. **Given** I send GET `/api/v1/todos?completed=false&priority=high`
   **When** using multiple filters
   **Then** I receive todos matching both filters (AND logic)

5. **Given** I send GET `/api/v1/todos?skip=10&limit=20`
   **When** using pagination
   **Then** I receive 20 items starting from offset 10

6. **Given** I send GET `/api/v1/todos?limit=200`
   **When** limit exceeds maximum
   **Then** limit is capped at 100 items

7. **Given** no todos exist in database
   **When** I send GET `/api/v1/todos`
   **Then** I receive empty array `[]` with 200 status

## Technical Details

### API Endpoint

**Endpoint**: `GET /api/v1/todos`

**Query Parameters**:
- `completed`: boolean (optional) - Filter by completion status
- `priority`: string (optional) - Filter by priority (low, medium, high)
- `skip`: integer (optional, default: 0, min: 0) - Pagination offset
- `limit`: integer (optional, default: 50, min: 1, max: 100) - Items per page

**Response** (200 OK):
```json
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string|null",
    "completed": boolean,
    "priority": "low|medium|high",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

**Empty Response** (200 OK):
```json
[]
```

### Filtering Logic

**Query Building**:
- Base query: SELECT all todos
- Add WHERE completed = ? if completed parameter provided
- Add WHERE priority = ? if priority parameter provided
- ORDER BY created_at DESC
- Apply OFFSET skip
- Apply LIMIT min(limit, 100)

**Filter Combination**:
- Multiple filters use AND logic
- `?completed=true&priority=high` returns todos that are both completed AND high priority

### Pagination

**Default Behavior**:
- skip = 0 (start from beginning)
- limit = 50 (reasonable default)

**Maximum Limit**:
- Hard cap at 100 items to prevent performance issues
- If client requests limit > 100, silently cap at 100

**Example**:
- Page 1: skip=0, limit=50 (items 1-50)
- Page 2: skip=50, limit=50 (items 51-100)
- Page 3: skip=100, limit=50 (items 101-150)

## Edge Cases & Error Handling

1. **Edge case**: No todos in database
   - **Handling**: Return empty array `[]`
   - **Response**: 200 OK with empty array

2. **Edge case**: Skip beyond available todos
   - **Handling**: Return empty array `[]`
   - **Response**: 200 OK with empty array

3. **Edge case**: Limit = 0
   - **Handling**: Validation error, limit must be >= 1
   - **Response**: 422 Unprocessable Entity

4. **Edge case**: Negative skip
   - **Handling**: Validation error, skip must be >= 0
   - **Response**: 422 Unprocessable Entity

5. **Edge case**: Invalid priority value
   - **Handling**: Validation error, priority must be low/medium/high
   - **Response**: 422 Unprocessable Entity

6. **Error**: Database query failure
   - **Message**: "500 Internal Server Error: Database query failed"
   - **Recovery**: Client retries after delay

## Testing Strategy

### Unit Tests

- [ ] Test query parameter validation (skip, limit)
- [ ] Test limit capping at 100
- [ ] Test completed filter parameter parsing
- [ ] Test priority filter parameter parsing

### Integration Tests

- [ ] Test listing all todos (no filters)
- [ ] Test filtering by completed=true
- [ ] Test filtering by completed=false
- [ ] Test filtering by priority (low, medium, high)
- [ ] Test combined filters (completed + priority)
- [ ] Test pagination (skip/limit)
- [ ] Test empty result when no todos exist
- [ ] Test empty result when filters match nothing
- [ ] Test ordering by created_at descending
- [ ] Test limit capping at maximum

### Performance Tests

- [ ] Test query performance with 1000+ todos
- [ ] Test pagination performance
- [ ] Verify indexes on filtered columns

### Test Coverage Goal

- 100% coverage on list_todos endpoint
- All filter combinations tested
- All edge cases tested

## Dependencies

- **Blocked by**: None
- **Blocks**: None
- **Related**: create-todo.md, update-todo.md, delete-todo.md

## Implementation Notes

### Decisions Made

- 2026-01-18: Default limit to 50 (balance between performance and UX)
- 2026-01-18: Max limit of 100 (prevent DoS via large queries)
- 2026-01-18: Order by created_at DESC (newest first is most useful)
- 2026-01-18: Empty array on no results (consistent with REST conventions)
- 2026-01-18: AND logic for multiple filters (most intuitive behavior)

### Database Optimization

- Add index on `completed` column for faster filtering
- Add index on `priority` column for faster filtering
- Add index on `created_at` column for faster sorting

### Implementation

See: [src/api/todos.py](../../src/api/todos.py)

---

**Template Version**: 1.0
**Last Updated**: 2026-01-18
