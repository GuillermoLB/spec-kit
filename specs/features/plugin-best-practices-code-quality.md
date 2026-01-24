# Feature: Best Practices Plugin - Code Quality

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-24
**Priority**: High

## Purpose

Add comprehensive code quality analysis to the best-practices plugin. This feature provides an auto-triggered code quality skill and a user-invoked command to help developers:

- Maintain consistent code style and formatting
- Identify code complexity issues
- Follow naming conventions and best practices
- Evaluate code maintainability
- Detect security vulnerabilities and anti-patterns
- Track dependency health

## Requirements

- [ ] Create `skills/code-quality/SKILL.md` - Auto-triggered code quality guidance
- [ ] Create `commands/check-quality.md` - Comprehensive quality assessment command
- [ ] Analyze code complexity (cyclomatic, cognitive)
- [ ] Check code style consistency
- [ ] Identify security vulnerabilities
- [ ] Evaluate test coverage impact
- [ ] Analyze code duplication
- [ ] Check dependency health and updates
- [ ] Provide language-agnostic patterns
- [ ] Generate actionable improvement recommendations

## User Stories

**As a** code reviewer
**I want** Claude to suggest code quality improvements
**So that** I can maintain high standards in my codebase

**As a** developer
**I want** to understand code complexity metrics
**So that** I can refactor complex code into simpler pieces

**As a** team lead
**I want** to see overall code quality trends
**So that** I can identify areas needing improvement

**As a** security-conscious developer
**I want** Claude to flag potential security issues
**So that** I can address them before production

## Acceptance Criteria

1. **Given** a developer runs `/best-practices:check-quality`
   **When** the command executes
   **Then** Claude generates a quality report with:
     - Code complexity metrics
     - Style consistency findings
     - Security vulnerability flags
     - Test coverage gaps
     - Dependency status
     - Prioritized recommendations

2. **Given** a codebase with high cyclomatic complexity
   **When** the skill analyzes code
   **Then** it identifies functions with >10 branches and suggests refactoring

3. **Given** a project with outdated dependencies
   **When** the quality check runs
   **Then** it flags vulnerable and outdated packages

4. **Given** a code file with security issues
   **When** Claude reviews it
   **Then** the skill triggers with specific security guidance

5. **Given** code has low test coverage
   **When** the quality report is generated
   **Then** coverage gaps are highlighted with priority

## Technical Details

### Skill: Code Quality

**File**: `skills/code-quality/SKILL.md`

**Purpose**: Auto-triggered skill that evaluates code quality and suggests improvements when developers write or review code.

**YAML Frontmatter**:
```yaml
---
name: code-quality
description: Evaluates code quality, complexity, security, and maintainability
---
```

**Key Sections**:

1. **When to Trigger This Skill**
   - Detecting code review or PR submissions
   - User asks about code quality
   - User submitting code for analysis
   - User refactoring code
   - Function/method exceeding size limits

2. **Code Complexity**
   - Cyclomatic complexity (target: <10)
   - Cognitive complexity (target: <15)
   - Nesting depth (target: <3)
   - Function size (target: <50 lines)
   - Class size (target: <200 lines)

3. **Naming Conventions**
   - Variable naming patterns
   - Function naming standards
   - Class naming conventions
   - Constant naming (UPPER_CASE)
   - Private member conventions

4. **Code Style**
   - Indentation and whitespace
   - Line length (target: <120 chars)
   - Bracket placement
   - Comment style and frequency
   - Documentation requirements

5. **Security Vulnerabilities**
   - SQL injection patterns
   - XSS vulnerabilities
   - Hardcoded secrets
   - Unsafe deserialization
   - Command injection risks
   - Weak cryptography
   - OWASP Top 10 patterns

6. **Maintainability**
   - DRY principle violations
   - God objects/functions
   - Magic numbers
   - Dead code
   - Circular dependencies
   - Unnecessary coupling

7. **Testing Requirements**
   - Functions needing tests
   - Error handling coverage
   - Edge case coverage
   - Integration test needs

8. **Performance Concerns**
   - N+1 query patterns
   - Inefficient loops
   - Memory leaks
   - Resource management

9. **Language-Specific Guidance**
   - Python: PEP 8, type hints
   - JavaScript: ESLint, async/await patterns
   - Go: interfaces, error handling
   - Java: design patterns, annotations
   - Ruby: conventions, metaprogramming

### Command: check-quality

**File**: `commands/check-quality.md`

**Purpose**: Comprehensive codebase quality assessment.

**Workflow**:

1. **Analyze codebase**
   - Scan all source files
   - Identify patterns and metrics
   - Check dependencies
   - Calculate coverage metrics

2. **Evaluate metrics**
   ```
   Complexity Analysis:
   - Average cyclomatic: 6.2
   - Functions > 10: 3 (auth.py, parser.py, utils.py)
   - Max nesting depth: 4

   Code Size:
   - Average function: 24 lines
   - Average class: 120 lines
   - Total lines: 12,450

   Test Coverage:
   - Overall: 82%
   - Untested functions: 23
   - Edge cases missing: 15
   ```

3. **Identify issues**
   - Security vulnerabilities
   - Code duplications
   - Outdated dependencies
   - Style inconsistencies
   - Unmaintained code

4. **Generate report**
   - Executive summary
   - Metrics dashboard
   - Issues by severity (Critical, High, Medium, Low)
   - Top recommendations
   - Effort estimates

5. **Provide improvements**
   - Refactoring suggestions
   - Performance optimizations
   - Security fixes
   - Test recommendations

**Invocation**: `/best-practices:check-quality`

**Example Output**:

```
Code Quality Assessment Report
==============================

Project: my-api
Language: Python
Last Updated: 2026-01-24

QUALITY SCORE: 7.2/10 (↑ from 6.8)

Metrics Summary:
├─ Complexity: 6.5/10 (⚠ Medium)
├─ Security: 8.2/10 (✓ Good)
├─ Maintainability: 6.8/10 (⚠ Medium)
├─ Test Coverage: 7.9/10 (⚠ Could be higher)
└─ Dependency Health: 8.5/10 (✓ Good)

🔴 CRITICAL ISSUES (Fix immediately)
1. SQL injection vulnerability in query_builder.py:142
   - User input not parameterized
   - Risk: Database compromise
   - Fix: Use parameterized queries

2. Hardcoded AWS credentials in config.py:18
   - Risk: Credential exposure
   - Fix: Use environment variables

🟠 HIGH PRIORITY (Fix soon)
1. Function create_order() is 87 lines (target: <50)
   - Suggestion: Split into smaller functions
   - Effort: 2-3 hours

2. 15 functions with cyclomatic complexity > 10
   - Suggestion: Refactor with guards and early returns
   - Effort: 4-6 hours

3. 3 outdated dependencies with security patches
   - jsonschema: 3.2.0 → 4.17.0 (security fix)
   - requests: 2.28.0 → 2.31.0 (recommended)
   - urllib3: 1.26.8 → 2.0.0 (major version)

🟡 MEDIUM PRIORITY (Improve quality)
1. Test coverage gaps
   - error_handling.py: 0% coverage
   - auth_service.py: 32% coverage
   - Suggestion: Add 12 unit tests
   - Effort: 8-10 hours

2. Code duplication detected
   - validate_email() repeated 3 times
   - parse_date() repeated 2 times
   - Suggestion: Extract into utils
   - Effort: 1-2 hours

3. Style consistency issues
   - 42 PEP 8 violations
   - Suggestion: Run black and flake8
   - Effort: 30 minutes

RECOMMENDATIONS (Prioritized)
============================
1. [CRITICAL] Fix SQL injection - 1 hour
2. [CRITICAL] Remove hardcoded credentials - 30 min
3. [HIGH] Refactor create_order() - 3 hours
4. [HIGH] Update security-related dependencies - 2 hours
5. [MEDIUM] Add missing tests - 10 hours
6. [MEDIUM] Extract duplicate code - 2 hours
7. [LOW] Fix style consistency - 30 minutes

Effort Summary:
├─ Critical fixes: 1.5 hours
├─ High priority: 5 hours
├─ Medium priority: 12 hours
└─ Low priority: 0.5 hours
   Total: 19 hours (≈ 3-4 days for one developer)
```

### Metrics and Standards

**Complexity Targets**:
```
Metric                 | Target | Warning | Critical
Cyclomatic complexity  | <10    | 10-15   | >15
Cognitive complexity   | <15    | 15-20   | >20
Nesting depth          | <3     | 3-4     | >4
Function size          | <50    | 50-75   | >75
Class size             | <200   | 200-300 | >300
```

**Test Coverage**:
```
Codebase area          | Minimum | Target | Excellence
Core business logic    | 90%     | 95%    | 98%+
Public APIs            | 85%     | 90%    | 95%+
Utilities/helpers      | 70%     | 80%    | 90%+
UI components          | 60%     | 75%    | 85%+
Configuration          | 0%      | 50%    | 75%+
```

**Dependency Health**:
- Up-to-date: Latest patch version
- Outdated: Newer patch available
- Vulnerable: Known security issues
- Abandoned: No updates in 2+ years

## Edge Cases & Error Handling

1. **Edge case**: Very large codebase (>100k lines)
   - **Handling**: Analyze in sections or by module
   - **Message**: "Large codebase detected. Analyzing by module..."

2. **Edge case**: Multiple languages in project
   - **Handling**: Analyze each language with appropriate tools
   - **Message**: "Detected Python and JavaScript. Analyzing separately..."

3. **Error**: Cannot determine language/framework
   - **Message**: "Could not detect project type. Please specify."
   - **Recovery**: Ask user for language and framework

4. **Edge case**: No meaningful metrics (e.g., only scripts)
   - **Handling**: Provide generic code quality feedback
   - **Message**: "Script-only project. Applying general best practices."

5. **Edge case**: Dependencies with security issues
   - **Handling**: Flag immediately with patch versions
   - **Message**: "⚠️  3 dependencies have known vulnerabilities"

## Security Considerations

- [ ] Identify OWASP Top 10 patterns
- [ ] Flag hardcoded secrets/credentials
- [ ] Check for unsafe deserialization
- [ ] Identify injection vulnerabilities
- [ ] Check cryptographic strength
- [ ] Flag insecure random generation
- [ ] Check authentication/authorization patterns
- [ ] Identify dependency vulnerabilities

## Testing Strategy

### Validation

- [ ] SKILL.md structure is valid
- [ ] Metrics calculations are accurate
- [ ] Security checks identify known patterns
- [ ] Report generation is reproducible
- [ ] Severity classifications are appropriate

### Manual Testing

- [ ] Analyze Python project with various complexity levels
- [ ] Analyze JavaScript project
- [ ] Test with project containing security issues
- [ ] Test with outdated dependencies
- [ ] Verify report formatting and clarity

## Dependencies

- **Blocked by**: plugin-best-practices-setup
- **Blocks**: None (parallel feature)
- **Related**:
  - plugin-best-practices-testing (coverage metrics)
  - plugin-best-practices-agents (quality-checker agent uses this)

## Implementation Notes

### Decisions Made

- **Severity-based prioritization**: Critical/High/Medium/Low helps users focus
- **Effort estimates**: Help teams plan improvement work
- **Language-agnostic patterns**: Core principles apply across languages
- **Actionable recommendations**: Every issue has suggested fix

### Metric Sources

**Python**:
- pylint, flake8, radon (complexity)
- bandit (security)
- pipdeptree (dependencies)

**JavaScript**:
- ESLint, SonarQube (complexity, style)
- npm audit (security)
- npm outdated (dependencies)

**Go**:
- gocyclo (complexity)
- gosec (security)
- go mod (dependencies)

### Severity Classification

**CRITICAL**:
- Security vulnerabilities (XSS, SQL injection, etc.)
- Hardcoded secrets/credentials
- Production outage risk

**HIGH**:
- Functions exceeding complexity limits
- Severe code duplication
- Outdated dependencies with security patches

**MEDIUM**:
- Low test coverage
- Code style issues
- Missing documentation

**LOW**:
- Minor style inconsistencies
- Optional refactorings
- Non-critical optimizations

## Open Questions

- [ ] Should we integrate with GitHub/GitLab security scanning APIs?
  - *Decision pending*: Could provide live vulnerability data
- [ ] Support for custom quality metrics per team?
  - *Decision pending*: Future enhancement for enterprise

## References

- Cyclomatic Complexity: https://en.wikipedia.org/wiki/Cyclomatic_complexity
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Code Coverage Best Practices: https://testdriven.io/
- SonarQube Quality Model: https://docs.sonarqube.org/latest/
- pylint Documentation: https://pylint.pycqa.org/
- ESLint: https://eslint.org/

---

**Template Version**: 1.0
**Last Updated**: 2026-01-24
