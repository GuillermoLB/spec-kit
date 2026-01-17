# Feature: [Feature Name]

**Status**: Draft
**Owner**: [Your Name]
**Last Updated**: [YYYY-MM-DD]
**Priority**: [High | Medium | Low]

## Purpose

[Why this feature exists. What problem does it solve? What value does it provide?]

## Requirements

- [ ] Requirement 1: [Specific, measurable requirement]
- [ ] Requirement 2: [Another clear requirement]
- [ ] Requirement 3: [Add as many as needed]

## User Stories

**As a** [type of user]
**I want** [goal]
**So that** [benefit]

### Example:

**As a** registered user
**I want** to reset my password via email
**So that** I can regain access if I forget my credentials

## Acceptance Criteria

How do we know this feature is complete and working correctly?

1. **Given** [context/precondition]
   **When** [action taken]
   **Then** [expected outcome]

2. **Given** [another context]
   **When** [action]
   **Then** [outcome]

### Example:

1. **Given** I'm on the login page
   **When** I click "Forgot Password" and enter my email
   **Then** I receive a password reset link within 5 minutes

2. **Given** I click the reset link
   **When** I enter a new valid password
   **Then** my password is updated and I can log in

## Technical Details

### Architecture

[High-level architecture or approach]

- Components involved: [List key components]
- Data flow: [Describe how data flows through the system]
- Dependencies: [External services, libraries, or APIs]

### API Changes

[If applicable, describe API endpoints or changes]

#### New Endpoints

```
POST /api/v1/resource
GET  /api/v1/resource/{id}
```

#### Request/Response Examples

```json
// POST /api/v1/resource
{
  "name": "Example",
  "description": "This is an example"
}

// Response: 201 Created
{
  "id": "uuid-here",
  "name": "Example",
  "created_at": "2024-01-17T10:00:00Z"
}
```

### Database Changes

[If applicable, describe schema changes]

**New Tables:**
- `table_name`: [Description]

**Modified Tables:**
- `table_name`: Added columns: `column1`, `column2`

### Security Considerations

- [ ] Authentication required: [Yes/No]
- [ ] Authorization: [Who can access this feature?]
- [ ] Input validation: [What validation is needed?]
- [ ] Data encryption: [Any sensitive data?]
- [ ] Rate limiting: [Should this be rate limited?]

## Edge Cases & Error Handling

1. **Edge case**: [Describe unusual scenario]
   - **Handling**: [How should we handle it?]

2. **Error**: [Type of error]
   - **Message**: [User-facing error message]
   - **Recovery**: [How can user recover?]

### Example:

1. **Edge case**: User requests password reset multiple times
   - **Handling**: Only send one email per 5-minute period, show message "Email already sent"

2. **Error**: Invalid email format
   - **Message**: "Please enter a valid email address"
   - **Recovery**: User can correct and resubmit

## Testing Strategy

### Unit Tests

- [ ] Test requirement 1
- [ ] Test requirement 2
- [ ] Test edge cases

### Integration Tests

- [ ] Test full user flow
- [ ] Test API endpoints
- [ ] Test error scenarios

### Manual Testing Checklist

- [ ] Happy path works end-to-end
- [ ] Error messages are clear and helpful
- [ ] UI/UX is intuitive
- [ ] Performance is acceptable
- [ ] Mobile responsive (if applicable)

## Dependencies

- **Blocked by**: [Other features or tasks that must complete first]
- **Blocks**: [Features that depend on this]
- **Related**: [Related features or specs]

## Timeline (Optional)

- **Estimated effort**: [e.g., 3-5 days]
- **Target completion**: [YYYY-MM-DD]
- **Actual completion**: [YYYY-MM-DD]

## Open Questions

- [ ] Question 1: [Something that needs clarification]
- [ ] Question 2: [Another open question]

## Implementation Notes

[Space for notes during implementation]

### Decisions Made

- [Date] - [Decision and rationale]

### Challenges Encountered

- [Date] - [Challenge and how it was resolved]

## References

- Design doc: [Link]
- API spec: [Link]
- Related tickets: [Links]

---

**Template Version**: 1.0
**Last Updated**: 2024-01-17
