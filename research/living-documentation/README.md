# Living Documentation Research

**Purpose**: Research findings on documentation automation tools and strategies for keeping documentation synchronized with code.

**Informs**: `specs/features/plugins/living-docs/`

## Research Area Overview

Living documentation is documentation that automatically updates when code changes. This research explores:
- Documentation generation tools (MkDocs, Sphinx, etc.)
- API documentation extraction (Griffe, AST analysis, etc.)
- Automation strategies (pre-commit hooks, CI/CD integration)
- Architecture documentation generation
- Documentation validation and testing

## Key Research Questions

- Which documentation tool best supports automation?
- How can we extract API documentation without manual maintenance?
- What's the fastest way to generate documentation from code?
- How do we keep architecture documentation in sync with code?
- What validation can catch outdated documentation?

## Documents in This Category

### Completed Research ✅

- `living-documentation-guide.md` - Comprehensive theory and practice guide for living documentation
- `mkdocs-ecosystem.md` - Analysis of MkDocs and its ecosystem (Material theme, plugins, etc.)
- `griffe-ast-analysis.md` - Detailed research on Griffe and AST-based documentation extraction
- `automation-strategies.md` - Automation workflows, git hooks, CI/CD integration strategies

### Planned Research (To Be Created)

#### Tool Analysis
- `sphinx-alternatives.md` - Why Sphinx and alternatives (Docusaurus, Hugo, etc.)
- `api-doc-tools-comparison.md` - Comparison of API documentation tools
- `diagram-tools-comparison.md` - Mermaid vs Graphviz vs other diagram tools

#### Strategy Research
- `documentation-testing.md` - How to validate documentation accuracy
- `architecture-extraction.md` - Extracting and documenting system architecture

#### Tool Comparisons
- `mkdocs-vs-sphinx.md` - Detailed feature and performance comparison

## Key Recommendations

Based on completed research:

| Topic | Recommendation | Rationale | Source |
|-------|-----------------|-----------|--------|
| Documentation Tool | MkDocs | Simpler config, Material theme, plugin ecosystem | [mkdocs-ecosystem.md](mkdocs-ecosystem.md) |
| API Extraction | Griffe | 10x faster than Sphinx, less configuration | [griffe-ast-analysis.md](griffe-ast-analysis.md) |
| Automation | Pre-commit + GitHub Actions | Catches issues early, CI/CD integration | [automation-strategies.md](automation-strategies.md) |
| Diagrams | Mermaid | Text-based, version control friendly | [living-documentation-guide.md](living-documentation-guide.md) |

## Research Status

| Document | Status | Key Finding |
|----------|--------|-------------|
| living-documentation-guide.md | ✅ Complete | Living docs require systematic automation to prevent drift |
| mkdocs-ecosystem.md | ✅ Complete | MkDocs provides best balance of simplicity and power |
| griffe-ast-analysis.md | ✅ Complete | Griffe is 10x faster than Sphinx for API extraction |
| automation-strategies.md | ✅ Complete | Pre-commit hooks + CI/CD integration are most effective |
| sphinx-alternatives.md | ⏳ Planned | — |
| documentation-testing.md | ⏳ Planned | — |
| architecture-extraction.md | ⏳ Planned | — |

(Fill in as research documents are created)

## Related Specs

- [Plugin: Living Documentation](../../specs/features/plugins/living-docs/plugin-definition.md)
- [Skill: Living Documentation Guidance](../../specs/features/plugins/living-docs/skill-docs-guidance.md)
- [Command: init-docs](../../specs/features/plugins/living-docs/command-init-docs.md)
- [Scripts Specification](../../specs/features/plugins/living-docs/scripts-specification.md)

## Research Priorities

1. **High Priority**: MkDocs vs Sphinx comparison (informs tool choice)
2. **High Priority**: Griffe vs AST analysis (informs API extraction)
3. **Medium Priority**: Automation strategies (informs CI/CD integration)
4. **Medium Priority**: Architecture extraction approaches
5. **Low Priority**: Diagram tool comparisons

## Tools & Technologies to Research

- **Documentation Generators**: MkDocs, Sphinx, Docusaurus, Hugo, Asciidoctor
- **API Documentation**: Griffe, Sphinx autodoc, pdoc, typedoc, JSDoc
- **AST Analysis**: Python AST module, JavaScript AST tools, Go AST
- **Diagram Tools**: Mermaid, Graphviz, PlantUML, Draw.io
- **Validation**: mktestdocs, linkchecker, doctest, pytest
- **Automation**: pre-commit, GitHub Actions, watchdog
- **Versioning**: mike, ghpages

## Contributing to This Research

1. Choose a research question from above
2. Create a new document using `research/_templates/research-document.md`
3. Investigate thoroughly with sources
4. Document findings and recommendations
5. Update this README with status and findings
6. Link from related spec

---

**Last Updated**: 2026-01-25
**Maintainer**: DevTools Team
