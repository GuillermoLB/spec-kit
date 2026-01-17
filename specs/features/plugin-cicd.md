# Feature: CI/CD Plugin

**Status**: Draft
**Owner**: spec-kit development team
**Last Updated**: 2026-01-17
**Priority**: Medium

## Purpose

Create a comprehensive CI/CD plugin providing GitHub Actions and GitLab CI patterns, deployment workflows, and automation best practices. This plugin helps teams set up continuous integration and deployment pipelines efficiently.

## Requirements

- [ ] SKILL.md with CI/CD patterns and best practices
- [ ] GitHub Actions workflow templates (Python, Node.js, Docker)
- [ ] GitLab CI configuration templates
- [ ] Pre-commit hook configurations
- [ ] Quality check workflows (linting, formatting, security scans)
- [ ] Deployment pipeline templates (AWS, Docker, Kubernetes)
- [ ] Makefile for common development tasks
- [ ] Badge generation examples
- [ ] Integration with install.sh
- [ ] Validation in verify.sh

## User Stories

**As a** DevOps engineer
**I want** CI/CD pipeline templates
**So that** I can set up automation quickly and correctly

**As a** developer
**I want** pre-commit hooks and quality checks
**So that** I catch issues before committing

**As a** team lead
**I want** consistent CI/CD patterns across projects
**So that** all projects follow the same automation standards

## Acceptance Criteria

1. **Given** I install the cicd plugin
   **When** I check .claude/skills/cicd/
   **Then** I see SKILL.md and template files

2. **Given** I copy a GitHub Actions workflow
   **When** I push code to GitHub
   **Then** the workflow executes automatically

3. **Given** I use the Makefile template
   **When** I run `make test`
   **Then** tests execute with proper configuration

4. **Given** I set up pre-commit hooks
   **When** I commit code
   **Then** linting and formatting run automatically

5. **Given** I use a deployment workflow
   **When** tests pass on main branch
   **Then** code deploys to staging environment

## Technical Details

### Plugin Structure

```
plugins/cicd/
├── skill.md                           # Main plugin file
└── templates/
    ├── github-actions/
    │   ├── python-ci.yml              # Python test workflow
    │   ├── python-deploy.yml          # Python deployment
    │   ├── docker-build.yml           # Docker build/push
    │   └── nodejs-ci.yml              # Node.js workflow
    ├── gitlab/
    │   ├── .gitlab-ci.yml             # GitLab CI template
    │   └── .gitlab-ci-python.yml      # Python-specific
    ├── pre-commit-config.yaml         # Pre-commit hooks
    ├── Makefile                       # Development tasks
    └── dependabot.yml                 # Dependency updates
```

### GitHub Actions Templates

**Template: python-ci.yml**

```yaml
name: Python CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Lint with ruff
      run: |
        pip install ruff
        ruff check .

    - name: Format check with black
      run: |
        pip install black
        black --check .

    - name: Type check with mypy
      run: |
        pip install mypy
        mypy src/

    - name: Security check with bandit
      run: |
        pip install bandit
        bandit -r src/

    - name: Run tests with pytest
      run: |
        pytest tests/ -v --cov=src --cov-report=xml --cov-report=term

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

**Template: python-deploy.yml**

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Run tests
      run: |
        pip install -r requirements.txt -r requirements-dev.txt
        pytest tests/

    - name: Build package
      run: |
        pip install build
        python -m build

    - name: Deploy to AWS
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      run: |
        pip install awscli
        aws s3 sync ./dist s3://my-bucket/releases/

    - name: Create Release
      if: startsWith(github.ref, 'refs/tags/')
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        draft: false
        prerelease: false
```

**Template: docker-build.yml**

```yaml
name: Docker Build and Push

on:
  push:
    branches: [ main ]
  release:
    types: [ published ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to DockerHub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: myorg/myapp
        tags: |
          type=ref,event=branch
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

    - name: Run Trivy security scan
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: myorg/myapp:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: 'trivy-results.sarif'
```

### GitLab CI Templates

**Template: .gitlab-ci.yml**

```yaml
stages:
  - test
  - build
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

before_script:
  - python -m venv venv
  - source venv/bin/activate
  - pip install -r requirements.txt

test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements-dev.txt
    - ruff check .
    - black --check .
    - mypy src/
    - pytest tests/ --cov=src --cov-report=xml --cov-report=term
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

build:
  stage: build
  image: python:3.11
  script:
    - pip install build
    - python -m build
  artifacts:
    paths:
      - dist/
  only:
    - main
    - tags

deploy_staging:
  stage: deploy
  image: python:3.11
  script:
    - pip install awscli
    - aws s3 sync ./dist s3://staging-bucket/
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - main

deploy_production:
  stage: deploy
  image: python:3.11
  script:
    - pip install awscli
    - aws s3 sync ./dist s3://production-bucket/
  environment:
    name: production
    url: https://example.com
  only:
    - tags
  when: manual
```

### Pre-commit Configuration

**Template: .pre-commit-config.yaml**

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: detect-private-key

  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.15
    hooks:
      - id: ruff
        args: [ --fix, --exit-non-zero-on-fix ]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: [-r, src/]
        exclude: tests/

  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.13.0
    hooks:
      - id: commitizen
```

### Makefile Template

```makefile
.PHONY: help install test lint format clean build deploy

# Default target
help:
	@echo "Available targets:"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run tests with coverage"
	@echo "  lint       - Run linters"
	@echo "  format     - Format code"
	@echo "  clean      - Remove build artifacts"
	@echo "  build      - Build package"
	@echo "  deploy     - Deploy to production"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-watch:
	pytest-watch tests/ -- -v

lint:
	ruff check .
	black --check .
	mypy src/
	bandit -r src/

format:
	black .
	ruff check --fix .

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

build: clean
	python -m build

deploy: test
	@echo "Deploying to production..."
	# Add deployment commands here

.PHONY: docker-build docker-run docker-test

docker-build:
	docker build -t myapp:latest .

docker-run:
	docker run -p 8000:8000 myapp:latest

docker-test:
	docker run myapp:latest pytest tests/
```

### Dependabot Configuration

**Template: .github/dependabot.yml**

```yaml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "devops-team"
    labels:
      - "dependencies"
      - "python"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    reviewers:
      - "devops-team"
    labels:
      - "dependencies"
      - "github-actions"

  # Docker
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

### SKILL.md Content Structure

1. **When to Use This Skill** - CI/CD scenarios
2. **GitHub Actions Patterns**
   - Workflow structure
   - Matrix builds
   - Caching strategies
   - Secrets management
3. **GitLab CI Patterns**
   - Pipeline stages
   - Job dependencies
   - Artifacts and caching
4. **Quality Gates**
   - Linting
   - Type checking
   - Security scanning
   - Coverage requirements
5. **Deployment Strategies**
   - Blue-green deployment
   - Canary releases
   - Rolling updates
6. **Pre-commit Hooks**
   - Setup and configuration
   - Custom hooks
7. **Monorepo CI/CD**
   - Path-based triggers
   - Selective testing

### Security Considerations

- [ ] Secrets stored in CI/CD secrets (never in code)
- [ ] Minimal permissions for CI/CD service accounts
- [ ] Security scanning in pipelines (Trivy, Bandit)
- [ ] Signed commits for production deployments
- [ ] Audit logs for deployments
- [ ] Branch protection rules

## Edge Cases & Error Handling

1. **Edge case**: Workflow fails on one Python version but passes on others
   - **Handling**: Allow matrix failures to be non-blocking for non-critical versions

2. **Edge case**: Deployment to production requires manual approval
   - **Handling**: Use environment protection rules, show in templates

3. **Error**: Secrets not configured
   - **Message**: Clear error indicating which secret is missing
   - **Recovery**: Documentation on secret setup

## Testing Strategy

### Validation Tests

- [ ] Verify SKILL.md has valid YAML frontmatter
- [ ] Verify workflow YAML files are valid
- [ ] Verify .pre-commit-config.yaml is valid
- [ ] Verify Makefile syntax

### Manual Testing

- [ ] Copy GitHub Actions workflow to test repository
- [ ] Trigger workflow and verify it runs
- [ ] Test pre-commit hooks locally
- [ ] Verify Makefile targets work

## Dependencies

- **Blocked by**: documentation-improvements
- **Blocks**: None
- **Related**: testing plugin (CI runs tests), examples (can use in CI/CD)

## Implementation Notes

### Decisions Made

- 2026-01-17 - Support both GitHub Actions and GitLab CI (most popular)
- 2026-01-17 - Include pre-commit hooks (catch issues early)
- 2026-01-17 - Makefile for platform-agnostic commands
- 2026-01-17 - Security scanning by default (Trivy, Bandit)
- 2026-01-17 - Matrix testing for Python versions

### Integration with install.sh

Add to plugin selection:

```bash
4) CI/CD Plugin - GitHub Actions, GitLab CI, automation workflows
```

Update verify.sh:

```bash
echo "Plugin: cicd"
check_file "plugins/cicd/skill.md"
check_file "plugins/cicd/templates/github-actions/python-ci.yml"
check_file "plugins/cicd/templates/Makefile"
```

## Verification

### GitHub Actions Verification

```bash
# Copy workflow
cp .claude/skills/cicd/templates/github-actions/python-ci.yml .github/workflows/

# Push and check Actions tab
git add .github/workflows/python-ci.yml
git commit -m "Add CI workflow"
git push

# Verify workflow runs on GitHub
```

### Pre-commit Verification

```bash
# Setup
cp .claude/skills/cicd/templates/pre-commit-config.yaml .pre-commit-config.yaml
pre-commit install

# Test
pre-commit run --all-files
```

### Makefile Verification

```bash
# Copy and test
cp .claude/skills/cicd/templates/Makefile .
make install
make test
make lint
```

## References

- GitHub Actions: https://docs.github.com/en/actions
- GitLab CI: https://docs.gitlab.com/ee/ci/
- Pre-commit: https://pre-commit.com/
- Make: https://www.gnu.org/software/make/manual/

---

**Template Version**: 1.0
**Last Updated**: 2026-01-17
