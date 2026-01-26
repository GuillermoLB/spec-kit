# Agent: Quality Checker

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: Medium

## Purpose

Comprehensive codebase quality assessment combining complexity, security, maintainability, and dependency analysis.

**Invocation**: `/code-quality:quality-checker` or `/code-quality:analyze`

## Capabilities

### 1. Complexity Analysis
- Calculate cyclomatic and cognitive complexity
- Identify complex functions/methods
- Find deep nesting patterns
- Measure class sizes
- Detect code duplication

### 2. Security Vulnerability Scanning
- Check for injection vulnerabilities
- Identify hardcoded credentials
- Find unsafe deserialization
- Check cryptographic patterns
- Identify OWASP Top 10 issues

### 3. Maintainability Assessment
- Evaluate code organization
- Check naming conventions
- Identify dead code
- Find code duplication
- Assess test coverage

### 4. Dependency Analysis
- Identify outdated packages
- Flag security vulnerabilities
- Check for unused dependencies
- Identify license compatibility
- Monitor abandoned projects

### 5. Documentation Evaluation
- Check README completeness
- Evaluate docstring coverage
- Verify API documentation
- Check for architecture docs
- Assess comment quality

## Analysis Steps

1. Repository scan - Detect language, framework, structure, dependencies
2. Static analysis - Measure code metrics, identify issues, calculate scores
3. Security analysis - Scan for vulnerabilities, check dependencies, review practices
4. Documentation review - Check README, analyze docstrings, review comments
5. Generate comprehensive assessment - Overall score, category breakdown, findings, recommendations

## Report Structure

**Executive Summary**:
- Overall quality score (0-10) with trend
- Category breakdown scores
- Critical issues count
- High priority items count

**Category Breakdown**:
- Complexity score and assessment
- Security score with vulnerability count
- Maintainability score and specific issues
- Test coverage score
- Dependency health score
- Documentation completeness

**Critical Findings**:
- Security vulnerabilities with risk levels
- Code complexity issues
- Dependency vulnerabilities
- Test coverage gaps

**Recommendations**:
- Prioritized by severity (CRITICAL, HIGH, MEDIUM, LOW)
- Effort estimates in hours/days
- Impact assessment
- Specific remediation steps

## Dependencies

- **Blocked by**:
  - plugin-code-quality (plugin definition)
  - skill-quality-guidance
  - command-check-quality
- **Blocks**: None
- **Related**: agent-test-reviewer (in testing plugin)
