# Spec-Kit Project Structure: Visual Guide

**Purpose**: Quick visual reference of complete project structure
**Status**: Planning Phase
**Date**: 2026-01-25

---

## Complete Folder Tree (Visual)

```
spec-kit/ (root)
│
├─📄 CLAUDE.md                                Development constitution
├─📄 README.md                                Project overview
├─📄 PROJECT_STRUCTURE.md                     Complete structure document
├─📄 PROJECT_STRUCTURE_SUMMARY.md             Executive summary
├─📄 LIVING_DOCUMENTATION_SKILL_STRUCTURE.md  Living-docs detail
├─📄 STRUCTURE_VISUAL_GUIDE.md               This file
│
├─📁 .claude/
│  ├─📄 settings.json                         Claude Code project settings
│  └─📁 skills/ (optional)
│
├─📁 specs/                                   ✅ SPECIFICATIONS LAYER
│  └─📁 features/
│     ├─📄 living-documentation-skill.md      ⭐ MAJOR SKILL
│     ├─📄 plugin-best-practices-setup.md     🔧 FOUNDATION
│     ├─📄 plugin-best-practices-testing.md
│     ├─📄 plugin-best-practices-ci-cd.md
│     ├─📄 plugin-best-practices-code-quality.md
│     ├─📄 plugin-best-practices-documentation.md
│     ├─📄 plugin-best-practices-spec-driven-dev.md
│     └─📄 plugin-best-practices-agents.md
│
├─📁 research/                                ✅ RESEARCH LAYER
│  ├─📄 CONCEPTS.md                           Plugin system concepts
│  ├─📄 griffe-ast-documentation-research.md
│  └─📁 living-documentation/
│     ├─📄 LIVING_DOCUMENTATION.md
│     └─📄 MKDOCS_ECOSYSTEM.md
│
└─📁 best-practices-plugin/                   🚀 PLUGIN LAYER (MAIN DELIVERABLE)
   │
   ├─📁 .claude-plugin/                       Plugin metadata
   │  ├─📄 plugin.json                        Manifest
   │  └─�� marketplace.json                   Marketplace config
   │
   ├─📁 skills/                               ✨ 6 AUTO-TRIGGERED SKILLS
   │  │
   │  ├─📁 living-documentation/              ⭐⭐⭐⭐⭐ MAJOR SKILL
   │  │  ├─📄 SKILL.md                        Skill definition
   │  │  ├─📁 guides/
   │  │  │  ├─📄 mkdocs-setup.md
   │  │  │  ├─📄 api-reference.md
   │  │  │  ├─📄 architecture-docs.md
   │  │  │  ├─📄 documentation-testing.md
   │  │  │  ├─📄 versioning.md
   │  │  │  └─📄 best-practices.md
   │  │  ├─📁 templates/
   │  │  │  ├─📄 mkdocs.yml.jinja
   │  │  │  ├─📁 docs/
   │  │  │  │  ├─📄 index.md.jinja
   │  │  │  │  ├─📄 architecture.md.jinja
   │  │  │  │  └─📄 contributing.md.jinja
   │  │  │  ├─📁 workflows/
   │  │  │  │  └─📄 docs.yml.jinja
   │  │  │  └─📄 .pre-commit-config.yaml
   │  │  ├─📁 scripts/
   │  │  │  ├─🐍 init_mkdocs.py
   │  │  │  ├─🐍 gen_api_reference.py
   │  │  │  ├─🐍 extract_architecture.py
   │  │  │  ├─🐍 generate_diagrams.py
   │  │  │  ├─🐍 validate_docs.py
   │  │  │  ├─🐍 check_freshness.py
   │  │  │  └─📄 requirements-docs.txt
   │  │  ├─📁 plugins/
   │  │  │  └─📁 mkdocs_spec_validator/
   │  │  │     ├─🐍 __init__.py
   │  │  │     └─🐍 plugin.py
   │  │  └─📄 README.md
   │  │
   │  ├─📁 testing/                           ⭐⭐⭐⭐ TESTING SKILL
   │  │  ├─📄 SKILL.md
   │  │  ├─📄 testing-guide.md
   │  │  └─📁 frameworks/
   │  │     ├─📄 pytest.md
   │  │     ├─📄 jest.md
   │  │     └─📄 go-testing.md
   │  │
   │  ├─📁 ci-cd/                            ⭐⭐⭐⭐ CI/CD SKILL
   │  │  ├─📄 SKILL.md
   │  │  ├─📄 ci-cd-guide.md
   │  │  └─📁 platforms/
   │  │     ├─📄 github-actions.md
   │  │     ├─📄 gitlab-ci.md
   │  │     ├─📄 jenkins.md
   │  │     └─📄 circleci.md
   │  │
   │  ├─📁 code-quality/                     ⭐⭐⭐⭐ CODE QUALITY SKILL
   │  │  ├─📄 SKILL.md
   │  │  ├─📄 quality-guide.md
   │  │  ├─📄 analysis-tools.md
   │  │  ├─📁 metrics/
   │  │  │  ├─📄 complexity.md
   │  │  │  ├─📄 coverage.md
   │  │  │  ├─📄 security.md
   │  │  │  └─📄 dependencies.md
   │  │  └─📁 standards/
   │  │     ├─📄 code-style.md
   │  │     ├─📄 performance.md
   │  │     └─📄 maintainability.md
   │  │
   │  ├─📁 documentation/                    ⭐⭐⭐ DOCUMENTATION SKILL
   │  │  ├─📄 SKILL.md
   │  │  ├─📄 docs-guide.md
   │  │  ├─📁 components/
   │  │  │  ├─📄 readme.md
   │  │  │  ├─📄 api-docs.md
   │  │  │  ├─📄 architecture.md
   │  │  │  ├─📄 changelog.md
   │  │  │  └─📄 contributing.md
   │  │  └─📁 tools/
   │  │     ├─📄 sphinx.md
   │  │     ├─📄 jsdoc.md
   │  │     ├─📄 godoc.md
   │  │     └─📄 mkdocs.md
   │  │
   │  └─📁 spec-driven/                      ⭐⭐⭐ SPEC-DRIVEN SKILL
   │     ├─📄 SKILL.md
   │     ├─📄 spec-guide.md
   │     ├─📁 templates/
   │     │  ├─📄 feature-spec.md
   │     │  ├─📄 architecture-spec.md
   │     │  └─📄 api-spec.md
   │     └─📁 practices/
   │        ├─📄 spec-writing.md
   │        ├─📄 validation.md
   │        └─📄 integration.md
   │
   ├─📁 commands/                             💻 USER-INVOKED COMMANDS
   │  ├─📁 run-tests/
   │  │  ├─📄 COMMAND.md
   │  │  ├─🐍 implementation.py
   │  │  └─🐍 results-formatter.py
   │  ├─📁 setup-ci/
   │  │  ├─📄 COMMAND.md
   │  │  ├─🐍 config-generator.py
   │  │  └─📁 templates/
   │  │     ├─📄 github-actions.yml
   │  │     ├─📄 gitlab-ci.yml
   │  │     ├─📄 jenkinsfile
   │  │     └─📄 circleci-config.yml
   │  ├─📁 check-quality/
   │  │  ├─📄 COMMAND.md
   │  │  ├─🐍 quality-checker.py
   │  │  └─📁 reporters/
   │  │     ├─🐍 json-reporter.py
   │  │     └─🐍 html-reporter.py
   │  ├─📁 init-project/
   │  │  ├─📄 COMMAND.md
   │  │  ├─🐍 project-initializer.py
   │  │  └─📁 templates/
   │  │     ├─📄 claude-md.template
   │  │     ├─📁 specs-dir/
   │  │     │  ├─📄 architecture.md
   │  │     │  ├─📁 features/
   │  │     │  └─📁 api/
   │  │     └─📄 claude-settings.template
   │  └─📁 generate-docs/
   │     ├─📄 COMMAND.md
   │     └─🐍 documentation-generator.py
   │
   ├─📁 agents/                              🤖 ANALYSIS AGENTS
   │  ├─📁 test-reviewer/
   │  │  ├─📄 AGENT.md
   │  │  ├─🐍 test-analyzer.py
   │  │  ├─🐍 coverage-reporter.py
   │  │  └─🐍 recommendations.py
   │  └─📁 quality-checker/
   │     ├─📄 AGENT.md
   │     ├─🐍 complexity-analyzer.py
   │     ├─🐍 security-scanner.py
   │     ├─🐍 performance-analyzer.py
   │     └─🐍 dependency-analyzer.py
   │
   ├─📁 hooks/                               🔗 EVENT-BASED POLICIES
   │  ├─📄 pre-tool-use.json
   │  └─📄 post-tool-use.json
   │
   ├─📁 .github/                             GitHub Integration
   │  ├─📁 workflows/
   │  │  ├─📄 test.yml
   │  │  └─📄 release.yml
   │  └─📁 ISSUE_TEMPLATE/
   │     ├─📄 bug_report.md
   │     └─📄 feature_request.md
   │
   ├─📄 README.md                            Plugin overview
   ├─📄 LICENSE.md                           MIT License
   ├─📄 CHANGELOG.md                         Version history
   ├─📄 CONTRIBUTING.md                      Contribution guidelines
   ├─📄 .gitignore                           Git configuration
   └─📄 package.json                         (Optional) Node.js support
│
└─📁 docs/                                   📚 GENERATED LIVING DOCUMENTATION
   ├─📄 mkdocs.yml                          MkDocs configuration
   ├─📄 index.md                            Home page
   ├─📄 getting-started.md
   ├─📁 architecture/
   │  ├─📄 overview.md
   │  ├─📄 plugin-structure.md
   │  ├─📄 skill-system.md
   │  └─📄 command-patterns.md
   ├─📁 skills/
   │  ├─📄 living-documentation.md
   │  ├─📄 testing.md
   │  ├─📄 ci-cd.md
   │  ├─📄 code-quality.md
   │  ├─📄 documentation.md
   │  └─📄 spec-driven.md
   ├─📁 commands/
   │  ├─📄 run-tests.md
   │  ├─📄 setup-ci.md
   │  ├─📄 check-quality.md
   │  └─📄 init-project.md
   ├─📁 api/
   │  ├─📄 skills-api.md
   │  ├─📄 commands-api.md
   │  └─📄 hooks-api.md
   ├─📁 guides/
   │  ├─📄 installation.md
   │  ├─📄 quick-start.md
   │  ├─📄 team-setup.md
   │  └─📄 faq.md
   └─📁 css/
      └─📄 extra.css
```

---

## Layer Visualization

### Layer 1: Specification & Research
```
┌─────────────────────────────────────────────────────────────────┐
│  SPECIFICATION LAYER (Complete & Ready)                         │
├─────────────────────────────────────────────────────────────────┤
│ 8 Specifications in Draft Status:                               │
│  1. living-documentation-skill (⭐ PRIMARY)                       │
│  2. plugin-best-practices-setup (🔧 FOUNDATION)                  │
│  3. plugin-best-practices-testing                                │
│  4. plugin-best-practices-ci-cd                                  │
│  5. plugin-best-practices-code-quality                           │
│  6. plugin-best-practices-documentation                          │
│  7. plugin-best-practices-spec-driven-dev                        │
│  8. plugin-best-practices-agents                                 │
│                                                                  │
│ Research Documents: CONCEPTS, Living Docs, AST Analysis         │
└─────────────────────────────────────────────────────────────────┘
```

### Layer 2: Plugin Distribution (Implementation Target)
```
┌─────────────────────────────────────────────────────────────────┐
│  PLUGIN DISTRIBUTION LAYER                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Plugin Metadata (.claude-plugin/)                        │   │
│  │  • plugin.json (manifest)                               │   │
│  │  • marketplace.json (distribution)                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↓                                     │
│  ┌──────────────┬──────────────┬──────────────┐                 │
│  │   SKILLS     │   COMMANDS   │    AGENTS    │                 │
│  ├──────────────┼──────────────┼──────────────┤                 │
│  │ 6 Skills     │ 4+ Commands  │ 2 Agents     │                 │
│  │              │              │              │                 │
│  │ 1. Living    │ 1. run-tests │ 1. Test      │                 │
│  │    Docs⭐    │ 2. setup-ci  │    Reviewer  │                 │
│  │ 2. Testing   │ 3. check-    │ 2. Quality   │                 │
│  │ 3. CI/CD     │    quality   │    Checker   │                 │
│  │ 4. Quality   │ 4. init-     │              │                 │
│  │ 5. Docs      │    project   │              │                 │
│  │ 6. Spec-     │ 5. generate- │              │                 │
│  │    Driven    │    docs      │              │                 │
│  └──────────────┴──────────────┴──────────────┘                 │
│                            ↓                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Hooks (Event-Based Policies)                             │   │
│  │  • pre-tool-use (remind about specs)                    │   │
│  │  • post-tool-use (validate implementation)              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Layer 3: Generated Documentation
```
┌─────────────────────────────────────────────────────────────────┐
│  GENERATED LIVING DOCUMENTATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Generated via: living-documentation-skill automation           │
│  Framework: MkDocs + Material Theme                            │
│  Deployment: GitHub Pages (via CI/CD)                          │
│                                                                  │
│  Contains:                                                      │
│  • Architecture documentation                                  │
│  • Skill guides (auto-generated)                               │
│  • Command reference (auto-generated)                          │
│  • API documentation (auto-generated)                          │
│  • Getting started guides                                      │
│  • Team setup instructions                                     │
│  • FAQ and troubleshooting                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Skill Complexity & Size

### Living Documentation Skill ⭐⭐⭐⭐⭐
```
┌─────────────────────────────────────────────────────────────────┐
│ LIVING DOCUMENTATION SKILL                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Guides (6 files):                                               │
│  • mkdocs-setup, api-reference, architecture-docs,             │
│    documentation-testing, versioning, best-practices           │
│                                                                  │
│ Scripts (6 files):                                              │
│  • init_mkdocs, gen_api_reference, extract_architecture,       │
│    generate_diagrams, validate_docs, check_freshness           │
│                                                                  │
│ Templates (8+ files):                                           │
│  • mkdocs.yml, docs/index.md, docs/architecture.md,            │
│    docs/contributing.md, workflows/docs.yml,                   │
│    .pre-commit-config.yaml                                     │
│                                                                  │
│ Plugins (1 custom plugin):                                      │
│  • mkdocs_spec_validator plugin                                │
│                                                                  │
│ Total: ~25-30 files                                             │
│ Complexity: ⭐⭐⭐⭐⭐ (Most complex)                             │
│ Dependencies: griffe, mkdocs, diagrams, pydeps, etc.           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Other Skills ⭐⭐⭐-⭐⭐⭐⭐
```
Testing    | CI/CD      | Code Quality | Docs       | Spec-Driven
⭐⭐⭐⭐   | ⭐⭐⭐⭐   | ⭐⭐⭐⭐     | ⭐⭐⭐    | ⭐⭐⭐
15-20 files| 15-20 files| 15-20 files  | 15-20 files| 10-15 files
```

---

## Implementation Sequence

### Phase 1: Foundation (Week 1)
```
specs/ (ready) ──→ plugin-setup spec ──→ .claude-plugin/
                                         ├─ plugin.json
                                         └─ marketplace.json
                                            ↓
                                      Plugin scaffold ready
```

### Phase 2: Living Documentation Skill (Weeks 2-3)
```
living-docs spec ──→ Scripts
                     ├─ init_mkdocs.py
                     ├─ gen_api_reference.py
                     ├─ extract_architecture.py
                     ├─ generate_diagrams.py
                     ├─ validate_docs.py
                     └─ check_freshness.py
                        ↓
                     Templates (jinja2)
                     Guides (markdown)
                     Custom plugin
                        ↓
                     Living-docs skill complete
```

### Phase 3: Other Skills (Weeks 4-5)
```
Testing spec    ──→ testing/
CI/CD spec      ──→ ci-cd/
Quality spec    ──→ code-quality/
Docs spec       ──→ documentation/
Spec-driven spec ──→ spec-driven/
                        ↓
                   5 skills complete
```

### Phase 4: Commands & Agents (Week 6)
```
All specs + skills ──→ commands/ (4+ commands)
                        agents/ (2 agents)
                        hooks/ (event policies)
                           ↓
                        User interaction layer ready
```

### Phase 5: Polish & Docs (Week 7)
```
Everything complete ──→ docs/ (living docs generated)
                        README, CHANGELOG, CONTRIBUTING
                        GitHub integration
                        Testing & QA
                           ↓
                        Production ready
```

---

## File Statistics

| Type | Count | Examples |
|------|-------|----------|
| Specifications | 8 | .md files in specs/features/ |
| Markdown (guides) | 50+ | Skills guides, templates |
| Python scripts | 20+ | Automation and commands |
| Configuration | 10+ | .yml, .json, .yaml files |
| Templates | 10+ | Jinja2 templates |
| Generated docs | 20+ | Auto-generated by living-docs |
| **TOTAL** | **~120** | Ready to build |

---

## Key Metrics

```
Specifications:     8 (all Draft)
Skills:             6 (1 major + 5 standard)
Commands:           4+
Agents:             2
Hooks:              2
Python Scripts:     20+
Markdown Files:     50+
Total Files:        ~200+
Implementation:     100-120 new files needed
Estimated Effort:   4-6 weeks for full implementation
```

---

## Living Documentation Skill Highlights

### 🎯 Purpose
Automate entire documentation lifecycle - prevent docs from going stale

### 🛠️ Tools
- **Generation**: Griffe, AST
- **Framework**: MkDocs + Material
- **Visualization**: diagrams, pyvis, mermaid
- **Testing**: pytest, doctest, linkchecker
- **Automation**: pre-commit, GitHub Actions

### 📊 Capabilities
- Auto-generate API docs from docstrings
- Extract architecture from code structure
- Create dependency diagrams
- Validate documentation accuracy
- Detect outdated documentation
- CI/CD integration for auto-deployment
- Version management with mike

### 📁 Structure
```
living-documentation/
├── 4 guides (educational)
├── 6 automation scripts
├── 8+ configuration templates
├── 1 custom MkDocs plugin
└── Comprehensive requirements file
```

---

## Quick Links

| Document | Purpose |
|----------|---------|
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Complete technical structure |
| [LIVING_DOCUMENTATION_SKILL_STRUCTURE.md](LIVING_DOCUMENTATION_SKILL_STRUCTURE.md) | Living-docs skill details |
| [PROJECT_STRUCTURE_SUMMARY.md](PROJECT_STRUCTURE_SUMMARY.md) | Executive summary |
| [CLAUDE.md](CLAUDE.md) | Development constitution |
| [specs/features/living-documentation-skill.md](specs/features/living-documentation-skill.md) | Living-docs spec |

---

*Visual reference for complete spec-kit project structure*
*Planning phase - ready for implementation*
*Last Updated: 2026-01-25*
