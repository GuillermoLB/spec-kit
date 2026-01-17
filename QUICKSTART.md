# Spec-Kit Quick Start Guide

Get started with spec-driven development in 5 minutes.

## Installation

```bash
# Navigate to your project
cd ~/my-project

# Run the installer
/path/to/spec-kit/install.sh .

# Select plugins when prompted
# Example: Enter "1 2" for api-development and ai-app
```

## Verify Installation

Check that these files were created:

```bash
ls -la
# Should see:
# - CLAUDE.md
# - .claude/skills/
# - specs/
```

## Your First Spec

### 1. Create a Feature Spec

```bash
# Copy the template
cp specs/feature.template.md specs/features/my-first-feature.md

# Edit the file
```

### 2. Fill in the Spec

```markdown
# Feature: Hello World API

**Status**: Draft
**Owner**: Your Name

## Purpose
Create a simple "hello world" API endpoint to test the setup.

## Requirements
- [ ] Endpoint responds to GET /hello
- [ ] Returns JSON with message "Hello, World!"
- [ ] Includes timestamp in response

## Acceptance Criteria
1. **Given** I call GET /hello
   **When** request is successful
   **Then** I receive 200 OK with JSON response
```

### 3. Implement with Claude

```bash
# Start Claude Code
claude
```

In Claude Code:
```
> "Implement the hello world feature from specs/features/my-first-feature.md using the API development patterns"
```

Or use the plugin directly:
```
> "/api create GET endpoint for /hello that returns a greeting with timestamp"
```

## Using Plugins

### API Development Plugin

The `/api` skill activates automatically when you mention API-related tasks, or you can invoke it explicitly:

```
> "/api create POST endpoint for user registration"
> "/api implement the API spec in specs/api/endpoints.yaml"
> "/api add error handling to the authentication endpoint"

# Or let it activate automatically:
> "Create a FastAPI endpoint for user login with JWT authentication"
```

### AI Application Plugin

The `/ai-app` skill activates automatically when you mention LLM integration, or invoke explicitly:

```
> "/ai-app create a Claude API client for chat"
> "/ai-app add streaming response support"
> "/ai-app implement cost tracking for LLM calls"

# Or let it activate automatically:
> "Integrate Claude API for the chat feature with streaming"
```

## Workflow Tips

### Daily Workflow

1. **Morning**: Review `specs/` directory
2. **Planning**: Create/update specs for today's work
3. **Development**: Use Claude with `/api` or `/ai-app` skills
4. **Testing**: Verify against acceptance criteria
5. **Completion**: Mark spec requirements as done

### When to Write a Spec

**Write a spec for**:
- New features
- Complex bug fixes
- API changes
- Architecture changes

**Skip the spec for**:
- Typo fixes
- Formatting changes
- Trivial updates

### Working with Templates

Reference templates are in `.spec-kit-templates/`:

```bash
# Copy a template to start coding
cp .spec-kit-templates/api-development/fastapi-endpoint.py src/api/users.py

# Then customize for your needs
```

## Example Session

```bash
# 1. Create spec
cat > specs/features/user-list.md << 'EOF'
# Feature: List Users

## Requirements
- [ ] GET /users endpoint
- [ ] Pagination support
- [ ] Returns user list as JSON

## Acceptance Criteria
1. Given I call GET /users?skip=0&limit=10
   When users exist
   Then I get up to 10 users
EOF

# 2. Start Claude
claude

# 3. In Claude, implement
> "/api implement the user list endpoint from specs/features/user-list.md"

# Claude will:
# - Read the spec
# - Create the endpoint following FastAPI patterns
# - Add pagination
# - Include error handling
# - Write tests
```

## Customization

### Add Your Own Plugin

Create `.claude/skills/my-plugin.md`:

```markdown
# My Custom Plugin

## When to Use
Activate with `/my-plugin` when working on [specific task].

## Patterns

### Pattern 1
[Your best practices here]

### Pattern 2
[Your templates here]
```

Use it:
```
> "/my-plugin do something specific"
```

### Modify the Constitution

Edit `CLAUDE.md` to add project-specific rules:

```markdown
## Project-Specific Rules

- Always use TypeScript strict mode
- Follow our naming convention: PascalCase for classes, camelCase for functions
- Add JSDoc comments to all public functions
```

## Troubleshooting

### Claude isn't reading CLAUDE.md

- Verify file exists: `ls -la CLAUDE.md`
- Restart Claude Code
- Check file permissions

### Plugins not working

- Verify skills exist: `ls -la .claude/skills/`
- Use exact skill name: `/api-development` not `/api-dev`
- Check skill file format (should be markdown)

### Templates not found

- Templates are optional reference files
- Check `.spec-kit-templates/` directory
- Re-run installer if missing

## Next Steps

1. **Try it out**: Implement a simple feature end-to-end
2. **Customize**: Modify CLAUDE.md for your project
3. **Expand**: Create custom plugins for your domain
4. **Share**: Help improve spec-kit with feedback

## Resources

- Full documentation: [README.md](README.md)
- Plugin development: [core/CLAUDE.md](core/CLAUDE.md)
- Templates: `.spec-kit-templates/`

## Support

- Issues: GitHub Issues (if published)
- Questions: Check README.md FAQ section

---

**Ready to build?** Start with a simple spec and let Claude Code implement it following your patterns.
