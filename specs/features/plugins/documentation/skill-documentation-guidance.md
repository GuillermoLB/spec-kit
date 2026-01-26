# Skill: Documentation Best Practices Guidance

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: Medium

## Purpose

Auto-triggered skill ensuring complete and clear documentation at project, API, and code levels.

## Key Topics

1. **Project-Level Documentation (README)**
   - Essential sections
   - Installation instructions
   - Quick start examples
   - Feature overview
   - Contributing guidelines

2. **API Documentation**
   - OpenAPI/Swagger patterns
   - REST endpoint documentation
   - Request/response examples
   - Error codes and handling
   - Authentication requirements

3. **Code Documentation**
   - Docstring patterns (Google, NumPy, Sphinx styles)
   - Comment best practices
   - Comment placement and clarity

4. **Architecture Documentation**
   - System overview
   - Component descriptions
   - Data flow diagrams
   - Design decisions and rationale
   - Scalability considerations

5. **Changelog Maintenance**
   - Keep a Changelog format
   - Version management
   - Release notes

6. **Documentation Completeness Checklist**
   - README, installation, quick start
   - API documentation
   - Code examples
   - Architecture docs
   - Contributing guidelines
   - License specification
   - Support/contact info

7. **Language-Specific Guidance**
   - Python: docstrings styles
   - JavaScript: JSDoc
   - Go: godoc
   - Java: Javadoc
   - Ruby: YARD

8. **Documentation Tools**
   - Sphinx for Python
   - MkDocs for general documentation
   - Swagger/OpenAPI for APIs
   - TypeDoc for TypeScript
   - GitBook for multi-page docs

## Trigger Conditions

When creating new projects, public functions without docstrings, API endpoints, or documentation updates needed.

## Documentation Maturity Levels

**Level 1 - Minimal**:
- README with basic description
- Installation instructions
- Simple usage example

**Level 2 - Adequate**:
- Complete README
- API documentation
- Development setup guide
- Contributing guidelines

**Level 3 - Comprehensive**:
- All Level 2 items
- Architecture documentation
- Troubleshooting guide
- Multiple examples
- Changelog

**Level 4 - Excellent**:
- All Level 3 items
- Tutorials
- Performance guide
- FAQ
- Video guides

## Dependencies

- **Blocked by**: plugin-documentation (plugin definition)
- **Related**: plugin-living-docs
