# Agent: Test Reviewer

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: Medium

## Purpose

Comprehensive test suite analysis providing coverage assessment, quality evaluation, and improvement recommendations.

**Invocation**: `/testing:review` or `/testing:test-reviewer`

## Requirements

- [ ] Create `agents/test-reviewer.md` agent
- [ ] Analyze test coverage per module
- [ ] Evaluate test quality
- [ ] Assess test performance
- [ ] Generate prioritized recommendations
- [ ] Provide test stubs for missing tests

## User Stories

**As a** tech lead wanting a full test audit
**I want** an agent to comprehensively analyze my test suite
**So that** I understand coverage gaps and quality issues at a glance

**As a** developer assigned to improve test quality
**I want** a detailed analysis with actionable recommendations
**So that** I can prioritize improvements by impact and effort

## Acceptance Criteria

1. **Given** a developer runs `/testing:review`
   **When** the agent completes
   **Then** they receive:
     - Coverage metrics for each module
     - Test quality findings
     - List of untested functions
     - Recommendations with effort estimates

2. **Given** the agent identifies coverage gaps
   **When** it completes analysis
   **Then** it suggests specific test cases to add

3. **Given** test performance issues
   **When** agent analyzes tests
   **Then** it identifies slow tests and parallelization opportunities

## Capabilities

### 1. Coverage Analysis
- Calculate metrics per module/component
- Identify functions with zero coverage
- Identify branches without coverage
- Identify edge cases not covered
- Track coverage trends

### 2. Test Quality Evaluation
- Analyze test naming conventions
- Check test organization (unit, integration, e2e)
- Identify flaky test patterns
- Evaluate fixture usage
- Check for over-mocking

### 3. Test Performance Analysis
- Identify slow tests (>1 second)
- Find serial tests that could parallelize
- Recommend test ordering optimizations
- Suggest test categorization (fast/slow)

### 4. Recommendations
- Generate list of missing test cases
- Suggest framework improvements
- Recommend test data strategies
- Suggest CI/CD optimizations
- Identify legacy tests needing cleanup

## Technical Details

### Analysis Steps

```
1. Scan all test files
   ├─ Count tests per module
   ├─ Analyze test names
   └─ Extract test patterns

2. Analyze coverage data
   ├─ Calculate coverage per module
   ├─ Identify zero-coverage code
   └─ Find coverage gaps

3. Evaluate test quality
   ├─ Check test isolation
   ├─ Identify mocking issues
   └─ Analyze assertions

4. Performance analysis
   ├─ Measure test execution time
   ├─ Identify slow tests
   └─ Find parallelization opportunities

5. Generate comprehensive report
   ├─ Coverage metrics
   ├─ Quality findings
   ├─ Performance insights
   └─ Prioritized recommendations
```

### Report Structure

The agent generates a comprehensive report including:

**Executive Summary**:
- Overall Test Health Score (0-10)
- Coverage percentage
- Test Quality Score
- Performance metrics
- Best Practices adherence

**Coverage Analysis**:
- Overall coverage percentage
- Per-module breakdowns
- Untested modules with priority
- Coverage trends

**Test Quality Assessment**:
- Positive findings
- Issues found with context
- Recommended improvements

**Performance Analysis**:
- Total execution time
- Test categorization
- Slow test identification
- Parallelization recommendations

**Recommendations**:
- Prioritized by severity (CRITICAL, HIGH, MEDIUM, LOW)
- Effort estimates (hours/days)
- Impact assessment
- Test stubs ready to implement

## Edge Cases & Error Handling

1. **Edge case**: Agents running on very large codebase
   - **Handling**: Show progress and interim results
   - **Message**: "Analyzing (found 5000+ files). Interim results available."

2. **Edge case**: Mixed language project
   - **Handling**: Analyze each language separately
   - **Message**: "Found Python and JavaScript. Analyzing separately..."

3. **Error**: Cannot determine project structure
   - **Message**: "Could not determine project type. Please specify language."
   - **Recovery**: Ask user for project type

4. **Edge case**: Tests take >10 minutes to run
   - **Handling**: Offer to skip test execution
   - **Message**: "Tests take 12+ minutes. Analyze without running? (y/n)"

## Security Considerations

- [ ] Don't expose actual secrets in reports
- [ ] Flag security findings prominently
- [ ] Verify vulnerability data is current
- [ ] Sanitize file paths in reports

## Testing Strategy

- [ ] Agent specifications are clear
- [ ] Report templates are well-structured
- [ ] Analysis steps are achievable
- [ ] Effort estimates are reasonable
- [ ] Recommendations are actionable
- [ ] Run on sample projects
- [ ] Verify report accuracy
- [ ] Test error handling

## Dependencies

- **Blocked by**:
  - plugin-testing (plugin definition)
  - skill-testing-guidance
  - command-run-tests
- **Blocks**: None
- **Related**: agent-quality-checker (in code-quality plugin)

---

**See command-run-tests.md for quick test execution and coverage.**
