# Scripts Specification: Living Documentation Automation

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: High

## Purpose

Define automation scripts that generate and maintain living documentation, ensuring docs stay synchronized with code.

## Scripts Overview

### 1. init_mkdocs.py
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
python scripts/docs/init_mkdocs.py [--project-name] [--theme] [--versioning] [--ci-provider]
```

### 2. gen_api_reference.py
**Purpose**: Generate API reference documentation from code

**Features**:
- Uses Griffe for fast extraction
- Supports multiple docstring styles (Google, NumPy, Sphinx)
- Generates markdown pages for all modules
- Creates automatic navigation
- Handles private/public API separation
- Includes inheritance diagrams
- Cross-references to external libraries

**Usage**:
```bash
python scripts/docs/gen_api_reference.py --src-dir src/ --docs-dir docs/api/
```

### 3. extract_architecture.py
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

### 4. generate_diagrams.py
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

### 5. validate_docs.py
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
python scripts/docs/validate_docs.py [--strict] [--check-external-links]
```

### 6. check_freshness.py
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
python scripts/docs/check_freshness.py [--threshold-days] [--report-format]
```

### 7. complexity_metrics.py
**Purpose**: Analyze code complexity and document findings

**Features**:
- Calculate cyclomatic complexity
- Measure code duplication
- Identify complex functions
- Generate complexity documentation
- Suggest refactoring opportunities

**Usage**:
```bash
python scripts/docs/complexity_metrics.py --src-dir src/
```

## Integration Points

### Pre-commit Hooks
- Validate documentation changes
- Check docstring coverage
- Run quick link checks
- Ensure examples are valid

### GitHub Actions
- Build documentation in strict mode
- Run all validation tests
- Check for broken links
- Validate code examples
- Deploy to GitHub Pages on main branch

### Local Development
- Watch mode for automatic regeneration
- Live preview with instant reload
- Auto-update on code changes
- Mark draft pages appropriately

## Custom MkDocs Plugin: spec-validator

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

## Dependencies

- **Blocked by**: plugin-living-docs (plugin definition)
- **Related**: skill-docs-guidance, command-init-docs

---

**Note**: Each script includes comprehensive error handling, progress reporting, and can be run independently or as part of a documentation pipeline.
