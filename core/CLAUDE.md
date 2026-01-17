# Spec-Driven Development Constitution

This file defines the core principles and workflow for spec-driven development. These rules are immutable and apply to every change.

## Core Principles

1. **Specification First**: Never implement features without a written specification
2. **Explicit Requirements**: All requirements must be clearly documented before coding
3. **Validation Required**: Every implementation must be validated against its spec
4. **Incremental Progress**: Break large features into small, spec'd increments

## Workflow

### Phase 1: Specify
**Before writing any code:**

1. Check if a specification exists in `specs/` directory
2. If no spec exists, create one or ask the user to provide it
3. Read and understand the complete specification
4. Ask clarifying questions if the spec is ambiguous

**Specification Format:**
```markdown
# Feature: [Name]

## Purpose
Why this feature exists

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Acceptance Criteria
How to verify success

## Technical Notes
Implementation considerations
```

### Phase 2: Plan
**After understanding the spec:**

1. Identify all files that need changes
2. Consider edge cases and error handling
3. Plan the implementation approach
4. Present the plan to the user for approval

### Phase 3: Implement
**During implementation:**

1. Follow existing code patterns and conventions
2. Implement requirements incrementally
3. Check off acceptance criteria as you complete them
4. Write tests that validate spec requirements

### Phase 4: Validate
**After implementation:**

1. Verify all acceptance criteria are met
2. Run tests (if applicable)
3. Update spec status to "Implemented"
4. Document any deviations from the spec

## Available Plugins

Plugins extend this workflow with domain-specific patterns. Activate them using skills:

- `/api` - API development patterns (FastAPI, AWS SAM)
- `/ai-app` - AI application patterns (LLM integration)

## File Organization

```
project/
├── CLAUDE.md           # This file (copied from spec-kit)
├── .claude/
│   └── skills/         # Plugin skills
├── specs/              # All specifications
│   ├── features/       # Feature specs
│   └── api/            # API specifications
└── src/                # Implementation code
```

## Spec Status Tracking

Mark spec status at the top of each spec file:

```markdown
**Status**: Draft | In Progress | Implemented | Deprecated
**Owner**: [Name]
**Last Updated**: YYYY-MM-DD
```

## Quality Standards

1. **No Dead Code**: Remove commented code and unused imports
2. **Error Handling**: Handle errors explicitly, don't silently fail
3. **Documentation**: Code should be self-documenting, add comments only for "why" not "what"
4. **Testing**: Critical paths must have tests

## When Specs Are Missing

If asked to implement something without a spec:

1. Inform the user that a spec is required
2. Offer to create a draft spec based on the request
3. Wait for spec approval before implementing

**Exception**: Trivial changes (typos, formatting) don't require specs.

---

*This constitution is based on industry-standard spec-driven development practices and is optimized for Claude Code workflows.*
