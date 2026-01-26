# Plugin Setup Template

**Use this template for each new plugin to establish consistent infrastructure.**

## Plugin Manifest: `.claude-plugin/plugin.json`

```json
{
  "name": "[plugin-name]",
  "description": "[Plugin description]",
  "version": "1.0.0",
  "author": {
    "name": "DevTools Team",
    "email": "devtools@company.com"
  },
  "homepage": "https://github.com/company/[plugin-name]-plugin",
  "repository": "https://github.com/company/[plugin-name]-plugin",
  "license": "MIT"
}
```

## Directory Structure

```
[plugin-name]-plugin/
├── .claude-plugin/
│   ├── plugin.json              # Plugin manifest
│   └── marketplace.json         # Marketplace configuration
├── skills/
│   └── [domain-name].md
├── commands/
│   └── [command-name].md
├── agents/
│   └── [agent-name].md          # If applicable
├── scripts/                     # If applicable
├── README.md                    # Installation & usage guide
├── LICENSE.md                   # MIT license
└── .gitignore
```

## Marketplace Configuration: `.claude-plugin/marketplace.json`

```json
{
  "name": "[plugin-name]",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@company.com"
  },
  "metadata": {
    "description": "[Plugin description]"
  },
  "plugins": [
    {
      "name": "[plugin-name]",
      "source": {
        "source": "github",
        "repo": "company/[plugin-name]-plugin",
        "ref": "v1.0.0"
      },
      "description": "[Plugin description]",
      "version": "1.0.0",
      "author": {
        "name": "DevTools Team"
      }
    }
  ]
}
```

## README.md Template

Create a README that includes:
1. Overview - What the plugin does
2. Installation instructions
3. Quick start
4. Available features (skills, commands, agents)
5. Team setup instructions
6. Support and documentation

## Installation Methods

**User Installation**:
```bash
/plugin marketplace add company/[plugin-name]-plugin
/plugin install [plugin-name]@[plugin-name]
```

**Project Installation** (in `.claude/settings.json`):
```json
{
  "extraKnownMarketplaces": {
    "[plugin-name]": {
      "source": {
        "source": "github",
        "repo": "company/[plugin-name]-plugin"
      }
    }
  },
  "enabledPlugins": {
    "[plugin-name]@[plugin-name]": true
  }
}
```

## `.gitignore`

```
# Standard Python/Node.js ignores
node_modules/
npm-debug.log
__pycache__/
*.py[cod]
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

# Build
dist/
build/
*.egg-info/
```

## LICENSE.md

MIT License - update year and copyright holder.

---

**See each plugin subdirectory for complete implementation details.**
