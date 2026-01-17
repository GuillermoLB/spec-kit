# Testing Spec-Kit

This guide walks you through testing spec-kit installation and functionality.

## Pre-Installation Tests

### 1. Verify Structure

```bash
cd /path/to/spec-kit
./verify.sh
```

Expected: All files present, installer executable.

### 2. Check File Permissions

```bash
ls -l install.sh verify.sh
```

Expected: Both scripts should have execute permissions (`-rwxr-xr-x`).

## Installation Test

### 1. Create Test Project

```bash
# Create a fresh test directory
mkdir -p ~/test-spec-kit
cd ~/test-spec-kit
git init
```

### 2. Run Installer

```bash
/path/to/spec-kit/install.sh .
```

**Interactive prompts:**
- When asked for plugins: Enter `1 2` (both plugins)
- Confirm installation: Enter `y`

**Expected output:**
```
╔══════════════════════════════════════════════════════════╗
║                    Spec-Kit Installer                    ║
║          Spec-Driven Development for Claude Code         ║
╚══════════════════════════════════════════════════════════╝

ℹ Target directory: /Users/you/test-spec-kit

ℹ Available plugins:

  1) api-development  - FastAPI + AWS SAM/Lambda patterns
  2) ai-app           - LLM integration (Claude, OpenAI)
  3) all              - Install all plugins

Enter plugin numbers (space-separated, e.g., '1 2') or 'all': 1 2

ℹ Selected plugins: api-development ai-app

Proceed with installation? (y/n): y

ℹ Installing core files...
✓ Installed CLAUDE.md
✓ Created .claude/skills directory
✓ Created specs directory structure
ℹ Installing plugins...
✓ Installed plugin: api-development
  └─ Copied templates to .spec-kit-templates/api-development/
✓ Installed plugin: ai-app
  └─ Copied templates to .spec-kit-templates/ai-app/
...
╔══════════════════════════════════════════════════════════╗
║              Installation Complete! 🎉                   ║
╚══════════════════════════════════════════════════════════╝
```

### 3. Verify Installation

```bash
# Check files created
ls -la

# Should see:
# - CLAUDE.md
# - .claude/
# - specs/
# - .spec-kit-templates/
# - .gitignore

# Check plugins
ls .claude/skills/

# Should see:
# - api-development.md
# - ai-app.md
```

## Functionality Tests

### Test 1: Spec Template

```bash
# Copy and verify feature template
cp specs/feature.template.md specs/features/test-feature.md

# File should exist and be readable
cat specs/features/test-feature.md | head -20
```

Expected: Template with sections for Purpose, Requirements, Acceptance Criteria.

### Test 2: API Template

```bash
# Copy API template
cp .spec-kit-templates/api-development/fastapi-endpoint.py test-endpoint.py

# Verify it's valid Python
python3 -m py_compile test-endpoint.py

# Check template
grep "ResourceName" test-endpoint.py
```

Expected: No syntax errors, placeholders present for customization.

### Test 3: AI Client Template

```bash
# Copy AI template
cp .spec-kit-templates/ai-app/anthropic-client.py test-client.py

# Verify it's valid Python
python3 -m py_compile test-client.py
```

Expected: Valid Python file with ClaudeClient class.

### Test 4: Claude Code Integration

```bash
# Start Claude Code
claude
```

In Claude Code:

**Test 4a: Check CLAUDE.md loaded**
```
> "What workflow should I follow for new features?"
```

Expected: Claude mentions checking specs/ directory first, spec-driven workflow.

**Test 4b: Test API Plugin**
```
> "/api what patterns do you provide?"
```

Expected: Response about FastAPI, AWS SAM, error handling patterns.

**Test 4c: Test AI Plugin**
```
> "/ai-app what patterns do you provide?"
```

Expected: Response about LLM integration, Claude API, prompt engineering.

### Test 5: End-to-End Feature Implementation

**Step 1: Create a spec**

```bash
cat > specs/features/hello-api.md << 'EOF'
# Feature: Hello API

**Status**: Draft

## Purpose
Simple hello world endpoint to test spec-driven workflow.

## Requirements
- [ ] GET /hello endpoint
- [ ] Returns JSON: {"message": "Hello, World!", "timestamp": "..."}
- [ ] Status code 200

## Acceptance Criteria
1. Given I call GET /hello
   When request succeeds
   Then I receive 200 OK with greeting and timestamp
EOF
```

**Step 2: Ask Claude to implement**

```
> "Implement the hello API feature from specs/features/hello-api.md"
```

**Expected behavior:**
1. Claude reads the spec file
2. Plans the implementation
3. Creates FastAPI endpoint
4. Follows patterns from /api plugin
5. Includes error handling
6. Suggests tests

**Step 3: Verify implementation**

Check that Claude:
- Created proper Pydantic models
- Used appropriate HTTP status codes
- Added error handling
- Followed FastAPI best practices from the plugin

## Troubleshooting Tests

### Issue: CLAUDE.md not being read

```bash
# Verify file exists
cat CLAUDE.md | head -5

# Check Claude Code is in correct directory
pwd

# Restart Claude Code
```

### Issue: Plugins not activating

```bash
# Check skill files exist
ls -la .claude/skills/

# Verify file names
# Should be: api-development.md, ai-app.md

# Try activating with exact name
```

In Claude:
```
> "/api-development"  # Try full name if /api doesn't work
```

### Issue: Templates missing

```bash
# Check templates directory
ls -la .spec-kit-templates/

# Re-run installer if needed
/path/to/spec-kit/install.sh . --force
```

## Clean Up Test Project

After testing:

```bash
cd ~
rm -rf test-spec-kit
```

## Integration Tests (Real Project)

### Test in Actual Project

```bash
# Use spec-kit in a real project
cd ~/your-real-project
/path/to/spec-kit/install.sh .

# Select only plugins you'll use
# Example: Just "1" for api-development

# Test with real feature
# Create spec -> Implement -> Verify
```

### Validation Checklist

- [ ] Installation completes without errors
- [ ] CLAUDE.md exists and is readable
- [ ] Plugins are in `.claude/skills/`
- [ ] Specs directory created
- [ ] Templates copied successfully
- [ ] Claude Code reads CLAUDE.md
- [ ] `/api` skill works
- [ ] `/ai-app` skill works
- [ ] Can implement from spec successfully
- [ ] Templates are valid (syntax check)
- [ ] Workflow improves development quality

## Performance Tests

### Installation Speed

```bash
time /path/to/spec-kit/install.sh test-dir
```

Expected: < 5 seconds for full installation.

### Claude Response Quality

Compare responses:

**Without spec-kit:**
```
> "Create a user API"
```

**With spec-kit:**
```
> [Create detailed spec first]
> "Implement user API from specs/api/users.md"
```

Expected: With spec-kit, Claude produces more consistent, complete, and correct implementation.

## Acceptance Criteria

Spec-kit passes testing if:

- ✅ Installation completes successfully
- ✅ All files present in target project
- ✅ CLAUDE.md is read by Claude Code
- ✅ Both plugins are accessible via skills
- ✅ Templates are valid and usable
- ✅ End-to-end feature implementation works
- ✅ Code quality improves vs. non-spec approach
- ✅ No errors or warnings during normal use

## Reporting Issues

If tests fail:

1. Note which test failed
2. Capture error messages
3. Check file permissions
4. Verify directory structure
5. Try clean installation

For spec-kit development:
- Document the issue
- Include reproduction steps
- Note your environment (OS, Claude Code version)

---

**Last Updated**: 2024-01-17
