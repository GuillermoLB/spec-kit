# Feature: Best Practices Plugin - Testing

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-24
**Priority**: High

## Purpose

Add comprehensive testing support to the best-practices plugin. This feature provides an auto-triggered testing skill and a user-invoked command to help developers:

- Write comprehensive test suites with proper coverage
- Understand testing patterns and best practices
- Analyze test coverage and identify gaps
- Follow test-driven development (TDD) workflows
- Support multiple testing frameworks across languages

## Requirements

- [ ] Create `skills/testing/SKILL.md` - Auto-triggered testing guidance
- [ ] Create `commands/run-tests.md` - Test execution and analysis command
- [ ] Support Python testing (pytest, unittest)
- [ ] Support JavaScript testing (jest, mocha, vitest)
- [ ] Support Go testing (testing, testify, ginkgo)
- [ ] Support TDD workflow guidance
- [ ] Support test coverage analysis
- [ ] Support mock/fixture patterns
- [ ] Provide framework-specific best practices

## User Stories

**As a** developer writing tests
**I want** Claude to automatically suggest testing patterns when I write test code
**So that** I can follow best practices and maintain high test quality

**As a** test-driven developer
**I want** Claude to guide me through Red-Green-Refactor cycles
**So that** I can practice TDD effectively

**As a** developer reviewing test coverage
**I want** to run a command that analyzes my test suite
**So that** I can identify untested code paths and add missing tests

**As a** new team member
**I want** to see testing standards and patterns used by my team
**So that** I can write tests consistent with our standards

## Acceptance Criteria

1. **Given** a developer creates a test file
   **When** Claude analyzes the code
   **Then** the testing skill triggers with relevant patterns and best practices

2. **Given** a developer runs `/best-practices:run-tests`
   **When** the command executes
   **Then** tests run and Claude provides:
     - Overall coverage percentage
     - Lines of code that are uncovered
     - Recommendations for missing test cases
     - Priority ranking of coverage gaps

3. **Given** a Python project with pytest
   **When** `/best-practices:run-tests` executes
   **Then** it detects pytest and runs with coverage analysis

4. **Given** a JavaScript project with jest
   **When** `/best-practices:run-tests` executes
   **Then** it detects jest and runs with coverage analysis

5. **Given** a developer asks about TDD
   **When** Claude responds
   **Then** it provides Red-Green-Refactor cycle guidance

## Technical Details

### Skill: Testing

**File**: `skills/testing/SKILL.md`

**Purpose**: Auto-triggered skill that provides testing patterns when developers write test code or ask about testing.

**YAML Frontmatter**:
```yaml
---
name: testing
description: Provides testing patterns, best practices, and TDD workflows
---
```

**Key Sections**:

1. **When to Trigger This Skill**
   - Detecting test files (test_*.py, *.test.js, etc.)
   - User asks about testing or test coverage
   - User implementing features that need tests
   - User debugging failing tests

2. **Testing Patterns**
   - Unit testing strategies
   - Integration testing patterns
   - End-to-end testing approaches
   - Isolation and dependencies

3. **Framework-Specific Guidance**
   - Python: pytest, unittest, nose2
   - JavaScript: jest, mocha, vitest
   - Go: testing, testify, ginkgo
   - Ruby: RSpec, minitest
   - Java: JUnit, TestNG

4. **Best Practices**
   - Test naming conventions
   - Test organization
   - DRY principles (fixtures, factories)
   - Parametrization
   - Markers/tags

5. **Mocking and Fixtures**
   - Unit mock patterns
   - Database mocking
   - HTTP mocking
   - File system mocking
   - Fixture vs factory pattern

6. **TDD Workflow**
   - Red-Green-Refactor cycle explanation
   - When to use TDD
   - TDD with spec-driven development
   - Example walkthrough

7. **Coverage Analysis**
   - Coverage goals and targets
   - Coverage tools per language
   - Interpreting coverage reports
   - Improving coverage

8. **Common Pitfalls**
   - Over-mocking
   - Testing implementation vs. behavior
   - Flaky tests and how to fix them
   - Test data management
   - Testing async code

### Command: run-tests

**File**: `commands/run-tests.md`

**Purpose**: User-invoked command that executes test suites, analyzes coverage, and provides recommendations.

**Workflow**:

1. **Detect project**
   - Language detection (Python, JavaScript, Go, etc.)
   - Test framework detection (pytest, jest, testify, etc.)
   - Test directory detection (tests/, __tests__, spec/, etc.)

2. **Ask questions**
   ```
   - Which tests to run? (unit / integration / e2e / all)
   - Generate coverage report? (yes / no)
   - Include performance tests? (yes / no)
   ```

3. **Execute tests**
   - Run with appropriate framework and options
   - Capture output and coverage data
   - Handle failures gracefully

4. **Analyze results**
   - Parse coverage reports
   - Identify uncovered code
   - Identify flaky tests
   - Measure test performance

5. **Generate report**
   ```
   Coverage Report:
   - Overall: 82%
   - Uncovered lines: 247
   - Uncovered branches: 53

   Recommendations:
   1. [Priority] Module X: 0% coverage (5 functions)
   2. [Medium] Error handling paths in module Y
   3. [Low] Edge cases in module Z

   Suggested new tests:
   - test_module_x_initialization
   - test_module_x_error_handling
   - test_edge_case_with_empty_input
   ```

6. **Offer improvements**
   - Generate test stubs
   - Suggest test frameworks
   - Recommend coverage goals

**Invocation**: `/best-practices:run-tests`

**Example Output**:
```
Test Execution Report
====================

Framework: pytest
Coverage: 82% (↑ from 79%)

Coverage Summary:
- src/core: 95%
- src/utils: 68%
- src/api: 75%

Top coverage gaps:
1. src/utils/formatting.py: 0% coverage
   Functions: format_date, format_currency, format_text

2. src/api/routes.py: 40% coverage
   Missing: error handlers, edge cases

Recommendations:
- Add 8 tests to reach 85% coverage
- Focus on error handling in api/routes.py
- Test edge cases in utils/formatting.py
```

### Framework Support

**Python**:
- pytest (recommended)
- unittest
- nose2
- Coverage.py for coverage reports

**JavaScript/TypeScript**:
- jest (recommended)
- mocha
- vitest
- nyc for coverage

**Go**:
- testing (standard library)
- testify (assertions)
- ginkgo (BDD)
- coverage tool

**Ruby**:
- RSpec
- minitest

**Java**:
- JUnit
- TestNG

### Test Coverage Goals

**Recommended by team**:
- Minimum: 80% code coverage
- Target: 85-90% coverage
- High-value areas: >95% (core logic, security)
- Less critical: 70%+ (utilities, helpers)

## Edge Cases & Error Handling

1. **Edge case**: Project with no tests
   - **Handling**: Offer to generate test scaffolds
   - **Message**: "No tests found. Would you like to create test stubs?"

2. **Edge case**: Unsupported test framework
   - **Handling**: Provide generic testing patterns
   - **Message**: "Framework [name] not recognized. Showing general pytest patterns."

3. **Error**: Tests fail during execution
   - **Handling**: Show failures and suggest debugging
   - **Message**: "3 tests failed. Show failure details?"

4. **Edge case**: Coverage report not generated
   - **Handling**: Provide manual coverage analysis
   - **Message**: "Coverage tool not found. Analyzing code to estimate coverage."

5. **Edge case**: Mixed test frameworks in project
   - **Handling**: Detect and run each framework
   - **Message**: "Found pytest and jest. Running both..."

6. **Edge case**: Tests depend on external services
   - **Handling**: Recommend mocking external dependencies
   - **Message**: "Tests require live API. Should we mock these services?"

## Security Considerations

- [ ] No sensitive data in test examples
- [ ] Test credentials clearly marked as fake
- [ ] No hardcoded secrets in test files
- [ ] Test databases isolated from production
- [ ] Mock external services (no real API calls)
- [ ] Clear guidance on handling secrets in tests

## Testing Strategy

### Validation

- [ ] Verify SKILL.md has valid structure
- [ ] Verify command handles common frameworks
- [ ] Test with sample Python project (pytest)
- [ ] Test with sample JavaScript project (jest)
- [ ] Test with sample Go project (testing)

### Manual Testing

- [ ] Run on Python project without coverage setup
- [ ] Run on JavaScript project with coverage gaps
- [ ] Test framework detection accuracy
- [ ] Test coverage report parsing
- [ ] Test error message clarity

## Dependencies

- **Blocked by**: plugin-best-practices-setup
- **Blocks**: None (other features are parallel)
- **Related**: plugin-best-practices-ci-cd (uses test results)

## Implementation Notes

### Decisions Made

- **pytest as primary Python framework**: Most popular, best coverage support
- **jest as primary JavaScript framework**: Default in React/Node.js
- **80% as minimum coverage**: Industry standard balance
- **Generic patterns for unsupported frameworks**: Broad applicability

### Framework Detection Heuristics

```
Python:
- Look for pytest.ini, setup.cfg, pyproject.toml
- Look for conftest.py
- Look for requirements*.txt with pytest

JavaScript:
- Look for jest.config.js
- Look for package.json with jest config
- Look for .jestrc files

Go:
- Look for *_test.go files
- Standard library testing is built-in
```

### Coverage Tool Integration

- Python: `pytest --cov` or `coverage` CLI
- JavaScript: `jest --coverage` or `nyc`
- Go: `go test -cover`

## Open Questions

- [ ] Should we support cross-language projects?
  - *Decision pending*: Analyze and report each language separately
- [ ] What coverage threshold should trigger warnings?
  - *Decision pending*: Below 80% flags yellow, below 70% flags red

## References

- pytest Documentation: https://docs.pytest.org/
- Jest Documentation: https://jestjs.io/
- Go Testing: https://golang.org/pkg/testing/
- Coverage.py: https://coverage.readthedocs.io/
- Code Coverage Best Practices: https://testdriven.io/

---

**Template Version**: 1.0
**Last Updated**: 2026-01-24
