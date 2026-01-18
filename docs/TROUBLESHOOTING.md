# Troubleshooting Guide

Common issues and solutions for Spec-Kit.

## Installation Issues

### Claude isn't reading CLAUDE.md

**Symptoms**: Claude doesn't follow spec-driven workflow after installation

**Solutions**:
1. Verify file exists: `ls -la CLAUDE.md`
2. Check file is in project root (not in subdirectory)
3. Restart Claude Code: Exit and relaunch with `claude`
4. Verify file permissions: `chmod 644 CLAUDE.md`
5. Ensure file is not empty: `cat CLAUDE.md` should show content

**Why this happens**: Claude Code reads CLAUDE.md automatically from the current working directory. If the file doesn't exist or isn't readable, Claude won't see the instructions.

### Plugins not activating

**Symptoms**: `/api` or `/ai-app` commands don't work or aren't recognized

**Solutions**:
1. Verify skills directory exists: `ls -la .claude/skills/`
2. Check skill file naming: Should be `SKILL.md` (uppercase, not `skill.md`)
3. Verify skill file has content: `cat .claude/skills/api-development/SKILL.md`
4. Use full plugin name: `/api-development` instead of variations like `/api-dev`
5. Try short alias: `/api` for `api-development`
6. Verify SKILL.md has proper YAML frontmatter (starts with `---`)
7. Restart Claude Code after adding new plugins

**Example of checking plugin structure**:
```bash
# Should show SKILL.md file
ls -la .claude/skills/api-development/

# Should show YAML frontmatter at the top
head -15 .claude/skills/api-development/SKILL.md
```

### Installer fails silently

**Symptoms**: `install.sh` runs but doesn't copy files to your project

**Solutions**:
1. Check you're in spec-kit directory: `pwd` should show path to spec-kit
2. Verify spec-kit core files exist: `./verify.sh` in spec-kit directory
3. Check target directory exists: `ls -la /path/to/target`
4. Run with bash explicitly: `bash install.sh .`
5. Check for permission issues: `ls -la core/CLAUDE.md`
6. Ensure target path is provided: `./install.sh .` (for current directory)

**Debug mode**:
```bash
# Add -x for debugging
bash -x ./install.sh .
```

### Templates not found after installation

**Symptoms**: `.spec-kit-templates/` directory is empty or missing

**Solutions**:
1. Re-run installer: `./install.sh .` from spec-kit directory
2. Check plugin selection - templates come with plugins
3. Verify source templates exist: `ls -la plugins/*/templates/` in spec-kit
4. Manual copy if needed:
   ```bash
   mkdir -p .spec-kit-templates
   cp -r /path/to/spec-kit/plugins/api-development/templates .spec-kit-templates/api-development/
   ```

### specs/ directory not created

**Symptoms**: No `specs/` directory after installation

**Solutions**:
1. Check if installer completed: Look for success message
2. Verify you're in the right directory: `pwd`
3. Manual creation:
   ```bash
   mkdir -p specs/features specs/api
   cp /path/to/spec-kit/templates/specs/feature.template.md specs/
   cp /path/to/spec-kit/templates/specs/api.template.yaml specs/
   ```

## Usage Issues

### Claude doesn't follow my spec

**Symptoms**: Implementation doesn't match the specification

**Solutions**:
1. Verify spec file is in `specs/` directory (not somewhere else)
2. Explicitly reference spec in your request:
   ```
   > "Implement the user authentication feature based on specs/features/user-auth.md"
   ```
3. Check spec has clear acceptance criteria section
4. Ensure spec status is "Draft" or "In Progress" (not "Implemented")
5. Make requirements specific and measurable
6. Ask Claude to read the spec first: `> "Read specs/features/my-feature.md and summarize the requirements"`

**Tip**: The more specific your spec, the better the implementation.

### Spec workflow feels too rigid

**Symptoms**: Feel constrained by always needing specs

**Guidance**:

Specs are **not required** for:
- Typo fixes
- Formatting changes
- Simple refactoring
- Quick debugging
- Minor documentation updates

Specs are **recommended** for:
- New features (even small ones)
- API changes
- Architectural changes
- Complex bug fixes
- Anything that affects multiple files

**Remember**: You control when to use spec-driven mode. CLAUDE.md has exceptions built in for trivial changes.

### Plugin patterns don't match my stack

**Symptoms**: Plugins provide FastAPI patterns but you use Flask, or Claude API but you use OpenAI

**Guidance**:

Spec-Kit plugins are **intentionally opinionated**:
- API plugin: FastAPI + AWS SAM (not Flask, not Django)
- AI plugin: Claude API (not OpenAI, not local LLMs)

**Options**:
1. **Adapt patterns** to your stack (patterns are transferable)
2. **Create custom plugin** for your stack (see [docs/PLUGIN_DEVELOPMENT.md](PLUGIN_DEVELOPMENT.md))
3. **Contribute plugin** back to spec-kit for others with same stack
4. **Use generic spec-driven workflow** without domain plugins

### Can't find template files

**Symptoms**: Don't know where templates are or which to use

**Solutions**:
1. Check README "Available Templates" section
2. List templates:
   ```bash
   # Specification templates
   ls -la specs/*.md specs/*.yaml

   # Plugin templates
   ls -la .spec-kit-templates/*/
   ```
3. Templates are in two places:
   - **Spec templates**: `specs/` directory (feature.template.md, api.template.yaml)
   - **Code templates**: `.spec-kit-templates/[plugin]/` (reference implementations)

## Verification Issues

### verify.sh reports missing files

**Symptoms**: Running `./verify.sh` shows ✗ for files you think exist

**Solutions**:
1. Ensure you're in **spec-kit root directory**: `pwd`
2. Check file paths exactly match what verify.sh expects
3. Verify file naming is correct (case-sensitive on Linux/Mac)
4. Re-run installer if files are actually missing

**Note**: verify.sh is for checking spec-kit itself, not your project.

### verify.sh not found

**Symptoms**: `./verify.sh: No such file or directory`

**Solution**: You're trying to run verify.sh in your project. This script only exists in the spec-kit repository, not in installed projects.

```bash
# Wrong: In your project
cd ~/my-project
./verify.sh  # ✗ Doesn't exist

# Right: In spec-kit repo
cd /path/to/spec-kit
./verify.sh  # ✓ Works
```

## Development Issues

### Git conflicts on CLAUDE.md

**Symptoms**: Merge conflicts when updating from spec-kit

**Guidance**:

CLAUDE.md is meant to be **customized per-project**:
- Core spec-kit CLAUDE.md is a starting point
- Your project's CLAUDE.md should have project-specific rules
- Conflicts are expected if you customize

**Resolution options**:
1. **Keep your version** if you've customized for your project
2. **Merge manually** to incorporate spec-kit updates
3. **Don't track CLAUDE.md in git** if it's purely for local development

**Best practice**: Add project-specific rules at the bottom:
```markdown
---
## Project-Specific Rules

- Always use TypeScript strict mode
- Follow naming convention: PascalCase for classes
...
```

### Getting updates from spec-kit

**Symptoms**: Want to update installed files with latest from spec-kit

**Options**:

**Option 1: Re-run installer (overwrites)**
```bash
cd /path/to/spec-kit
git pull  # Update spec-kit
cd ~/my-project
/path/to/spec-kit/install.sh .  # Re-install
```
**Warning**: Overwrites CLAUDE.md and skills

**Option 2: Manual merge**
```bash
# Compare and merge specific files
diff ~/my-project/CLAUDE.md /path/to/spec-kit/core/CLAUDE.md
# Merge changes manually
```

**Option 3: Git submodule (advanced)**
```bash
# Add spec-kit as submodule
git submodule add <spec-kit-repo-url> .spec-kit
# Update when needed
git submodule update --remote
```

### Want to use spec-kit with a team

**Guidance**:

**Approach 1: Commit installed files**
```bash
# After installation
git add CLAUDE.md .claude/ specs/
git commit -m "Add spec-kit"
```
**Pros**: Everyone gets the same setup
**Cons**: Updates require re-installation

**Approach 2: Installation script**
```bash
# Create setup.sh in your project
#!/bin/bash
/path/to/spec-kit/install.sh .
```
**Pros**: Easy to update
**Cons**: Requires spec-kit to be accessible

**Approach 3: Fork spec-kit**
- Customize for your organization
- Team uses your fork
- Contribute improvements back

## Performance Issues

### Installation is slow

**Symptom**: `install.sh` takes a long time

**This is normal if**:
- Installing multiple plugins
- Large number of template files

**If unusually slow**:
1. Check disk space: `df -h`
2. Check for antivirus scanning (Windows)
3. Use SSD if available

### Claude seems slow after installation

**This is unlikely to be spec-kit**, but check:
1. CLAUDE.md file size (should be <10KB)
2. Number of plugin SKILL.md files (more files = more for Claude to load)
3. Remove unused plugins: Delete from `.claude/skills/`

## Still Having Issues?

### Before Opening an Issue

1. **Check you're using latest spec-kit version**
   ```bash
   cd /path/to/spec-kit
   git pull
   ```

2. **Search existing issues**: [GitHub Issues]

3. **Try in a fresh project**:
   ```bash
   mkdir /tmp/test-spec-kit
   cd /tmp/test-spec-kit
   /path/to/spec-kit/install.sh .
   ```

### Opening a New Issue

Include:
- **Spec-kit version**: (git commit hash or release version)
- **Operating system**: macOS, Linux, Windows
- **Claude Code version**: (if relevant)
- **Full error message**: Copy exact error text
- **Steps to reproduce**:
  1. Step one
  2. Step two
  3. Expected vs actual behavior

**Template**:
```markdown
## Issue Description
Brief description of the problem

## Environment
- Spec-kit version: [commit hash or version]
- OS: [macOS 14.0 / Ubuntu 22.04 / Windows 11]
- Claude Code version: [if applicable]

## Steps to Reproduce
1. First step
2. Second step
3. What happened vs what you expected

## Error Output
```
Paste full error message here
```

## Additional Context
Any other relevant information
```

## Common Patterns

### "It worked before, now it doesn't"

**Debugging steps**:
1. What changed? (updated spec-kit? modified files? new plugins?)
2. Check git diff: `git diff CLAUDE.md`
3. Try reverting to previous version
4. Re-install fresh: Back up customizations, re-run installer

### "Works on my machine, not teammate's"

**Check for differences**:
1. Same spec-kit version?
2. Same Claude Code version?
3. Same operating system?
4. Compare file structures: `ls -laR .claude/`
5. Compare CLAUDE.md: `diff CLAUDE.md teammate-CLAUDE.md`

---

**Most issues are installation-related**. If stuck, try a fresh installation in a test directory to isolate the problem.

For more help:
- [README.md](../README.md) - Full documentation
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Development setup
- [PLUGIN_DEVELOPMENT.md](PLUGIN_DEVELOPMENT.md) - Creating custom plugins
