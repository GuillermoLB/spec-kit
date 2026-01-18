# Plugin Development Guide

Learn how to create high-quality plugins that extend Spec-Kit with domain-specific patterns and templates.

## Table of Contents

- [Overview](#overview)
- [Plugin Structure](#plugin-structure)
- [SKILL.md Format](#skillmd-format)
- [Creating Templates](#creating-templates)
- [Plugin Quality Checklist](#plugin-quality-checklist)
- [Testing Your Plugin](#testing-your-plugin)
- [Submitting Your Plugin](#submitting-your-plugin)
- [Examples](#examples)

## Overview

Plugins extend Spec-Kit with domain-specific knowledge. A good plugin provides:

1. **Patterns** - Best practices and architectural guidance
2. **Templates** - Production-ready code examples
3. **Context** - When and how to use each pattern
4. **Examples** - Real-world usage scenarios

## Plugin Structure

```
plugins/your-plugin/
├── SKILL.md                # Main plugin file (with YAML frontmatter)
└── templates/              # Template files (optional)
    ├── template1.py
    ├── template2.yaml
    └── README.md           # Template usage guide
```

### Directory Naming

- Use **lowercase with hyphens**: `database-plugin`, not `Database_Plugin`
- Be specific: `api-development`, not just `api`
- Keep it short: 1-3 words maximum

### File Requirements

- **SKILL.md** - Required, must be uppercase
- **templates/** - Optional, but recommended for comprehensive plugins
- **templates/README.md** - Optional, explains template usage

## SKILL.md Format

### Required YAML Frontmatter

Every SKILL.md must start with valid YAML frontmatter:

```yaml
---
name: your-plugin-name
description: One-sentence description of what this plugin does (50-100 chars)
version: 1.0.0
authors:
  - Your Name
  - Another Contributor
tags:
  - relevant-domain
  - technology
  - use-case
---
```

**Frontmatter Guidelines**:
- `name`: Match directory name (lowercase-with-hyphens)
- `description`: Clear, concise, actionable (what user gets, not what plugin is)
- `version`: Semantic versioning (MAJOR.MINOR.PATCH)
- `authors`: Real names or GitHub usernames
- `tags`: 2-5 relevant tags for discovery

### Required Content Sections

After frontmatter, include these sections:

#### 1. When to Use This Skill

Explain when the plugin should activate:

```markdown
## When to Use This Skill

Activate this skill when:
- Designing database schemas
- Setting up SQLAlchemy models and relationships
- Creating Alembic migrations
- Working with DynamoDB in serverless apps

**Auto-activation keywords**: database, schema, migration, SQLAlchemy, Alembic, DynamoDB
```

**Guidelines**:
- List specific scenarios (not vague "when working with databases")
- Mention auto-activation keywords
- Explain both explicit (`/plugin`) and implicit activation

#### 2. Patterns

This is the heart of your plugin. Provide **comprehensive** patterns, not just examples:

```markdown
## Patterns

### Pattern 1: SQLAlchemy Model Definition

**When to use**: Defining ORM models for relational databases

**Best practices**:
- Use declarative base for all models
- Define relationships with `back_populates`
- Include `__repr__` for debugging
- Add indexes for frequently queried fields
- Use mixins for common patterns (timestamps, soft delete)

**Example**:
[Full, production-ready example code]

**Common pitfalls**:
- Circular imports (use string references for relationships)
- Missing indexes on foreign keys
- N+1 query problems (use joinedload)
```

**Pattern Guidelines**:
- **Comprehensive, not basic**: Cover edge cases, not just happy path
- **Production-ready**: Include error handling, logging, best practices
- **Explain "why"**: Don't just show code, explain decisions
- **Common pitfalls**: Warn about mistakes beginners make
- **Multiple approaches**: Show when to use different techniques

#### 3. Templates

Reference template files with clear explanation:

```markdown
## Templates

The `templates/` directory contains production-ready starting points:

### models.py
**Purpose**: SQLAlchemy model template with common patterns
**Usage**:
```bash
cp .spec-kit-templates/database/models.py src/models/user.py
# Customize for your domain
```

**Includes**:
- Base model with timestamps
- Relationship examples (one-to-many, many-to-many)
- Custom column types
- Model methods and properties

### alembic.ini
**Purpose**: Alembic configuration for migrations
**Usage**: [Clear instructions]
```

#### 4. Examples

Show real-world usage:

```markdown
## Examples

### Example 1: E-commerce Product Catalog

**Scenario**: Building product catalog with categories and inventory

**Approach**:
[Step-by-step walkthrough with code]

**Key decisions**:
- Why this relationship structure
- Performance considerations
- Trade-offs made

### Example 2: Multi-tenant SaaS

**Scenario**: Isolating tenant data with row-level security

**Approach**:
[Different pattern for different use case]
```

## Creating Templates

### Template Quality Guidelines

Templates should be **production-ready**, not toys:

1. **Complete**: Include all necessary imports, dependencies, configuration
2. **Well-commented**: Explain non-obvious choices, not obvious syntax
3. **Error handling**: Don't assume happy path
4. **Logging**: Include appropriate logging
5. **Type hints**: Use for Python code
6. **Modular**: Easy to extract and customize
7. **Best practices**: Follow language/framework conventions

### Template Example Structure

**Python Template** (`templates/example.py`):

```python
"""
Module description.

This template demonstrates [specific pattern]. Use it when [scenario].

Dependencies:
    - package>=1.0.0
    - another-package>=2.0.0

Usage:
    from module import ExampleClass
    instance = ExampleClass(config)
    result = instance.method()
"""
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ExampleClass:
    """
    Brief class description.

    This class provides [functionality]. Use it for [use case].

    Attributes:
        param: Description of param

    Example:
        >>> instance = ExampleClass("value")
        >>> result = instance.method()
        >>> print(result)
        "Expected output"
    """

    def __init__(self, param: str) -> None:
        """
        Initialize the class.

        Args:
            param: Description of what this parameter controls
        """
        self.param = param
        logger.info(f"ExampleClass initialized with param: {param}")

    def method(self) -> Optional[str]:
        """
        Does something useful.

        Returns:
            Result or None if operation fails

        Raises:
            ValueError: If param is invalid
        """
        try:
            # Implementation with comments explaining non-obvious parts
            result = self._process(self.param)
            return result
        except Exception as e:
            logger.error(f"Error in method: {e}", exc_info=True)
            return None

    def _process(self, value: str) -> str:
        """Private helper method."""
        if not value:
            raise ValueError("Value cannot be empty")
        return value.upper()
```

**YAML/Config Template** (`templates/config.yaml`):

```yaml
# Configuration template for [purpose]
#
# Usage:
#   1. Copy this file to your project
#   2. Update the values below
#   3. Reference in your code: config = load_config("config.yaml")

# Application settings
app:
  name: "your-app-name"  # Change to your app name
  version: "1.0.0"
  environment: "development"  # development | staging | production

# Database configuration
database:
  # For local development, use SQLite
  # url: "sqlite:///./app.db"

  # For production, use PostgreSQL
  url: "postgresql://user:pass@localhost/dbname"

  # Connection pool settings (adjust for your load)
  pool_size: 5
  max_overflow: 10

# Logging configuration
logging:
  level: "INFO"  # DEBUG | INFO | WARNING | ERROR
  format: "json"  # json | text
  output: "stdout"  # stdout | file
```

### Template Documentation

Include a `templates/README.md` explaining:

```markdown
# [Plugin Name] Templates

## Overview

This directory contains templates for [purpose].

## Available Templates

### template1.py
**Use when**: [Scenario]
**Includes**: [Key features]
**Setup**: [Dependencies, configuration]

### template2.yaml
**Use when**: [Scenario]
**Includes**: [Key sections]
**Setup**: [How to use]

## Quick Start

[Step-by-step example of using templates]

## Customization

Common modifications:
1. [Change X for Y]
2. [Adjust Z based on W]
```

## Plugin Quality Checklist

Before submitting, ensure:

### Content Quality
- [ ] SKILL.md has valid YAML frontmatter (test with YAML parser)
- [ ] Frontmatter includes all required fields (name, description, version, authors, tags)
- [ ] Patterns are comprehensive (not just basic examples)
- [ ] Patterns explain "why", not just "what"
- [ ] Templates are production-ready (error handling, logging, typing)
- [ ] Templates are well-commented (explain non-obvious choices)
- [ ] Examples show real-world usage (not toy scenarios)
- [ ] Documentation is clear and complete

### Testing
- [ ] Tested in 2-3 real projects (not just theoretical)
- [ ] Templates successfully used in production code
- [ ] Patterns validated by domain experts
- [ ] Auto-activation works with relevant keywords
- [ ] Explicit activation works (`/plugin-name`)

### Integration
- [ ] Plugin added to `install.sh` menu
- [ ] Plugin added to `verify.sh` checks
- [ ] README updated with plugin description
- [ ] QUICKSTART updated with usage example

### Polish
- [ ] Spelling and grammar checked
- [ ] Code examples tested and working
- [ ] Links in documentation verified
- [ ] Consistent formatting throughout

## Testing Your Plugin

### Local Testing

1. **Install in test project**:
```bash
cd /tmp/test-project
/path/to/spec-kit/install.sh .
# Select your plugin when prompted
```

2. **Verify structure**:
```bash
ls -la .claude/skills/your-plugin/
cat .claude/skills/your-plugin/SKILL.md
```

3. **Test activation**:
```bash
claude
> "/your-plugin help me with [task]"
```

4. **Use templates**:
```bash
cp .spec-kit-templates/your-plugin/template.py src/
# Customize and verify it works
```

### Real Project Testing

Test your plugin in **2-3 actual projects**:

1. Different project sizes (small, medium, large)
2. Different use cases for your domain
3. Get feedback from other developers

**Validation criteria**:
- Did the patterns apply to real scenarios?
- Were templates useful or did users rewrite everything?
- Did auto-activation work as expected?
- What was missing or confusing?

### YAML Validation

Test frontmatter is valid:

```python
import yaml

with open('.claude/skills/your-plugin/SKILL.md') as f:
    content = f.read()
    # Extract frontmatter (between --- markers)
    if content.startswith('---'):
        parts = content.split('---', 2)
        frontmatter = parts[1]
        # Parse YAML
        data = yaml.safe_load(frontmatter)
        print("Valid YAML:", data)
```

## Submitting Your Plugin

### 1. Create Specification

Create `specs/features/plugin-yourname.md`:

```bash
cd /path/to/spec-kit
cp templates/specs/feature.template.md specs/features/plugin-database.md
# Fill in the specification
```

### 2. Implement Plugin

Following the spec:
1. Create `plugins/your-plugin/` directory
2. Write SKILL.md with frontmatter
3. Create templates (if applicable)
4. Test in real projects

### 3. Update Installation Scripts

**Update install.sh**:
```bash
# Add to plugin menu
echo "5. Your Plugin - Brief description"

# Add to installation cases
case $plugin_num in
    # ... existing cases ...
    5)
        echo "Installing Your Plugin..."
        mkdir -p "$TARGET/.claude/skills/your-plugin"
        cp "$BASE/plugins/your-plugin/SKILL.md" "$TARGET/.claude/skills/your-plugin/"
        if [ -d "$BASE/plugins/your-plugin/templates" ]; then
            mkdir -p "$TARGET/.spec-kit-templates/your-plugin"
            cp -r "$BASE/plugins/your-plugin/templates/"* "$TARGET/.spec-kit-templates/your-plugin/"
        fi
        ;;
esac
```

**Update verify.sh**:
```bash
# Add plugin verification
if [ -f "plugins/your-plugin/SKILL.md" ]; then
    echo -e "${GREEN}✓${NC} Plugin: your-plugin"
else
    echo -e "${RED}✗${NC} Plugin: your-plugin"
fi
```

### 4. Update Documentation

**Update README.md**:
```markdown
### Your Plugin (`/your-plugin`)

**Focus**: Brief description

- Pattern 1
- Pattern 2
- Pattern 3

**Templates**:
- `template1.ext` - Description
- `template2.ext` - Description
```

**Update QUICKSTART.md** (if applicable):
```markdown
### Your Plugin

[Example of using your plugin]
```

### 5. Submit Pull Request

Use this PR template:

```markdown
## Description
New plugin: [Your Plugin Name]

Provides [brief description of what it does].

## Specification
`specs/features/plugin-yourname.md`

## Testing
Tested in:
1. Project 1 (description)
2. Project 2 (description)
3. Project 3 (description)

Validated by:
- [Name/Role] - Domain expert review
- [Name/Role] - Code review

## Checklist
- [ ] Spec created and approved
- [ ] SKILL.md has valid YAML frontmatter
- [ ] Templates are production-ready
- [ ] Tested in 2-3 real projects
- [ ] install.sh updated
- [ ] verify.sh updated
- [ ] README updated
- [ ] QUICKSTART updated (if applicable)
- [ ] Domain expert review completed
```

## Plugin Maintenance

After your plugin is merged:

### Keep Templates Updated

- Monitor for library updates (new versions, deprecated features)
- Update templates when best practices change
- Add new patterns as they emerge

### Respond to Feedback

- Address issues related to your plugin
- Incorporate user suggestions
- Fix bugs promptly

### Version Updates

When to bump version:
- **Patch (1.0.X)**: Bug fixes, typo corrections
- **Minor (1.X.0)**: New patterns, new templates, enhancements
- **Major (X.0.0)**: Breaking changes, major rewrites

### Deprecation

If your plugin becomes obsolete:
1. Mark as deprecated in frontmatter
2. Provide migration guide to replacement
3. Keep for 2-3 versions before removal

## Examples of Good Plugins

Study existing plugins for reference:

### API Development Plugin

**Location**: [plugins/api-development/](../plugins/api-development/)

**What makes it good**:
- Comprehensive FastAPI and AWS SAM patterns
- Production-ready templates with error handling
- Clear examples for common scenarios
- Well-documented activation triggers

### AI Application Plugin

**Location**: [plugins/ai-app/](../plugins/ai-app/)

**What makes it good**:
- Covers multiple LLM providers
- Streaming and cost tracking patterns
- Prompt engineering best practices
- Real-world async handling

### Anti-Examples (What NOT to Do)

**Bad Plugin Example**:
```markdown
---
name: web
description: web stuff
version: 1.0
authors:
  - Me
tags:
  - web
---

# Web Plugin

Use this for web development.

## Patterns

### Flask App

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello"
```

## Templates

See code above.
```

**Problems**:
- Vague name ("web" is too broad)
- Poor description ("web stuff")
- No comprehensive patterns
- Toy example, not production code
- No error handling or best practices
- Missing when-to-use guidance
- No real-world examples

## Questions?

- Check existing plugins for examples
- Open an issue with "Plugin Idea:" prefix
- Join discussions on plugin proposals

---

**Ready to create a plugin?** Start with a specification, validate with real usage, then share with the community!
