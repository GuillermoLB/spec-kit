# Skill: Code Quality Guidance

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: High

## Purpose

Auto-triggered skill evaluating code quality and suggesting improvements during code review and development.

## Key Topics

1. **Code Complexity** - Cyclomatic complexity, cognitive complexity, nesting depth, function/class size
2. **Naming Conventions** - Variable, function, class naming standards
3. **Code Style** - Indentation, line length, bracket placement, comments, documentation
4. **Security Vulnerabilities** - SQL injection, XSS, hardcoded secrets, unsafe deserialization, OWASP Top 10
5. **Maintainability** - DRY principle, God objects, magic numbers, dead code, circular dependencies
6. **Testing Requirements** - Functions needing tests, error handling, edge cases
7. **Performance** - N+1 queries, inefficient loops, memory leaks
8. **Language-Specific Guidance** - Python, JavaScript, Go, Java, Ruby

## Trigger Conditions

During code review, PR submissions, refactoring, or when quality issues are detected.

## Dependencies

- **Blocked by**: plugin-code-quality (plugin definition)
- **Related**: command-check-quality, agent-quality-checker
