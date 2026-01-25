# Feature: Living Documentation Skill

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: High

## Purpose

Create a sophisticated skill that automates the generation and maintenance of living documentation that never becomes outdated. This skill combines MkDocs, Griffe, AST analysis, and automation tools to create a comprehensive documentation system that:

- Auto-generates API documentation from code
- Extracts and visualizes architecture from codebase
- Keeps documentation synchronized with code changes
- Validates documentation accuracy through testing
- Generates diagrams and dependency graphs
- Integrates with CI/CD for continuous documentation updates

## Background

Based on comprehensive research (see [research/living-documentation/](../../research/living-documentation/) and [research/griffe-ast-documentation-research.md](../../research/griffe-ast-documentation-research.md)), the modern documentation stack includes:

- **MkDocs** with Material theme for documentation sites
- **Griffe** for fast API signature extraction (10x faster than Sphinx)
- **AST analysis** for code introspection without runtime overhead
- **mkdocstrings** for automatic API reference generation
- **Automation tools** (pre-commit hooks, GitHub Actions, watch modes)

## Requirements

### Core Functionality

- [ ] Create `/living-docs` skill that guides documentation setup
- [ ] Provide MkDocs project initialization scripts
- [ ] Auto-configure essential plugins (mkdocstrings, gen-files, literate-nav, material)
- [ ] Generate API reference from codebase using Griffe
- [ ] Extract architecture documentation from code structure
- [ ] Create dependency graphs and visualizations
- [ ] Set up automation workflows (pre-commit, GitHub Actions)
- [ ] Implement documentation testing (doctest, link checking, code validation)
- [ ] Generate complexity metrics and include in documentation
- [ ] Support versioning with mike

### Automation Scripts

- [ ] `scripts/docs/init_mkdocs.py` - Initialize MkDocs project with best practices
- [ ] `scripts/docs/gen_api_reference.py` - Generate API reference pages
- [ ] `scripts/docs/extract_architecture.py` - Extract architecture from code
- [ ] `scripts/docs/generate_diagrams.py` - Create dependency and architecture diagrams
- [ ] `scripts/docs/validate_docs.py` - Validate documentation accuracy
- [ ] `scripts/docs/check_freshness.py` - Detect outdated documentation
- [ ] `scripts/docs/complexity_metrics.py` - Generate code complexity reports

### Integration

- [ ] Pre-commit hooks for documentation validation
- [ ] GitHub Actions workflow for automatic doc building
- [ ] Watch mode for local development
- [ ] Spec-driven documentation validation
- [ ] Integration with existing spec-kit architecture

## User Stories

**As a** developer starting a new Python project
**I want** to initialize comprehensive living documentation with one command
**So that** my documentation is set up with industry best practices from day one

**As a** project maintainer
**I want** API documentation to automatically update when code changes
**So that** I never have outdated API references

**As a** software architect
**I want** architecture documentation extracted from the codebase
**So that** architectural diagrams stay synchronized with implementation

**As a** documentation consumer
**I want** to see code complexity metrics and dependency graphs
**So that** I can understand the system structure and quality

**As a** CI/CD engineer
**I want** documentation to build and validate automatically
**So that** broken docs never reach production

## Acceptance Criteria

### AC1: Skill Activation
**Given** a user wants to set up living documentation
**When** they invoke `/living-docs`
**Then** Claude guides them through the setup process with interactive questions

### AC2: MkDocs Initialization
**Given** a Python project without documentation
**When** the initialization script runs
**Then** it creates:
- `docs/` directory with proper structure
- `mkdocs.yml` with Material theme and essential plugins
- `docs/index.md` with project overview
- `.github/workflows/docs.yml` for CI/CD
- Pre-commit hooks for validation

### AC3: API Reference Generation
**Given** a Python codebase with docstrings
**When** the API reference generation script runs
**Then** it:
- Uses Griffe to extract API signatures
- Generates markdown pages for all modules
- Creates navigation structure automatically
- Includes type hints and cross-references
- Supports Google, NumPy, and Sphinx docstring styles

### AC4: Architecture Extraction
**Given** a Python project with multiple modules
**When** the architecture extraction script runs
**Then** it:
- Analyzes import structure to create dependency graph
- Generates module relationship diagrams
- Extracts design patterns from code
- Creates C4 model diagrams (if configured)
- Documents database schema (if using SQLAlchemy/similar)

### AC5: Documentation Testing
**Given** documentation with code examples
**When** the validation script runs
**Then** it:
- Runs doctest on all examples
- Validates all internal links
- Checks external links (configurable)
- Ensures code snippets are syntactically valid
- Verifies documentation coverage meets threshold

### AC6: Continuous Integration
**Given** a pull request with code changes
**When** CI runs
**Then** it:
- Builds documentation in strict mode
- Runs all documentation tests
- Checks for broken links
- Validates code examples
- Deploys to GitHub Pages (on main branch)

### AC7: Local Development
**Given** a developer working on code
**When** they run `mkdocs serve`
**Then** it:
- Watches both `src/` and `docs/` for changes
- Auto-regenerates API reference on code changes
- Shows live preview with instant reload
- Marks draft pages appropriately

### AC8: Versioning Support
**Given** a project with multiple releases
**When** a new version is released
**Then** the documentation:
- Uses mike to create versioned docs
- Shows version selector in UI
- Maintains docs for all supported versions
- Links to appropriate version from package

## Technical Design

### Architecture

```
living-docs/
├── skill.md                          # Skill definition and guidance
├── templates/
│   ├── mkdocs.yml.jinja             # MkDocs configuration template
│   ├── docs/
│   │   ├── index.md.jinja           # Homepage template
│   │   ├── architecture.md.jinja    # Architecture doc template
│   │   └── contributing.md.jinja    # Contributing guide template
│   ├── workflows/
│   │   └── docs.yml.jinja           # GitHub Actions workflow
│   └── .pre-commit-config.yaml      # Pre-commit hooks
├── scripts/
│   ├── init_mkdocs.py               # Project initialization
│   ├── gen_api_reference.py         # API reference generation
│   ├── extract_architecture.py      # Architecture extraction
│   ├── generate_diagrams.py         # Diagram generation
│   ├── validate_docs.py             # Documentation validation
│   ├── check_freshness.py           # Freshness detection
│   └── complexity_metrics.py        # Complexity analysis
└── plugins/
    └── mkdocs_spec_validator/       # Custom MkDocs plugin
        ├── __init__.py
        └── plugin.py                # Validates docs against specs
```

### Key Technologies

1. **MkDocs Stack**
   - mkdocs (core)
   - mkdocs-material (theme)
   - mkdocstrings[python] (API docs)
   - mkdocs-gen-files (dynamic page generation)
   - mkdocs-literate-nav (automatic navigation)
   - mkdocs-section-index (clickable sections)
   - mike (versioning)

2. **Code Analysis**
   - griffe (API extraction)
   - ast (syntax tree analysis)
   - inspect (runtime introspection)
   - radon (complexity metrics)
   - pydeps (dependency graphs)

3. **Diagram Generation**
   - diagrams (Python diagrams)
   - pyvis (interactive graphs)
   - mermaid (embedded diagrams)
   - graphviz (dependency visualization)

4. **Testing & Validation**
   - pytest (test framework)
   - doctest (example testing)
   - mktestdocs (markdown code testing)
   - linkchecker (link validation)
   - interrogate (docstring coverage)

5. **Automation**
   - pre-commit (git hooks)
   - watchdog (file watching)
   - GitHub Actions (CI/CD)

### Script Specifications

#### 1. `init_mkdocs.py`

**Purpose**: Initialize MkDocs project with best practices

**Features**:
- Interactive prompts for project configuration
- Detects existing project structure
- Installs required dependencies
- Creates directory structure
- Generates configuration files
- Sets up CI/CD workflows
- Configures pre-commit hooks

**Usage**:
```bash
python scripts/docs/init_mkdocs.py
```

**Options**:
- `--project-name`: Project name
- `--theme`: Theme choice (material, readthedocs, mkdocs)
- `--versioning`: Enable mike versioning
- `--ci-provider`: CI provider (github, gitlab, none)
- `--plugins`: Additional plugins to install

#### 2. `gen_api_reference.py`

**Purpose**: Generate API reference documentation from code

**Features**:
- Uses Griffe for fast extraction
- Supports multiple docstring styles
- Generates markdown pages for all modules
- Creates automatic navigation
- Handles private/public API separation
- Includes inheritance diagrams
- Cross-references to external libraries

**Usage**:
```bash
python scripts/docs/gen_api_reference.py --src-dir src/ --docs-dir docs/api/
```

**Options**:
- `--src-dir`: Source code directory
- `--docs-dir`: Documentation output directory
- `--docstring-style`: google, numpy, sphinx
- `--exclude-private`: Exclude private members
- `--full-import-path`: Use full import paths

#### 3. `extract_architecture.py`

**Purpose**: Extract architecture documentation from codebase

**Features**:
- Analyzes module structure
- Creates dependency graphs
- Detects design patterns
- Generates architecture markdown
- Extracts database schema (if applicable)
- Identifies architectural layers
- Creates C4 diagrams (optional)

**Usage**:
```bash
python scripts/docs/extract_architecture.py --src-dir src/ --output docs/architecture.md
```

**Options**:
- `--src-dir`: Source code directory
- `--output`: Output markdown file
- `--diagram-format`: png, svg, mermaid
- `--c4-model`: Enable C4 model generation
- `--db-schema`: Include database schema

#### 4. `generate_diagrams.py`

**Purpose**: Generate visual diagrams for documentation

**Features**:
- Module dependency graphs
- Class inheritance diagrams
- Package structure visualization
- Call graphs for key functions
- Database ER diagrams
- Architecture diagrams
- Multiple output formats (PNG, SVG, Mermaid)

**Usage**:
```bash
python scripts/docs/generate_diagrams.py --type dependency --output docs/images/
```

**Options**:
- `--type`: dependency, inheritance, architecture, database
- `--output`: Output directory
- `--format`: png, svg, mermaid
- `--interactive`: Generate interactive HTML diagrams

#### 5. `validate_docs.py`

**Purpose**: Validate documentation accuracy and completeness

**Features**:
- Run doctests on code examples
- Validate internal links
- Check external links (optional)
- Verify code snippets syntax
- Check docstring coverage
- Ensure spec-to-doc alignment
- Generate validation report

**Usage**:
```bash
python scripts/docs/validate_docs.py --strict
```

**Options**:
- `--strict`: Fail on any error
- `--check-external-links`: Validate external URLs
- `--min-coverage`: Minimum docstring coverage (%)
- `--skip-examples`: Skip example validation

#### 6. `check_freshness.py`

**Purpose**: Detect outdated documentation

**Features**:
- Compare code modification dates with docs
- Detect API changes without doc updates
- Check for TODO/FIXME in docs
- Verify version numbers match
- Identify orphaned documentation
- Generate freshness report with recommendations

**Usage**:
```bash
python scripts/docs/check_freshness.py --report-format markdown
```

**Options**:
- `--threshold-days`: Days before considering stale
- `--report-format`: markdown, json, html
- `--auto-update`: Automatically update timestamps
- `--ignore-patterns`: Patterns to ignore

#### 7. `complexity_metrics.py`

**Purpose**: Generate code complexity metrics for documentation

**Features**:
- Calculate McCabe complexity
- Compute maintainability index
- Generate complexity heatmaps
- Identify complex modules
- Create complexity badges
- Integrate metrics into docs

**Usage**:
```bash
python scripts/docs/complexity_metrics.py --src-dir src/ --output docs/metrics/
```

**Options**:
- `--src-dir`: Source code directory
- `--output`: Output directory
- `--format`: json, markdown, html
- `--threshold`: Complexity threshold for warnings
- `--badge`: Generate complexity badge

### Custom MkDocs Plugin: spec-validator

**Purpose**: Validate that documentation stays synchronized with specifications

**Features**:
- Reads specs from `specs/` directory
- Validates implemented features have documentation
- Checks acceptance criteria coverage
- Warns about undocumented features
- Links specs to relevant doc pages

**Configuration**:
```yaml
plugins:
  - spec-validator:
      specs_dir: specs/
      strict: true
      coverage_threshold: 90
```

### Workflow Integration

#### Pre-commit Hooks
```yaml
repos:
  - repo: local
    hooks:
      - id: validate-docs
        name: Validate documentation
        entry: python scripts/docs/validate_docs.py
        language: system
        pass_filenames: false

      - id: check-docstring-coverage
        name: Check docstring coverage
        entry: interrogate --fail-under 80 src/
        language: system
        pass_filenames: false
```

#### GitHub Actions
```yaml
name: Documentation

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  build-and-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e ".[docs]"

      - name: Validate documentation
        run: |
          python scripts/docs/validate_docs.py --strict

      - name: Build documentation
        run: |
          mkdocs build --strict

      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        run: |
          mkdocs gh-deploy --force
```

## Skill Definition (`skill.md`)

The skill should guide users through:

1. **Initial Assessment**
   - Check if project has existing documentation
   - Identify documentation needs
   - Assess project complexity

2. **Setup Guidance**
   - Run initialization script
   - Explain configuration options
   - Help customize for project needs

3. **Content Creation**
   - Guide writing overview documentation
   - Help structure documentation
   - Suggest what to document manually vs auto-generate

4. **Automation Setup**
   - Configure CI/CD workflows
   - Set up pre-commit hooks
   - Enable watch mode for development

5. **Maintenance**
   - Run freshness checks
   - Update architecture docs
   - Regenerate API reference

6. **Best Practices**
   - Write effective docstrings
   - Structure documentation properly
   - Balance manual vs automatic docs
   - Keep specs and docs synchronized

## Dependencies

### Python Packages
```toml
[project.optional-dependencies]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.5.0",
    "mkdocstrings[python]>=0.24.0",
    "mkdocs-gen-files>=0.5.0",
    "mkdocs-literate-nav>=0.6.0",
    "mkdocs-section-index>=0.3.0",
    "mike>=2.0.0",
    "griffe>=0.40.0",
    "radon>=6.0.0",
    "pydeps>=1.12.0",
    "diagrams>=0.23.0",
    "pyvis>=0.3.0",
    "interrogate>=1.5.0",
    "linkchecker>=10.0.0",
    "mktestdocs>=0.2.0",
]
```

### External Tools
- Git (for versioning and hooks)
- Graphviz (for dependency graphs)

## Success Metrics

- [ ] Documentation coverage > 90%
- [ ] All code examples pass validation
- [ ] Zero broken links in documentation
- [ ] Architecture diagrams auto-update on code changes
- [ ] CI/CD documentation builds complete in < 3 minutes
- [ ] Documentation freshness score > 95%
- [ ] Positive user feedback on documentation quality

## Future Enhancements

- [ ] Support for multi-language projects (TypeScript, Go, Rust)
- [ ] AI-powered documentation suggestions
- [ ] Integration with Swagger/OpenAPI for REST APIs
- [ ] GraphQL schema documentation
- [ ] Automated screenshot generation for UI documentation
- [ ] Documentation search analytics
- [ ] Documentation quality scoring
- [ ] Automatic changelog generation from commits
- [ ] Integration with Notion/Confluence for team docs

## References

- [Research: MkDocs Ecosystem](../../research/living-documentation/MKDOCS_ECOSYSTEM.md)
- [Research: Griffe and AST Documentation](../../research/griffe-ast-documentation-research.md)
- [Research: Living Documentation Automation](../../research/living-documentation-automation.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [MkDocs Documentation](https://www.mkdocs.org/)
- [Griffe Documentation](https://mkdocstrings.github.io/griffe/)

## Notes

This specification is based on extensive research of modern documentation practices used by top open-source projects like FastAPI, Pydantic, and MkDocs itself. The approach prioritizes:

1. **Automation First**: Minimize manual documentation maintenance
2. **Living Documentation**: Docs that evolve with code
3. **Validation**: Ensure docs are accurate through testing
4. **Developer Experience**: Make it easy to maintain good docs
5. **Integration**: Work seamlessly with existing workflows

The skill should be opinionated about best practices while remaining flexible for different project needs.
