# CodeFlow Release Process

This document describes the release process for CodeFlow repositories.

---

## Release Types

### Major Release (X.0.0)
- Breaking changes
- Significant new features
- Architecture changes

### Minor Release (0.X.0)
- New features (backward compatible)
- New integrations
- Performance improvements

### Patch Release (0.0.X)
- Bug fixes
- Security patches
- Documentation updates

---

## Pre-Release Checklist

### Code Quality
- [ ] All tests pass
- [ ] Code coverage meets threshold (>80% for critical code)
- [ ] Linting passes
- [ ] Type checking passes
- [ ] Security scanning passes

### Documentation
- [ ] CHANGELOG.md updated
- [ ] README.md updated (if needed)
- [ ] API documentation updated (if needed)
- [ ] Migration guides created (for breaking changes)

### Version Management
- [ ] Version bumped in appropriate file
- [ ] Versions synchronized across repos (if coordinated release)
- [ ] Version format validated

### Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass (if applicable)
- [ ] Manual testing completed

---

## Release Process

### Step 1: Prepare Release

1. **Update CHANGELOG.md**
   ```markdown
   ## [1.2.0] - 2025-01-XX
   
   ### Added
   - New feature X
   - New integration Y
   
   ### Changed
   - Improved performance
   
   ### Fixed
   - Bug fix Z
   ```

2. **Bump Version**
   ```bash
   # Using bump-version script
   pwsh scripts/bump-version.ps1 -Type minor
   
   # Or manually update version in pyproject.toml or package.json
   ```

3. **Synchronize Versions** (if coordinated release)
   ```bash
   pwsh scripts/sync-versions.ps1 -Version "1.2.0"
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "chore: prepare release v1.2.0"
   git push
   ```

### Step 2: Create Release Branch (Optional)

For major releases, create a release branch:

```bash
git checkout -b release/v1.2.0
git push origin release/v1.2.0
```

### Step 3: Create Release Tag

```bash
# Create annotated tag
git tag -a v1.2.0 -m "Release version 1.2.0"

# Push tag
git push origin v1.2.0
```

### Step 4: GitHub Release

1. **Create GitHub Release**
   - Go to repository → Releases → Draft a new release
   - Tag: `v1.2.0`
   - Title: `Release v1.2.0`
   - Description: Copy from CHANGELOG.md

2. **Release Notes Format**
   ```markdown
   ## What's New
   
   ### Features
   - Feature X
   - Feature Y
   
   ### Improvements
   - Improvement A
   - Improvement B
   
   ### Bug Fixes
   - Fix C
   - Fix D
   
   ### Breaking Changes
   - Breaking change E (migration guide: [link])
   
   ## Full Changelog
   See [CHANGELOG.md](CHANGELOG.md) for full details.
   ```

3. **Attach Artifacts** (if applicable)
   - Build artifacts
   - Checksums
   - Installation packages

### Step 5: Post-Release

1. **Merge to Main** (if release branch used)
   ```bash
   git checkout main
   git merge release/v1.2.0
   git push origin main
   ```

2. **Update Documentation**
   - Update version in documentation
   - Update installation instructions
   - Update compatibility matrix

3. **Announce Release**
   - GitHub release notes
   - Blog post (if applicable)
   - Community announcements

---

## Automated Release Workflow

### GitHub Actions Release Workflow

The release workflow automates:
- Version validation
- Tag creation
- GitHub release creation
- Artifact building and upload

### Triggering Automated Release

1. **Create Release Tag**
   ```bash
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

2. **Workflow Runs Automatically**
   - Validates version
   - Builds artifacts
   - Creates GitHub release
   - Uploads artifacts

---

## Coordinated Releases

For releases across multiple repositories:

### Step 1: Plan Release

1. **Determine Release Version**
   - Use same MAJOR.MINOR version
   - PATCH versions can differ

2. **Check Dependencies**
   - Verify compatibility
   - Update dependency versions

### Step 2: Synchronize Versions

```bash
# Sync all repos to same version
pwsh scripts/sync-versions.ps1 -Version "1.2.0"
```

### Step 3: Release Order

1. **codeflow-engine** (core)
2. **codeflow-desktop** (depends on engine)
3. **codeflow-vscode-extension** (depends on engine)
4. **codeflow-website** (depends on engine)
5. **codeflow-infrastructure** (if needed)

### Step 4: Update Dependencies

After each release, update dependent repos:
- Update dependency versions
- Test integration
- Release dependent component

---

## Release Calendar

### Regular Releases

- **Patch Releases:** As needed (bug fixes, security)
- **Minor Releases:** Monthly (new features)
- **Major Releases:** Quarterly (breaking changes)

### Release Freeze Periods

- **End of Quarter:** No major releases
- **Holiday Periods:** Limited releases
- **Critical Bug Fixes:** Always allowed

---

## Emergency Releases

For critical security fixes:

1. **Immediate Action**
   - Create hotfix branch
   - Apply fix
   - Bump PATCH version
   - Release immediately

2. **Post-Release**
   - Update CHANGELOG.md
   - Create security advisory
   - Notify users

---

## Release Notes Template

```markdown
# Release v1.2.0

**Release Date:** YYYY-MM-DD

## Highlights

- Major feature X
- Performance improvement Y
- Security fix Z

## What's New

### Features
- Feature 1
- Feature 2

### Improvements
- Improvement 1
- Improvement 2

### Bug Fixes
- Fix 1
- Fix 2

### Breaking Changes
- Breaking change 1 (see [migration guide](link))

## Installation

[Installation instructions]

## Upgrade Guide

[Upgrade instructions]

## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for full details.

## Contributors

Thank you to all contributors!
```

---

## Additional Resources

- [Versioning Policy](./VERSIONING_POLICY.md)
- [CHANGELOG.md Template](./CHANGELOG_TEMPLATE.md)
- [Release Checklist](./RELEASE_CHECKLIST.md)

---

## Support

For release questions:
- GitHub Issues: [codeflow-orchestration/issues](https://github.com/JustAGhosT/codeflow-orchestration/issues)
- Documentation: This document

