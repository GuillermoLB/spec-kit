# Skill: Testing Best Practices Guidance

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: High

## Purpose

Auto-triggered skill that provides testing patterns when developers write test code or ask about testing.

## Requirements

- [ ] Create `skills/testing/SKILL.md`
- [ ] Trigger when test files created
- [ ] Provide testing patterns (unit, integration, E2E)
- [ ] Support multiple frameworks
- [ ] Guide TDD workflow
- [ ] Cover coverage analysis best practices
- [ ] Address mocking and fixtures
- [ ] Identify and prevent common pitfalls

## Trigger Conditions

The skill should trigger when:
- Detecting test files (test_*.py, *.test.js, etc.)
- User asks about testing or test coverage
- User implementing features that need tests
- User debugging failing tests

## Key Topics

1. **Testing Patterns**
   - Unit testing strategies
   - Integration testing patterns
   - End-to-end testing approaches
   - Isolation and dependencies

2. **Framework-Specific Guidance**
   - Python: pytest, unittest, nose2
   - JavaScript: jest, mocha, vitest
   - Go: testing, testify, ginkgo
   - Ruby: RSpec, minitest
   - Java: JUnit, TestNG

3. **Best Practices**
   - Test naming conventions
   - Test organization
   - DRY principles (fixtures, factories)
   - Parametrization
   - Markers/tags

4. **Mocking and Fixtures**
   - Unit mock patterns
   - Database mocking
   - HTTP mocking
   - File system mocking
   - Fixture vs factory pattern

5. **TDD Workflow**
   - Red-Green-Refactor cycle
   - When to use TDD
   - TDD with spec-driven development
   - Example walkthrough

6. **Coverage Analysis**
   - Coverage goals and targets
   - Coverage tools per language
   - Interpreting coverage reports
   - Improving coverage

7. **Common Pitfalls**
   - Over-mocking
   - Testing implementation vs. behavior
   - Flaky tests and how to fix them
   - Test data management
   - Testing async code

## Acceptance Criteria

1. **Given** a developer creates a test file
   **When** Claude analyzes the code
   **Then** the skill triggers with patterns

2. **Given** a developer asks about TDD
   **When** Claude responds
   **Then** it provides Red-Green-Refactor guidance

3. **Given** a developer requests coverage help
   **When** the skill triggers
   **Then** it explains coverage best practices

## Dependencies

- **Blocked by**: plugin-testing (plugin definition)
- **Blocks**: None
- **Related**: command-run-tests, agent-test-reviewer

---

**See command-run-tests.md and agent-test-reviewer.md for command and agent specs.**
