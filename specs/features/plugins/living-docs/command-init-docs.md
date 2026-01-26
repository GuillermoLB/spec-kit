# Command: init-docs

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: High

## Purpose

Initialize MkDocs project with best practices, automated API generation, and CI/CD integration.

**Invocation**: `/living-docs:init-docs` or `/living-docs:init`

## Key Workflow

1. Detect existing documentation setup
2. Ask configuration questions (theme, plugins, versioning, CI provider)
3. Create `docs/` directory with proper structure
4. Generate `mkdocs.yml` with Material theme and essential plugins
5. Create documentation templates
6. Generate GitHub Actions workflow for CI/CD
7. Configure pre-commit hooks
8. Provide setup and next steps

## Features

- **Interactive Setup** - Guided configuration with sensible defaults
- **Plugin Configuration** - mkdocstrings, gen-files, literate-nav, material, section-index, mike
- **Template Generation** - Homepage, architecture, contributing guides
- **CI/CD Integration** - GitHub Actions workflow with documentation deployment
- **Pre-commit Hooks** - Validation checks before commits
- **Watch Mode** - Live preview during development
- **Versioning Support** - Multiple documentation versions with mike

## Output Structure

Creates:
- `docs/` directory with index, architecture, contributing templates
- `mkdocs.yml` configured with Material theme and plugins
- `.github/workflows/docs.yml` for CI/CD
- Pre-commit configuration
- README with setup instructions

## Dependencies

- **Blocked by**: plugin-living-docs (plugin definition)
- **Related**: skill-docs-guidance, scripts-specification
