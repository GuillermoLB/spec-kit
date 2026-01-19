# Feature: Architecture Documentation Support

**Status**: In Progress
**Owner**: spec-kit development team
**Last Updated**: 2026-01-19
**Priority**: High

## Purpose

Add first-class support for architecture documentation in spec-kit, enabling projects to maintain both stable architectural principles and tracked architectural changes. This feature implements a hybrid approach where:

1. **Living Architecture Document**: `specs/architecture.md` captures current architectural principles and system design
2. **Architectural Change Specs**: `specs/features/architecture-*.md` documents major architectural decisions and migrations
3. **Governance Integration**: Architecture becomes a first-class specification domain following spec-driven development principles

This solves the problem of architecture being undocumented or documented outside the spec-driven workflow, ensuring architectural decisions receive the same rigor as feature specifications.

## Requirements

- [ ] Requirement 1: Create `architecture.template.md` template in `templates/specs/`
- [ ] Requirement 2: Update `core/CLAUDE.md` to reference architecture in the workflow
- [ ] Requirement 3: Update project `CLAUDE.md` with architecture governance guidelines
- [ ] Requirement 4: Modify `install.sh` to optionally create `specs/architecture.md`
- [ ] Requirement 5: Update `verify.sh` to check for architecture documentation
- [ ] Requirement 6: Document the distinction between architecture.md (living) and architecture-*.md (versioned changes)

## User Stories

**As a** developer using spec-kit
**I want** a standardized way to document system architecture
**So that** architectural decisions are transparent, tracked, and aligned with spec-driven principles

**As a** developer implementing features
**I want** to understand current architectural principles before coding
**So that** my features align with the system design

**As a** technical lead
**I want** architectural changes to go through the spec workflow
**So that** major decisions are reviewed before implementation

## Acceptance Criteria

1. **Given** I'm starting a new project with spec-kit
   **When** I run `install.sh`
   **Then** I'm offered the option to create `specs/architecture.md` from a template

2. **Given** I have `specs/architecture.md` in my project
   **When** Claude reads my project context
   **Then** it references architecture.md before planning features

3. **Given** I need to make a major architectural change
   **When** I follow the spec-kit workflow
   **Then** I create `specs/features/architecture-[change-name].md` using the standard feature template

4. **Given** I've implemented an architectural change
   **When** the architecture-*.md spec is marked "Implemented"
   **Then** `specs/architecture.md` is updated to reflect the new current state

5. **Given** I run `verify.sh`
   **When** my project has architecture documentation
   **Then** the verification passes and confirms architecture.md exists

## Technical Details

### Architecture

**Components Involved:**
- Template system: New `architecture.template.md`
- Installer: Modified `install.sh`
- Verification: Updated `verify.sh`
- Constitution: Updated `core/CLAUDE.md` and project `CLAUDE.md`

**Data Flow:**
```
1. User runs install.sh
2. Optionally creates specs/architecture.md from template
3. During development, Claude reads architecture.md first
4. For architectural changes, creates specs/features/architecture-*.md
5. After implementation, updates specs/architecture.md
6. verify.sh confirms architecture documentation exists
```

**Dependencies:**
- Existing feature template (`templates/specs/feature.template.md`)
- Current CLAUDE.md workflow structure
- Installer and verification scripts

### File Structure

**New Files:**
```
templates/specs/architecture.template.md
```

**Modified Files:**
```
core/CLAUDE.md
CLAUDE.md
install.sh
verify.sh
```

**Generated in Projects:**
```
specs/architecture.md (optional, created by installer)
specs/features/architecture-*.md (created as needed for changes)
```

### Template Design

The `architecture.template.md` will include:

1. **Metadata Section**
   - Status: Living Document
   - Owner, Last Updated, Priority

2. **System Overview**
   - High-level architecture description
   - Visual diagram placeholder
   - Technology stack

3. **Core Principles**
   - Design principles that guide all decisions
   - Non-negotiable constraints
   - Architectural patterns in use

4. **Current Architecture**
   - Component breakdown
   - Data flow descriptions
   - Integration points

5. **Key Decisions**
   - Summary of major architectural choices
   - References to detailed architecture-*.md specs

6. **Evolution Guidelines**
   - When to create architecture-*.md specs
   - How to update this living document
   - Governance process

### Security Considerations

- [ ] Authentication required: No (documentation)
- [ ] Authorization: Standard file system permissions
- [ ] Input validation: Template validation during install
- [ ] Data encryption: Not applicable
- [ ] Rate limiting: Not applicable

## Edge Cases & Error Handling

1. **Edge case**: User runs install.sh on existing project that already has architecture.md
   - **Handling**: Detect existing file, skip creation, inform user

2. **Edge case**: User creates architecture-*.md but doesn't update architecture.md
   - **Handling**: CLAUDE.md should remind developers to update architecture.md after implementation

3. **Edge case**: verify.sh runs on project without architecture.md
   - **Handling**: Show informational message, not error (architecture is optional)

4. **Error**: Template file missing during installation
   - **Message**: "Warning: architecture.template.md not found, skipping architecture creation"
   - **Recovery**: User can manually create later or reinstall spec-kit

## Testing Strategy

### Manual Testing Checklist

- [ ] Run install.sh on new project, opt-in to architecture.md creation
- [ ] Verify generated architecture.md matches template
- [ ] Run install.sh on existing project with architecture.md, verify no overwrite
- [ ] Run verify.sh with and without architecture.md
- [ ] Create architecture-*.md spec, verify it follows feature template
- [ ] Confirm CLAUDE.md updates are read by Claude during sessions
- [ ] Test full workflow: create arch spec → implement → update architecture.md

## Dependencies

- **Blocked by**: None (can implement independently)
- **Blocks**: None (optional feature)
- **Related**:
  - `testing-infrastructure.md` (similar template addition pattern)
  - `documentation-improvements.md` (improves overall documentation strategy)

## Timeline

- **Estimated effort**: 2-3 hours
- **Target completion**: 2026-01-19
- **Actual completion**: [TBD]

## Open Questions

- [x] Should architecture.md be mandatory or optional?
  - **Answer**: Optional. Not all projects need formal architecture documentation. Small projects can skip it.

- [x] Should verify.sh error or warn if architecture.md is missing?
  - **Answer**: Warn only. Architecture documentation is recommended but not required.

- [ ] Should there be a separate template for architecture-*.md or reuse feature.template.md?
  - **Current approach**: Reuse feature.template.md since architectural changes are features

## Implementation Notes

### Decisions Made

- 2026-01-19 - Architecture documentation will be optional, not mandatory. Projects can choose to adopt it.
- 2026-01-19 - Hybrid approach chosen: living architecture.md + versioned architecture-*.md specs
- 2026-01-19 - Reuse existing feature.template.md for architecture-*.md specs to maintain consistency

### Challenges Encountered

- None yet

## References

- Core template: [templates/specs/feature.template.md](../../templates/specs/feature.template.md)
- Constitution: [core/CLAUDE.md](../../core/CLAUDE.md)
- Project constitution: [CLAUDE.md](../../CLAUDE.md)

---

**Template Version**: 1.0
**Last Updated**: 2026-01-19
