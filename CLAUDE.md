# Spec-Kit Development Constitution

This file defines the development workflow for the spec-kit project itself. We practice what we preach: spec-kit is developed using spec-driven development.

## Core Principles

1. **Specification First**: Never implement features without a written specification in `specs/features/`
2. **Dogfooding**: Use spec-kit's own methodology to develop spec-kit
3. **Quality Over Speed**: Maintain high standards for all components
4. **Documentation Required**: Every feature must be documented

## Workflow

### Phase 1: Specify

**Before writing any code:**

1. Check if a specification exists in `specs/features/` directory
2. If no spec exists, create one using `templates/specs/feature.template.md`
3. Read and understand the complete specification
4. Ask clarifying questions if the spec is ambiguous

**Specification Requirements:**
- Use the feature template format
- Include clear acceptance criteria
- Define verification steps
- List dependencies
- Mark status: Draft → In Progress → Implemented

### Phase 2: Plan

**After understanding the spec:**

1. Identify all files that need changes
2. Consider edge cases and error handling
3. Plan the implementation approach
4. Present the plan for approval

### Phase 3: Implement

**During implementation:**

1. Follow existing code patterns and conventions
2. Implement requirements incrementally
3. Check off acceptance criteria as you complete them
4. Write tests that validate spec requirements (once testing infrastructure exists)
5. Update documentation as features are added

### Phase 4: Validate

**After implementation:**

1. Verify all acceptance criteria are met
2. Run tests (once testing infrastructure available)
3. Run `./verify.sh` to ensure project structure is valid
4. Update spec status to "Implemented"
5. Document any deviations from the spec

## Project Structure

```
spec-kit/
├── CLAUDE.md                  # This file
├── README.md                  # Main documentation
├── QUICKSTART.md              # Quick start guide
├── core/
│   └── CLAUDE.md              # Constitution distributed to projects
├── plugins/                   # Plugin implementations
│   ├── api-development/
│   └── ai-app/
├── templates/                 # Specification templates
│   └── specs/
│       ├── feature.template.md
│       └── api.template.yaml
├── specs/                     # Specifications for spec-kit features
│   └── features/              # Feature specifications
│       ├── testing-infrastructure.md
│       ├── documentation-improvements.md
│       ├── example-fastapi-todo.md
│       ├── example-ai-chatbot.md
│       ├── example-sam-serverless.md
│       ├── plugin-testing.md
│       ├── plugin-cicd.md
│       ├── plugin-database.md
│       └── plugin-frontend.md
├── examples/                  # Example projects (to be created)
├── tests/                     # Test suite (to be created)
├── docs/                      # Detailed documentation (to be created)
├── install.sh                 # Interactive installer
└── verify.sh                  # Project structure verification
```

## Spec Status Tracking

Mark spec status at the top of each spec file:

```markdown
**Status**: Draft | In Progress | Implemented | Deprecated
**Owner**: spec-kit development team
**Last Updated**: YYYY-MM-DD
**Priority**: High | Medium | Low
```

## Quality Standards

1. **No Dead Code**: Remove commented code and unused imports
2. **Error Handling**: Handle errors explicitly, don't silently fail
3. **Documentation**: Every feature must be documented in README or docs/
4. **Testing**: Once testing infrastructure exists, all features must have tests
5. **Examples**: Complex features should have example projects
6. **Verification**: All changes must pass `./verify.sh`

## Development Priorities

### Priority 1: Foundation
- Testing infrastructure
- Documentation improvements

### Priority 2: Examples
- FastAPI Todo API
- AI Chatbot
- Serverless API (SAM)

### Priority 3: Plugins
- Testing plugin
- CI/CD plugin
- Database plugin
- Frontend plugin

## Code Standards

### Bash Scripts
- Use shellcheck for validation
- Include error handling (`set -e`)
- Clear error messages
- Colored output for user feedback

### Python Code
- Follow PEP 8
- Use type hints
- Include docstrings
- Use pytest for testing

### Markdown Documentation
- Use consistent formatting
- Include table of contents for long docs
- Test all links
- Use relative links within repository

### Plugin Development
- Follow SKILL.md format with YAML frontmatter
- Include comprehensive patterns (not just basic examples)
- Provide production-ready templates
- Test in real projects before merging

## When Specs Are Missing

If asked to implement something without a spec:

1. Inform that a spec is required
2. Offer to create a draft spec based on the request
3. Wait for spec approval before implementing

**Exception**: Trivial changes (typos, formatting, minor README updates) don't require specs.

## Contributing to Spec-Kit

1. **For Features**: Create spec first, get approval, then implement
2. **For Bug Fixes**: Create issue describing bug, then fix
3. **For Documentation**: Can update directly for minor changes, spec for major rewrites
4. **For Plugins**: Follow plugin development spec, test in 2-3 projects first

## Verification Before Commits

Before committing changes:

1. Run `./verify.sh` - Ensure all required files exist
2. Run tests (once available) - `./tests/run_tests.sh`
3. Check documentation is updated
4. Ensure spec status is updated
5. Review git diff for unintended changes

## Version Management

- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Update CHANGELOG.md with all changes
- Tag releases in git
- Update version in README

## Current Development Phase

**Status**: Building core enhancements
**Active Specs**:
- testing-infrastructure.md (Draft)
- documentation-improvements.md (Draft)

**Next Steps**:
1. Complete all feature specifications
2. Review and approve specs
3. Implement testing infrastructure first
4. Implement documentation improvements
5. Build example projects
6. Develop new plugins

## Philosophy

Spec-kit is developed using the same spec-driven methodology it promotes:

- **Transparency**: All features have clear specifications
- **Quality**: Every component meets high standards
- **Usability**: Real developers use this daily
- **Practicality**: Solve actual problems, not theoretical ones
- **Consistency**: Follow our own rules

---

*This constitution ensures spec-kit maintains quality and consistency while practicing the methodology it teaches.*

**Version**: 1.0.0
**Last Updated**: 2026-01-17
