# Skill: Living Documentation Guidance

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: High

## Purpose

Auto-triggered skill guiding setup and maintenance of living documentation that stays synchronized with code changes.

## Key Topics

1. **Living Documentation Concept**
   - Why documentation becomes outdated
   - Automation-first approach
   - Benefits of living documentation

2. **MkDocs Setup**
   - Project initialization
   - Theme configuration (Material)
   - Essential plugins
   - Navigation structure

3. **API Reference Generation**
   - Using Griffe for fast extraction
   - Docstring style support (Google, NumPy, Sphinx)
   - Automatic markdown generation
   - Cross-references and navigation

4. **Architecture Documentation**
   - Extracting design from code
   - Dependency graph generation
   - Design pattern identification
   - C4 model diagrams
   - Database schema documentation

5. **Automation and CI/CD**
   - Pre-commit hooks for validation
   - GitHub Actions workflows
   - Watch mode for development
   - Automatic deployment
   - Build optimization

6. **Documentation Testing**
   - Doctest validation
   - Link checking
   - Code example validation
   - Coverage metrics
   - Spec-to-doc alignment

7. **Versioning Strategy**
   - Using mike for multi-version docs
   - Release management
   - Version selector UI
   - Backward compatibility

8. **Best Practices**
   - Automation vs manual documentation balance
   - Keeping specs and docs synchronized
   - Documentation quality standards
   - Team documentation workflows

## Trigger Conditions

When users want to set up living documentation, ask about maintaining docs, or need to keep docs synchronized with code.

## Implementation Tools

- **MkDocs**: Static site generation
- **Griffe**: Fast API documentation extraction
- **Mermaid**: Embedded diagrams in markdown
- **GitHub Actions**: CI/CD automation
- **Pre-commit**: Local validation hooks

## Dependencies

- **Blocked by**: plugin-living-docs (plugin definition)
- **Related**: command-init-docs, scripts-specification, skill-documentation-guidance
