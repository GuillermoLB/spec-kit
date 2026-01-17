# Feature: Testing Plugin

**Status**: Draft
**Owner**: spec-kit development team
**Last Updated**: 2026-01-17
**Priority**: Medium

## Purpose

Create a comprehensive testing plugin that provides pytest patterns, test organization strategies, mocking techniques, and TDD workflows. This plugin helps developers write high-quality tests following industry best practices.

## Requirements

- [ ] SKILL.md with testing patterns and best practices
- [ ] pytest configuration templates (pytest.ini, conftest.py)
- [ ] Test example templates showing different testing patterns
- [ ] Fixture examples for common scenarios
- [ ] Mocking strategies (unittest.mock, pytest-mock)
- [ ] Coverage configuration (.coveragerc)
- [ ] Factory pattern examples for test data
- [ ] TDD workflow guidance
- [ ] Integration with install.sh
- [ ] Validation in verify.sh

## User Stories

**As a** developer writing tests
**I want** pytest patterns and templates
**So that** I can write comprehensive tests efficiently

**As a** TDD practitioner
**I want** test-driven development workflow guidance
**So that** I can follow TDD methodology effectively

**As a** team lead
**I want** consistent testing standards
**So that** my team writes high-quality, maintainable tests

## Acceptance Criteria

1. **Given** I install the testing plugin
   **When** I check .claude/skills/testing/
   **Then** I see SKILL.md and template files

2. **Given** I activate the testing plugin
   **When** I ask Claude to help with tests
   **Then** Claude provides pytest patterns and best practices

3. **Given** I copy the pytest.ini template
   **When** I run pytest
   **Then** tests execute with proper configuration

4. **Given** I use the fixture templates
   **When** I create tests
   **Then** I have reusable test fixtures

5. **Given** I follow TDD workflow from plugin
   **When** I develop features
   **Then** I write tests first, then implementation

## Technical Details

### Plugin Structure

```
plugins/testing/
├── skill.md                   # Main plugin file
└── templates/
    ├── conftest.py            # Pytest fixtures
    ├── pytest.ini             # Pytest configuration
    ├── .coveragerc            # Coverage configuration
    ├── test_example.py        # Example test file
    ├── factories.py           # Factory pattern for test data
    └── mocking_examples.py    # Mocking patterns
```

### SKILL.md Content

**Sections:**

1. **When to Use This Skill**
2. **Testing Patterns**
   - Unit testing
   - Integration testing
   - End-to-end testing
3. **Pytest Best Practices**
   - Test organization
   - Fixture usage
   - Parametrization
   - Markers
4. **Mocking Strategies**
   - unittest.mock patterns
   - pytest-mock usage
   - HTTP mocking
   - Database mocking
5. **Test Data Management**
   - Factory pattern
   - Fixtures vs factories
   - Test data cleanup
6. **Coverage and Quality**
   - Coverage configuration
   - Coverage goals
   - Quality metrics
7. **TDD Workflow**
   - Red-Green-Refactor cycle
   - When to use TDD
   - TDD with spec-driven development

### Template: pytest.ini

```ini
[pytest]
# Test discovery
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Output options
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80

# Markers
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow-running tests
    smoke: Smoke tests for CI

# Ignore
norecursedirs = .git .tox dist build *.egg venv
```

### Template: conftest.py

```python
"""
Shared pytest fixtures and configuration.
"""
import pytest
from typing import Generator

@pytest.fixture
def sample_data() -> dict:
    """Provide sample test data."""
    return {
        "id": "123",
        "name": "Test Item",
        "active": True
    }

@pytest.fixture
def mock_database(monkeypatch):
    """Mock database connection."""
    class MockDB:
        def __init__(self):
            self.data = {}

        def get(self, key):
            return self.data.get(key)

        def set(self, key, value):
            self.data[key] = value

    db = MockDB()
    monkeypatch.setattr("your_module.database", db)
    return db

@pytest.fixture
def api_client():
    """Provide test API client."""
    from your_app import create_app

    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="session")
def database_setup():
    """Setup test database (session scope)."""
    # Setup
    create_test_database()

    yield

    # Teardown
    drop_test_database()
```

### Template: factories.py

```python
"""
Factory pattern for creating test data.
"""
from typing import Dict, Any
from datetime import datetime
from uuid import uuid4

class UserFactory:
    """Factory for creating test users."""

    @staticmethod
    def create(
        email: str = None,
        name: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a test user with default or custom values.

        Args:
            email: User email (default: random)
            name: User name (default: "Test User")
            **kwargs: Additional fields

        Returns:
            User dictionary
        """
        return {
            "id": str(uuid4()),
            "email": email or f"test{uuid4().hex[:8]}@example.com",
            "name": name or "Test User",
            "created_at": datetime.utcnow().isoformat(),
            **kwargs
        }

    @staticmethod
    def create_batch(count: int, **kwargs) -> list:
        """Create multiple test users."""
        return [UserFactory.create(**kwargs) for _ in range(count)]


class TodoFactory:
    """Factory for creating test todos."""

    @staticmethod
    def create(
        title: str = None,
        completed: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a test todo."""
        return {
            "id": str(uuid4()),
            "title": title or "Test Todo",
            "completed": completed,
            "created_at": datetime.utcnow().isoformat(),
            **kwargs
        }
```

### Template: mocking_examples.py

```python
"""
Examples of mocking patterns for tests.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import requests

# Example 1: Mocking functions
def test_function_mock():
    """Mock a function call."""
    with patch('module.function_name') as mock_func:
        mock_func.return_value = 42

        result = call_function_that_uses_it()

        assert result == 42
        mock_func.assert_called_once()


# Example 2: Mocking HTTP requests
def test_http_request_mock():
    """Mock HTTP request."""
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        response = requests.get('https://api.example.com/data')

        assert response.status_code == 200
        assert response.json() == {"key": "value"}


# Example 3: Mocking database
@pytest.fixture
def mock_db():
    """Mock database for testing."""
    with patch('app.database.get_connection') as mock_conn:
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"id": 1, "name": "Test"}
        mock_cursor.fetchall.return_value = [{"id": 1}, {"id": 2}]

        mock_conn.return_value.cursor.return_value = mock_cursor

        yield mock_conn


def test_with_mock_db(mock_db):
    """Test using mocked database."""
    result = fetch_user_from_db(user_id=1)

    assert result["name"] == "Test"
    mock_db.assert_called()


# Example 4: Mocking environment variables
def test_env_variable_mock(monkeypatch):
    """Mock environment variable."""
    monkeypatch.setenv("API_KEY", "test-key-123")

    api_key = get_api_key_from_env()

    assert api_key == "test-key-123"


# Example 5: Mocking file operations
def test_file_read_mock(tmp_path):
    """Mock file reading."""
    # Create temporary file
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    result = read_file(test_file)

    assert result == "test content"
```

### Template: test_example.py

```python
"""
Example test file showing pytest patterns.
"""
import pytest
from your_module import Calculator

class TestCalculator:
    """Test suite for Calculator."""

    @pytest.fixture
    def calculator(self):
        """Provide calculator instance."""
        return Calculator()

    def test_add(self, calculator):
        """Test addition."""
        result = calculator.add(2, 3)
        assert result == 5

    def test_subtract(self, calculator):
        """Test subtraction."""
        result = calculator.subtract(5, 3)
        assert result == 2

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 6),
        (0, 5, 0),
        (-2, 3, -6),
    ])
    def test_multiply_parametrized(self, calculator, a, b, expected):
        """Test multiplication with multiple inputs."""
        result = calculator.multiply(a, b)
        assert result == expected

    def test_divide_by_zero(self, calculator):
        """Test division by zero raises error."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

    @pytest.mark.slow
    def test_complex_operation(self, calculator):
        """Test complex operation (marked as slow)."""
        # Long-running test
        pass
```

### Template: .coveragerc

```ini
[run]
source = src
omit =
    */tests/*
    */venv/*
    */__pycache__/*
    */site-packages/*

[report]
precision = 2
show_missing = True
skip_covered = False

exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod

[html]
directory = htmlcov
```

### TDD Workflow Guidance

**Red-Green-Refactor Cycle:**

```python
# 1. RED - Write failing test first
def test_create_user():
    user = create_user(email="test@example.com", name="Test")
    assert user["email"] == "test@example.com"
    assert user["name"] == "Test"
    # This fails because create_user doesn't exist yet

# 2. GREEN - Write minimal code to pass
def create_user(email, name):
    return {"email": email, "name": name}
    # Test passes now

# 3. REFACTOR - Improve code quality
def create_user(email: str, name: str) -> dict:
    """Create user with validation."""
    if not email or "@" not in email:
        raise ValueError("Invalid email")
    if not name:
        raise ValueError("Name required")

    return {
        "id": str(uuid4()),
        "email": email,
        "name": name,
        "created_at": datetime.utcnow().isoformat()
    }
    # Tests still pass, code is better
```

### Security Considerations

- [ ] No sensitive data in test fixtures
- [ ] Test database isolated from production
- [ ] Mock external services (no real API calls in tests)
- [ ] Temporary files cleaned up after tests
- [ ] Test credentials clearly marked as fake

## Edge Cases & Error Handling

1. **Edge case**: Tests with external dependencies
   - **Handling**: Always mock external services, provide guidance in SKILL.md

2. **Edge case**: Flaky tests
   - **Handling**: Document strategies to identify and fix (retries, isolation)

3. **Error**: Coverage below threshold
   - **Message**: "Coverage 75% is below threshold of 80%"
   - **Recovery**: Identify uncovered code, add tests

## Testing Strategy

Since this is a plugin (not executable code), testing focuses on:

### Validation Tests

- [ ] Verify SKILL.md has valid YAML frontmatter
- [ ] Verify template files are syntactically valid Python
- [ ] Verify pytest.ini is valid configuration
- [ ] Verify .coveragerc is valid

### Manual Testing

- [ ] Install plugin in test project
- [ ] Copy templates and run pytest
- [ ] Verify templates work as expected
- [ ] Test with real pytest project

## Dependencies

- **Blocked by**: documentation-improvements (installation docs)
- **Blocks**: None
- **Related**: testing-infrastructure (uses these patterns), examples (can demonstrate plugin)

## Implementation Notes

### Decisions Made

- 2026-01-17 - Focus on pytest (most popular Python testing framework)
- 2026-01-17 - Include coverage by default (industry standard)
- 2026-01-17 - Factory pattern over fixtures for flexibility
- 2026-01-17 - Show both unittest.mock and pytest-mock

### Integration with install.sh

Add to plugin selection menu:

```bash
3) Testing Plugin - pytest patterns and TDD workflows
```

Update verify.sh:

```bash
echo "Plugin: testing"
check_file "plugins/testing/skill.md"
check_file "plugins/testing/templates/pytest.ini"
check_file "plugins/testing/templates/conftest.py"
```

## References

- pytest documentation: https://docs.pytest.org/
- Coverage.py: https://coverage.readthedocs.io/
- Testing best practices: https://testdriven.io/blog/testing-best-practices/

---

**Template Version**: 1.0
**Last Updated**: 2026-01-17
