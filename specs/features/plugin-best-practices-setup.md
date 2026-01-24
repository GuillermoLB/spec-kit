# Feature: Best Practices Plugin - Setup & Infrastructure

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-24
**Priority**: High

## Purpose

Establish the core plugin infrastructure for the best-practices plugin. This feature creates the plugin manifest, marketplace configuration, and overall plugin structure that will serve as the foundation for testing, CI/CD, code quality, documentation, and agent features.

This enables teams to install and enable a unified best-practices plugin through Claude Code's marketplace, providing the scaffolding for all subsequent features.

## Requirements

- [ ] Create plugin manifest (`.claude-plugin/plugin.json`)
- [ ] Create marketplace configuration (`.claude-plugin/marketplace.json`)
- [ ] Create base plugin directory structure
- [ ] Create `README.md` with installation and usage instructions
- [ ] Create `LICENSE.md` (MIT license)
- [ ] Initialize Git repository for plugin distribution
- [ ] Support marketplace installation via `/plugin marketplace add`
- [ ] Support plugin installation via `/plugin install best-practices@best-practices`
- [ ] Create project's `.claude/settings.json` example with plugin enabled

## User Stories

**As a** DevTools team lead
**I want** to create a centralized best-practices plugin for my organization
**So that** I can distribute standardized development practices to my entire team

**As a** developer
**I want** to install the best-practices plugin from my company's marketplace
**So that** I have access to all best-practice skills and commands

**As a** team member
**I want** my team's `.claude/settings.json` to auto-enable best-practices
**So that** I don't have to manually install the plugin

## Acceptance Criteria

1. **Given** a developer runs `/plugin marketplace add company/best-practices-plugin`
   **When** the marketplace is added
   **Then** the plugin appears as available for installation

2. **Given** a developer runs `/plugin install best-practices@best-practices`
   **When** the plugin is installed
   **Then** the installation completes without errors and the plugin is available

3. **Given** a project team commits `.claude/settings.json` with the plugin enabled
   **When** team members open the project
   **Then** Claude Code prompts to trust and enable the plugin automatically

4. **Given** a developer runs `/best-practices`
   **When** the plugin is enabled
   **Then** they see the available commands and can access help

5. **Given** a developer views the README
   **When** they follow the installation instructions
   **Then** they successfully install the plugin in their Claude Code setup

## Technical Details

### Plugin Structure

```
best-practices-plugin/
├── .claude-plugin/
│   ├── plugin.json              # Plugin manifest
│   └── marketplace.json         # Marketplace configuration
├── skills/                      # Created by subsequent features
│   ├── testing/
│   ├── ci-cd/
│   ├── code-quality/
│   └── documentation/
├── commands/                    # Created by subsequent features
├── agents/                      # Created by subsequent features
├── README.md                    # Installation & usage guide
├── LICENSE.md                   # MIT license
└── .gitignore
```

### Plugin Manifest: `.claude-plugin/plugin.json`

```json
{
  "name": "best-practices",
  "description": "Comprehensive plugin for testing, CI/CD, and code quality best practices",
  "version": "1.0.0",
  "author": {
    "name": "DevTools Team",
    "email": "devtools@company.com"
  },
  "homepage": "https://github.com/company/best-practices-plugin",
  "repository": "https://github.com/company/best-practices-plugin",
  "license": "MIT"
}
```

**Key Fields**:
- `name`: Used in command invocation (`/best-practices:command-name`)
- `version`: Semantic versioning for marketplace updates
- `description`: Shown in plugin marketplace and manager
- `author`: Team responsible for maintaining plugin

### Marketplace Configuration: `.claude-plugin/marketplace.json`

```json
{
  "name": "best-practices",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@company.com"
  },
  "metadata": {
    "description": "Company-wide best practices for testing, CI/CD, and code quality"
  },
  "plugins": [
    {
      "name": "best-practices",
      "source": {
        "source": "github",
        "repo": "company/best-practices-plugin",
        "ref": "v1.0.0"
      },
      "description": "Comprehensive plugin for testing, CI/CD, and code quality best practices",
      "version": "1.0.0",
      "author": {
        "name": "DevTools Team"
      }
    }
  ]
}
```

**Marketplace Features**:
- Holds multiple plugins (just one now, extendable later)
- Supports version pinning (`ref: "v1.0.0"`)
- Supports multiple source types (GitHub, GitLab, Bitbucket, local)
- Can be hosted on any Git service

### README.md Structure

**Sections**:
1. Overview - What the plugin does
2. Installation instructions
   - Marketplace setup
   - Plugin installation
   - Verification steps
3. Quick start
   - Basic command examples
   - How to enable in projects
4. Available features
   - Skills (auto-triggered)
   - Commands (user-invoked)
   - Agents (comprehensive analysis)
5. Team setup
   - `.claude/settings.json` configuration
   - Enabling for project teams
6. Support and documentation

**Example Content**:
```markdown
# Best Practices Plugin

Comprehensive plugin for enforcing testing, CI/CD, and code quality standards.

## Installation

### Add the Marketplace

\`\`\`bash
/plugin marketplace add company/best-practices-plugin
\`\`\`

### Install the Plugin

\`\`\`bash
/plugin install best-practices@best-practices
\`\`\`

## Quick Start

### View Available Commands

\`\`\`bash
/best-practices
\`\`\`

### Run Tests with Analysis

\`\`\`bash
/best-practices:run-tests
\`\`\`

### Set Up CI/CD

\`\`\`bash
/best-practices:setup-ci
\`\`\`

### Check Code Quality

\`\`\`bash
/best-practices:check-quality
\`\`\`

## For Teams

Add to your project's `.claude/settings.json`:

\`\`\`json
{
  "extraKnownMarketplaces": {
    "best-practices": {
      "source": {
        "source": "github",
        "repo": "company/best-practices-plugin"
      }
    }
  },
  "enabledPlugins": {
    "best-practices@best-practices": true
  }
}
\`\`\`
```

### Plugin Repository Setup

**File**: `.gitignore`
```
# Node/npm
node_modules/
npm-debug.log
yarn.lock

# Python
__pycache__/
*.py[cod]
*$py.class
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build artifacts
dist/
build/
*.egg-info/
```

**File**: `LICENSE.md`
```
MIT License

Copyright (c) 2026 DevTools Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

[Standard MIT License text...]
```

### Installation Methods

**Method 1: User Installation** (User scope)
```bash
/plugin marketplace add company/best-practices-plugin
/plugin install best-practices@best-practices
```

**Method 2: Project Installation** (Project scope)
Add to `.claude/settings.json` in project repository:
```json
{
  "extraKnownMarketplaces": {
    "best-practices": {
      "source": {
        "source": "github",
        "repo": "company/best-practices-plugin"
      }
    }
  },
  "enabledPlugins": {
    "best-practices@best-practices": true
  }
}
```

**Method 3: Private Repository**
With GitHub/GitLab authentication:
```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
/plugin marketplace add company/best-practices-plugin
```

## Edge Cases & Error Handling

1. **Edge case**: User doesn't have marketplace access
   - **Handling**: Provide fallback installation instructions
   - **Message**: "If you can't access the marketplace, ask your admin for GitHub access"

2. **Edge case**: Plugin already installed
   - **Handling**: Offer to update to latest version
   - **Message**: "Plugin already installed (v1.0.0). Update to latest?"

3. **Error**: Repository access denied
   - **Message**: "Cannot access plugin repository. Check authentication and permissions."
   - **Recovery**: Provide GitHub token setup instructions

4. **Edge case**: Conflicting plugin name
   - **Handling**: Plugin manager prevents duplicate installation
   - **Message**: "best-practices already installed, please uninstall first"

5. **Edge case**: Network unreachable
   - **Handling**: Marketplace operations fail gracefully
   - **Message**: "Cannot connect to marketplace. Check your internet connection."

## Security Considerations

- [ ] Plugin repository requires HTTPS
- [ ] No hardcoded credentials in plugin files
- [ ] Version pinning in marketplace prevents unexpected upgrades
- [ ] Plugin permissions configuration respected
- [ ] License clearly documented (MIT)

## Testing Strategy

### Installation Testing

- [ ] Marketplace can be added via `/plugin marketplace add`
- [ ] Plugin can be installed from marketplace
- [ ] Plugin appears in `/plugin` list after installation
- [ ] Plugin can be enabled/disabled without errors
- [ ] Plugin cache is properly managed

### Integration Testing

- [ ] Settings file properly loads marketplace configuration
- [ ] Project-level `.claude/settings.json` enables plugin for team
- [ ] Subsequent features (testing, CI/CD, etc.) install correctly on top

### Documentation Testing

- [ ] README installation steps work end-to-end
- [ ] All links in README are valid
- [ ] Example `.claude/settings.json` is syntactically valid JSON

## Dependencies

- **Blocked by**: None (this is the foundation)
- **Blocks**:
  - plugin-best-practices-testing
  - plugin-best-practices-ci-cd
  - plugin-best-practices-code-quality
  - plugin-best-practices-documentation
  - plugin-best-practices-agents
- **Related**: Claude Code plugin marketplace system

## Implementation Notes

### Decisions Made

- **Single marketplace with multiple plugins**: Simplifies team distribution
- **MIT License**: Standard open-source license, allows commercial use
- **GitHub as primary host**: Most common, best documented
- **Version 1.0.0 release**: Conservative initial release
- **Project-level configuration**: Enables team-wide adoption

### Repository Structure Rationale

- `.claude-plugin/` directory marks this as a plugin (required)
- `skills/`, `commands/`, `agents/` match Claude Code plugin conventions
- README provides both user and team installation paths
- `.gitignore` prevents committing unnecessary files

### Authentication Strategy

- Environment variables (GITHUB_TOKEN, GITLAB_TOKEN) for private repos
- No embedded credentials
- Documentation guides users through authentication

## Open Questions

- [ ] Should we create a public GitHub repo or keep it private?
  - *Decision pending*: User preference on company vs. public distribution
- [ ] Will there be an approval/review process for plugin updates?
  - *Decision pending*: Version numbering and release process TBD

## References

- Claude Code Plugins: https://code.claude.com/docs/en/plugins.md
- Plugin Marketplaces: https://code.claude.com/docs/en/plugin-marketplaces.md
- Installing Plugins: https://code.claude.com/docs/en/discover-plugins.md
- GitHub OAuth Tokens: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

---

**Template Version**: 1.0
**Last Updated**: 2026-01-24
