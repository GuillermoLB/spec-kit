# Feature: Modern Professional CLI Interface

**Status**: Draft
**Owner**: spec-kit development team
**Last Updated**: 2026-01-18
**Priority**: High

## Purpose

Replace the current bash script installation workflow with a modern, professional Python-based CLI that provides:
- Professional developer experience comparable to tools like Poetry, AWS CLI, or GitHub CLI
- Intuitive command structure (`spec-kit init`, `spec-kit new`, etc.)
- Better discoverability of features
- Easier installation and distribution (via pip/pipx)
- Improved error messages and help documentation
- Reduced friction for first-time users

**Current Pain Points:**
- `./install.sh` feels unprofessional compared to modern CLIs
- No global installation option
- Manual template copying required
- No validation/verification commands
- Plugin management is manual
- Inconsistent naming conventions

## Requirements

- [ ] Create Python CLI package with `spec-kit` command
- [ ] Support both global installation (pipx) and local usage
- [ ] Maintain zero-dependency philosophy (Python stdlib only, or minimal deps)
- [ ] Preserve existing bash script functionality internally
- [ ] Add intuitive command structure with subcommands
- [ ] Include comprehensive help text and examples
- [ ] Support both interactive and non-interactive modes
- [ ] Provide colored, formatted output for better UX
- [ ] Add shell completion support (bash, zsh, fish)
- [ ] Maintain backward compatibility during transition

## User Stories

### Story 1: First-time Installation

**As a** developer discovering spec-kit
**I want** to install it with a single professional command
**So that** I can quickly try it without feeling it's a "hacky" tool

### Story 2: Creating Specifications

**As a** developer using spec-kit
**I want** to run `spec-kit new feature user-auth` to scaffold a spec
**So that** I don't have to manually copy and rename template files

### Story 3: Plugin Management

**As a** developer needing API specifications
**I want** to run `spec-kit plugin add api` and see what plugins are available
**So that** I can easily extend functionality without reading documentation

### Story 4: Verification

**As a** developer who just set up spec-kit
**I want** to run `spec-kit verify` to confirm everything works
**So that** I have confidence my setup is correct before starting work

## Acceptance Criteria

1. **Given** I have Python 3.8+ installed
   **When** I run `pipx install spec-kit`
   **Then** the `spec-kit` command is available globally

2. **Given** I'm in a project directory
   **When** I run `spec-kit init`
   **Then** all spec-kit files are installed with interactive plugin selection

3. **Given** spec-kit is installed in my project
   **When** I run `spec-kit new feature user-authentication`
   **Then** a new spec file is created at `specs/features/user-authentication.md` from the template

4. **Given** I want to add a plugin
   **When** I run `spec-kit plugin add api`
   **Then** the api-development plugin is installed and I see confirmation

5. **Given** I run `spec-kit plugin list`
   **When** the command executes
   **Then** I see all available plugins with descriptions and installation status

6. **Given** I run `spec-kit verify`
   **When** the command executes
   **Then** I see a report of installation status and any issues found

7. **Given** I run `spec-kit --help`
   **When** the help displays
   **Then** I see clear, well-formatted documentation for all commands

8. **Given** I run any command with `--verbose` flag
   **When** the command executes
   **Then** I see detailed logging of what's happening

## Technical Details

### Architecture

**Package Structure:**
```
spec-kit/
├── pyproject.toml              # Python package metadata
├── spec_kit/                   # Main Python package
│   ├── __init__.py
│   ├── __main__.py            # Entry point for python -m spec_kit
│   ├── cli.py                 # Main CLI with argparse/click
│   ├── commands/              # Command implementations
│   │   ├── __init__.py
│   │   ├── init.py           # spec-kit init
│   │   ├── new.py            # spec-kit new
│   │   ├── plugin.py         # spec-kit plugin
│   │   └── verify.py         # spec-kit verify
│   ├── core/                  # Core logic (wraps bash when needed)
│   │   ├── installer.py
│   │   ├── template.py
│   │   ├── plugin_manager.py
│   │   └── validator.py
│   └── utils/                 # Utilities
│       ├── colors.py          # Terminal colors/formatting
│       ├── prompts.py         # Interactive prompts
│       └── git.py             # Git operations
├── scripts/                   # Original bash scripts (deprecated or internal)
│   ├── install.sh            # Keep for manual use, mark deprecated
│   └── verify.sh             # Wrapped by Python CLI
└── README.md
```

**Technology Choices:**
- **CLI Framework**: argparse (stdlib, zero deps) OR click (professional, 1 dep)
- **Package Manager**: setuptools with pyproject.toml
- **Distribution**: PyPI for `pip install spec-kit`
- **Colored Output**: colorama (optional dep) or ANSI codes (zero dep)
- **Prompts**: built-in input() with enhancements OR simple-term-menu (lightweight)

**Recommendation**: Start with stdlib only (argparse, ANSI codes), add click/rich later if needed.

### Command Structure

```bash
spec-kit --version              # Show version
spec-kit --help                 # Show help

# Initialization
spec-kit init [PATH]            # Install to project (default: current dir)
  --plugins api,ai              # Pre-select plugins
  --no-interactive              # Skip prompts, use defaults
  --force                       # Overwrite existing installation

# Spec Creation
spec-kit new feature <name>     # Create feature spec
spec-kit new api <name>         # Create API spec
  --template custom.md          # Use custom template
  --open                        # Open in $EDITOR after creation

# Plugin Management
spec-kit plugin list            # List all available plugins
spec-kit plugin add <name>      # Add plugin(s)
spec-kit plugin remove <name>   # Remove plugin(s)
spec-kit plugin info <name>     # Show plugin details

# Validation & Info
spec-kit verify                 # Verify installation
  --fix                         # Auto-fix common issues
spec-kit status                 # Show current project status
spec-kit doctor                 # Diagnose issues

# Utilities
spec-kit templates              # List available templates
spec-kit config                 # Show/edit configuration
```

### API Design (Python)

```python
# spec_kit/cli.py
import argparse
from spec_kit.commands import init, new, plugin, verify

def main():
    parser = argparse.ArgumentParser(
        prog='spec-kit',
        description='Professional spec-driven development toolkit',
        epilog='Visit https://github.com/yourusername/spec-kit for docs'
    )
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # spec-kit init
    init_parser = subparsers.add_parser('init', help='Initialize spec-kit in project')
    init_parser.add_argument('path', nargs='?', default='.', help='Project directory')
    init_parser.add_argument('--plugins', help='Comma-separated plugin names')
    init_parser.add_argument('--no-interactive', action='store_true')

    # spec-kit new
    new_parser = subparsers.add_parser('new', help='Create new specification')
    new_subparsers = new_parser.add_subparsers(dest='spec_type')

    feature_parser = new_subparsers.add_parser('feature')
    feature_parser.add_argument('name', help='Feature name (kebab-case)')

    api_parser = new_subparsers.add_parser('api')
    api_parser.add_argument('name', help='API name (kebab-case)')

    # spec-kit plugin
    plugin_parser = subparsers.add_parser('plugin', help='Manage plugins')
    plugin_subparsers = plugin_parser.add_subparsers(dest='plugin_action')
    plugin_subparsers.add_parser('list')

    add_parser = plugin_subparsers.add_parser('add')
    add_parser.add_argument('names', nargs='+', help='Plugin name(s)')

    # spec-kit verify
    verify_parser = subparsers.add_parser('verify', help='Verify installation')
    verify_parser.add_argument('--fix', action='store_true')

    args = parser.parse_args()

    # Route to command handlers
    if args.command == 'init':
        init.execute(args)
    elif args.command == 'new':
        new.execute(args)
    elif args.command == 'plugin':
        plugin.execute(args)
    elif args.command == 'verify':
        verify.execute(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
```

```python
# spec_kit/commands/init.py
import os
import shutil
from spec_kit.utils import colors, prompts
from spec_kit.core.installer import Installer

def execute(args):
    """Initialize spec-kit in a project directory."""
    target_path = os.path.abspath(args.path)

    print(colors.bold(f"Initializing spec-kit in {target_path}"))

    installer = Installer(target_path)

    # Validate
    if not installer.validate_target():
        print(colors.error("Target directory validation failed"))
        return 1

    # Select plugins
    if args.no_interactive:
        selected_plugins = args.plugins.split(',') if args.plugins else []
    else:
        selected_plugins = prompts.select_plugins(installer.available_plugins)

    # Install
    try:
        installer.install(selected_plugins)
        print(colors.success("✓ spec-kit installed successfully!"))
        print(f"\nNext steps:")
        print(f"  1. Run: spec-kit new feature your-feature-name")
        print(f"  2. Edit the spec in specs/features/")
        print(f"  3. Start Claude Code and request implementation")
    except Exception as e:
        print(colors.error(f"Installation failed: {e}"))
        return 1

    return 0
```

### Migration Strategy

**Phase 1: Parallel Support (v2.0)**
- Add Python CLI package alongside bash scripts
- Bash scripts marked as deprecated but still work
- Documentation shows Python commands first
- `install.sh` prints message: "Install spec-kit CLI: pipx install spec-kit"

**Phase 2: Python Primary (v2.1)**
- Python CLI is recommended approach
- Bash scripts moved to `legacy/` directory
- Documentation updated to Python-first

**Phase 3: Bash Removal (v3.0)**
- Remove bash scripts entirely (breaking change)
- Python CLI is only option

### Dependencies

**Core (required):**
- Python >= 3.8 (use stdlib as much as possible)

**Optional (enhance UX):**
- `click` (7.1+): Professional CLI framework (better than argparse)
- `rich` (13.0+): Beautiful terminal formatting, progress bars
- `questionary` (2.0+): Beautiful interactive prompts

**Initial Recommendation**: Start with stdlib only, add deps later:
```toml
[project]
dependencies = []

[project.optional-dependencies]
interactive = ["click>=7.1", "rich>=13.0", "questionary>=2.0"]
```

### Database Changes

N/A - No database in spec-kit

### Security Considerations

- [ ] Authentication required: No (local CLI tool)
- [ ] Authorization: File system permissions only
- [x] Input validation: Validate all user inputs (paths, names, plugin names)
- [ ] Data encryption: No sensitive data
- [ ] Rate limiting: N/A

**Input Validation:**
- Feature/API names: alphanumeric + hyphens only (kebab-case)
- Paths: must exist and be writable
- Plugin names: must be in available plugins list
- Template names: must exist in templates directory

**Path Traversal Protection:**
```python
def validate_path(user_path, base_dir):
    abs_path = os.path.abspath(user_path)
    abs_base = os.path.abspath(base_dir)
    if not abs_path.startswith(abs_base):
        raise ValueError("Path traversal detected")
    return abs_path
```

## Edge Cases & Error Handling

1. **Edge case**: Running `spec-kit init` in directory with existing spec-kit installation
   - **Handling**: Detect existing installation, ask to confirm overwrite or abort
   - **Message**: "spec-kit already installed. Overwrite? [y/N]"

2. **Edge case**: Creating spec with name that already exists
   - **Handling**: Detect existing file, ask to confirm overwrite or use different name
   - **Message**: "Spec 'user-auth' already exists at specs/features/user-auth.md. Overwrite? [y/N]"

3. **Error**: Python version too old (< 3.8)
   - **Message**: "spec-kit requires Python 3.8+. Current version: 3.7"
   - **Recovery**: User upgrades Python or uses bash scripts

4. **Error**: Not in a git repository when running init
   - **Message**: "Warning: Not a git repository. spec-kit works best with git. Initialize? [y/N]"
   - **Recovery**: Offer to run `git init` or continue anyway

5. **Error**: Plugin name not found
   - **Message**: "Plugin 'xyz' not found. Available plugins: api-development, ai-app"
   - **Recovery**: Show available plugins, suggest closest match

6. **Error**: Permission denied writing files
   - **Message**: "Permission denied creating .claude/ directory. Check file permissions."
   - **Recovery**: User fixes permissions or uses sudo (not recommended)

7. **Edge case**: spec-kit run from spec-kit's own repo
   - **Handling**: Detect if CWD is spec-kit repo, warn about self-reference
   - **Message**: "Warning: Running inside spec-kit repo. Are you developing spec-kit itself? [y/N]"

8. **Error**: Template file missing or corrupted
   - **Message**: "Template 'feature.template.md' not found or invalid"
   - **Recovery**: Offer to re-download templates or reinstall spec-kit

## Testing Strategy

### Unit Tests

- [ ] Test command parsing (all commands and flags)
- [ ] Test path validation and normalization
- [ ] Test plugin discovery and listing
- [ ] Test template rendering
- [ ] Test name validation (kebab-case enforcement)
- [ ] Test error message formatting
- [ ] Test color output (with/without TTY)
- [ ] Test installer validation logic

### Integration Tests

- [ ] Test full `init` workflow in temp directory
- [ ] Test `new feature` creates correct file with template
- [ ] Test `new api` creates correct YAML spec
- [ ] Test `plugin add` installs plugin files
- [ ] Test `verify` detects missing files
- [ ] Test `verify --fix` repairs installation
- [ ] Test non-interactive mode with --no-interactive

### Manual Testing Checklist

- [ ] Install via `pipx install spec-kit` works
- [ ] All commands show proper help with --help
- [ ] Interactive prompts are clear and intuitive
- [ ] Error messages are helpful and actionable
- [ ] Colors work in terminal but not in pipes
- [ ] Shell completion works (if implemented)
- [ ] Works on macOS, Linux, and WSL
- [ ] Python 3.8, 3.9, 3.10, 3.11, 3.12 compatibility

### Test Files Structure

```
tests/
├── __init__.py
├── conftest.py                # pytest fixtures
├── unit/
│   ├── test_cli.py
│   ├── test_installer.py
│   ├── test_template.py
│   ├── test_plugin_manager.py
│   └── test_validator.py
├── integration/
│   ├── test_init_command.py
│   ├── test_new_command.py
│   ├── test_plugin_command.py
│   └── test_verify_command.py
└── fixtures/
    ├── sample_project/
    └── templates/
```

## Dependencies

- **Blocked by**: None (can start immediately)
- **Blocks**:
  - Documentation improvements (need to update for new commands)
  - Example projects (should use new CLI in setup instructions)
  - Plugin development (new plugin installation method)
- **Related**:
  - [testing-infrastructure.md](testing-infrastructure.md) - Provides test framework for CLI
  - [documentation-improvements.md](documentation-improvements.md) - Must update for new CLI

## Timeline (Optional)

- **Estimated effort**:
  - Phase 1 (Basic CLI): 2-3 days
  - Phase 2 (Full features): 4-5 days
  - Phase 3 (Polish + tests): 2-3 days
  - **Total**: ~8-11 days for complete implementation
- **Target completion**: TBD
- **Actual completion**: TBD

## Open Questions

- [x] Should we use argparse (stdlib) or click (dependency)?
  - **Decision**: Start with argparse, migrate to click in v2.1 if needed

- [x] Should we keep bash scripts working or deprecate immediately?
  - **Decision**: Keep as deprecated in v2.0, remove in v3.0

- [ ] Should we support configuration files (`.spec-kit.toml`)?
  - **Discussion needed**: Could store defaults like preferred plugins, template locations

- [ ] Should `spec-kit verify` auto-fix by default or require --fix flag?
  - **Recommendation**: Require --fix flag (safer, follows git/terraform pattern)

- [ ] Should we build shell completion or defer to v2.1?
  - **Recommendation**: Defer to v2.1, not critical for MVP

- [ ] Package name on PyPI: `spec-kit` or `speckit`?
  - **Recommendation**: `spec-kit` (matches GitHub repo, clearer branding)
  - **Fallback**: Register both, make one alias to other

- [ ] Should we vendor templates in Python package or reference from GitHub?
  - **Recommendation**: Vendor in package for offline use, add `--update-templates` command later

## Implementation Notes

### Phase 1: Core CLI (MVP)

**Priority**: Get basic commands working
- `spec-kit init` - replaces install.sh
- `spec-kit new feature` - creates feature spec
- `spec-kit verify` - validates installation
- Minimal styling (basic colors)
- No interactive prompts (use --plugins flag)

**Files to create:**
- `pyproject.toml`
- `spec_kit/__init__.py`
- `spec_kit/__main__.py`
- `spec_kit/cli.py`
- `spec_kit/commands/init.py`
- `spec_kit/commands/new.py`
- `spec_kit/commands/verify.py`

### Phase 2: Enhanced UX

**Add:**
- Interactive plugin selection
- Beautiful formatting (consider rich)
- `spec-kit plugin` commands
- Better error messages
- Progress indicators

### Phase 3: Polish

**Add:**
- Comprehensive tests
- Shell completion
- `spec-kit doctor` diagnostic
- `spec-kit config` for defaults
- Performance optimization

### Decisions Made

- **2026-01-18** - Use Python stdlib for initial implementation to maintain zero-dependency philosophy. Can add click/rich later as optional dependencies.
- **2026-01-18** - Keep bash scripts as deprecated during transition (v2.0-2.x), remove in v3.0
- **2026-01-18** - Use argparse initially, consider click migration in future based on user feedback

### Challenges Encountered

(To be filled during implementation)

## References

- CLI Design: [clig.dev](https://clig.dev/) - Command Line Interface Guidelines
- Python Packaging: [PyPA packaging guide](https://packaging.python.org/)
- argparse docs: https://docs.python.org/3/library/argparse.html
- click docs: https://click.palletsprojects.com/
- rich docs: https://rich.readthedocs.io/
- Related specs:
  - [testing-infrastructure.md](testing-infrastructure.md)
  - [documentation-improvements.md](documentation-improvements.md)

---

**Template Version**: 1.0
**Last Updated**: 2026-01-18
