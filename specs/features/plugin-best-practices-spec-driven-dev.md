# Feature: Best Practices Plugin - Spec-Driven Development

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-24
**Priority**: High

## Purpose

Add spec-driven development support to the best-practices plugin. This feature helps teams adopt specification-first development practices by:

- Providing project initialization with spec structure
- Creating CLAUDE.md for project-specific Claude Code configuration
- Offering specification templates (feature, architecture, API)
- Guiding teams through spec-driven workflows
- Enforcing specs before implementation

When developers install the plugin and initialize a project, they immediately have the infrastructure and guidance for writing specifications before code—ensuring alignment, documentation, and quality from the start.

## Requirements

- [ ] Create `skills/spec-driven/SKILL.md` - Auto-triggered spec guidance
- [ ] Create `commands/init-project.md` - Project initialization command
- [ ] Generate CLAUDE.md template for new projects
- [ ] Generate `specs/` directory structure
- [ ] Create feature specification template
- [ ] Create architecture specification template
- [ ] Create API specification template
- [ ] Provide specification writing guidance
- [ ] Generate specifications summary document
- [ ] Enforce specs before implementation suggestions
- [ ] Integrate with other plugin features

## User Stories

**As a** tech lead starting a new project
**I want** to initialize it with spec-driven development structure
**So that** my team starts with specifications instead of jumping to code

**As a** developer writing a new feature
**I want** Claude to guide me through writing a spec first
**So that** I clarify requirements before implementing

**As a** team onboarding to the best-practices plugin
**I want** clear CLAUDE.md configuration for our project
**So that** Claude understands our project structure and conventions

**As a** maintainer enforcing quality standards
**I want** Claude to suggest specs when developers start coding
**So that** we avoid scope creep and maintain clear documentation

## Acceptance Criteria

1. **Given** a developer runs `/best-practices:init-project`
   **When** they answer project questions
   **Then** they get:
     - CLAUDE.md configured for the project
     - `specs/` directory with templates
     - Example feature spec
     - Example architecture spec
     - SPECIFICATIONS_SUMMARY.md ready to track all specs

2. **Given** a project is initialized with spec-driven development
   **When** a developer asks about a new feature
   **Then** the spec-driven skill suggests writing a spec first

3. **Given** a developer has a spec written
   **When** they ask for implementation help
   **Then** Claude references the spec for requirements

4. **Given** a team uses the plugin
   **When** they enable the project
   **Then** CLAUDE.md hooks trigger spec-driven workflows

5. **Given** a developer tries to implement without a spec
   **When** the spec-driven skill detects this
   **Then** it suggests writing a spec first with template help

## Technical Details

### Skill: Spec-Driven Development

**File**: `skills/spec-driven/SKILL.md`

**Purpose**: Auto-triggered skill that guides spec-driven development practices and suggests writing specifications.

**YAML Frontmatter**:
```yaml
---
name: spec-driven
description: Guides specification-first development practices and ensures specs before implementation
---
```

**Key Sections**:

1. **When to Trigger This Skill**
   - User asks about starting a new feature
   - User begins implementation without mentioning specs
   - User asks for design/architecture help
   - User seeks clarification on requirements
   - Feature ticket lacks clear requirements

2. **Spec-Driven Development Philosophy**
   - Write specifications before code
   - Specifications clarify requirements
   - Reduce scope creep
   - Enable better code reviews
   - Create living documentation
   - Facilitate asynchronous communication

3. **Specification Types**
   - **Feature specs**: User stories, requirements, acceptance criteria
   - **Architecture specs**: System design, components, data flow
   - **API specs**: Endpoints, request/response, error handling
   - **Database specs**: Schema design, relationships, migrations

4. **Writing a Good Specification**
   - Purpose: Why is this needed?
   - Requirements: What needs to be done?
   - User stories: Who uses it and why?
   - Acceptance criteria: How do we know it's complete?
   - Technical details: How should it be implemented?
   - Dependencies: What else is needed?
   - Edge cases: What could go wrong?

5. **Specification Review Process**
   - Share with stakeholders early
   - Get alignment before implementation
   - Document decisions made
   - Link to related specifications
   - Version your specifications

6. **Using Specs for Implementation**
   - Reference specs during development
   - Update specs if requirements change
   - Use acceptance criteria for testing
   - Link PR to spec
   - Update SPECIFICATIONS_SUMMARY.md

7. **Spec-Driven Development Workflow**
   ```
   1. Write Feature Spec
      ↓
   2. Review & Align
      ↓
   3. Reference in Implementation
      ↓
   4. Test Against Acceptance Criteria
      ↓
   5. Update Spec if Needed
      ↓
   6. Track in SPECIFICATIONS_SUMMARY.md
   ```

8. **Common Spec Mistakes**
   - Specs too vague ("do great things")
   - Specs too detailed (over-engineering)
   - Missing acceptance criteria
   - Not involving stakeholders
   - Outdated specs after implementation
   - No dependencies documented

9. **Integration with Testing**
   - Write tests based on acceptance criteria
   - Test coverage validates spec implementation
   - Failed tests indicate spec misalignment

10. **Integration with CI/CD**
    - Reference spec in PR description
    - Link spec to commits
    - Ensure specs pass review before deployment

### Command: init-project

**File**: `commands/init-project.md`

**Purpose**: Initialize a new or existing project with spec-driven development structure and CLAUDE.md configuration.

**Workflow**:

1. **Detect project**
   - Check if project exists
   - Detect language and framework
   - Check existing structure

2. **Ask configuration questions**
   ```
   Project name: my-awesome-api
   Project description: REST API for e-commerce platform
   Primary language: Python
   Team size: 5-10 people
   Project visibility: Internal / Public
   ```

3. **Create directory structure**
   ```
   ├── specs/
   │   ├── SPECIFICATIONS_SUMMARY.md
   │   ├── features/
   │   ├── api/
   │   └── architecture/
   ├── .claude/
   │   └── settings.json
   ├── CLAUDE.md
   └── .gitignore (updated)
   ```

4. **Generate CLAUDE.md**
   - Project context and structure
   - Key files and directories
   - Team guidelines
   - Specification templates to use
   - Integration with best-practices plugin

5. **Create example specs**
   - Feature spec example
   - Architecture spec example
   - API spec example

6. **Configure .claude/settings.json**
   - Enable best-practices plugin
   - Set up hooks for spec enforcement
   - Configure spec-driven workflows

7. **Provide next steps**
   - Write first feature spec
   - Review CLAUDE.md
   - Add team members

**Invocation**: `/best-practices:init-project`

**Example Output**:

```
Spec-Driven Development Initialization
======================================

Initializing: my-awesome-api

✓ Created specs/ directory
✓ Created CLAUDE.md (see below)
✓ Created SPECIFICATIONS_SUMMARY.md
✓ Created example specifications
✓ Configured .claude/settings.json
✓ Updated .gitignore

Next Steps:
──────────
1. Review CLAUDE.md (customize if needed)
2. Write your first feature spec:
   specs/features/your-first-feature.md
3. Share CLAUDE.md with your team
4. Start implementing based on specs!

CLAUDE.md Preview:
─────────────────
[Generated CLAUDE.md shown below]
```

### CLAUDE.md Template

**File**: Generated in project root

**Purpose**: Project-specific Claude Code configuration that defines project structure, conventions, and Claude Code usage.

**Structure**:

```markdown
# CLAUDE.md - Project Configuration for Claude Code

## Project Overview

**Project**: [Name]
**Description**: [Brief description]
**Language**: [Primary language]
**Framework**: [Framework if applicable]
**Team**: [Team size and roles]

## Project Structure

```
project/
├── src/                    # Source code
├── tests/                  # Test files
├── specs/                  # Specifications
├── docs/                   # Documentation
└── .claude/                # Claude Code config
```

## Using Claude Code with This Project

### Key Files Claude Should Know About

- `src/main.py` - Main application file
- `src/config.py` - Configuration
- `src/database.py` - Database setup
- `specs/SPECIFICATIONS_SUMMARY.md` - All project specifications

### Spec-Driven Development

We use **spec-driven development**. Before implementing:

1. Write a specification in `specs/features/`
2. Get alignment from stakeholders
3. Reference the spec during implementation
4. Test against acceptance criteria
5. Update `specs/SPECIFICATIONS_SUMMARY.md`

### Writing Specifications

Use templates in `specs/features/` and `specs/api/`

Checklist for every spec:
- [ ] Purpose is clear
- [ ] Requirements are specific
- [ ] User stories included
- [ ] Acceptance criteria defined
- [ ] Technical details specified
- [ ] Dependencies documented
- [ ] Status and owner noted

### Best Practices Plugin

This project uses the best-practices plugin for Claude Code:

```bash
/plugin marketplace add company/best-practices-plugin
/plugin install best-practices@best-practices
```

Available commands:
- `/best-practices:run-tests` - Analyze test coverage
- `/best-practices:setup-ci` - Generate CI/CD pipeline
- `/best-practices:check-quality` - Full code quality assessment
- `/best-practices:init-project` - Initialize new projects
- `/best-practices:test-reviewer` - Comprehensive test analysis
- `/best-practices:quality-checker` - Full codebase assessment

### Code Standards

- Testing: Minimum 80% coverage (pytest)
- Quality: Cyclomatic complexity <10
- Documentation: README, docstrings required
- CI/CD: Automated testing and linting
- Specs: Required before implementation

### Review Process

1. Write spec (feature spec for features)
2. Implement based on spec
3. Run tests: `/best-practices:run-tests`
4. Check quality: `/best-practices:check-quality`
5. Code review (reference spec)
6. Merge and deploy

### Important Conventions

- Feature branches: `feature/feature-name`
- Bug fixes: `fix/bug-description`
- Specs reference: Link spec in PR description
- Commit messages: Reference spec or issue
- Docstrings: Google style (Python)

### Getting Help

For help with specifications:
```
/best-practices:init-project  # If adding new feature
```

For help with implementation:
Ask about the feature spec, Claude will reference it.

### Team Communication

Specifications are the source of truth. Always:
- Reference the spec in discussions
- Update spec if requirements change
- Link PR to spec
- Update SPECIFICATIONS_SUMMARY.md

---

**Generated**: 2026-01-24
**Last Updated**: [Update as needed]
```

### Generated Specification Templates

**Location**: `specs/features/`, `specs/api/`, `specs/architecture/`

**Templates Created**:
1. Feature specification template
2. Architecture specification template
3. API specification template (OpenAPI)
4. Database schema template

### SPECIFICATIONS_SUMMARY.md

**Purpose**: Track all project specifications with status and dependencies.

**Structure**:

```markdown
# Project Specifications Summary

## Overview

This document tracks all specifications for [Project Name].

## Specification Status

| Feature | Owner | Status | Priority | Dependencies |
|---------|-------|--------|----------|--------------|
| User Authentication | @alice | Draft | High | None |
| API Documentation | @bob | In Progress | Medium | User Auth |
| Database Schema | @charlie | Implemented | High | None |

## Specification Phases

### Phase 1: Core Features (v1.0)
- [ ] User Authentication (specs/features/user-auth.md)
- [ ] API Endpoints (specs/api/endpoints.md)
- [ ] Database Schema (specs/database/schema.md)

### Phase 2: Enhanced Features (v1.1)
- [ ] User Profiles
- [ ] Advanced Search
- [ ] Caching

### Phase 3: Future Features (v2.0)
- [ ] Mobile App
- [ ] Real-time Notifications

## Specification Details

### User Authentication
- **File**: specs/features/user-authentication.md
- **Owner**: @alice
- **Status**: Draft
- **Priority**: High
- **Blocked by**: None
- **Blocks**: API Documentation, User Profiles
- **Created**: 2026-01-24
- **Last Updated**: 2026-01-24

[More specifications listed...]

## Statistics

- Total Specifications: 8
- Draft: 2
- In Progress: 3
- Implemented: 3
- Coverage: 80% code coverage

```

### Integration with Other Plugin Features

**With Testing Feature**:
- Acceptance criteria become test requirements
- Test coverage validated against spec completeness

**With Code Quality Feature**:
- Code reviewed against spec requirements
- Architecture reviewed against architecture spec

**With CI/CD Feature**:
- Pipeline configurations based on spec requirements
- Deployment stages match spec phases

**With Documentation Feature**:
- Architecture spec becomes system documentation
- API spec becomes API documentation

## Hooks for Spec Enforcement

**In `.claude/settings.json`**:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "model",
            "prompt": "Before implementing, check if there's a spec in specs/features/. If starting new feature, suggest `/best-practices:init-project` or writing a spec first."
          }
        ]
      }
    ]
  }
}
```

This automatically reminds developers to write specs before coding.

## Edge Cases & Error Handling

1. **Edge case**: Project already has specs
   - **Handling**: Ask to merge with existing specs
   - **Message**: "Existing specs found. Preserve existing? (y/n)"

2. **Edge case**: No specs directory yet
   - **Handling**: Create with templates
   - **Message**: "Created specs/ with templates"

3. **Error**: Cannot determine project type
   - **Handling**: Ask user for project language
   - **Message**: "Could not detect project type. What's the primary language?"

4. **Edge case**: Team already has CLAUDE.md
   - **Handling**: Merge our best-practices guidance
   - **Message**: "Found existing CLAUDE.md. Preserve and add to it?"

## Security Considerations

- [ ] Don't include secrets in CLAUDE.md
- [ ] Don't include real credentials in examples
- [ ] Document security requirements in specs
- [ ] Security checklist in API specs
- [ ] CLAUDE.md not committed (optional .claude/.gitignore)

## Testing Strategy

### Validation

- [ ] CLAUDE.md template is complete
- [ ] Specification templates are usable
- [ ] Directory structure is correct
- [ ] Settings.json is valid
- [ ] Example specs follow best practices

### Manual Testing

- [ ] Run init-project on new project
- [ ] Verify CLAUDE.md is created
- [ ] Verify specs/ has all templates
- [ ] Test on existing project
- [ ] Verify hooks work

## Dependencies

- **Blocked by**: plugin-best-practices-setup
- **Blocks**: None (enhances all other features)
- **Related**: All other plugin features

## Implementation Notes

### Decisions Made

- **CLAUDE.md is required foundation**: Guides all Claude Code interactions
- **Templates provided**: Reduces friction for first spec
- **Integration with hooks**: Enforces spec-first without being restrictive
- **Optional spec directory**: Can be customized per team

### Team Onboarding Flow

```
1. New team member joins
2. Clones project
3. Opens CLAUDE.md first
4. Understands project structure
5. Reads specification guidelines
6. Knows to write specs before code
7. Finds examples in specs/features/
8. Ready to contribute!
```

### Customization Strategy

Teams can customize:
- CLAUDE.md content
- Specification templates
- Spec location (specs/ vs docs/)
- Spec naming conventions
- Integration hooks

## Open Questions

- [ ] Should CLAUDE.md be committed or generated locally?
  - *Decision pending*: Recommend committing (team communication)
- [ ] Auto-generate SPECIFICATIONS_SUMMARY.md from specs?
  - *Decision pending*: Future enhancement

## References

- Your Project's CLAUDE.md: (as example)
- Specification Templates: (from your project)
- Spec-Driven Development: https://en.wikipedia.org/wiki/Specification_by_example
- Living Documentation: https://leanpub.com/livingdocumentation

---

**Template Version**: 1.0
**Last Updated**: 2026-01-24
