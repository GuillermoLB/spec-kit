# Living Documentation: Theory & Practice

A comprehensive guide to implementing living documentation in your projects.

**Last Updated**: 2026-01-24
**Research Date**: 2026-01-24

---

## Table of Contents

1. [What is Living Documentation?](#what-is-living-documentation)
2. [Core Principles](#core-principles)
3. [Living vs Traditional Documentation](#living-vs-traditional-documentation)
4. [Documentation as Code (Docs as Code)](#documentation-as-code)
5. [Executable Documentation](#executable-documentation)
6. [Implementation Patterns](#implementation-patterns)
7. [Tools & Technologies](#tools--technologies)
8. [Best Practices](#best-practices)
9. [Spec-Kit Integration](#spec-kit-integration)
10. [Getting Started](#getting-started)

---

## What is Living Documentation?

Living documentation is a **dynamic approach to documentation** that evolves in real-time as your codebase and project requirements change.

### Key Characteristics

✅ **Always Accurate** - Documentation stays synchronized with the actual codebase
✅ **Automatically Updated** - Changes to code trigger documentation updates
✅ **Collaborative** - Multiple team members can contribute insights
✅ **Executable** - Documentation can be tested to prove accuracy
✅ **Version Controlled** - Documented alongside code in git
✅ **Self-Documenting** - Code structure informs documentation structure

### The Fundamental Problem It Solves

Traditional documentation quickly becomes **outdated** because:
- Manual updates are tedious and forgotten
- Code changes aren't reflected in docs
- Disconnect between implementation and documentation
- Knowledge becomes scattered across wikis, comments, and Slack

Living documentation solves this by making documentation:
- Part of the development workflow
- Automated through CI/CD
- Validated through tests
- Embedded in the codebase itself

---

## Core Principles

Based on **Cyrille Martraire's "Living Documentation" methodology**, living documentation should be:

### 1. **Reliable**

Documentation reflects actual system behavior, not intended behavior.

```markdown
❌ Bad: "The API returns paginated results"
✅ Good: "The API returns paginated results with max 100 items per page (see code: api/pagination.py:42)"
```

- Link documentation to code locations
- Show actual implementation details
- Include version information
- Document edge cases and limitations

### 2. **Low Effort**

Documentation should be generated or maintained automatically, not manually.

```python
# Instead of writing API docs separately:
def get_users(page: int = 1, limit: int = 100) -> List[User]:
    """
    Retrieve paginated list of users.

    Args:
        page: Page number (default: 1)
        limit: Items per page (default: 100, max: 1000)

    Returns:
        List[User]: Users on requested page

    Example:
        >>> users = get_users(page=2, limit=50)
    """
    pass

# Documentation can be auto-generated from docstrings
# No separate markdown file needed
```

- Use auto-documentation tools (Sphinx, pdoc, Swagger)
- Generate from code comments and type hints
- Let tests serve as documentation
- Keep source-of-truth in one place

### 3. **Collaborative**

Documentation evolves with team input, not owned by one person.

```markdown
# Feature: User Authentication

**Status**: In Progress
**Owner**: @frontend-team, @backend-team
**Last Updated**: 2026-01-24
**Reviewers**: @security-team

## Implementation Details
- Created by: @alice (2026-01-20)
- Updated by: @bob (2026-01-23)
```

- Use specs for collaborative documentation
- Track who contributed what
- Version control all documentation
- Link to pull requests and commits

### 4. **Insightful**

Documentation provides context: the "why" not just the "what".

```markdown
❌ Bad: "We use Redis for caching"
✅ Good:
"We use Redis for caching to reduce database load by ~60%
(see performance tests: tests/performance/cache_impact.py).
Alternative considered: Memcached, rejected due to poor cluster support."
```

- Document decisions and trade-offs
- Include performance implications
- Link to related decisions
- Explain architectural choices

---

## Living vs Traditional Documentation

### Side-by-Side Comparison

| Aspect | Traditional | Living |
|--------|-------------|--------|
| **Update Cycle** | Periodic (quarterly, manual) | Continuous (every commit) |
| **Source of Truth** | Separate wiki/docs folder | Code itself + specs |
| **Accuracy** | Degrades over time | Always current |
| **Effort** | High (manual updates) | Low (automated generation) |
| **Validation** | Manual review (if at all) | Automated tests/CI |
| **Collaboration** | Async, often siloed | Real-time, integrated |
| **Versioning** | Separate from code | Same git repo, same version |
| **Examples** | Often outdated | Always work (executable) |

### Real-World Example: API Documentation

#### ❌ Traditional Approach

```markdown
# User API Documentation

## GET /api/users

Returns a list of users.

**Parameters:**
- page (optional): Page number
- limit (optional): Items per page

**Response:**
```json
{
  "users": [...],
  "total": 100
}
```

# Problem: If API changes, docs must be manually updated
# Outdated docs are worse than no docs
```

#### ✅ Living Documentation Approach

```python
# api/users.py
from fastapi import FastAPI, Query
from typing import List

app = FastAPI()

@app.get("/users")
async def get_users(
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    limit: int = Query(100, ge=1, le=1000, description="Items per page, max 1000")
) -> dict:
    """
    Retrieve paginated list of users.

    Returns:
        dict: Object containing 'users' array and 'total' count

    Example:
        GET /users?page=2&limit=50
        Response: {"users": [...], "total": 100}
    """
    pass

# FastAPI auto-generates OpenAPI docs at /docs
# Docs are always in sync with code
# Examples are tested to ensure they work
```

```python
# tests/test_users_api.py
async def test_get_users_pagination():
    """
    Living test: serves as both test AND documentation.
    Proves the API actually works this way.
    """
    response = await client.get("/users?page=2&limit=50")
    assert response.status_code == 200
    assert "users" in response.json()
    assert len(response.json()["users"]) <= 50
```

```bash
# CI/CD Pipeline
# 1. Run tests (validates examples work)
# 2. Generate API docs from code
# 3. Publish docs automatically
# 4. Deploy with matching version

pytest  # If tests fail, docs are wrong
mkdocs build  # Generates docs from code
```

---

## Documentation as Code

**Documentation as Code (Docs as Code)** is the practice of treating documentation exactly like code.

### Core Principles

### 1. **Use Plain Text Markup**

Documentation in version-controlled format (Markdown, reStructuredText, AsciiDoc):

```markdown
# Architecture

## Components

### API Layer
- FastAPI server
- Rate limiting middleware
- Error handling middleware

### Database Layer
- PostgreSQL
- SQLAlchemy ORM
- Alembic migrations
```

**Benefits**:
- Version controlled in git
- Reviewable in pull requests
- Mergeable with clear diffs
- Searchable in code editors

### 2. **Store with Code**

Keep documentation files in the same repository:

```
project/
├── README.md              # Project overview
├── docs/
│   ├── ARCHITECTURE.md    # System design
│   ├── API.md            # API reference
│   ├── SETUP.md          # Development setup
│   └── CONCEPTS.md       # Key concepts
├── specs/                # Feature specifications
│   ├── features/
│   └── architecture/
├── src/
└── tests/
```

**Benefits**:
- Documentation versioned with code
- Easy to update during code review
- Same git history for docs and code
- No separate wiki to maintain

### 3. **Use Same Workflow as Code**

Documentation changes follow the same process:

```
1. Create branch: git checkout -b docs/update-api-docs
2. Edit documentation files
3. Create pull request
4. Team review and feedback
5. Merge to main
6. Auto-publish updated docs
```

**Benefits**:
- Documentation reviewed like code
- Clear change tracking
- Audit trail of who changed what
- Can request changes before merge

### 4. **Automate Generation & Publishing**

Use CI/CD to generate and publish docs:

```yaml
# .github/workflows/docs.yml
name: Generate and Publish Docs

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'src/**'

jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      # Generate docs from code
      - run: mkdocs build

      # Test that docs build correctly
      - run: npm run test:docs

      # Publish to GitHub Pages
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

**Benefits**:
- Docs published automatically
- No manual deployment
- Same version as code
- Tested before publishing

---

## Executable Documentation

Executable documentation goes beyond describing what code does—it **proves** the documentation is accurate by running tests.

### The Key Insight

> If your documentation includes code examples, those examples should be executable and tested. If they fail, your documentation is wrong.

### Approaches

### 1. **Specification by Example**

Write specifications as executable examples:

```python
# tests/features/user_login.py
"""
Feature: User Authentication

Scenario: User logs in with valid credentials
    Given: User "alice@example.com" with password "secret123"
    When: User submits login form
    Then: User is authenticated
    And: User sees dashboard
"""

def test_user_can_login_with_valid_credentials():
    # Arrange
    user = create_user("alice@example.com", password="secret123")

    # Act
    response = client.post("/login", {
        "email": "alice@example.com",
        "password": "secret123"
    })

    # Assert
    assert response.status_code == 200
    assert response.json()["authenticated"] == True
```

This test serves **two purposes**:
- **Documentation**: Shows exactly how login works
- **Validation**: Proves it actually works this way

### 2. **Documented Examples in Code**

Examples in docstrings that are tested:

```python
def calculate_discount(price: float, customer_type: str) -> float:
    """
    Calculate discount based on customer type.

    Args:
        price: Original price
        customer_type: 'premium' or 'standard'

    Returns:
        float: Discounted price

    Examples:
        >>> calculate_discount(100.0, 'standard')
        100.0

        >>> calculate_discount(100.0, 'premium')
        80.0  # 20% discount
    """
    if customer_type == "premium":
        return price * 0.8
    return price

# Test the docstring examples:
# python -m doctest mymodule.py
# If examples fail, docstring is wrong
```

### 3. **Test-Driven Documentation**

Write tests first, then implementation:

```python
# tests/test_password_validation.py
def test_password_must_be_at_least_8_characters():
    """
    Documentation: Password must be at least 8 characters
    Proof: This test validates it
    """
    with pytest.raises(ValueError, match="at least 8 characters"):
        create_user(email="user@example.com", password="short")

def test_password_must_contain_uppercase():
    """
    Documentation: Password must contain uppercase letter
    Proof: This test validates it
    """
    with pytest.raises(ValueError, match="uppercase"):
        create_user(email="user@example.com", password="lowercase123")

def test_password_must_contain_number():
    """
    Documentation: Password must contain at least one number
    Proof: This test validates it
    """
    with pytest.raises(ValueError, match="number"):
        create_user(email="user@example.com", password="NoNumbers!")
```

These tests **are** the documentation of password requirements.

### 4. **API Documentation Generation**

Auto-generate API docs from code and tests:

```python
# api/endpoints/users.py
from fastapi import FastAPI

app = FastAPI(
    title="User API",
    description="Manage user accounts",
    version="1.0.0"
)

@app.get(
    "/users/{user_id}",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"}
    }
)
def get_user(user_id: int):
    """
    Get user by ID.

    Returns user details including name, email, and account status.
    """
    pass

# FastAPI generates OpenAPI docs automatically
# Docs always match actual API at /docs
```

### Benefits of Executable Documentation

✅ **Accuracy**: Examples actually work
✅ **Currency**: Changes fail tests immediately
✅ **Trust**: You can rely on documentation
✅ **Low Maintenance**: Tests serve as docs
✅ **Quality**: Developers write better examples

---

## Implementation Patterns

### Pattern 1: Living Architecture Documentation

```markdown
# Architecture

**Status**: Living Document
**Last Updated**: 2026-01-24
**Owners**: @architecture-team

## Current System Design

### Components
- [API Layer](#api-layer) - FastAPI
- [Database Layer](#database-layer) - PostgreSQL
- [Cache Layer](#cache-layer) - Redis

### API Layer

**Implementation**: `src/api/` (FastAPI)
**Related Spec**: `specs/architecture/api-design.md`
**Status**: Implemented

Components:
- `api/routers/` - Endpoint definitions
- `api/schemas/` - Request/response models
- `api/middleware/` - Request processing

See tests: `tests/test_api/`

### Decision Log

#### Decision: Use PostgreSQL for primary storage
**Date**: 2025-06-15
**Rationale**: ACID compliance, JSON support, scalability
**Alternatives Considered**:
- MongoDB (rejected: requires transactions for data consistency)
- MySQL (rejected: JSON support inferior to PostgreSQL)
**Status**: Current decision, revisit if data exceeds 1TB
**Related Tests**: `tests/database/test_transactions.py`
```

### Pattern 2: Living API Documentation

```python
# api/users.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    """User model - always matches database schema"""
    id: int
    email: str
    name: str
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "alice@example.com",
                "name": "Alice",
                "created_at": "2026-01-01T00:00:00"
            }
        }

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """
    Get user by ID.

    This endpoint retrieves user information including email,
    name, and account creation date.

    **Parameters:**
    - user_id: The unique identifier of the user

    **Returns:**
    User object with all fields populated

    **Example:**
    ```
    GET /users/1
    Response:
    {
        "id": 1,
        "email": "alice@example.com",
        "name": "Alice",
        "created_at": "2026-01-01T00:00:00"
    }
    ```

    **Errors:**
    - 404: User not found
    """
    pass
```

FastAPI generates OpenAPI docs automatically at `/docs`

### Pattern 3: Living Spec-Driven Documentation

```markdown
# Feature: User Authentication

**Status**: In Progress
**Owner**: @security-team
**Last Updated**: 2026-01-24
**Related Tests**: `tests/test_auth/`
**Related Code**: `src/auth/`
**Related Spec**: `specs/features/user-authentication.md`

## Current Implementation Status

- [x] Login with email/password
- [x] JWT token generation
- [ ] Social login (Google, GitHub)
- [ ] Two-factor authentication

## Acceptance Criteria (Implemented)

✅ User can log in with email and password
✅ Password must be at least 8 characters
✅ JWT token expires after 24 hours
✅ Failed attempts are logged

See: `tests/test_auth/test_login.py`

## Recent Changes

- **2026-01-23**: Added rate limiting to login endpoint (5 attempts/15min)
  - See: `src/auth/middleware.py:42`
  - Tests: `tests/test_auth/test_rate_limiting.py`

- **2026-01-20**: Improved error messages for security
  - Now returns generic "Invalid credentials" instead of revealing if email exists
  - See: `src/auth/errors.py`
```

---

## Tools & Technologies

### Documentation Generation

| Tool | Purpose | Format | Best For |
|------|---------|--------|----------|
| **Sphinx** | Python documentation | reStructuredText, Markdown | Python projects |
| **MkDocs** | Static site generator | Markdown | Team wikis, guides |
| **Swagger/OpenAPI** | API documentation | YAML/JSON | REST APIs |
| **pdoc** | Python auto-docs | HTML | Quick API reference |
| **JavaDoc** | Java documentation | Java comments | Java projects |
| **TSDoc** | TypeScript docs | TypeScript comments | TypeScript/JavaScript |

### Testing Documentation

| Tool | Purpose | Language | Use Case |
|------|---------|----------|----------|
| **pytest** | Testing framework | Python | Python tests |
| **Jest** | Testing framework | JavaScript | JavaScript tests |
| **Cucumber** | BDD testing | Gherkin | Behavior specs |
| **Relish** | Test documentation | Gherkin | Publish test specs |
| **Doctest** | Docstring tests | Python | Python docstrings |

### CI/CD for Documentation

| Service | Purpose | Integration |
|---------|---------|-------------|
| **GitHub Actions** | Automate docs build/publish | GitHub native |
| **GitLab CI** | Automate docs build/publish | GitLab native |
| **Netlify** | Host & auto-publish docs | GitHub/GitLab |
| **ReadTheDocs** | Host Sphinx docs | GitHub integration |
| **GitHub Pages** | Free static hosting | GitHub native |

### Version Control

| Approach | Description | Example |
|----------|-------------|---------|
| **Docs as Code** | Docs in same repo as code | `/docs/` folder in main repo |
| **Separate Docs Repo** | Documentation in dedicated repo | `company/docs-repo` |
| **Monorepo** | Multiple projects, one repo | Nx, Turborepo style |
| **Integration with Code** | Docs generated from code | FastAPI `/docs` endpoint |

---

## Best Practices

### 1. **Make Documentation Easy to Find**

```markdown
# Good Doc Structure

project/
├── README.md              # Start here
├── GETTING_STARTED.md     # Quick setup (5 min)
├── ARCHITECTURE.md        # System design
├── docs/
│   ├── API.md            # API reference
│   ├── DATABASE.md       # Data models
│   ├── TESTING.md        # Testing guide
│   ├── DEPLOYMENT.md     # Deployment process
│   └── TROUBLESHOOTING.md # Common issues
└── specs/
    ├── features/
    ├── api/
    └── architecture/
```

**Link from README** to guide readers:

```markdown
# MyProject

## Quick Links
- **Getting Started**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **API Docs**: [docs/API.md](docs/API.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
```

### 2. **Keep Examples Working**

```python
# ✅ Good: Example is tested
def parse_json(text: str) -> dict:
    """
    Parse JSON string.

    Example:
        >>> parse_json('{"name": "Alice"}')
        {'name': 'Alice'}

    The above example is run by: pytest --doctest-modules
    """
    return json.loads(text)

# ❌ Bad: Example might be outdated
def parse_json(text: str) -> dict:
    """Parse JSON string."""
    return json.loads(text)
    # No examples, so no accountability
```

### 3. **Document the "Why" Not Just "What"**

```markdown
❌ Bad:
"We use Redis for caching"

✅ Good:
"We use Redis for caching to reduce database load by ~60%
during peak hours (see performance test: tests/perf/cache_impact.py).

Alternative solutions considered:
- Memcached: Rejected due to poor cluster/HA support
- PostgreSQL query caching: Rejected, insufficient for hot data

Decision made: 2025-08-15, reviewed: 2026-01-15"
```

### 4. **Link Documentation to Code**

```markdown
# Architecture Decision: Use FastAPI

**Implementation**:
- Main app: `src/main.py:1-50`
- Router registration: `src/api/routers/__init__.py:10-30`
- Middleware: `src/api/middleware.py`

**Tests**:
- Basic routing: `tests/test_api/test_routing.py`
- Error handling: `tests/test_api/test_errors.py`
- Performance: `tests/perf/test_endpoints.py`

**Related Spec**:
- `specs/architecture/api-framework.md`
- Status: Implemented ✅
```

### 5. **Use Markdown Frontmatter for Metadata**

```markdown
---
title: User Authentication
status: In Progress
owner: security-team
last_updated: 2026-01-24
version: 2.0
reviewers: alice, bob
---

# User Authentication

Content here...
```

### 6. **Include Version Information**

```markdown
# API Reference

**Current Version**: 2.1.0
**Last Updated**: 2026-01-24
**Python Version**: 3.11+
**FastAPI Version**: 0.104+

## Changelog

### v2.1.0 (2026-01-24)
- Added rate limiting to login endpoint
- Improved error messages for security

### v2.0.0 (2025-12-15)
- **BREAKING**: Changed auth to JWT tokens
- Removed session-based auth
```

### 7. **Separate Developer and User Documentation**

```
docs/
├── README.md              # User overview
├── GETTING_STARTED.md     # User setup
├── API.md                 # API users
├── dev/
│   ├── ARCHITECTURE.md    # Dev: system design
│   ├── SETUP.md          # Dev: dev environment
│   ├── CONTRIBUTING.md   # Dev: contribution guide
│   ├── TESTING.md        # Dev: testing approach
│   └── DEPLOYMENT.md     # Dev: deployment process
```

---

## Spec-Kit Integration

### How Living Documentation Fits Spec-Kit

Spec-kit enforces spec-driven development. Living documentation extends this:

```
Spec-Driven Development + Living Documentation
         ↓
    Both emphasize: Requirements must be explicit and validated
```

### Pattern: Specs as Living Documentation

```markdown
# Feature: Export Data to CSV

**Status**: In Progress
**Owner**: @data-team
**Last Updated**: 2026-01-24
**Related Code**: `src/export/csv.py`
**Related Tests**: `tests/test_export/test_csv.py`

## Purpose
Users need to export query results to CSV for analysis in Excel/Sheets

## Requirements

- [x] Export all selected rows to CSV format
- [x] Include column headers
- [x] Handle special characters properly
- [ ] Support custom column ordering
- [ ] Compress large exports (>10MB)

## Acceptance Criteria

✅ User can click "Export as CSV" button
✅ File downloads with timestamp in filename
✅ CSV is properly formatted and opens in Excel
✅ Special characters (quotes, newlines) are escaped

Tests verify all criteria: `tests/test_export/test_csv.py`

## Implementation Details

### File Format
- UTF-8 encoding
- CRLF line endings (Windows compatibility)
- Double-quote escaping for fields with special chars

### Code Location
- Export logic: `src/export/csv.py:42-100`
- Request handler: `src/api/routers/export.py:10-30`
- Tests: `tests/test_export/test_csv.py`

### Recent Changes
- **2026-01-23**: Added support for timezone-aware datetime
  - See: `src/export/formatters.py:50-60`
  - Tests: `tests/test_export/test_datetimes.py`

### Testing Evidence
All acceptance criteria are tested. To verify:
```bash
pytest tests/test_export/test_csv.py -v
```

Expected output:
```
test_export_csv_format PASSED
test_special_character_escaping PASSED
test_column_headers PASSED
test_file_download PASSED
```
```

### Pattern: Architecture Documentation

Keep `specs/architecture.md` as a living document:

```markdown
---
status: Living Document
last_updated: 2026-01-24
owner: architecture-team
---

# Architecture

## Current State

### Technology Stack
- **Language**: Python 3.11
- **Web Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Queue**: Celery + RabbitMQ
- **Deployment**: Docker, Kubernetes

### System Diagram
```
[Client] → [API Gateway] → [FastAPI App] → [PostgreSQL]
                         ↓
                      [Redis Cache]
                         ↓
                      [Celery Workers] → [RabbitMQ]
```

### Key Decisions

#### Decision: Microservices vs Monolith
**Current**: Monolith (FastAPI single app)
**Status**: Revisit when reaching 10M users or adding async job processing
**Why**: Simpler to develop, debug, and deploy. Can scale vertically first.
**When to split**: When different services need independent scaling

See test performance baseline: `tests/perf/baseline_2026_01_24.py`

#### Decision: PostgreSQL for Primary Data
**Current**: Using PostgreSQL
**Status**: Stable, reviewed Jan 2026
**Why**: ACID compliance, JSON support, powerful query language
**Alternative**: None at this scale

See: `tests/database/test_transactions.py`

## Recent Updates

### 2026-01-20: Added Redis Caching
- Reduced database queries by 60% for hot data
- See: `src/cache/strategies.py`
- Tests: `tests/perf/cache_impact.py`
- Spec: `specs/features/caching-strategy.md` ✅ Implemented

### 2025-12-15: Migrated to Async/Await
- Improved request handling with asyncio
- See: `src/api/` all endpoints now async
- Tests: `tests/test_api/test_async_handling.py`
- Spec: `specs/architecture/async-migration.md` ✅ Implemented
```

---

## Getting Started

### Step 1: Choose Your Documentation Approach

**For API-Centric Projects**:
```
→ Use FastAPI auto-generated OpenAPI docs
→ Keep examples in docstrings
→ Test examples with doctest
```

**For Service/Library Projects**:
```
→ Use Sphinx or MkDocs
→ Store docs with code in /docs
→ Generate API reference from docstrings
```

**For Enterprise/Complex Projects**:
```
→ Combine specs/, docs/, and code documentation
→ Use multiple tools (OpenAPI + Sphinx + custom)
→ Automate generation and publishing
```

### Step 2: Set Up Documentation Infrastructure

```bash
# Create docs directory
mkdir -p docs

# Create basic structure
touch docs/ARCHITECTURE.md
touch docs/API.md
touch docs/TESTING.md
touch docs/DEPLOYMENT.md

# Create specs directory (already exists in spec-kit)
mkdir -p specs/architecture
```

### Step 3: Add Documentation to CI/CD

```yaml
# .github/workflows/docs.yml
name: Build and Publish Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'src/**'
      - 'specs/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      # Generate docs
      - run: pip install mkdocs
      - run: mkdocs build

      # Test docs (optional)
      - run: pytest --doctest-modules src/

      # Publish
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

### Step 4: Document Key Decision Points

In `specs/architecture.md`, document:

```markdown
## Key Decisions

### Decision: [Topic]
**Date**: YYYY-MM-DD
**Status**: Current | Reviewing | Deprecated
**Rationale**: Why this decision?
**Alternatives**: What else was considered?
**Evidence**: Related tests, metrics, specs
**Review Schedule**: When to revisit?
```

### Step 5: Embed Tests as Documentation

```python
# tests/test_user_auth.py
"""
Living documentation for user authentication.

These tests prove the authentication system works exactly as described.
If a test fails, the documentation is wrong.
"""

def test_user_login_with_valid_credentials():
    """
    Documentation: Users can log in with email and password.
    Proof: This test validates it works.
    """
    user = create_user("alice@example.com", password="secret123")
    response = login(email="alice@example.com", password="secret123")
    assert response.status_code == 200
    assert "token" in response.json()

def test_password_requires_minimum_8_characters():
    """
    Documentation: Passwords must be at least 8 characters.
    Proof: This test validates the constraint.
    """
    with pytest.raises(ValueError, match="at least 8"):
        create_user("bob@example.com", password="short")
```

### Step 6: Link Everything Together

In README.md:

```markdown
# MyProject

## Documentation

- **Quick Start**: [GETTING_STARTED.md](GETTING_STARTED.md) (5 min)
- **Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **API Reference**: [docs/API.md](docs/API.md)
- **Testing**: [docs/TESTING.md](docs/TESTING.md)
- **Feature Specs**: [specs/features/](specs/features/)

## Guarantees

🔒 All documentation is tested and verified
⚡ Examples are executable and maintained
📅 Last verified: [Auto-updated by CI/CD]
✅ Coverage: [API: 100%, Core: 95%, Tests: 100%]
```

---

## Summary

Living documentation represents a **paradigm shift** from static, manual docs to dynamic, automated, tested documentation:

| Old Approach | New Approach (Living Docs) |
|--------------|---------------------------|
| Write docs, they rot | Docs generated from code, stay current |
| Manual updates | Automated via CI/CD |
| Examples might be wrong | Examples are tested and proven correct |
| Separate wiki | Docs in code repository |
| Trust issues | Validated by tests |
| Scattered knowledge | Single source of truth |

### Key Takeaway

> **Living documentation is not a tool—it's a culture shift toward making documentation a first-class citizen of your codebase.**

Start small:
1. Pick one project component
2. Document it with code comments + tests
3. Auto-generate docs
4. Expand to other areas

Your future self (and team) will thank you for docs that actually work.

---

## References & Further Reading

- [Living Documentation: Continuous Knowledge Sharing by Design](https://www.oreilly.com/library/view/living-documentation-continuous/9780134689418/) - Cyrille Martraire
- [Living Documentation by Cyrille Martraire](https://leanpub.com/livingdocumentation)
- [Docs as Code - Write the Docs Guide](https://www.writethedocs.org/guide/docs-as-code/)
- [Documentation as Code - Home Office Engineering](https://engineering.homeoffice.gov.uk/patterns/docs-as-code/)
- [Executable Documentation Benefits](https://apiumacademy.com/executable-documentation-benefits/)
- [Specification by Example](https://gojko.net/2008/11/08/specification-by-example/)
- [GitHub - Tools and Techniques for Code Documentation](https://github.com/resources/articles/tools-and-techniques-for-effective-code-documentation/)
- [Swimm - Code Documentation Best Practices](https://swimm.io/learn/code-documentation/code-documentation-benefits-challenges-and-tips-for-success/)

---

**Last Updated**: 2026-01-24
**Status**: Living Document - Please contribute improvements!
**Owner**: Documentation Team
**Next Review**: 2026-04-24
