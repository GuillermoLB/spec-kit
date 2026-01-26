# Skill: CI/CD Best Practices Guidance

**Status**: Draft
**Owner**: DevTools Team
**Last Updated**: 2026-01-25
**Priority**: High

## Purpose

Auto-triggered skill providing CI/CD pipeline patterns and best practices.

## Key Topics

1. **Pipeline Architecture** - Stage organization, job dependencies, conditional execution
2. **Platform-Specific Guidance** - GitHub Actions, GitLab CI, Jenkins, CircleCI
3. **Best Practices** - Fail-fast, caching, parallelization, artifact management
4. **Deployment Strategies** - Blue-green, canary, rolling deployments
5. **Security in Pipelines** - Secret management, credential handling, access control
6. **Performance Optimization** - Build caching, Docker layer caching, test parallelization
7. **Troubleshooting** - Debugging failed builds, timeout issues, permission errors

## Trigger Conditions

When developers work with pipeline configs, CI/CD platforms, or ask about deployment.

## Dependencies

- **Blocked by**: plugin-ci-cd (plugin definition)
- **Related**: command-setup-ci
