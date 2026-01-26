# Command: check-quality

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: High

## Purpose

Comprehensive codebase quality assessment generating detailed reports with prioritized recommendations.

**Invocation**: `/code-quality:check-quality`

## Key Workflow

1. Analyze entire codebase for metrics
2. Identify complexity, security, and style issues
3. Check dependencies for vulnerabilities and updates
4. Evaluate test coverage impact
5. Generate comprehensive quality report
6. Provide prioritized improvement recommendations

## Analysis Areas

- **Complexity Metrics** - Cyclomatic, cognitive, nesting depth, function/class size
- **Code Style** - Consistency, naming, formatting
- **Security** - Vulnerabilities, hardcoded secrets, weak patterns
- **Maintainability** - Duplication, dead code, coupling
- **Test Coverage** - Overall coverage, untested functions, gaps
- **Dependency Health** - Outdated packages, vulnerable dependencies, abandoned projects

## Output

Comprehensive report with:
- Quality score (0-10) with trends
- Category breakdowns
- Critical issues requiring immediate attention
- Prioritized recommendations with effort estimates
- Test stubs and improvement guidance

## Dependencies

- **Blocked by**: plugin-code-quality (plugin definition)
- **Related**: skill-quality-guidance, agent-quality-checker
