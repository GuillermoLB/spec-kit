# Research Documents

This directory contains research, investigations, and background analysis that informed the specification-driven development approach and plugin architecture. These documents represent deep dives into tools, frameworks, patterns, and best practices.

**Research is not part of specs, but specs reference research for context and rationale.**

## Quick Navigation

| Topic | Purpose | Related Specs |
|-------|---------|---------------|
| [Living Documentation](living-documentation/README.md) | Documentation automation tools and strategies | `specs/features/plugins/living-docs/` |
| [Plugin Architecture](plugin-architecture/README.md) | How Claude Code plugins work and best patterns | `specs/features/plugins/*/plugin-definition.md` |
| [Testing Strategies](testing-strategies/README.md) | Testing frameworks, patterns, and best practices | `specs/features/plugins/testing/` |
| [CI/CD Platforms](ci-cd-platforms/README.md) | CI/CD platforms, deployment strategies, optimization | `specs/features/plugins/ci-cd/` |
| [Code Quality](code-quality/README.md) | Code metrics, tools, quality assessment approaches | `specs/features/plugins/code-quality/` |
| [Tools & Libraries](tools-and-libraries/README.md) | Ecosystem analysis for Python, JavaScript, Go | All specs |

## How to Use This Research

### Finding Background Information
1. Pick a topic area (e.g., "Living Documentation")
2. Read the README in that directory for overview
3. Browse individual research documents for deep dives

### Understanding Spec Decisions
Each spec links to related research:
```markdown
## Background Research

This was informed by:
- See [research/living-documentation/mkdocs-ecosystem.md](...)
- See [research/plugin-architecture/plugin-distribution-approaches.md](...)
```

### Adding New Research
1. Choose or create appropriate topic directory
2. Use the template: `research/_templates/research-document.md`
3. Update the topic's README.md with reference
4. Update RESEARCH_SUMMARY.md with key findings

### Comparing Alternatives
Each research document compares different options:
- What options were evaluated?
- What are the pros and cons?
- What was recommended and why?

## Research Standards

Research documents should:
- ✅ Answer a specific question or investigate a specific topic
- ✅ Compare alternatives and options
- ✅ Include pros, cons, and effort estimates
- ✅ Make clear recommendations
- ✅ Link to authoritative sources
- ✅ Be dated and marked with status
- ✅ Reference related specs

## Organization by Domain

### Living Documentation Research ✅ (4 documents)
Focus: Tools and strategies for keeping documentation synchronized with code
- ✅ Living Documentation guide (comprehensive theory and practice)
- ✅ MkDocs ecosystem analysis
- ✅ Griffe vs AST comparison
- ✅ Documentation automation approaches
- ⏳ Sphinx vs alternative tools (planned)

### Plugin Architecture Research ✅ (1 document, 3+ planned)
Focus: How Claude Code plugins work and best practices for plugin design
- ✅ Plugin concepts guide (comprehensive explanations)
- ⏳ Plugin system capabilities and limitations (planned)
- ⏳ Skills vs Commands design patterns (planned)
- ⏳ Agent architecture and use cases (planned)
- ⏳ Plugin distribution and marketplace (planned)

### Testing Strategies Research
Focus: Testing frameworks, patterns, and best practices across languages
- TDD workflows and Red-Green-Refactor
- Coverage analysis and goals
- Mocking and fixture patterns
- Framework comparison (pytest, jest, testify, etc.)

### CI/CD Platforms Research
Focus: Continuous integration and deployment platforms and strategies
- GitHub Actions capabilities and optimization
- GitLab CI for enterprise
- Jenkins vs modern alternatives
- Deployment strategies (blue-green, canary, rolling)
- Secret management and security

### Code Quality Research
Focus: Code metrics, tools, and approaches for quality assessment
- Complexity metrics (cyclomatic, cognitive)
- Security scanning tools and patterns
- Code quality standards and benchmarks
- Refactoring strategies

### Tools & Libraries Research
Focus: Deep analysis of ecosystems and available tools
- Python ecosystem (testing, linting, documentation, security)
- JavaScript/TypeScript ecosystem
- Go ecosystem
- Cross-language tool comparisons

## Key Research Findings

See [RESEARCH_SUMMARY.md](RESEARCH_SUMMARY.md) for quick reference of major findings and recommendations made based on this research.

## Status Legend

- **In Progress** - Currently being investigated
- **Complete** - Finished investigation, ready to reference
- **Superseded** - Replaced by newer research
- **Draft** - Initial findings, needs review

## Linking Between Documents

Research documents can reference each other:
```markdown
See also:
- [MkDocs Ecosystem](./mkdocs-ecosystem.md)
- [Griffe vs AST Analysis](./griffe-ast-analysis.md)
```

Specs reference research for context:
```markdown
**Background Research**: See [research/living-documentation/mkdocs-ecosystem.md](...)
```

## Contributing to Research

1. Identify a gap or question
2. Create investigation document using template
3. Research thoroughly with sources
4. Document findings clearly
5. Update relevant README.md files
6. Add key findings to RESEARCH_SUMMARY.md
7. Link from related specs

## File Naming Convention

- `descriptive-name.md` - Use hyphens for readability
- `[tool]-[comparison-type].md` - For comparison documents
- `[topic]-[aspect].md` - For topic-focused documents

Examples:
- `mkdocs-ecosystem.md`
- `sphinx-vs-mkdocs-comparison.md`
- `griffe-ast-analysis.md`
- `tdd-workflows.md`
- `plugin-distribution-approaches.md`

---

**Last Updated**: 2026-01-25
**Maintainer**: DevTools Team
