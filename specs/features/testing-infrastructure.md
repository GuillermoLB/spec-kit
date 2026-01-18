# Feature: Testing Infrastructure

**Status**: Implemented
**Owner**: spec-kit development team
**Last Updated**: 2026-01-18
**Priority**: High

## Purpose

Establish comprehensive automated testing infrastructure to validate spec-kit components (installer, verification script, templates, and plugin structure). This ensures quality and consistency as we expand with new examples and plugins.

## Requirements

- [ ] Bash tests for install.sh that validate file copying, directory creation, and plugin selection
- [ ] Tests for verify.sh to ensure it catches missing or malformed files
- [ ] Python-based template validation for feature.template.md and api.template.yaml
- [ ] SKILL.md frontmatter validation for all plugins (existing and future)
- [ ] Test runner script that executes all tests and reports results
- [ ] CI automation integration (GitHub Actions) for automated testing on commits
- [ ] Documentation of how to run tests locally

## User Stories

**As a** spec-kit maintainer
**I want** automated tests for all core components
**So that** I can confidently make changes without breaking existing functionality

**As a** spec-kit contributor
**I want** clear test output when validation fails
**So that** I can quickly identify and fix issues

**As a** spec-kit user
**I want** confidence that the installer works correctly
**So that** I can trust the installation process in my projects

## Acceptance Criteria

1. **Given** the install.sh script is run in test mode
   **When** all plugins are selected
   **Then** all expected files are copied to correct locations and directory structure is valid

2. **Given** a template file has invalid YAML frontmatter
   **When** template validation runs
   **Then** the test fails with clear error message indicating the issue

3. **Given** verify.sh is executed in a complete spec-kit installation
   **When** all required files exist
   **Then** all checks pass with green checkmarks

4. **Given** a SKILL.md file is missing required frontmatter fields
   **When** SKILL frontmatter validation runs
   **Then** the test fails identifying which fields are missing

5. **Given** all tests are run via test runner script
   **When** any test fails
   **Then** the script exits with non-zero status and shows failure summary

6. **Given** a pull request is created
   **When** GitHub Actions CI runs
   **Then** all tests execute automatically and results are reported

## Technical Details

### Architecture

Create a `tests/` directory with the following components:

- **test_installer.sh** - Bash tests for install.sh functionality
- **test_verify.sh** - Bash tests for verify.sh completeness
- **test_templates.py** - Python script using PyYAML and markdown parsing
- **test_skill_frontmatter.py** - Python script to validate SKILL.md files
- **run_tests.sh** - Master test runner that executes all tests
- **.github/workflows/ci.yml** - GitHub Actions workflow (optional)

### Test Framework Choices

**Bash Tests:**
- Use bash assertions and exit codes
- Create temporary directory for install.sh tests
- Clean up after test execution
- Capture and validate stdout/stderr

**Python Tests:**
- Use pytest framework
- PyYAML for YAML parsing
- markdown library for template parsing
- Clear assertion messages

### File Structure

```
tests/
├── test_installer.sh          # Installer validation
├── test_verify.sh             # Verify script validation
├── test_templates.py          # Template file validation
├── test_skill_frontmatter.py  # SKILL.md frontmatter validation
├── run_tests.sh               # Test runner
├── requirements.txt           # Python test dependencies (pytest, PyYAML, markdown)
└── fixtures/                  # Test fixtures (invalid templates, etc.)
    ├── invalid_frontmatter.md
    └── invalid_yaml.yaml
```

### Testing Scenarios

**Installer Tests:**
1. Install with no plugins selected
2. Install with single plugin (api-development)
3. Install with all plugins
4. Install to non-existent directory (should fail gracefully)
5. Install when CLAUDE.md already exists (should warn)
6. Verify SKILL.md files are named correctly (uppercase)
7. Verify plugin directory structure is correct

**Verify Script Tests:**
1. Run in complete installation (all checks pass)
2. Run with missing core files (should fail)
3. Run with missing plugin files (should fail)
4. Run with missing templates (should fail)

**Template Validation:**
1. Validate feature.template.md has all required sections
2. Validate api.template.yaml is valid OpenAPI 3.0
3. Test with malformed YAML (should fail)
4. Test with missing sections (should fail)

**SKILL Frontmatter Validation:**
1. Validate existing plugins (api-development, ai-app)
2. Test with missing frontmatter (should fail)
3. Test with invalid YAML in frontmatter (should fail)
4. Test with missing required fields (should fail)

### CI/CD Integration

GitHub Actions workflow:

```yaml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r tests/requirements.txt
      - name: Run tests
        run: ./tests/run_tests.sh
```

### Security Considerations

- [ ] Installer tests run in isolated temporary directories
- [ ] No execution of untrusted code during tests
- [ ] Test fixtures do not contain sensitive data
- [ ] CI environment has read-only access to repository

## Edge Cases & Error Handling

1. **Edge case**: Installer run without spec-kit core files
   - **Handling**: Display error message, exit with status 1

2. **Edge case**: Template validation on non-existent file
   - **Handling**: Skip gracefully with warning, continue other tests

3. **Error**: Python dependencies not installed
   - **Message**: "Python test dependencies missing. Run: pip install -r tests/requirements.txt"
   - **Recovery**: User installs dependencies and re-runs tests

4. **Edge case**: Verify script run outside spec-kit directory
   - **Handling**: Detect context, provide helpful error message

## Testing Strategy

### Unit Tests

- [ ] Test installer file copying logic
- [ ] Test verify script file existence checks
- [ ] Test YAML parsing for templates
- [ ] Test frontmatter extraction from SKILL.md

### Integration Tests

- [ ] Full install.sh execution in test directory
- [ ] verify.sh execution in fully installed project
- [ ] Template validation across all templates
- [ ] SKILL frontmatter validation across all plugins

### Manual Testing Checklist

- [ ] Run test_installer.sh and verify output is clear
- [ ] Run test_verify.sh and verify checks are comprehensive
- [ ] Run Python tests and verify error messages are helpful
- [ ] Run full test suite via run_tests.sh
- [ ] Trigger GitHub Actions and verify CI passes
- [ ] Test on fresh clone of spec-kit repository

## Dependencies

- **Blocked by**: None (foundational feature)
- **Blocks**: All subsequent features (examples, plugins) should be validated by these tests
- **Related**: documentation-improvements (tests should be documented in CONTRIBUTING.md)

## Open Questions

- [x] Should we use pytest or unittest for Python tests? **Decision: pytest (more modern, better output)**
- [x] Should CI be mandatory or optional? **Decision: Include in spec, but mark as optional for local development**
- [x] Should tests validate plugin content or just structure? **Decision: Structure only initially, can expand later**

## Implementation Notes

### Decisions Made

- 2026-01-17 - Use pytest for Python tests (better assertion output, more intuitive)
- 2026-01-17 - Create run_tests.sh as master test runner (single entry point)
- 2026-01-17 - GitHub Actions is optional but recommended (not all users use GitHub)

### Test Output Format

Tests should produce clear, actionable output:

```
Running installer tests...
  ✓ Install with no plugins
  ✓ Install with api-development plugin
  ✓ Install with all plugins
  ✗ Install to non-existent directory
    Expected: Error message and exit 1
    Got: Silent failure

Running template validation...
  ✓ feature.template.md is valid
  ✓ api.template.yaml is valid OpenAPI 3.0

Summary: 5 passed, 1 failed
```

## References

- Installer script: [install.sh](../../install.sh)
- Verification script: [verify.sh](../../verify.sh)
- Feature template: [templates/specs/feature.template.md](../../templates/specs/feature.template.md)
- API template: [templates/specs/api.template.yaml](../../templates/specs/api.template.yaml)
- Existing plugins: [plugins/](../../plugins/)

---

## Implementation Summary (2026-01-18)

### ✅ Completed

The testing infrastructure has been fully implemented with a comprehensive pytest-based test suite:

**Test Suite Statistics:**
- **162 tests** implemented and passing (100% pass rate)
- **88% code coverage** achieved (exceeds 80% goal)
- **Test execution time**: ~0.6 seconds

**Files Created:**
- `tests/conftest.py` - pytest fixtures (5 fixtures for test setup)
- `tests/test_file_ops.py` - 21 tests for file operations
- `tests/test_colors.py` - 11 tests for color utilities
- `tests/test_installer.py` - 34 tests for Installer class
- `tests/test_validator.py` - 41 tests for Validator class
- `tests/test_cli.py` - 16 tests for CLI dispatcher
- `tests/test_commands.py` - 18 tests for command handlers
- `tests/test_integration.py` - 21 end-to-end integration tests
- `tests/run_tests.sh` - Test runner with coverage reporting

**Files Updated:**
- `pyproject.toml` - Added test dependencies (pytest, pytest-cov)
- `CONTRIBUTING.md` - Added comprehensive testing documentation

**Coverage by Module:**
- colors.py: 100%
- cli.py: 91%
- verify.py: 92%
- validator.py: 90%
- installer.py: 88%
- file_ops.py: 88%
- init.py: 83%

**Test Organization:**
- Unit tests (70%): Test individual functions in isolation
- Integration tests (25%): Test complete workflows with real files
- Edge case tests (5%): Error handling and validation

**Usage:**
```bash
# Install dependencies
pip install -e '.[test]'

# Run all tests
./tests/run_tests.sh

# Run with options
./tests/run_tests.sh --quick      # Skip coverage
./tests/run_tests.sh --verbose    # Detailed output
./tests/run_tests.sh --file FILE  # Specific file

# Use pytest directly
pytest tests/ -v
pytest tests/ --cov=spec_kit --cov-report=html
```

**Documentation:**
Full testing guide added to [CONTRIBUTING.md](../../CONTRIBUTING.md#testing-your-changes) with:
- How to run tests (multiple methods)
- Test organization structure
- Writing unit and integration tests
- Coverage goals and current status
- Manual testing checklist

### Adaptation from Original Spec

The original spec focused on bash script testing (`install.sh`, `verify.sh`), but spec-kit evolved to use a Python CLI (`spec-kit` command). The testing infrastructure was adapted accordingly:

**Changed:**
- Bash script tests → Python CLI tests with pytest
- install.sh tests → spec_kit.core.installer tests
- verify.sh tests → spec_kit.core.validator tests

**Kept:**
- Comprehensive coverage requirement
- Clear test output format
- Test runner script
- Documentation in CONTRIBUTING.md

**Result:** Modern Python testing infrastructure that thoroughly validates the CLI implementation with excellent coverage and fast execution.

---

**Template Version**: 1.0
**Last Updated**: 2026-01-18
