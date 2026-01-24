# Feature: Best Practices Plugin - Documentation

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-24
**Priority**: Medium

## Purpose

Add comprehensive documentation best practices to the best-practices plugin. This feature provides an auto-triggered documentation skill to help developers:

- Write complete and clear READMEs
- Document code with proper comments and docstrings
- Create API documentation
- Maintain architecture documentation
- Follow documentation standards
- Keep documentation up-to-date

This skill ensures projects are well-documented for current and future team members.

## Requirements

- [ ] Create `skills/documentation/SKILL.md` - Auto-triggered documentation guidance
- [ ] Provide README completeness checklist
- [ ] Provide API documentation patterns
- [ ] Provide code comment best practices
- [ ] Provide architecture documentation guidance
- [ ] Provide changelog maintenance guidance
- [ ] Support multiple documentation tools (Sphinx, Swagger, etc.)
- [ ] Provide language-agnostic documentation patterns

## User Stories

**As a** developer on-boarding to a project
**I want** clear documentation to understand the codebase
**So that** I can contribute effectively without constant questions

**As a** API consumer
**I want** clear API documentation with examples
**So that** I can integrate correctly on the first try

**As a** project maintainer
**I want** Claude to remind me about documentation
**So that** I keep docs in sync with code changes

**As a** user of open-source software
**I want** comprehensive project documentation
**So that** I can understand and use the project successfully

## Acceptance Criteria

1. **Given** a developer creates a project
   **When** they ask about documentation
   **Then** Claude provides README structure and best practices

2. **Given** a developer creates a public function/method
   **When** Claude analyzes the code
   **Then** the documentation skill triggers with docstring guidance

3. **Given** a project has an API
   **When** Claude encounters API endpoints
   **Then** it suggests OpenAPI/Swagger documentation patterns

4. **Given** a developer updates code
   **When** they don't update documentation
   **Then** Claude suggests documenting the changes

5. **Given** a project lacks architecture documentation
   **When** Claude analyzes the codebase
   **Then** it suggests architecture documentation benefits

## Technical Details

### Skill: Documentation

**File**: `skills/documentation/SKILL.md`

**Purpose**: Auto-triggered skill that ensures proper documentation coverage and provides guidance.

**YAML Frontmatter**:
```yaml
---
name: documentation
description: Ensures complete and clear documentation at project, API, and code levels
---
```

**Key Sections**:

1. **When to Trigger This Skill**
   - User creating a new project
   - Public functions/methods without docstrings
   - API endpoints without documentation
   - User asks about documentation
   - Code changes without documentation updates
   - README missing or incomplete

2. **Project-Level Documentation (README.md)**

   **Essential Sections**:
   ```markdown
   # Project Name

   Brief description (1-2 sentences)

   ## Quick Start
   - How to install
   - How to run basic example
   - Link to full documentation

   ## Features
   - What does it do?
   - Why should someone use it?

   ## Installation
   - Step-by-step installation
   - System requirements
   - Dependencies

   ## Usage
   - Common use cases
   - Code examples
   - Configuration options

   ## Documentation
   - Links to full docs
   - API reference
   - Architecture docs

   ## Contributing
   - How to contribute
   - Development setup
   - Testing guidelines

   ## License
   - License type
   - Link to LICENSE file

   ## Support
   - Contact/issue tracker
   - Community channels
   ```

3. **API Documentation**

   **OpenAPI/Swagger Patterns**:
   - Endpoint documentation
   - Request/response schemas
   - Error codes
   - Authentication requirements
   - Example requests and responses

   **REST Endpoint Documentation**:
   ```
   GET /api/users/{id}

   Description: Retrieve user by ID

   Parameters:
   - id (path): User ID (required)

   Response (200):
   {
     "id": "123",
     "name": "John",
     "email": "john@example.com"
   }

   Errors:
   - 404: User not found
   - 401: Unauthorized
   ```

4. **Code Documentation**

   **Docstring Patterns**:
   ```python
   def calculate_total(items: List[Item], tax_rate: float = 0.1) -> float:
       """
       Calculate total price including tax.

       Args:
           items: List of items to total
           tax_rate: Tax rate as decimal (default: 0.1 for 10%)

       Returns:
           Total price including tax

       Raises:
           ValueError: If tax_rate is negative

       Example:
           >>> items = [Item(10), Item(20)]
           >>> calculate_total(items, 0.1)
           33.0
       """
   ```

   **Comment Best Practices**:
   - Explain WHY, not WHAT
   - Keep comments current with code
   - Use clear language
   - Avoid obvious comments
   - Link to issues/specs

5. **Architecture Documentation**

   **Structure**:
   ```markdown
   # Architecture

   ## Overview
   High-level system design

   ## Components
   - Component A: Responsibility
   - Component B: Responsibility

   ## Data Flow
   Diagram and explanation of data movement

   ## Design Decisions
   - Decision 1: Rationale
   - Decision 2: Rationale

   ## Trade-offs
   What was chosen and what was rejected

   ## Scalability
   How does this scale?
   ```

6. **API Documentation Tools**
   - OpenAPI/Swagger for REST APIs
   - GraphQL schema for GraphQL
   - Protocol Buffers documentation
   - gRPC service definitions

7. **Changelog Maintenance**

   **Format** (Keep a Changelog):
   ```markdown
   # Changelog

   ## [1.1.0] - 2026-01-24

   ### Added
   - New feature X
   - New feature Y

   ### Changed
   - Modified behavior of Z

   ### Fixed
   - Fixed bug in module A

   ### Deprecated
   - Old API endpoint (use new one)

   ### Removed
   - Removed legacy feature
   ```

8. **Documentation Completeness Checklist**
   - [ ] README exists and covers basics
   - [ ] Installation instructions are clear
   - [ ] Quick start example works
   - [ ] Public APIs documented
   - [ ] Common use cases explained
   - [ ] Configuration documented
   - [ ] Troubleshooting section included
   - [ ] Contributing guidelines provided
   - [ ] Code examples are current
   - [ ] Architecture documented
   - [ ] Changelog maintained
   - [ ] License specified
   - [ ] Contact/support info provided

9. **Language-Specific Guidance**
   - **Python**: docstrings (Google, NumPy, Sphinx style)
   - **JavaScript**: JSDoc comments
   - **Go**: godoc comments
   - **Java**: Javadoc
   - **Ruby**: YARD documentation

10. **Documentation Tools**
    - Sphinx for Python documentation
    - MkDocs for general project documentation
    - Swagger/OpenAPI for APIs
    - TypeDoc for TypeScript
    - GitBook for multi-page documentation

## Acceptance Criteria Details

### Detailed Documentation Requirements

**Minimum for Public Projects**:
- README.md (500+ words)
- API documentation
- Contributing guidelines
- License

**Recommended for Teams**:
- Architecture documentation
- Development setup guide
- Deployment guide
- Troubleshooting guide
- Changelog/Release notes
- FAQ

**Full Documentation Package**:
- All above items
- Tutorials and examples
- Performance tuning guide
- Migration guides
- Code comments on complex logic
- Design decision document

## Edge Cases & Error Handling

1. **Edge case**: Project with no external users
   - **Handling**: Recommend internal documentation
   - **Message**: "Even for internal projects, document architecture"

2. **Edge case**: Very simple project
   - **Handling**: Provide minimal documentation template
   - **Message**: "This project is simple. Here's a minimal README template."

3. **Edge case**: Rapidly changing project
   - **Handling**: Emphasize keeping docs in sync
   - **Message**: "Rapidly changing project? Establish doc update cadence."

4. **Error**: Code examples in docs are outdated
   - **Handling**: Check examples against actual code
   - **Message**: "Found stale code examples. Update them?"

5. **Edge case**: Multi-language documentation need
   - **Handling**: Suggest i18n approach
   - **Message**: "Need docs in multiple languages? Consider i18n."

## Security Considerations

- [ ] Don't document sensitive credentials
- [ ] Don't include real API keys in examples
- [ ] Warn about security-sensitive configurations
- [ ] Document authentication requirements
- [ ] Include security best practices
- [ ] Document security-related configuration

## Testing Strategy

### Validation

- [ ] SKILL.md structure is valid
- [ ] Documentation templates are complete
- [ ] Example code follows best practices
- [ ] Checklist items are comprehensive
- [ ] Templates work for various project types

### Manual Testing

- [ ] Apply documentation checklist to sample projects
- [ ] Review generated documentation templates
- [ ] Verify template completeness
- [ ] Test with Python, JavaScript, Go projects
- [ ] Verify language-specific guidance is accurate

## Dependencies

- **Blocked by**: plugin-best-practices-setup
- **Blocks**: None (parallel feature)
- **Related**:
  - plugin-best-practices-code-quality (code style affects docs)
  - plugin-best-practices-testing (document test examples)

## Implementation Notes

### Decisions Made

- **No separate command for documentation**: Skill is triggered auto as part of normal workflow
- **Checklist-based approach**: Simple way to verify documentation completeness
- **Templates for common sections**: Accelerates documentation creation
- **Language-agnostic patterns**: Apply across all programming languages

### Documentation Maturity Levels

**Level 1 - Minimal**:
- README with basic description
- Installation instructions
- Simple usage example

**Level 2 - Adequate**:
- Complete README
- API documentation
- Development setup guide
- Contributing guidelines

**Level 3 - Comprehensive**:
- All Level 2 items
- Architecture documentation
- Troubleshooting guide
- Multiple examples
- Changelog

**Level 4 - Excellent**:
- All Level 3 items
- Tutorials
- Performance guide
- FAQ
- Video guides (optional)

### Documentation Tools Integration

**Python**:
- Sphinx + Read the Docs
- pdoc for auto-documentation

**JavaScript**:
- JSDoc + TypeDoc
- Swagger UI for APIs

**General**:
- MkDocs for static docs
- GitHub Pages for hosting

## Open Questions

- [ ] Should we enforce specific documentation tools per language?
  - *Decision pending*: Recommend but don't enforce
- [ ] How often should documentation be reviewed?
  - *Decision pending*: Suggest quarterly minimum reviews

## References

- Sphinx Documentation: https://www.sphinx-doc.org/
- JSDoc: https://jsdoc.app/
- Keep a Changelog: https://keepachangelog.com/
- OpenAPI Specification: https://spec.openapis.org/
- Python Docstring Conventions: https://peps.python.org/pep-0257/
- Write the Docs: https://www.writethedocs.org/

---

**Template Version**: 1.0
**Last Updated**: 2026-01-24
