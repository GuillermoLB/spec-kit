# Claude Code Concepts Guide

This document explains all the key concepts used in the spec-kit project and how they work together to create a powerful development workflow.

**Audience**: Team members, developers, and anyone contributing to spec-kit
**Purpose**: Shared understanding of architecture, terminology, and workflows

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Detailed Explanations](#detailed-explanations)
3. [How They Work Together](#how-they-work-together)
4. [Quick Reference](#quick-reference)
5. [Configuration & Setup](#configuration--setup)

---

## Core Concepts

### 🔌 Plugin

**What it is**: A self-contained package that extends Claude Code with domain-specific functionality.

**Key traits**:
- Bundles multiple features (skills, commands, agents)
- Installed via marketplace
- Versioned and released independently
- Discoverable by teams

**Example**: `best-practices` plugin provides testing, CI/CD, code quality, and documentation features.

**User perspective**: `/plugin install company/best-practices-plugin`

---

### 💡 Skill

**What it is**: Context-aware guidance that triggers automatically when relevant patterns are detected.

**Key traits**:
- Auto-triggered (no user action needed)
- Appears when relevant code/action detected
- Provides suggestions, not commands
- Non-intrusive and helpful

**Examples**:
- **Testing skill**: Activates when creating test files → suggests testing patterns
- **CI/CD skill**: Activates when working with pipelines → provides deployment guidance
- **Code quality skill**: Activates on code review → suggests improvements

**User perspective**: Developer sees suggestions appear automatically

---

### ⚙️ Command

**What it is**: A user-invoked action that performs a specific task and returns concrete results.

**Key traits**:
- Explicitly invoked by user
- Performs specific, deterministic action
- Returns files or configuration
- Interactive (asks clarifying questions)

**Examples**:
- `/best-practices:run-tests` → Execute tests and generate coverage report
- `/best-practices:setup-ci` → Generate CI/CD pipeline configuration
- `/best-practices:check-quality` → Analyze code quality

**User perspective**: `/<plugin>:<command>` syntax in Claude Code

---

### 🤖 Agent

**What it is**: A sophisticated analysis tool that performs deep, multi-step examination combining multiple domains.

**Key traits**:
- User-invoked (like commands)
- Time-intensive (1-5 minutes vs seconds)
- Comprehensive analysis
- Returns detailed, actionable reports

**Examples**:
- `test-reviewer` → Comprehensive test audit with prioritized recommendations
- `quality-checker` → Full codebase quality assessment with effort estimates

**User perspective**: `/best-practices:test-reviewer` for deep analysis

---

### 🪝 Hook

**What it is**: An event handler that intercepts Claude's operations before or after execution.

**Key traits**:
- Configured in `.claude/settings.json`
- Intercepts specific tool usage
- Can validate, remind, or block actions
- Enforces project standards

**Examples**:
- Remind developers to write specs before implementing
- Validate code follows project conventions
- Block dangerous operations

**User perspective**: Automatic reminders/validations appear before/after actions

---

### ⚙️ Settings & Configuration

**What it is**: Project-level configuration that controls Claude Code behavior.

**Key files**:
- `.claude/settings.json` - Project configuration (committed)
- `.claude/settings.local.json` - Local overrides (not committed)
- `CLAUDE.md` - Project development constitution

**Configures**:
- Which plugins are enabled
- Hook enforcement rules
- Permissions and tool access
- Custom marketplaces

**User perspective**: Developers inherit project settings when they clone the repo

---

## Detailed Explanations

### Plugin: The Container

A plugin is the **top-level organizational unit** in Claude Code. Think of it like an npm package, but for development workflows.

#### Structure
```
best-practices-plugin/
├── .claude-plugin/               # Plugin metadata
│   ├── plugin.json               # Name, version, author
│   └── marketplace.json          # Distribution config
├── skills/                       # Auto-triggered guidance
│   ├── testing/SKILL.md
│   ├── ci-cd/SKILL.md
│   └── code-quality/SKILL.md
├── commands/                     # User-invoked actions
│   ├── run-tests.md
│   ├── setup-ci.md
│   └── check-quality.md
├── agents/                       # Deep analysis tools
│   ├── test-reviewer.md
│   └── quality-checker.md
├── README.md                     # Installation guide
└── LICENSE                       # Open source license
```

#### How to Install
```bash
# Add to marketplace
/plugin marketplace add company/best-practices-plugin

# Install into project
/plugin install best-practices@best-practices

# Enable in .claude/settings.json
{
  "enabledPlugins": {
    "best-practices@best-practices": true
  }
}
```

---

### Skill: Contextual Guidance

Skills are the **passive assistants** of the system. They activate automatically based on conversation context and Claude Code's own actions.

#### How They Trigger

Skills activate based on:
1. **Keywords in the skill description matching your conversation** - If you mention "testing" or ask about tests, Claude loads skills with testing-related descriptions
2. **Claude Code's own file operations** - When Claude Code writes/edits test files through its own tools (Write, Edit), relevant skills activate
3. **Explicit skill invocation** - You can directly invoke skills with `/skill-name`

**Important**: Skills only have visibility into actions that Claude Code itself takes or content you explicitly share. Creating files directly in your IDE (VSCode, etc.) won't trigger skills automatically—Claude won't know about them unless you mention it in conversation.

| Context | Skill | Provides |
|---------|-------|----------|
| You mention testing / ask about test patterns | Testing | Pytest patterns, assertions, mocks |
| You work with `.github/workflows/` or mention CI/CD | CI/CD | Pipeline guidance, best practices |
| You ask for code review help or mention refactoring | Code Quality | Complexity analysis, improvements |
| You ask about documentation or mention docstrings | Documentation | Template guidance, API docs |
| You ask about starting a new feature | Spec-Driven | Feature spec template, workflow |

#### Example: Testing Skill in Action

**Scenario 1: Claude Code creates the file**
1. You ask: "Write a test file for the API"
2. Claude Code creates `tests/test_api.py` using the Write tool
3. Testing skill automatically activates
4. Claude provides testing patterns and best practices

**Scenario 2: You create the file manually**
1. You create `tests/test_api.py` in VSCode
2. Claude Code does NOT automatically know about it
3. You mention it: "I created test_api.py, help me write tests"
4. Claude loads the testing skill based on your request

#### Skill File Format

```yaml
---
name: testing
description: Provides testing patterns and best practices. Use when writing tests, asking about testing approaches, or creating test files.
---

# Testing Patterns

## When This Activates
- User asks about testing approaches
- User requests help writing tests
- Claude Code writes test files
- User mentions test-related topics

## Common Patterns

### Pytest Fixtures
[guidance content...]

### Parametrized Tests
[guidance content...]
```

---

### Command: User-Invoked Actions

Commands are the **active tools** that users invoke explicitly to perform tasks.

#### Available Commands

```
/best-practices:run-tests
  → Execute test suite with coverage analysis
  → Reports coverage gaps and recommendations

/best-practices:setup-ci
  → Generate CI/CD pipeline configuration
  → Detects project type and asks deployment target

/best-practices:check-quality
  → Analyze code complexity and security
  → Returns prioritized recommendations

/best-practices:init-project
  → Initialize spec-driven development structure
  → Creates specs/ directory and templates
```

#### Command Workflow Pattern

All commands follow this standard pattern:

1. **Detect** - Identify project type, structure, language
2. **Ask** - Get user preferences and decisions
3. **Analyze** - Gather metrics or requirements
4. **Generate** - Create outputs or perform actions
5. **Report** - Present results in human-readable format

#### Example: `setup-ci` Command

```
User runs: /best-practices:setup-ci

Step 1: Detect
  → Detects: Python project, FastAPI framework

Step 2: Ask
  → "Deploy to AWS Lambda or Docker?"
  → "Which regions?"

Step 3: Analyze
  → Gathers dependencies, build requirements

Step 4: Generate
  → Creates: .github/workflows/main.yml

Step 5: Report
  → "✅ CI/CD pipeline ready at .github/workflows/main.yml"
```

---

### Agent: Deep Analysis

Agents are the **investigators** - sophisticated tools that provide comprehensive analysis.

#### Key Characteristics

- **User-invoked** like commands
- **Time-intensive** (1-5 minutes)
- **Multi-faceted analysis** combining multiple domains
- **Detailed reports** with effort estimates
- **Actionable insights** with prioritization

#### Available Agents

**test-reviewer**: Comprehensive test audit
```
/best-practices:test-reviewer

Analyzes:
- Overall test health (score 0-100)
- Coverage metrics per module
- Test quality (readability, maintainability)
- Flaky test detection
- Performance bottlenecks

Returns:
- Test health scorecard
- Module-by-module breakdown
- Prioritized recommendations with effort estimates
```

**quality-checker**: Full codebase quality assessment
```
/best-practices:quality-checker

Analyzes:
- Code complexity (cyclomatic, cognitive)
- Security vulnerabilities (OWASP Top 10)
- Maintainability metrics
- Dependency health
- Documentation completeness

Returns:
- Quality score and trend
- Vulnerability report
- Improvement roadmap with priorities
```

#### Agent vs Skill vs Command

| Dimension | Skill | Command | Agent |
|-----------|-------|---------|-------|
| **Trigger** | Automatic | User invokes | User invokes |
| **Scope** | Quick guidance | Single action | Comprehensive |
| **Depth** | Surface-level tips | Specific task | Deep analysis |
| **Output** | Suggestions | Config/results | Detailed report |
| **Time** | Immediate | Few minutes | 1-5 minutes |
| **Example** | "Consider fixtures" | "Generate CI config" | "Full test audit" |

---

### Hook: Event Interception

Hooks are **policy enforcers** that intercept operations to validate, remind, or block actions.

#### How Hooks Work

```
User Action → Claude Code
              ↓
         [PreToolUse Hook]
         (Can validate, remind, or block)
              ↓
         Tool Executes
              ↓
         [PostToolUse Hook]
         (Can validate results)
              ↓
         User Sees Result
```

#### Hook Types

**PreToolUse**: Executes before a tool runs
```json
{
  "type": "PreToolUse",
  "matcher": "Edit|Write",
  "action": "Remind to check spec requirements"
}
```

**PostToolUse**: Executes after a tool runs
```json
{
  "type": "PostToolUse",
  "matcher": "Bash",
  "action": "Validate git commit follows conventions"
}
```

#### Example: Spec-Driven Hook

This hook enforces spec-driven development:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "model",
            "prompt": "Before implementing: Is there a spec in specs/features/? If starting new feature, suggest writing a spec first."
          }
        ]
      }
    ]
  }
}
```

**In action**:
1. Developer tries to edit source code without a spec
2. Hook intercepts and asks: "Is there a spec for this feature?"
3. If no spec, suggests: `/best-practices:init-project`
4. Developer can confirm or proceed anyway

#### Common Hook Patterns

**Pattern 1: Quality Gate**
```json
{
  "matcher": "Bash(git push)",
  "action": "Run tests and check coverage before push"
}
```

**Pattern 2: Convention Enforcement**
```json
{
  "matcher": "Write",
  "action": "Check file naming follows convention"
}
```

**Pattern 3: Security Check**
```json
{
  "matcher": "Bash",
  "action": "Block commands that delete sensitive files"
}
```

---

### Settings & Configuration

Configuration controls how Claude Code behaves in your project.

#### .claude/settings.json

**Purpose**: Project-wide configuration (committed to git)

**Controls**:
- Which plugins are enabled
- Hook enforcement rules
- Known plugin marketplaces
- Permission policies

```json
{
  "enabledPlugins": {
    "best-practices@best-practices": true,
    "scientific-skills@claude-scientific-skills": true
  },
  "extraKnownMarketplaces": {
    "company": {
      "source": {
        "source": "github",
        "repo": "company/plugins"
      }
    }
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "model",
            "prompt": "Check for spec before implementing..."
          }
        ]
      }
    ]
  }
}
```

#### .claude/settings.local.json

**Purpose**: Local-only overrides (NOT committed)

**Use cases**:
- Developer-specific tool access
- Local testing configurations
- API keys and credentials
- Machine-specific settings

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm *)"
    ]
  }
}
```

#### CLAUDE.md

**Purpose**: Development constitution and workflow

**Defines**:
- Core principles (spec-first, validation required)
- File organization standards
- Workflow phases (Specify → Plan → Implement → Validate)
- Quality standards
- Architecture documentation expectations

**Example section**:
```markdown
## Workflow

### Phase 1: Specify
Before writing any code:
1. Read specs/architecture.md
2. Check if spec exists in specs/
3. If no spec, create one or ask user

### Phase 2: Plan
Identify all affected files and plan approach

### Phase 3: Implement
Follow patterns and implement incrementally

### Phase 4: Validate
Verify acceptance criteria and run tests
```

---

## How They Work Together

### Scenario 1: Developer Starting a New Feature

```
Step 1: Product/Developer describes the feature need
  → Says: "We need user authentication with OAuth2"
  → Provides: Business context and goals

Step 2: Claude Code (spec-driven skill) assists in spec creation
  → Generates: Draft spec with requirements and acceptance criteria
  → Asks: Clarifying questions about constraints, architecture, integrations
  → Proposes: Technical approach based on architectural principles
  → References: specs/architecture.md for alignment

Step 3: Product/Architect reviews and approves spec
  → Validates: Requirements are clear and testable
  → Approves: Technical approach aligns with architecture
  → Updates: Spec status to "In Progress"
  → Creates: specs/features/user-authentication-oauth2.md

Step 4: Hook validates spec exists
  → Checks: specs/features/ contains approved spec
  → Blocks: Code writing without approved spec

Step 5: Claude Code implements feature
  → Reads: Feature spec and architectural constraints
  → Spec-driven skill activates: Suggests patterns aligned with spec
  → Implements: Exactly to spec requirements
  → Validates: Each acceptance criterion during development

Step 6: Claude Code runs tests (automated)
  → Verifies: All acceptance criteria met
  → Validates: Against spec requirements

Step 7: Developer reviews implementation
  → Checks: Code quality and spec compliance
  → Verifies: All requirements implemented
  → Updates: Spec status to "Implemented"

Step 8: Quality-checker agent validates
  → Reports: Quality against project standards
  → Ensures: No deviations from architectural principles
```

### Scenario 2: Testing Workflow

```
Step 1: Feature spec references test requirements
  → Spec includes: Acceptance criteria that drive test cases
  → Defines: Coverage expectations and test scenarios

Step 2: Claude Code (testing skill) generates test spec
  → Reads: Feature spec acceptance criteria
  → Generates: Test plan with test cases mapped to requirements
  → Asks: Clarifying questions about edge cases and integration points
  → Proposes: Testing strategy (unit, integration, e2e)

Step 3: Developer reviews and approves test spec
  → Validates: All acceptance criteria covered by tests
  → Approves: Testing approach
  → Creates: specs/tests/feature-name-tests.md

Step 4: Hook validates test spec exists
  → Checks: Test specification aligns with feature spec

Step 5: Claude Code implements tests
  → Reads: Test spec and feature spec
  → Testing skill activates: Suggests pytest patterns, assertions, mocks
  → Implements: All test cases from test spec
  → Validates: Coverage meets requirements

Step 6: Claude Code runs test suite (automated)
  → Executes: Test suite with coverage analysis
  → Verifies: All acceptance criteria covered
  → Reports: Coverage against test spec

Step 7: Quality-checker agent validates tests
  → Reports: Test quality and maintainability
  → Ensures: Tests align with project standards

Step 8: Developer reviews
  → Checks: Tests pass and coverage meets spec
  → Updates: Spec status to "Implemented"
```

### Scenario 3: Setting Up CI/CD

```
Step 1: Team needs to establish CI/CD pipeline
  → Describes: Deployment needs and environments
  → Provides: Current infrastructure context

Step 2: Claude Code (CI/CD skill) generates CI/CD spec
  → Reads: specs/architecture.md for system design
  → Generates: CI/CD specification with:
    - Build stages and triggers
    - Test gates and coverage requirements
    - Deployment environments and approval gates
    - Security controls and secret management
  → Asks: Clarifying questions about deployment strategy
  → Proposes: Platform-specific approach (GitHub Actions, etc.)

Step 3: DevOps/Architect reviews and approves spec
  → Validates: Pipeline aligns with architectural principles
  → Approves: Security and deployment strategy
  → Updates: Spec status to "In Progress"
  → Creates: specs/ci-cd/pipeline-setup.md

Step 4: Hook validates CI/CD spec exists
  → Checks: specs/ci-cd/ contains approved specification

Step 5: Claude Code implements CI/CD configuration
  → Reads: CI/CD spec and architectural constraints
  → CI/CD skill activates: Suggests best practices for chosen platform
  → Implements: All pipeline stages from spec
  → Validates: All gates and checks per specification

Step 6: Claude Code validates configuration
  → Tests: Pipeline syntax and stage definitions
  → Verifies: All security practices implemented
  → Reports: Configuration against spec

Step 7: DevOps/Developer reviews implementation
  → Tests: Actual pipeline with sample builds
  → Verifies: All requirements from spec met
  → Updates: Spec status to "Implemented"

Step 8: Quality-checker agent validates
  → Reports: Security compliance and best practices
  → Ensures: No deviations from architectural principles
```

---

## Quick Reference

### Plugin Invocations
```bash
# Install plugin from marketplace
/plugin install best-practices@best-practices

# Discover available commands
/<plugin>:<command>    # Tab autocomplete shows options
```

### Command Invocations
```bash
/best-practices:run-tests
/best-practices:setup-ci
/best-practices:check-quality
/best-practices:init-project
```

### Agent Invocations
```bash
/best-practices:test-reviewer
/best-practices:quality-checker
```

### Skills
- Auto-triggered on relevant context
- No explicit invocation needed
- Appear as contextual suggestions

### Hook Configuration
```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|Bash",
        "hooks": [{ "type": "model", "prompt": "..." }]
      }
    ]
  }
}
```

---

## Configuration & Setup

### Initial Project Setup

**Step 1**: Create `.claude/settings.json`
```json
{
  "enabledPlugins": {
    "best-practices@best-practices": true
  }
}
```

**Step 2**: Create `CLAUDE.md` with project constitution
```
# Project Development Standards

## Core Principles
1. Specification First
2. Explicit Requirements
3. Validation Required
4. Incremental Progress
```

**Step 3**: Create `specs/` directory structure
```
specs/
├── SPECIFICATIONS_SUMMARY.md
├── features/
├── api/
└── architecture.md
```

**Step 4**: Enable hooks for enforcement
```json
{
  "hooks": {
    "PreToolUse": [...]
  }
}
```

### Developer Onboarding

1. **Clone repository**
   ```bash
   git clone <repo>
   cd <project>
   ```

2. **Understand project standards**
   ```bash
   # Read project constitution
   cat CLAUDE.md

   # Review architecture
   cat specs/architecture.md
   ```

3. **Check available tools**
   ```bash
   # Tab autocomplete shows available commands
   /best-practices:[TAB]
   ```

4. **Start development**
   ```bash
   # Run init command if needed
   /best-practices:init-project

   # Check quality anytime
   /best-practices:check-quality
   ```

### For Team Leaders

**Configure team standards** in `.claude/settings.json`:
1. Enable required plugins
2. Set up enforcement hooks
3. Define custom marketplaces
4. Configure permission policies

**Create `CLAUDE.md`** to document:
1. Development workflow
2. Code review standards
3. Architecture principles
4. Quality requirements

**Monitor compliance** using agents:
1. `/best-practices:test-reviewer` - Test health
2. `/best-practices:quality-checker` - Code quality
3. Review spec status in `SPECIFICATIONS_SUMMARY.md`

---

## Summary

| Concept | Role | Invoked | Output |
|---------|------|---------|--------|
| **Plugin** | Container for features | Installation | Unlocks skills, commands, agents |
| **Skill** | Auto guidance | Automatic | Contextual suggestions |
| **Command** | User actions | `/plugin:command` | Specific results/configs |
| **Agent** | Deep analysis | `/plugin:agent` | Detailed reports |
| **Hook** | Policy enforcement | Automatic | Validation/reminders |
| **Settings** | Configuration | Runtime | Behavior control |
| **CLAUDE.md** | Constitution | Reference | Team standards |

Together, these concepts create a powerful, intelligent development environment that guides teams toward better practices while remaining flexible to project-specific needs.

---

**Questions?** Check `specs/` for feature specifications, or ask your team lead for project-specific details.
