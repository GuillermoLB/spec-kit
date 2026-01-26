# Skill: Spec-Driven Development Guidance

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: High

## Purpose

Auto-triggered skill that guides spec-driven development practices and suggests writing specifications before implementation.

## Requirements

- [ ] Create `skills/spec-driven/SKILL.md`
- [ ] Trigger when user starts new feature without spec
- [ ] Provide specification writing guidance
- [ ] Suggest specification templates
- [ ] Guide spec review process
- [ ] Integrate with implementation workflow
- [ ] Enforce specs before implementation

## User Stories

**As a** developer starting a new feature
**I want** Claude to suggest writing a spec first
**So that** I clarify requirements before implementing

**As a** tech lead wanting spec-first culture
**I want** Claude to enforce specs during development
**So that** my team maintains documentation and alignment

## Acceptance Criteria

1. **Given** a developer starts a new feature
   **When** they ask for implementation help
   **Then** the skill triggers with spec guidance

2. **Given** a developer tries to implement without a spec
   **When** they begin writing code
   **Then** the skill suggests writing a spec first

3. **Given** a developer writes a spec
   **When** they ask for implementation help
   **Then** Claude references the spec

## Technical Details

### Skill Definition

**File**: `skills/spec-driven/SKILL.md`

**YAML Frontmatter**:
```yaml
---
name: spec-driven
description: Guides specification-first development practices and ensures specs before implementation
---
```

### Trigger Conditions

The skill should trigger when:
- User asks about starting a new feature
- User begins implementation without mentioning specs
- User asks for design/architecture help
- User seeks clarification on requirements
- Feature ticket lacks clear requirements

### Key Sections in Skill

1. **Spec-Driven Development Philosophy**
   - Write specifications before code
   - Specifications clarify requirements
   - Reduce scope creep
   - Enable better code reviews
   - Create living documentation
   - Facilitate asynchronous communication

2. **Specification Types**
   - **Feature specs**: User stories, requirements, acceptance criteria
   - **Architecture specs**: System design, components, data flow
   - **API specs**: Endpoints, request/response, error handling
   - **Database specs**: Schema design, relationships, migrations

3. **Writing a Good Specification**
   - Purpose: Why is this needed?
   - Requirements: What needs to be done?
   - User stories: Who uses it and why?
   - Acceptance criteria: How do we know it's complete?
   - Technical details: How should it be implemented?
   - Dependencies: What else is needed?
   - Edge cases: What could go wrong?

4. **Specification Review Process**
   - Share with stakeholders early
   - Get alignment before implementation
   - Document decisions made
   - Link to related specifications
   - Version your specifications

5. **Using Specs for Implementation**
   - Reference specs during development
   - Update specs if requirements change
   - Use acceptance criteria for testing
   - Link PR to spec
   - Update SPECIFICATIONS_SUMMARY.md

6. **Spec-Driven Development Workflow**
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

7. **Common Spec Mistakes**
   - Specs too vague ("do great things")
   - Specs too detailed (over-engineering)
   - Missing acceptance criteria
   - Not involving stakeholders
   - Outdated specs after implementation
   - No dependencies documented

8. **Integration with Testing**
   - Write tests based on acceptance criteria
   - Test coverage validates spec implementation
   - Failed tests indicate spec misalignment

9. **Integration with CI/CD**
   - Reference spec in PR description
   - Link spec to commits
   - Ensure specs pass review before deployment

## Dependencies

- **Blocked by**: plugin-spec-driven (plugin definition)
- **Blocks**: None
- **Related**: command-init-project

## Testing Strategy

- [ ] Verify skill triggers on correct conditions
- [ ] Verify guidance is clear and actionable
- [ ] Test with various feature types
- [ ] Verify links to templates work

---

**See command-init-project.md for project initialization command details.**
