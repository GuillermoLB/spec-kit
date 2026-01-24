# Feature: Best Practices Plugin - CI/CD

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-24
**Priority**: High

## Purpose

Add comprehensive CI/CD pipeline support to the best-practices plugin. This feature provides an auto-triggered CI/CD skill and a user-invoked command to help teams:

- Set up continuous integration and deployment pipelines
- Optimize pipeline performance and reliability
- Implement deployment strategies (blue-green, canary, rolling)
- Manage secrets and security in pipelines
- Support multiple CI/CD platforms

## Requirements

- [ ] Create `skills/ci-cd/SKILL.md` - Auto-triggered CI/CD guidance
- [ ] Create `commands/setup-ci.md` - CI/CD pipeline setup command
- [ ] Support GitHub Actions
- [ ] Support GitLab CI
- [ ] Support Jenkins
- [ ] Support CircleCI
- [ ] Generate platform-specific pipeline configs
- [ ] Include linting, testing, building, and deployment stages
- [ ] Optimize for performance (caching, parallelization)
- [ ] Provide security and secret management guidance

## User Stories

**As a** developer setting up CI/CD for a new project
**I want** Claude to generate a complete pipeline configuration
**So that** I can establish reliable deployment workflows quickly

**As a** DevOps engineer optimizing pipelines
**I want** Claude to suggest performance improvements
**So that** I can reduce build times and deployment latency

**As a** team lead enforcing pipeline standards
**I want** to see best practices guidance in Claude Code
**So that** all projects follow consistent CI/CD patterns

**As a** developer deploying to production
**I want** guidance on deployment strategies and safety
**So that** I can deploy with confidence

## Acceptance Criteria

1. **Given** a developer runs `/best-practices:setup-ci`
   **When** they answer project questions
   **Then** Claude generates a complete pipeline configuration

2. **Given** a Python project with pytest
   **When** the setup-ci command runs
   **Then** the generated config includes:
     - Dependency installation
     - Linting (flake8/black)
     - Test execution with coverage
     - Build step (if applicable)

3. **Given** a JavaScript project
   **When** the setup-ci command runs
   **Then** the generated config includes:
     - npm install
     - ESLint and Prettier
     - Jest tests with coverage
     - Build step (if applicable)

4. **Given** a developer uses GitHub Actions
   **When** Claude generates a pipeline
   **Then** it creates `.github/workflows/main.yml`

5. **Given** a developer uses GitLab CI
   **When** Claude generates a pipeline
   **Then** it creates `.gitlab-ci.yml`

6. **Given** a developer asks about deployment strategies
   **When** Claude responds
   **Then** it explains blue-green, canary, and rolling deployments

## Technical Details

### Skill: CI/CD

**File**: `skills/ci-cd/SKILL.md`

**Purpose**: Auto-triggered skill that provides CI/CD patterns and best practices when developers work with pipeline configs.

**YAML Frontmatter**:
```yaml
---
name: ci-cd
description: Provides CI/CD pipeline patterns, deployment strategies, and platform guidance
---
```

**Key Sections**:

1. **When to Trigger This Skill**
   - Detecting pipeline files (.github/workflows, .gitlab-ci.yml, Jenkinsfile)
   - User asks about CI/CD or deployment
   - User modifying deployment configurations
   - User setting up new project pipeline

2. **Pipeline Architecture**
   - Stage organization (lint, test, build, deploy)
   - Job dependencies and ordering
   - Conditional execution
   - Matrix builds

3. **Platform-Specific Guidance**
   - GitHub Actions workflows
   - GitLab CI/CD
   - Jenkins pipelines
   - CircleCI config
   - Travis CI
   - Azure Pipelines

4. **Best Practices**
   - Fail-fast strategies
   - Caching dependencies
   - Parallelization
   - Artifact management
   - Log retention
   - Environment management

5. **Deployment Strategies**
   - Blue-green deployment
   - Canary deployments
   - Rolling deployments
   - Feature flags
   - Rollback strategies

6. **Security in Pipelines**
   - Secret management
   - Credential handling
   - Access control
   - Audit logging
   - Container scanning
   - Dependency scanning

7. **Performance Optimization**
   - Build caching strategies
   - Docker layer caching
   - Test parallelization
   - Artifact caching
   - Dependency caching

8. **Common Patterns**
   - Branch-based workflows
   - Release workflows
   - Pull request validation
   - Scheduled jobs
   - Webhook triggers

9. **Troubleshooting**
   - Debugging failed builds
   - Timeout issues
   - Permission errors
   - Secret access problems

### Command: setup-ci

**File**: `commands/setup-ci.md`

**Purpose**: User-invoked command that generates and configures CI/CD pipelines.

**Workflow**:

1. **Detect project**
   - Language detection
   - Build system detection (Maven, Gradle, npm, pip, go)
   - Test framework detection
   - Git platform detection (GitHub, GitLab, Bitbucket)

2. **Ask questions**
   ```
   Which CI/CD platform? (GitHub Actions / GitLab CI / Jenkins / CircleCI)
   What's your primary language? (Python / JavaScript / Go / Java)
   Deploy to production? (yes / no)
   If yes, where? (AWS / GCP / Heroku / Docker Hub)
   Use containers? (yes / no)
   ```

3. **Ask deployment details**
   ```
   Deployment strategy? (blue-green / canary / rolling / simple)
   Environment count? (dev / staging / production)
   Approval required for prod? (yes / no)
   ```

4. **Generate pipeline**
   - Create platform-specific config file
   - Include all detected stages
   - Add secrets placeholders
   - Include comments explaining each step

5. **Provide guidance**
   - Explain each stage
   - List required secrets to configure
   - Provide deployment instructions
   - Link to platform documentation

**Invocation**: `/best-practices:setup-ci`

**Example Output (GitHub Actions)**:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install flake8 black
      - run: flake8 src/
      - run: black --check src/

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt pytest pytest-cov
      - run: pytest --cov=src tests/
      - uses: codecov/codecov-action@v3

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          # Add your deployment script here
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
```

**Setup Instructions Generated**:
```
GitHub Actions Pipeline Created
================================

1. Configure Secrets:
   - Go to Settings > Secrets and variables > Actions
   - Add DEPLOY_KEY (your deployment credential)

2. Review the Pipeline:
   - Pipeline file: .github/workflows/main.yml
   - Stages: lint → test → deploy
   - Runs on: Push to main/develop, Pull requests

3. Test the Pipeline:
   - Push to a branch and create a pull request
   - Watch the Actions tab for execution

4. Enable Auto-Deploy:
   - Update the deploy step with your deployment command
   - Add any additional environment variables needed
```

### Platform Support

**GitHub Actions**:
- Generate `.github/workflows/main.yml`
- Support matrix builds
- Environment variables and secrets
- Conditional steps
- Action reuse

**GitLab CI**:
- Generate `.gitlab-ci.yml`
- Support stages and needs
- Cache and artifacts
- Protected branches
- Manual approval jobs

**Jenkins**:
- Generate `Jenkinsfile` (declarative)
- Support stages
- Post actions
- Parallel execution
- Library usage

**CircleCI**:
- Generate `.circleci/config.yml`
- Support workflows
- Caching strategies
- Machine specifications
- Context management

### Deployment Strategy Patterns

**Blue-Green**:
```yaml
deploy:
  script:
    - deploy-to-green-environment
    - smoke-tests-on-green
    - switch-traffic-blue-to-green
    - keep-blue-as-rollback
```

**Canary**:
```yaml
deploy:
  script:
    - deploy-to-canary
    - route-5%-traffic-to-canary
    - monitor-metrics
    - gradually-increase-traffic
    - rollback-if-errors
```

**Rolling**:
```yaml
deploy:
  script:
    - update-replica-1
    - verify-health
    - update-replica-2
    - verify-health
    - update-replica-3
```

## Edge Cases & Error Handling

1. **Edge case**: Mixed deployment targets
   - **Handling**: Create separate deployment jobs per target
   - **Message**: "Detected multiple deployment targets. Creating separate jobs."

2. **Edge case**: No tests in project
   - **Handling**: Skip test stage, note recommendation
   - **Message**: "No tests found. Consider adding tests to your pipeline."

3. **Error**: Unsupported CI/CD platform
   - **Message**: "Platform not directly supported. Showing generic patterns."
   - **Recovery**: Provide guidance for manual adaptation

4. **Edge case**: Complex monorepo structure
   - **Handling**: Offer matrix builds or conditional paths
   - **Message**: "Detected monorepo. Would you like matrix builds per module?"

5. **Edge case**: Self-hosted infrastructure
   - **Handling**: Provide guidance for self-hosted runners
   - **Message**: "Using self-hosted infrastructure? Here's how to configure runners."

## Security Considerations

- [ ] No hardcoded secrets in generated configs
- [ ] Clear placeholders for secrets (e.g., `${{ secrets.API_KEY }}`)
- [ ] Guidance on secret management per platform
- [ ] Branch protection recommendations
- [ ] Audit logging setup instructions
- [ ] Container image scanning recommendations
- [ ] Dependency scanning integration

## Testing Strategy

### Validation

- [ ] SKILL.md has valid structure
- [ ] Generated GitHub Actions workflows are valid YAML
- [ ] Generated GitLab CI configs are valid YAML
- [ ] Jenkins pipeline syntax is valid
- [ ] All placeholders are clearly marked

### Manual Testing

- [ ] Generate pipeline for Python project
- [ ] Generate pipeline for JavaScript project
- [ ] Test with GitHub Actions
- [ ] Test with GitLab CI
- [ ] Verify generated secrets setup instructions
- [ ] Verify deployment strategy explanations

## Dependencies

- **Blocked by**: plugin-best-practices-setup
- **Blocks**: None (parallel with other features)
- **Related**:
  - plugin-best-practices-testing (test stage in pipeline)
  - plugin-best-practices-code-quality (linting stage in pipeline)

## Implementation Notes

### Decisions Made

- **GitHub Actions as primary platform**: Most popular for public projects
- **Declarative pipelines**: Easier to read and maintain
- **Separate jobs per stage**: Better parallelization
- **Generated vs. template approach**: Direct CLI generation is faster

### Platform Detection

```
GitHub: .git/config contains github.com
GitLab: .git/config contains gitlab.com
Jenkins: Jenkinsfile exists
CircleCI: .circleci/ directory exists
```

### Default Stage Structure

```
lint    → test    → build    → deploy-staging    → deploy-prod
  ↓        ↓        ↓              ↓
Fail → Fail  → Optional    → Optional              Need approval
```

## Open Questions

- [ ] Should we auto-detect deployment targets from code?
  - *Decision pending*: User preference on automation vs. explicit config
- [ ] Support for Infrastructure as Code (Terraform, CloudFormation)?
  - *Decision pending*: Future enhancement

## References

- GitHub Actions: https://docs.github.com/en/actions
- GitLab CI/CD: https://docs.gitlab.com/ee/ci/
- Jenkins Documentation: https://www.jenkins.io/doc/
- CircleCI Documentation: https://circleci.com/docs/
- Deployment Strategies: https://martinfowler.com/bliki/BlueGreenDeployment.html

---

**Template Version**: 1.0
**Last Updated**: 2026-01-24
