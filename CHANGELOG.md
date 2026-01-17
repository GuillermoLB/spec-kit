# Changelog

All notable changes to spec-kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2024-01-17

### Fixed
- **Plugin installation now follows official Claude Code conventions**
  - Skills installed as directories (e.g., `.claude/skills/api-development/`) instead of flat files
  - Renamed skill files to `SKILL.md` (uppercase) as per official standard
  - Templates moved to `skill-name/references/` directory structure
  - Maintains backward compatibility with `.spec-kit-templates/` for easy access

### Changed
- Added YAML frontmatter to all skills (`name` and `description` fields)
  - Enables auto-activation based on user context
  - Improves skill discoverability
  - Follows official skill-creator guide patterns

### Improved
- Better skill triggering reliability
- Auto-activation now works (skills load without explicit `/skill-name` command)
- Progressive disclosure pattern matches official Claude Code architecture

## [1.0.0] - 2024-01-17

### Added

#### Core
- Core constitution file (CLAUDE.md) with spec-driven workflow
- Interactive installer script with plugin selection
- Comprehensive README documentation
- Quick start guide (QUICKSTART.md)
- Verification script for structure validation
- .gitignore file

#### Plugins
- **api-development** plugin for FastAPI + AWS SAM/Lambda
  - Complete CRUD endpoint template
  - AWS SAM CloudFormation template
  - Error handling patterns
  - Testing best practices
  - OpenAPI integration guidance

- **ai-app** plugin for LLM integration
  - Production-ready Anthropic Claude API client
  - Streaming response support
  - Cost tracking and metrics
  - Prompt engineering patterns guide
  - Multi-turn conversation handling
  - Retry logic with exponential backoff

#### Templates
- Feature specification template
- API specification template (OpenAPI 3.0)

### Philosophy

Following Anthropic's principle of building tools you'll actually use daily:
- Minimal dependencies (just markdown)
- Claude Code native integration
- Based on industry standards (GitHub Spec Kit, Thoughtworks SDD)
- Practical, not theoretical

### Credits

Inspired by:
- GitHub Spec Kit
- Thoughtworks Tech Radar: Spec-Driven Development
- Anthropic's Building Effective Agents
- Martin Fowler on SDD

---

## Future Versions

### [Unreleased]

Ideas for future releases (add when validated by real usage):

- CI/CD plugin (GitHub Actions, GitLab CI, CircleCI)
- Testing plugin (pytest, coverage, TDD workflows)
- Database plugin (migrations, ORMs, schema design)
- Frontend plugin (React, TypeScript, component patterns)
- Documentation plugin (auto-generate from specs)

**Note**: New features added only after validation across multiple real projects.

---

## Version History

- **1.0.0** (2024-01-17) - Initial release
