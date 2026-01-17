# Spec-Kit

**A spec-driven development layer for Claude Code**

Spec-Kit is a lightweight, professional toolkit that brings industry-standard spec-driven development practices to your Claude Code workflows. It provides a constitution-based approach with pluggable skills for common development patterns.

## What is Spec-Driven Development?

Spec-driven development (SDD) is a methodology where:

1. **Specifications come first** - Write clear requirements before coding
2. **AI follows specs** - Claude implements based on explicit specifications
3. **Validation is built-in** - Acceptance criteria ensure correctness
4. **Consistency across teams** - Quality doesn't depend on individual prompting skills

This approach is [recommended by Thoughtworks](https://www.thoughtworks.com/en-us/radar/techniques/spec-driven-development), [adopted by GitHub](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/), and aligns with [Anthropic's agent patterns](https://www.anthropic.com/research/building-effective-agents).

## Features

- **Constitution-based workflow** - Core principles that guide all development
- **Plugin system** - Modular skills for different domains (API dev, AI apps, CI/CD)
- **Claude Code native** - Uses CLAUDE.md and skills (no external dependencies)
- **Project templates** - Reusable spec and code templates
- **Easy distribution** - One-command installation into any project

## Quick Start

### 1. Install spec-kit into your project

```bash
cd your-project/
/path/to/spec-kit/install.sh .
```

The installer will:
- Copy `CLAUDE.md` (the constitution)
- Set up `.claude/skills/` with selected plugins
- Create `specs/` directory structure
- Add template files for reference

### 2. Start Claude Code

```bash
claude
```

Claude will automatically read `CLAUDE.md` and operate in spec-driven mode.

### 3. Create a specification

```bash
# Copy the template
cp specs/feature.template.md specs/features/user-auth.md

# Edit the spec with your requirements
# ... fill in purpose, requirements, acceptance criteria ...
```

### 4. Implement with Claude

```
> "Implement the user authentication feature based on specs/features/user-auth.md"
```

Claude will:
1. Read the specification
2. Plan the implementation
3. Write code according to requirements
4. Validate against acceptance criteria

### 5. Use plugins for domain-specific patterns

```
> "/api create endpoint for user registration"
```

The API plugin provides FastAPI and AWS SAM/Lambda patterns.

```
> "/ai-app integrate Claude API for chat feature"
```

The AI-app plugin provides LLM integration best practices.

## Architecture

```
your-project/
├── CLAUDE.md                   # Core constitution (from spec-kit)
├── .claude/
│   └── skills/                 # Plugins (official Claude Code structure)
│       ├── api-development/
│       │   ├── SKILL.md        # Skill instructions
│       │   └── references/     # Templates and code examples
│       └── ai-app/
│           ├── SKILL.md
│           └── references/
├── specs/                      # Your specifications
│   ├── features/
│   │   └── user-auth.md
│   └── api/
│       └── endpoints.yaml
├── .spec-kit-templates/        # Quick reference (copy of templates)
│   ├── api-development/
│   └── ai-app/
└── src/                        # Your code
```

## Available Plugins

### API Development (`/api`)

**Focus**: FastAPI + AWS SAM/Lambda

- REST API patterns and best practices
- OpenAPI/Pydantic model generation
- AWS Lambda handler templates
- SAM CloudFormation templates
- Error handling and logging
- pytest testing patterns

**Templates**:
- `fastapi-endpoint.py` - Full CRUD endpoint template
- `sam-template.yaml` - AWS SAM serverless configuration

### AI Application (`/ai-app`)

**Focus**: LLM integration (Anthropic Claude, OpenAI)

- Claude/OpenAI API client setup
- Streaming responses
- Multi-turn conversations
- Prompt engineering patterns
- Cost tracking and rate limiting
- Error handling and retries

**Templates**:
- `anthropic-client.py` - Production-ready Claude API client
- `prompt-patterns.md` - Battle-tested prompt engineering techniques

## Workflow Example

### Traditional Approach (Without Spec-Kit)

```
You: "Add user authentication"
Claude: [Writes code based on assumptions]
You: "Actually, I need OAuth, not JWT"
Claude: [Rewrites everything]
You: "And it needs to work with AWS Cognito"
Claude: [Rewrites again]
```

### Spec-Driven Approach (With Spec-Kit)

```
You: [Create spec with requirements: OAuth, AWS Cognito, etc.]
You: "Implement user authentication per specs/features/user-auth.md"
Claude: [Reads spec, asks clarifying questions, implements correctly first time]
```

**Result**: Less back-and-forth, higher quality, consistent patterns.

## Philosophy

Spec-Kit follows Anthropic's principle of building tools you'll actually use daily. It's:

- **Minimal** - No complex frameworks or dependencies
- **Practical** - Solves real workflow problems
- **Standard** - Based on industry best practices
- **Extensible** - Add your own plugins as needed

## Creating Your Own Plugins

A plugin is just a markdown file in `.claude/skills/`:

```markdown
# My Custom Plugin

## When to Use This Skill
Activate with `/my-plugin` when...

## Patterns
[Your domain-specific patterns and best practices]

## Templates
[Code examples and scaffolding]
```

Save as `.claude/skills/my-plugin.md` and activate with `/my-plugin`.

## Best Practices

### Writing Good Specifications

**Good Spec**:
```markdown
## Requirements
- [ ] User can reset password via email link
- [ ] Link expires after 24 hours
- [ ] Password must meet complexity requirements (8+ chars, 1 number, 1 special)

## Acceptance Criteria
1. Given user requests reset
   When valid email provided
   Then link sent within 2 minutes
```

**Bad Spec**:
```markdown
## Requirements
- Password reset feature

## Acceptance Criteria
- It works
```

### Using Plugins Effectively

- **Be specific**: `/api create POST endpoint for user registration with email validation`
- **Reference specs**: `/api implement the endpoints in specs/api/user-service.yaml`
- **Combine plugins**: Use `/api` for structure, then `/ai-app` for LLM features

## Project Structure Recommendations

```
your-project/
├── specs/
│   ├── architecture.md         # High-level system design
│   ├── features/               # Feature specifications
│   │   ├── auth.md
│   │   └── payments.md
│   └── api/                    # API specifications
│       └── openapi.yaml
├── src/
│   ├── api/                    # API endpoints
│   ├── services/               # Business logic
│   └── models/                 # Data models
└── tests/
    ├── unit/
    └── integration/
```

## FAQ

### Do I need to write specs for everything?

No. Spec-Kit automatically handles exceptions:
- Trivial changes (typos, formatting) don't need specs
- Quick fixes and debugging can skip the spec process
- You control when to use spec-driven mode

### Can I use this without Claude Code?

Spec-Kit is optimized for Claude Code, but the specs and patterns are valuable regardless of tool. The CLAUDE.md file could be adapted for other AI coding assistants.

### Can I modify the installed files?

Yes! Once installed, files are copied to your project. Customize them for your needs. The `.spec-kit-templates/` folder contains reference templates.

### How do I update spec-kit in my projects?

Option 1: Re-run the installer (overwrites)
Option 2: Manually copy updated files from spec-kit repo
Option 3: Keep spec-kit as a git submodule

## Examples

See the `examples/` directory (coming soon) for:
- Sample FastAPI project with spec-kit
- AI chatbot with LLM integration
- Serverless API on AWS SAM

## Contributing

Spec-Kit is designed to grow with real-world use. Share your custom plugins:

1. Create a plugin for your domain
2. Test it across 2-3 projects
3. Submit a PR with the plugin and documentation

## Roadmap

- [ ] CI/CD plugin (GitHub Actions, GitLab CI)
- [ ] Testing plugin (pytest, coverage, TDD workflows)
- [ ] Database plugin (migrations, ORMs, schema design)
- [ ] Frontend plugin (React, TypeScript patterns)
- [ ] Documentation plugin (auto-generate from specs)

New plugins added based on community validation and real usage.

## License

MIT

## Credits

Inspired by:
- [GitHub Spec Kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [Thoughtworks Tech Radar: Spec-Driven Development](https://www.thoughtworks.com/en-us/radar/techniques/spec-driven-development)
- [Anthropic's Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Martin Fowler on SDD](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)

Built for developers who want consistent, high-quality AI-assisted coding.

---

**Version**: 1.0.0
**Last Updated**: 2024-01-17
