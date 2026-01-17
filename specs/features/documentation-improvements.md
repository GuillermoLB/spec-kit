# Feature: Documentation Improvements

**Status**: Draft
**Owner**: spec-kit development team
**Last Updated**: 2026-01-17
**Priority**: High

## Purpose

Improve spec-kit documentation to make features more discoverable, provide clear contribution guidelines, and help users troubleshoot common issues. Currently, api.template.yaml exists but isn't prominently documented, and there's no structured guide for contributors or troubleshooting.

## Requirements

- [ ] Add prominent mention of api.template.yaml in README.md
- [ ] Create "File Reference" section in README listing all templates and their purposes
- [ ] Improve plugin activation examples to show both automatic and explicit activation
- [ ] Create CONTRIBUTING.md with guidelines for contributing to spec-kit
- [ ] Create docs/TROUBLESHOOTING.md with common issues and solutions
- [ ] Create docs/PLUGIN_DEVELOPMENT.md with detailed plugin creation guide
- [ ] Update README to mention testing infrastructure once available
- [ ] Add table of contents to README for easier navigation
- [ ] Clarify plugin naming (README says "/api" but directory is "api-development")

## User Stories

**As a** new spec-kit user
**I want** to easily find all available templates
**So that** I can start using them in my project

**As a** potential contributor
**I want** clear guidelines on how to contribute
**So that** I can submit high-quality pull requests

**As a** user experiencing issues
**I want** a troubleshooting guide
**So that** I can resolve common problems without external help

**As a** developer creating custom plugins
**I want** detailed plugin development documentation
**So that** I can create plugins that follow best practices

## Acceptance Criteria

1. **Given** I'm reading the README
   **When** I look for available templates
   **Then** I see a "File Reference" section listing feature.template.md, api.template.yaml, and all plugin templates with descriptions

2. **Given** I want to contribute to spec-kit
   **When** I open CONTRIBUTING.md
   **Then** I see clear guidelines for code style, testing requirements, and PR process

3. **Given** my installer isn't working
   **When** I check docs/TROUBLESHOOTING.md
   **Then** I find common installation issues with step-by-step solutions

4. **Given** I want to create a custom plugin
   **When** I read docs/PLUGIN_DEVELOPMENT.md
   **Then** I understand the plugin structure, frontmatter requirements, and template organization

5. **Given** I'm confused about plugin naming
   **When** I read the README
   **Then** I understand that "/api" is shorthand for the "api-development" plugin

6. **Given** I want to navigate the README quickly
   **When** I open README.md
   **Then** I see a table of contents with links to major sections

## Technical Details

### Architecture

Documentation improvements span multiple files:

1. **README.md** - Update existing file with new sections
2. **CONTRIBUTING.md** - New file with contribution guidelines
3. **docs/TROUBLESHOOTING.md** - New file with troubleshooting guide
4. **docs/PLUGIN_DEVELOPMENT.md** - New file with plugin development guide

### README.md Updates

**New Table of Contents** (add after project description):

```markdown
## Table of Contents

- [What is Spec-Driven Development?](#what-is-spec-driven-development)
- [Features](#features)
- [Quick Start](#quick-start)
- [File Reference](#file-reference)
- [Available Plugins](#available-plugins)
- [Workflow Example](#workflow-example)
- [Best Practices](#best-practices)
- [Examples](#examples)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Roadmap](#roadmap)
```

**New "File Reference" Section** (add after "Available Plugins"):

```markdown
## File Reference

### Templates

| File | Purpose | Usage |
|------|---------|-------|
| `templates/specs/feature.template.md` | Feature specification template | Copy to `specs/features/your-feature.md` |
| `templates/specs/api.template.yaml` | OpenAPI 3.0 API specification | Copy to `specs/api/your-api.yaml` |

### Plugin Templates

#### API Development Plugin
| File | Purpose |
|------|---------|
| `plugins/api-development/templates/fastapi-endpoint.py` | Complete FastAPI CRUD endpoint template |
| `plugins/api-development/templates/sam-template.yaml` | AWS SAM CloudFormation template |

#### AI Application Plugin
| File | Purpose |
|------|---------|
| `plugins/ai-app/templates/anthropic-client.py` | Production-ready Claude API client |
| `plugins/ai-app/templates/prompt-patterns.md` | Prompt engineering best practices |
```

**Plugin Naming Clarification** (update in "Available Plugins" section):

```markdown
### API Development (`/api`)

**Plugin name**: `api-development`
**Shorthand activation**: `/api` or mention "API development" in your request

**Note**: The plugin directory is named `api-development`, but you can activate it with `/api` for convenience.
```

**API Template Prominence** (add to Quick Start section):

```markdown
### 3. Create a specification

You can create either a feature spec or an API spec:

**Feature Spec:**
```bash
cp specs/feature.template.md specs/features/user-auth.md
# Edit with your requirements...
```

**API Spec (OpenAPI 3.0):**
```bash
cp specs/api.template.yaml specs/api/user-service.yaml
# Edit with your endpoints...
```
```

**Add Links to New Documentation**:

```markdown
## Contributing

Spec-Kit welcomes contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Troubleshooting

Having issues? Check [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common problems and solutions.
```

### CONTRIBUTING.md

Create comprehensive contribution guide:

```markdown
# Contributing to Spec-Kit

## Welcome

Spec-Kit is designed to grow with real-world use. We welcome contributions!

## Before You Start

1. Check existing issues and PRs
2. Open an issue to discuss major changes
3. Ensure changes align with spec-driven development philosophy

## Development Setup

```bash
git clone https://github.com/your-org/spec-kit.git
cd spec-kit
./verify.sh  # Ensure all files are present
```

## Testing Your Changes

[Once testing infrastructure exists]

```bash
./tests/run_tests.sh  # Run all tests
```

## Code Style

- **Bash scripts**: Use shellcheck, follow Google Shell Style Guide
- **Python**: Follow PEP 8, use type hints
- **Markdown**: Use consistent formatting, check links

## Plugin Contributions

See [docs/PLUGIN_DEVELOPMENT.md](docs/PLUGIN_DEVELOPMENT.md) for detailed guide.

### Plugin Quality Requirements

- Comprehensive patterns (not just examples)
- Production-ready templates
- Clear SKILL.md with proper frontmatter
- Tested in 2-3 real projects

## Pull Request Process

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes following spec-driven approach (create spec first!)
3. Add tests if applicable
4. Update documentation (README, relevant guides)
5. Run verification: `./verify.sh`
6. Submit PR with clear description

## PR Description Template

```markdown
## Description
[What does this PR do?]

## Specification
[Link to spec file if applicable]

## Testing
[How was this tested?]

## Checklist
- [ ] Spec created (if applicable)
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] verify.sh passes
```

## Review Process

- All PRs require review
- Tests must pass
- Documentation must be updated
- Changes must align with project philosophy

## Questions?

Open an issue or start a discussion.
```

### docs/TROUBLESHOOTING.md

Create troubleshooting guide:

```markdown
# Troubleshooting Guide

## Installation Issues

### Claude isn't reading CLAUDE.md

**Symptoms**: Claude doesn't follow spec-driven workflow

**Solutions**:
1. Verify file exists: `ls -la CLAUDE.md`
2. Check file is in project root (not subdirectory)
3. Restart Claude Code: `exit` then `claude`
4. Verify file permissions: `chmod 644 CLAUDE.md`

### Plugins not activating

**Symptoms**: `/api` or `/ai-app` commands don't work

**Solutions**:
1. Verify skills directory: `ls -la .claude/skills/`
2. Check skill file naming: Should be `SKILL.md` (uppercase)
3. Use full plugin name: `/api-development` instead of `/api-dev`
4. Verify SKILL.md has proper YAML frontmatter
5. Restart Claude Code

### Installer fails silently

**Symptoms**: install.sh runs but doesn't copy files

**Solutions**:
1. Check you're running from spec-kit directory: `pwd`
2. Verify spec-kit core files exist: `./verify.sh`
3. Check target directory exists: `ls -la /path/to/target`
4. Run with bash explicitly: `bash install.sh .`
5. Check for permission issues: `ls -la core/`

### Templates not found after installation

**Symptoms**: `.spec-kit-templates/` directory is empty or missing

**Solutions**:
1. Re-run installer: `./install.sh .`
2. Check plugin selection (templates come with plugins)
3. Verify source templates exist: `ls -la plugins/*/templates/`
4. Manual copy: `cp -r plugins/api-development/templates .spec-kit-templates/api-development/`

## Usage Issues

### Claude doesn't follow my spec

**Symptoms**: Implementation doesn't match specification

**Solutions**:
1. Verify spec file is in `specs/` directory
2. Explicitly reference spec in request: "Implement based on specs/features/my-feature.md"
3. Check spec has clear acceptance criteria
4. Ensure spec status is "Draft" or "In Progress" (not "Implemented")

### Spec workflow feels too rigid

**Guidance**:
- Specs are for non-trivial features (not typos, formatting)
- You can skip specs for quick fixes (constitution allows this)
- Start with simple specs, add detail as needed
- Specs can be iterative (Draft → update → implement)

### Plugin patterns don't match my stack

**Guidance**:
- Plugins are opinionated (FastAPI, not Flask; Claude API, not OpenAI)
- Create custom plugin for your stack (see docs/PLUGIN_DEVELOPMENT.md)
- Contribute plugin back to spec-kit!

## Verification Issues

### verify.sh reports missing files

**Symptoms**: Checkmarks show ✗ for existing files

**Solutions**:
1. Ensure you're in spec-kit root: `pwd`
2. Check file paths match expectations
3. Verify file naming (case-sensitive)
4. Re-run installer if files actually missing

## Development Issues

### Git conflicts on CLAUDE.md

**Guidance**:
- CLAUDE.md is meant to be customized per-project
- Keep spec-kit constitution as reference
- Resolve conflicts favoring your project-specific rules
- Consider not tracking CLAUDE.md in git

### Updates from spec-kit repo

**Options**:
1. Re-run installer (overwrites your changes)
2. Manual merge of updates
3. Use git submodule: `git submodule add <spec-kit-repo> .spec-kit`

## Still Having Issues?

1. Check you're using latest spec-kit version
2. Search existing issues: [GitHub Issues]
3. Open new issue with details:
   - spec-kit version
   - Operating system
   - Full error message
   - Steps to reproduce
```

### docs/PLUGIN_DEVELOPMENT.md

Create plugin development guide:

```markdown
# Plugin Development Guide

## Overview

Plugins extend spec-kit with domain-specific patterns and templates. This guide shows how to create high-quality plugins.

## Plugin Structure

```
plugins/your-plugin/
├── skill.md                # Main plugin file (with YAML frontmatter)
└── templates/              # Template files (optional)
    ├── template1.py
    └── template2.yaml
```

## SKILL.md Format

### Required Frontmatter

```yaml
---
name: your-plugin
description: Brief description (1-2 sentences)
version: 1.0.0
authors:
  - Your Name
tags:
  - domain
  - technology
---
```

### Required Sections

1. **When to Use This Skill** - Activation scenarios
2. **Patterns** - Best practices and patterns
3. **Templates** - Reference to template files
4. **Examples** - Real-world usage examples

### Example SKILL.md

```markdown
---
name: database
description: Database patterns with SQLAlchemy, Alembic, and schema design
version: 1.0.0
authors:
  - Spec-Kit Team
tags:
  - database
  - sqlalchemy
  - migrations
---

# Database Development Plugin

## When to Use This Skill

Activate this skill when:
- Designing database schemas
- Setting up SQLAlchemy models
- Creating Alembic migrations
- Working with DynamoDB (serverless)

## Patterns

### SQLAlchemy Models

[Detailed patterns here...]

### Alembic Migrations

[Migration patterns here...]

## Templates

See `templates/` directory for:
- `models.py` - SQLAlchemy model template
- `alembic.ini` - Alembic configuration
- `migration_template.py` - Migration template

## Examples

[Real-world examples...]
```

## Creating Templates

### Template Guidelines

1. **Production-ready**: Include error handling, logging, best practices
2. **Well-commented**: Explain non-obvious choices
3. **Modular**: Easy to extract and customize
4. **Complete**: Include imports, configuration, tests

### Template Example

```python
# templates/example.py
"""
Example template with best practices.

This template demonstrates...
"""
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def example_function(param: str) -> Optional[str]:
    """
    Does something useful.

    Args:
        param: Description

    Returns:
        Result or None
    """
    try:
        # Implementation
        return result
    except Exception as e:
        logger.error(f"Error: {e}")
        return None
```

## Plugin Quality Checklist

- [ ] SKILL.md has valid YAML frontmatter
- [ ] Frontmatter includes all required fields
- [ ] Patterns are comprehensive (not just basic examples)
- [ ] Templates are production-ready
- [ ] Tested in 2-3 real projects
- [ ] Examples show real-world usage
- [ ] Documentation is clear and complete

## Testing Your Plugin

1. **Install in test project**: Use install.sh
2. **Verify structure**: Check `.claude/skills/your-plugin/`
3. **Test activation**: Try `/your-plugin` command
4. **Use templates**: Copy and customize templates
5. **Get feedback**: Have others test your plugin

## Submitting Your Plugin

1. Create spec: `specs/features/plugin-yourname.md`
2. Implement plugin following spec
3. Test in multiple projects
4. Update install.sh to include plugin
5. Update verify.sh to validate plugin
6. Update README with plugin documentation
7. Submit PR with:
   - Spec file
   - Plugin implementation
   - Updated scripts
   - Updated documentation

## Plugin Maintenance

- Keep templates updated with latest best practices
- Respond to issues and feedback
- Update when underlying technologies change
- Consider deprecating if no longer relevant

## Examples of Good Plugins

Study existing plugins for reference:

- [plugins/api-development/](../../plugins/api-development/) - Comprehensive API patterns
- [plugins/ai-app/](../../plugins/ai-app/) - LLM integration patterns

## Questions?

Open an issue or discussion on GitHub.
```

### Security Considerations

- [ ] No sensitive data in documentation examples
- [ ] Clear warnings about security implications
- [ ] Links to external resources are HTTPS
- [ ] Code examples follow security best practices

## Edge Cases & Error Handling

1. **Edge case**: User has customized README significantly
   - **Handling**: Provide update as PR suggestion, not forced merge

2. **Edge case**: Documentation links break when files move
   - **Handling**: Use relative links, test with link checker

3. **Error**: CONTRIBUTING.md conflicts with existing file
   - **Message**: "CONTRIBUTING.md already exists. Review and merge changes manually."
   - **Recovery**: User reviews both versions

## Testing Strategy

### Manual Testing Checklist

- [ ] All links in README work correctly
- [ ] Table of contents links jump to correct sections
- [ ] File Reference table is accurate and complete
- [ ] CONTRIBUTING.md provides clear guidance
- [ ] TROUBLESHOOTING.md addresses real issues users face
- [ ] PLUGIN_DEVELOPMENT.md enables users to create plugins
- [ ] Plugin naming clarification is clear
- [ ] api.template.yaml is prominently mentioned

### Documentation Review

- [ ] Grammar and spelling checked
- [ ] Technical accuracy verified
- [ ] Examples tested
- [ ] Links validated
- [ ] Formatting consistent

## Dependencies

- **Blocked by**: None
- **Blocks**: None (but improves usability of all features)
- **Related**: testing-infrastructure (will be mentioned in CONTRIBUTING.md)

## Implementation Notes

### File Locations

- `/Users/guillermolopez/Documents/Proyectos/spec-kit/README.md` - Update
- `/Users/guillermolopez/Documents/Proyectos/spec-kit/CONTRIBUTING.md` - Create
- `/Users/guillermolopez/Documents/Proyectos/spec-kit/docs/TROUBLESHOOTING.md` - Create
- `/Users/guillermolopez/Documents/Proyectos/spec-kit/docs/PLUGIN_DEVELOPMENT.md` - Create

### README Update Strategy

1. Read current README in full
2. Identify insertion points for new sections
3. Add table of contents at top
4. Insert File Reference section after Available Plugins
5. Add Contributing and Troubleshooting links before FAQ
6. Update plugin activation examples
7. Add api.template.yaml to Quick Start

## References

- Current README: [README.md](../../README.md)
- API template: [templates/specs/api.template.yaml](../../templates/specs/api.template.yaml)
- Existing plugins: [plugins/](../../plugins/)

---

**Template Version**: 1.0
**Last Updated**: 2026-01-17
