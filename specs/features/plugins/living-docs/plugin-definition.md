# Plugin: Living Documentation

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: High

## Purpose

Sophisticated living documentation automation that keeps documentation synchronized with code. Combines MkDocs, Griffe, AST analysis, and CI/CD integration for documentation that never becomes outdated.

## Components

- **Skill**: `skill-docs-guidance.md` - Living docs setup and maintenance guidance
- **Command**: `command-init-docs.md` - Initialize MkDocs with best practices
- **Scripts**: `scripts-specification.md` - Automation scripts for API generation, architecture extraction, diagram generation, and validation

## Key Features

- Auto-generates API documentation from code using Griffe
- Extracts and visualizes architecture from codebase
- Keeps documentation synchronized with code changes
- Validates documentation accuracy through testing
- Generates diagrams and dependency graphs
- Integrates with CI/CD for continuous documentation updates
- Detects outdated documentation
- Supports versioning with mike

## Technologies

**MkDocs Stack**:
- mkdocs, mkdocs-material, mkdocstrings[python]
- mkdocs-gen-files, mkdocs-literate-nav, mkdocs-section-index
- mike for versioning

**Code Analysis**:
- griffe (API extraction), ast, inspect, pydeps

**Diagram Generation**:
- diagrams, pyvis, mermaid, graphviz

**Testing & Validation**:
- pytest, doctest, mktestdocs, linkchecker, interrogate

**Automation**:
- pre-commit hooks, watchdog, GitHub Actions

## Scripts

1. **init_mkdocs.py** - Initialize MkDocs with configuration
2. **gen_api_reference.py** - Generate API reference from code
3. **extract_architecture.py** - Extract architecture from code structure
4. **generate_diagrams.py** - Create visual diagrams
5. **validate_docs.py** - Validate documentation accuracy
6. **check_freshness.py** - Detect outdated documentation
7. **complexity_metrics.py** - Analyze code complexity

## Dependencies

- **Blocked by**: plugin-spec-driven (foundation)
- **Related**: plugin-documentation (manual docs), skill-docs-guidance

---

**See component specs for detailed implementation.**
