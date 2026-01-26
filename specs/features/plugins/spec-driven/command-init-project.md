# Command: init-project

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: High

## Purpose

Initialize a new or existing project with spec-driven development structure and CLAUDE.md configuration.

**Invocation**: `/spec-driven:init-project`

## Requirements

- [ ] Create `commands/init-project.md` command
- [ ] Detect existing project structure
- [ ] Ask configuration questions
- [ ] Create `specs/` directory structure
- [ ] Generate CLAUDE.md configuration
- [ ] Create example specifications
- [ ] Configure `.claude/settings.json`
- [ ] Update `.gitignore`
- [ ] Provide next steps guidance

## User Stories

**As a** developer starting a new project
**I want** to initialize it with spec-driven structure
**So that** my team starts with specifications instead of jumping to code

**As a** tech lead
**I want** to set up new projects consistently
**So that** all projects follow the same structure and conventions

## Acceptance Criteria

1. **Given** a developer runs `/spec-driven:init-project`
   **When** they answer project questions
   **Then** they get a complete project structure with:
     - CLAUDE.md configured for the project
     - `specs/` directory with templates
     - Example feature spec
     - Example architecture spec
     - SPECIFICATIONS_SUMMARY.md

2. **Given** a project is initialized
   **When** developers start working
   **Then** they reference CLAUDE.md for guidance

3. **Given** a developer creates a new spec
   **When** they use the examples
   **Then** they follow the established patterns

## Technical Details

### Workflow

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
   - Integration with plugins

5. **Create example specs**
   - Feature spec example
   - Architecture spec example
   - API spec example

6. **Configure .claude/settings.json**
   - Enable spec-driven plugin
   - Set up hooks for spec enforcement
   - Configure spec-driven workflows

7. **Provide next steps**
   - Write first feature spec
   - Review CLAUDE.md
   - Add team members

### Example Output

```
Spec-Driven Development Initialization
======================================

Initializing: my-awesome-api

✓ Created specs/ directory
✓ Created CLAUDE.md
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
```

### Generated Specification Templates

**Location**: `specs/features/`, `specs/api/`, `specs/architecture/`

**Templates Created**:
1. Feature specification template
2. Architecture specification template
3. API specification template (OpenAPI)
4. Database schema template

### CLAUDE.md Template

The command generates a CLAUDE.md file with:
- Project overview
- Project structure
- Claude Code integration guidelines
- Specification writing standards
- Code standards and review process
- Team communication conventions

### SPECIFICATIONS_SUMMARY.md

The command creates a tracking document with:
- Specification status table
- Phase breakdown
- Specification details
- Statistics

### Configuration Template (.claude/settings.json)

```json
{
  "extraKnownMarketplaces": {
    "spec-driven": {
      "source": {
        "source": "github",
        "repo": "company/spec-driven-plugin"
      }
    }
  },
  "enabledPlugins": {
    "spec-driven@spec-driven": true
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "model",
            "prompt": "Before implementing, check if there's a spec in specs/features/. If starting new feature, suggest writing a spec first."
          }
        ]
      }
    ]
  }
}
```

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
   - **Handling**: Merge our guidance
   - **Message**: "Found existing CLAUDE.md. Preserve and add to it?"

## Security Considerations

- [ ] Don't include secrets in CLAUDE.md
- [ ] Don't include real credentials in examples
- [ ] Document security requirements in specs
- [ ] Security checklist in API specs

## Testing Strategy

- [ ] CLAUDE.md template is complete
- [ ] Specification templates are usable
- [ ] Directory structure is correct
- [ ] Settings.json is valid
- [ ] Example specs follow best practices
- [ ] Run on new project (fresh directory)
- [ ] Run on existing project (with existing files)
- [ ] Verify hooks work correctly

## Dependencies

- **Blocked by**: plugin-spec-driven (plugin definition)
- **Blocks**: None
- **Related**: skill-spec-guidance

---

**See skill-spec-guidance.md for auto-triggered guidance details.**
