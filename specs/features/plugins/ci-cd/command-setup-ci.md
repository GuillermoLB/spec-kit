# Command: setup-ci

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: High

## Purpose

Generate and configure CI/CD pipelines for multiple platforms.

**Invocation**: `/ci-cd:setup-ci`

## Key Workflow

1. Detect project language and build system
2. Ask platform and deployment questions
3. Generate platform-specific configuration
4. Include linting, testing, building, deployment stages
5. Provide secrets setup instructions
6. Offer deployment strategy explanations

## Supported Platforms

- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI

## Features

- Multi-language support (Python, JavaScript, Go, Java)
- Multiple deployment strategies (blue-green, canary, rolling)
- Caching and parallelization optimization
- Security and secret management guidance
- Comprehensive stage organization

## Dependencies

- **Blocked by**: plugin-ci-cd (plugin definition)
- **Related**: skill-ci-cd-guidance, plugin-testing
