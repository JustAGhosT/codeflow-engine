# GitHub Workflows

This directory contains the GitHub Actions workflows for the CodeFlow monorepo.

## Workflow Architecture

The monorepo uses a combination of engine-specific workflows, path-aware component workflows, and release workflows.

### Workflow Overview

| Workflow                          | Purpose                                                                                    | Triggers                     |
| --------------------------------- | ------------------------------------------------------------------------------------------ | ---------------------------- |
| `ci.yml`                          | Engine test and build validation                                                           | Push, PR, manual             |
| `lint.yml`                        | Engine lint and type checks                                                                | Push, PR                     |
| `security.yml`                    | Engine dependency and filesystem security checks                                           | Push, PR, schedule           |
| `monorepo-ci.yml`                 | Path-aware builds for engine, desktop, website, orchestration utils, and VS Code extension | Push, PR, manual             |
| `release.yml`                     | Engine package release                                                                     | Tags, manual                 |
| `release-desktop.yml`             | Desktop release build                                                                      | Tags, manual                 |
| `release-website.yml`             | Website release build                                                                      | Tags, manual                 |
| `release-vscode-extension.yml`    | VS Code extension release packaging                                                        | Tags, manual                 |
| `release-orchestration-utils.yml` | Shared utility package release build                                                       | Tags, manual                 |
| `deploy-autopr-engine.yml`        | Engine container build and Azure deployment                                                | Push to `master`, PR, manual |

## Workflow Details

### Key conventions

- Engine workflows run from [engine](engine) via `working-directory`.
- Component workflows use path filters so unrelated changes do not trigger full builds.
- Release workflows use component-specific tag prefixes such as `engine-v0.2.0-alpha.1` and `desktop-v0.2.0-alpha.1`.
- Infrastructure for the website and engine is sourced from [orchestration](orchestration).
- The engine deployment workflow still uses the filename [deploy-autopr-engine.yml](.github/workflows/deploy-autopr-engine.yml) for backward compatibility, but it deploys the current CodeFlow Engine.

### Archival follow-up

Before archiving the legacy repositories, update their README files with the redirect snippets from [docs/LEGACY_REPO_REDIRECTS.md](docs/LEGACY_REPO_REDIRECTS.md).

### Execution Order

1. **PR Created/Updated:**
   - `PR-Checks` runs immediately (fast validation)
   - `Quality Feedback` runs (detailed feedback)
   - `CI` runs (comprehensive checks)

2. **Push to master:**
   - `CI` runs with full volume settings

3. **Manual/Scheduled:**
   - `BG-Fix` runs for maintenance

### Volume Integration

All workflows respect the CODEFLOW volume system:

```bash
# Repository variables (set in GitHub settings)
CODEFLOW_VOLUME_PR=100      # PR volume
CODEFLOW_VOLUME_CHECKIN=50  # Push volume
CODEFLOW_VOLUME_DEV=200     # Development volume
```

### Status Badges

Add these badges to your README:

```markdown
![CI](https://github.com/owner/repo/workflows/CI/badge.svg)
![Quality](https://github.com/owner/repo/workflows/Quality%20Feedback/badge.svg)
![PR Checks](https://github.com/owner/repo/workflows/PR%20Checks/badge.svg)
```

## Troubleshooting

### Common Issues

**Workflow not running:**

- Check branch protection rules
- Verify workflow file syntax
- Check repository permissions

**Volume-based execution issues:**

- Verify repository variables are set
- Check volume calculation logic
- Review conditional job logic

**Pre-commit failures:**

- Run `pre-commit install` locally
- Check `.pre-commit-config.yaml` syntax
- Verify hook dependencies

**Codecov warnings ("Please install the 'codecov app svg image'"):**

- Install the Codecov GitHub App: https://github.com/apps/codecov
- Grant access to your repository in the app settings
- Ensure `CODECOV_TOKEN` secret is set in repository settings
- See `codecov.yml` in the repository root for configuration

### Debugging

**Enable debug logging:**

```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

**Check workflow runs:**

- Go to Actions tab in GitHub
- Select specific workflow
- Review logs for errors

## Contributing

### Adding New Workflows

1. **Define purpose:** What unique value does this workflow provide?
2. **Check overlap:** Ensure no redundancy with existing workflows
3. **Add documentation:** Update this README
4. **Test thoroughly:** Verify triggers and conditions

### Modifying Existing Workflows

1. **Update documentation:** Reflect changes in this README
2. **Test changes:** Use workflow dispatch for testing
3. **Consider impact:** How do changes affect other workflows?

### Best Practices

- **Keep workflows focused:** Each workflow should have a single, clear purpose
- **Use volume awareness:** Leverage the volume system for conditional execution
- **Provide feedback:** Always give clear feedback to contributors
- **Handle failures gracefully:** Use `continue-on-error` and `if: always()` appropriately
- **Optimize for speed:** Minimize redundant work and optimize execution time

## Configuration

### Repository Variables

Set these in GitHub repository settings:

| Variable                  | Description              | Default |
| ------------------------- | ------------------------ | ------- |
| `CODEFLOW_VOLUME_PR`      | Volume for pull requests | 100     |
| `CODEFLOW_VOLUME_CHECKIN` | Volume for pushes        | 50      |
| `CODEFLOW_VOLUME_DEV`     | Volume for development   | 200     |

### Environment Variables

| Variable                    | Description               | Default |
| --------------------------- | ------------------------- | ------- |
| `PYTHON_VERSION`            | Python version to use     | 3.13    |
| `CODEFLOW_PRECOMMIT_VOLUME` | Pre-commit volume         | 100     |
| `CODEFLOW_BG_BATCH`         | Background fix batch size | 30      |

## Support

For workflow issues:

1. Check this documentation
2. Review workflow logs
3. Create an issue with workflow name and error details
4. Tag with `workflow` label
