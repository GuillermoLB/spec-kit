# Command: run-tests

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: High

## Purpose

Execute test suites, analyze coverage, and provide recommendations for improvement.

**Invocation**: `/testing:run-tests`

## Requirements

- [ ] Create `commands/run-tests.md` command
- [ ] Detect test framework (pytest, jest, testify, etc.)
- [ ] Execute tests with coverage analysis
- [ ] Parse coverage reports
- [ ] Identify coverage gaps
- [ ] Generate actionable recommendations
- [ ] Support Python, JavaScript, Go projects

## User Stories

**As a** developer reviewing test coverage
**I want** to run a command that analyzes my test suite
**So that** I can identify untested code paths and add missing tests

**As a** test-driven developer
**I want** to see coverage metrics easily
**So that** I can maintain high test quality

## Acceptance Criteria

1. **Given** a developer runs `/testing:run-tests`
   **When** the command executes
   **Then** tests run and Claude provides:
     - Overall coverage percentage
     - Lines of code that are uncovered
     - Recommendations for missing test cases
     - Priority ranking of coverage gaps

2. **Given** a Python project with pytest
   **When** `/testing:run-tests` executes
   **Then** it detects pytest and runs with coverage analysis

3. **Given** a JavaScript project with jest
   **When** `/testing:run-tests` executes
   **Then** it detects jest and runs with coverage analysis

## Technical Details

### Workflow

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
   - **Message**: "Framework [name] not recognized. Showing general patterns."

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

## Testing Strategy

- [ ] Verify command handles common frameworks
- [ ] Test with sample Python project (pytest)
- [ ] Test with sample JavaScript project (jest)
- [ ] Test with sample Go project (testing)
- [ ] Verify framework detection accuracy
- [ ] Test coverage report parsing
- [ ] Test error message clarity

## Dependencies

- **Blocked by**: plugin-testing (plugin definition)
- **Blocks**: None
- **Related**: skill-testing-guidance, agent-test-reviewer

---

**See agent-test-reviewer.md for comprehensive test suite analysis.**
