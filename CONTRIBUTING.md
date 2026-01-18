# Contributing to Spec-Kit

## Welcome

Spec-Kit is designed to grow with real-world use. We welcome contributions that make spec-driven development more practical and accessible!

## Before You Start

1. **Check existing issues and PRs** - Someone may already be working on it
2. **Open an issue to discuss major changes** - Get feedback before investing time
3. **Ensure changes align with spec-driven development philosophy** - Quality over features

## Development Setup

```bash
# Clone the repository
git clone https://github.com/your-org/spec-kit.git
cd spec-kit

# Verify all files are present
./verify.sh
```

## Spec-Kit Development Philosophy

**We practice what we preach**: Spec-kit is developed using spec-driven development.

### For Non-Trivial Changes

1. **Create a specification first** in `specs/features/`
2. Use the template: `cp templates/specs/feature.template.md specs/features/your-feature.md`
3. Get spec approval before implementing
4. Implement following the spec
5. Validate against acceptance criteria

### Exceptions

Trivial changes don't require specs:
- Typo fixes
- Formatting improvements
- Minor documentation updates
- Small bug fixes with obvious solutions

## Testing Your Changes

Once testing infrastructure exists, run:

```bash
./tests/run_tests.sh  # Run all tests
```

Currently, manual testing is required:
1. Run `./verify.sh` to ensure file structure is correct
2. Test `install.sh` in a clean project directory
3. Verify all documentation links work
4. Test any new features in a real project

## Code Style

### Bash Scripts

- **Use shellcheck** for validation
- **Include error handling**: `set -e` at script start
- **Clear error messages**: Tell users what went wrong and how to fix it
- **Colored output**: Use colors to highlight success/failure/warnings

**Example**:
```bash
#!/bin/bash
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

if [ -f "target/file" ]; then
    echo -e "${GREEN}✓${NC} File found"
else
    echo -e "${RED}✗${NC} File not found. Run install.sh first."
    exit 1
fi
```

### Python Code

- **Follow PEP 8** style guide
- **Use type hints** for function parameters and returns
- **Include docstrings** for public functions and classes
- **Use pytest** for testing

**Example**:
```python
from typing import Optional

def example_function(param: str) -> Optional[str]:
    """
    Does something useful.

    Args:
        param: Description of parameter

    Returns:
        Result or None if operation fails
    """
    if not param:
        return None
    return param.upper()
```

### Markdown Documentation

- **Use consistent formatting**: Follow existing docs structure
- **Include table of contents** for documents over 100 lines
- **Test all links**: Ensure relative links work
- **Use relative links** within repository (not absolute URLs)

## Plugin Contributions

See [docs/PLUGIN_DEVELOPMENT.md](docs/PLUGIN_DEVELOPMENT.md) for detailed guide on creating plugins.

### Plugin Quality Requirements

Before submitting a plugin:

- [ ] **Comprehensive patterns** - Not just basic examples, but production-ready guidance
- [ ] **Production-ready templates** - Include error handling, logging, best practices
- [ ] **Clear SKILL.md** with proper YAML frontmatter
- [ ] **Tested in 2-3 real projects** - Validate patterns actually work
- [ ] **Well-documented** - Clear explanations of when and how to use patterns

### Plugin YAML Frontmatter

All plugins must have valid YAML frontmatter:

```yaml
---
name: plugin-name
description: One-sentence description of plugin purpose
version: 1.0.0
authors:
  - Your Name
tags:
  - relevant
  - tags
---
```

## Pull Request Process

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Follow spec-driven approach (create spec first for non-trivial changes)
- Add or update tests if applicable
- Update documentation (README, relevant guides)
- Ensure code follows style guidelines

### 3. Verify Your Changes

```bash
# Run verification script
./verify.sh

# Test installation in a clean directory
cd /tmp/test-project
/path/to/spec-kit/install.sh .

# Verify documentation links
# (Manual check for now, automated link checker coming)
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

**Commit message format**:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions/changes
- `refactor:` for code refactoring

### 5. Submit Pull Request

**PR Description Template**:

```markdown
## Description
Brief description of what this PR does

## Specification
Link to spec file if applicable: `specs/features/your-feature.md`

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Plugin addition
- [ ] Breaking change

## Testing
Describe how you tested this:
- Manual testing steps
- Test suite results (once available)
- Projects where you validated changes

## Checklist
- [ ] Spec created (if non-trivial change)
- [ ] Tests added/updated (once testing infrastructure exists)
- [ ] Documentation updated
- [ ] verify.sh passes
- [ ] install.sh tested in clean directory
- [ ] Code follows style guidelines
```

## Review Process

1. **All PRs require review** from a maintainer
2. **Tests must pass** (once CI/CD is set up)
3. **Documentation must be updated** for user-facing changes
4. **Changes must align with project philosophy**:
   - Spec-driven development
   - Practical over theoretical
   - Quality over quantity
   - Minimal over complex

## What We Look For

### Good Contributions ✅

- Solves a real problem you encountered
- Includes clear specification (for features)
- Well-tested in real projects
- Documentation is clear and complete
- Follows existing patterns and conventions

### Needs Improvement ⚠️

- No specification for non-trivial changes
- Overly complex solutions
- Missing documentation
- Not tested in real scenarios
- Breaks existing functionality

## Getting Help

- **Questions?** Open an issue with "Question:" prefix
- **Ideas?** Open an issue with "Idea:" prefix
- **Stuck?** Add "help wanted" label to your PR

## Recognition

Contributors will be:
- Listed in project credits
- Mentioned in release notes for their contributions

## Code of Conduct

- Be respectful and constructive
- Focus on what's best for the project
- Welcome newcomers
- Give credit where due

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Spec-Kit!** 🙏

Your contributions help developers adopt spec-driven development and build better software with AI assistance.
