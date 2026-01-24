# Feature: Best Practices Plugin - Analysis Agents

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-24
**Priority**: Medium

## Purpose

Add specialized analysis agents to the best-practices plugin. These agents provide comprehensive, multi-faceted analysis by combining insights from testing, CI/CD, code quality, and documentation skills. They help teams:

- Conduct thorough test suite reviews and improvements
- Perform complete codebase quality assessments
- Identify improvement priorities
- Get actionable recommendations

Agents differ from skills and commands by providing deep, multi-step analysis rather than quick guidance or single actions.

## Requirements

- [ ] Create `agents/test-reviewer.md` - Comprehensive test suite analyzer
- [ ] Create `agents/quality-checker.md` - Full codebase quality assessor
- [ ] Test reviewer provides:
  - [ ] Coverage analysis
  - [ ] Test quality evaluation
  - [ ] Missing test recommendations
  - [ ] Performance issues
- [ ] Quality checker provides:
  - [ ] Code complexity analysis
  - [ ] Security vulnerability scan
  - [ ] Dependency health check
  - [ ] Documentation completeness
  - [ ] Performance assessment

## User Stories

**As a** tech lead wanting a full test audit
**I want** an agent to comprehensively analyze my test suite
**So that** I understand coverage gaps and quality issues at a glance

**As a** developer assigned to improve code quality
**I want** a detailed analysis of the entire codebase
**So that** I can prioritize improvements by impact and effort

**As a** team planning a code quality sprint
**I want** a comprehensive assessment with prioritized recommendations
**So that** we can plan work effectively

## Acceptance Criteria

1. **Given** a developer runs `/best-practices:test-reviewer`
   **When** the agent completes
   **Then** they receive:
     - Coverage metrics for each module
     - Test quality findings
     - List of untested functions
     - Recommendations with effort estimates

2. **Given** a developer runs `/best-practices:quality-checker`
   **When** the agent analyzes the codebase
   **Then** they receive:
     - Overall quality score
     - Breakdown by category (complexity, security, etc.)
     - Critical issues requiring immediate action
     - Actionable recommendations prioritized by impact

3. **Given** the test-reviewer agent runs
   **When** it identifies coverage gaps
   **Then** it suggests specific test cases to add

4. **Given** the quality-checker agent runs
   **When** it identifies security issues
   **Then** it flags them as CRITICAL and provides remediation steps

5. **Given** a developer wants improvement effort estimates
   **When** agents provide recommendations
   **Then** each includes time estimate (hours/days)

## Technical Details

### Agent: Test Reviewer

**File**: `agents/test-reviewer.md`

**Purpose**: Comprehensive test suite analysis providing coverage assessment, quality evaluation, and improvement recommendations.

**Capabilities**:

1. **Coverage Analysis**
   - Calculate metrics per module/component
   - Identify functions with zero coverage
   - Identify branches without coverage
   - Identify edge cases not covered
   - Track coverage trends

2. **Test Quality Evaluation**
   - Analyze test naming conventions
   - Check test organization (unit, integration, e2e)
   - Identify flaky test patterns
   - Evaluate fixture usage
   - Check for over-mocking

3. **Test Performance Analysis**
   - Identify slow tests (>1 second)
   - Find serial tests that could parallelize
   - Recommend test ordering optimizations
   - Suggest test categorization (fast/slow)

4. **Recommendations**
   - Generate list of missing test cases
   - Suggest framework improvements
   - Recommend test data strategies
   - Suggest CI/CD optimizations
   - Identify legacy tests needing cleanup

**Analysis Steps**:

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

**Report Structure**:

```
Test Suite Review Report
========================

Project: my-api
Language: Python
Framework: pytest

Executive Summary
─────────────────
Overall Test Health: 7.5/10
├─ Coverage: 82% (↑ from 79%)
├─ Test Quality: 7.2/10
├─ Performance: 8.1/10
└─ Best Practices: 6.9/10

Coverage Analysis
─────────────────
Overall: 82% (Good)
├─ core/auth: 95% (Excellent)
├─ core/api: 78% (Adequate)
├─ utils: 65% (Needs improvement)
└─ config: 0% (Zero coverage)

Untested Modules:
1. config.py - 0% coverage
   Functions: 5
   Priority: LOW (configuration file)

2. utils/formatting.py - 18% coverage
   Functions: 8 (7 untested)
   Priority: MEDIUM

3. api/routes.py - 63% coverage
   Functions: 12 (4 untested)
   Priority: HIGH

Test Quality Assessment
──────────────────────
Positive Findings:
✓ Good test organization (unit/integration/e2e)
✓ Clear test naming conventions
✓ Proper use of fixtures
✓ Isolated unit tests

Issues Found:
⚠ 3 flaky tests (database-dependent)
⚠ Over-mocking in auth tests
⚠ 2 tests with unclear assertions
⚠ Missing error handling tests

Performance Analysis
────────────────────
Total Execution: 15.3 seconds
├─ Unit tests: 3.2s (27 tests)
├─ Integration: 9.1s (12 tests)
└─ E2E: 3.0s (5 tests)

Slow Tests:
1. test_large_data_processing: 2.3s
2. test_database_migration: 1.8s
3. test_api_performance: 1.2s

Recommendation: Run slow tests separately

Recommendations (Prioritized)
────────────────────────────
🔴 CRITICAL (Do immediately)
1. Add error handling tests to api/routes.py
   Effort: 3-4 hours
   Impact: 15% coverage increase
   Suggested tests: 5 new test functions

🟠 HIGH (This sprint)
1. Reduce coupling in auth tests
   Effort: 2-3 hours
   Impact: Better test reliability
   Action: Remove mocks, use fixtures

2. Add tests for utils/formatting.py
   Effort: 4-6 hours
   Impact: 40% coverage increase for module
   Suggested tests: 7 new test functions

🟡 MEDIUM (Next sprint)
1. Fix flaky database tests
   Effort: 4-5 hours
   Impact: More reliable CI/CD

2. Add config module tests
   Effort: 1-2 hours
   Impact: 100% coverage for module

Low Priority:
- Improve slow test performance (refactor as bonus)

Test Stubs Generated
───────────────────
Ready to implement:
```

**Invocation**: `/best-practices:test-reviewer`

### Agent: Quality Checker

**File**: `agents/quality-checker.md`

**Purpose**: Comprehensive codebase quality assessment combining complexity, security, maintainability, and dependency analysis.

**Capabilities**:

1. **Complexity Analysis**
   - Calculate cyclomatic complexity
   - Identify complex functions/methods
   - Find deep nesting patterns
   - Measure class sizes
   - Detect code duplication

2. **Security Vulnerability Scanning**
   - Check for injection vulnerabilities
   - Identify hardcoded credentials
   - Find unsafe deserialization
   - Check cryptographic patterns
   - Identify OWASP Top 10 issues

3. **Maintainability Assessment**
   - Evaluate code organization
   - Check naming conventions
   - Identify dead code
   - Find code duplication
   - Assess test coverage

4. **Dependency Analysis**
   - Identify outdated packages
   - Flag security vulnerabilities
   - Check for unused dependencies
   - Identify license compatibility
   - Monitor abandoned projects

5. **Documentation Evaluation**
   - Check README completeness
   - Evaluate docstring coverage
   - Verify API documentation
   - Check for architecture docs
   - Assess comment quality

**Analysis Steps**:

```
1. Repository scan
   ├─ Detect language and framework
   ├─ Identify project structure
   └─ Locate dependencies

2. Static analysis
   ├─ Measure code metrics
   ├─ Identify issues
   └─ Calculate scores

3. Security analysis
   ├─ Scan for vulnerabilities
   ├─ Check dependencies
   └─ Review practices

4. Documentation review
   ├─ Check README
   ├─ Analyze docstrings
   └─ Review comments

5. Generate comprehensive assessment
   ├─ Overall quality score
   ├─ Category breakdown
   ├─ Critical findings
   └─ Prioritized recommendations
```

**Report Structure**:

```
Comprehensive Code Quality Assessment
======================================

Project: e-commerce-api
Language: Python
Last Assessment: 2026-01-24

QUALITY SCORE: 6.8/10 (↓ from 7.2)

Category Breakdown:
├─ Complexity: 6.5/10 (⚠ Medium)
├─ Security: 7.8/10 (✓ Good)
├─ Maintainability: 6.2/10 (⚠ Medium)
├─ Test Coverage: 8.1/10 (✓ Good)
├─ Dependency Health: 7.5/10 (✓ Good)
└─ Documentation: 5.9/10 (⚠ Needs work)

🔴 CRITICAL (Fix Immediately)
───────────────────────────────
1. Security: Hardcoded AWS credentials in config.py:42
   Risk Level: CRITICAL
   Exposure: Database access, data breach
   Time to Fix: 30 minutes
   Action: Use environment variables

2. Security: SQL injection vulnerability in user_repo.py:128
   Risk Level: CRITICAL
   Exposure: Database compromise
   Time to Fix: 1-2 hours
   Action: Use parameterized queries

3. Dependency: django-rest-framework 3.2.0 has 2 vulnerabilities
   Risk: Authentication bypass, XSS
   Upgrade to: 3.14.0
   Time: 30 minutes

🟠 HIGH PRIORITY (This Sprint)
──────────────────────────────
1. Complexity: checkout_service.py has 5 functions >15 complexity
   Current: 18-24 complexity
   Target: <10 complexity
   Effort: 6-8 hours
   Benefit: Easier testing, fewer bugs

2. Maintainability: 8% code duplication detected
   Files: users.py, auth.py, utils.py
   Duplicated code: 120 lines
   Effort: 4-6 hours
   Benefit: Reduced maintenance burden

3. Documentation: README lacks API documentation
   Missing sections: Endpoints, Auth, Examples
   Effort: 2-3 hours
   Benefit: Easier for new developers

🟡 MEDIUM PRIORITY (Next Sprint)
────────────────────────────────
1. Complexity: 12 functions with complexity >10
   Effort: 10-15 hours total
   Suggestion: Refactor with guard clauses

2. Coverage: Error handling untested in 4 modules
   Missing tests: 15 test cases
   Effort: 8-10 hours
   Benefit: Better error handling

3. Dependencies: numpy 1.19.0 (2 years old)
   Latest: 1.26.0
   Action: Update when possible
   Risk: Medium (compatibility checks needed)

🟢 LOW PRIORITY (Quality Improvements)
──────────────────────────────────────
1. Documentation: Add module-level docstrings
   Coverage: 60% (target: 100%)
   Effort: 2-3 hours

2. Style: 23 PEP 8 violations
   Effort: 1 hour (auto-fix with black)

Effort Summary:
────────────────
Critical fixes: 2 hours
High priority: 18 hours
Medium priority: 25 hours
Low priority: 3 hours
─────────────────────────
TOTAL: 48 hours (~6 days for one developer)

Recommended Improvement Plan:
1. Fix critical security issues (2 hours)
2. Refactor complex functions (8 hours)
3. Remove code duplication (5 hours)
4. Add documentation (3 hours)
5. Remaining improvements (30 hours)

Dependencies to Update (with vulnerabilities):
- django-rest-framework: 3.2.0 → 3.14.0
- requests: 2.25.0 → 2.31.0
- urllib3: 1.26.0 → 2.0.0

License Compatibility:
All dependencies: ✓ Compatible (MIT, Apache 2.0)

Next Steps:
1. Address critical security issues immediately
2. Plan refactoring sprint (8-10 hours)
3. Update dependencies (1-2 hours)
4. Improve documentation (2-3 hours)
```

**Invocation**: `/best-practices:quality-checker`

## Comparison: Skills vs Commands vs Agents

| Aspect | Skill | Command | Agent |
|--------|-------|---------|-------|
| Trigger | Auto | User | User |
| Scope | Guidance | Single action | Deep analysis |
| Depth | Quick tips | Specific task | Comprehensive |
| Output | Suggestions | Config/results | Detailed report |
| Time | Immediate | Minutes | 1-5 minutes |
| Example | "When writing tests, try..." | "Generate CI pipeline" | "Full test suite audit" |

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

4. **Edge case**: Project with no dependencies
   - **Handling**: Skip dependency analysis
   - **Message**: "No external dependencies detected."

5. **Edge case**: Tests take >10 minutes to run
   - **Handling**: Offer to skip test execution
   - **Message**: "Tests take 12+ minutes. Analyze without running? (y/n)"

## Security Considerations

- [ ] Don't expose actual secrets in reports
- [ ] Flag security findings prominently
- [ ] Verify vulnerability data is current
- [ ] Sanitize file paths in reports
- [ ] Warn about sensitive code patterns

## Testing Strategy

### Validation

- [ ] Agent specifications are clear and complete
- [ ] Report templates are well-structured
- [ ] Analysis steps are achievable
- [ ] Effort estimates are reasonable
- [ ] Recommendations are actionable

### Manual Testing

- [ ] Run test-reviewer on sample projects
- [ ] Run quality-checker on sample projects
- [ ] Verify report accuracy
- [ ] Test error handling
- [ ] Validate recommendations

## Dependencies

- **Blocked by**:
  - plugin-best-practices-setup (foundation)
  - plugin-best-practices-testing (test analysis)
  - plugin-best-practices-code-quality (quality metrics)
- **Blocks**: None
- **Related**: All other plugin features

## Implementation Notes

### Decisions Made

- **Separate agents from commands**: Agents provide comprehensive analysis vs quick actions
- **Comprehensive reporting**: Full context helps prioritization
- **Effort estimates**: Helps teams plan improvement work
- **Actionable findings**: Every issue has suggested remediation

### Report Generation

- Combine data from multiple analysis sources
- Prioritize by severity and impact
- Include context and rationale
- Provide implementation guidance
- Estimate effort for improvements

### Analysis Depth

**Test Reviewer focuses on**:
- Coverage metrics
- Test quality
- Test performance

**Quality Checker focuses on**:
- Code complexity
- Security vulnerabilities
- Maintainability
- Dependencies
- Documentation

## Open Questions

- [ ] Should agents offer to implement improvements automatically?
  - *Decision pending*: Recommend manual review for safety
- [ ] Cache analysis results for faster subsequent runs?
  - *Decision pending*: Could optimize for large projects
- [ ] Generate trend reports over time?
  - *Decision pending*: Future enhancement

## References

- Testing Best Practices: https://testdriven.io/
- Code Quality Metrics: https://www.sonarqube.org/
- Security Scanning: https://cheatsheetseries.owasp.org/
- OWASP Top 10: https://owasp.org/www-project-top-ten/

---

**Template Version**: 1.0
**Last Updated**: 2026-01-24
