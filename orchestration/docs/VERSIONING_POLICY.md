# CodeFlow Versioning Policy

This document defines the versioning strategy for all CodeFlow repositories.

---

## Semantic Versioning

All CodeFlow repositories use [Semantic Versioning (SemVer)](https://semver.org/) with the format:

```
MAJOR.MINOR.PATCH
```

### Version Components

- **MAJOR** (X.0.0): Breaking changes that are not backward compatible
- **MINOR** (0.X.0): New features that are backward compatible
- **PATCH** (0.0.X): Bug fixes that are backward compatible

---

## Versioning Rules

### MAJOR Version Increment

Increment MAJOR version when:
- API changes break backward compatibility
- Database schema changes require migration
- Configuration format changes
- Dependencies are upgraded with breaking changes
- Command-line interface changes
- Environment variable changes

**Examples:**
- Removing an API endpoint
- Changing API request/response format
- Removing a configuration option
- Changing database schema without migration path

### MINOR Version Increment

Increment MINOR version when:
- New features are added
- New API endpoints are added
- New configuration options are added
- New environment variables are added
- Dependencies are upgraded with new features
- Performance improvements

**Examples:**
- Adding a new API endpoint
- Adding a new configuration option
- Adding support for a new integration
- Adding a new command-line option

### PATCH Version Increment

Increment PATCH version when:
- Bug fixes are applied
- Security patches are applied
- Documentation updates
- Code refactoring (no behavior change)
- Dependency patches (bug fixes only)

**Examples:**
- Fixing a bug in existing functionality
- Fixing a security vulnerability
- Updating documentation
- Code cleanup and refactoring

---

## Pre-release Versions

### Release Candidates

Use `-rc.N` suffix for release candidates:

```
1.2.0-rc.1
1.2.0-rc.2
```

### Beta Versions

Use `-beta.N` suffix for beta versions:

```
1.2.0-beta.1
1.2.0-beta.2
```

### Alpha Versions

Use `-alpha.N` suffix for alpha versions:

```
1.2.0-alpha.1
1.2.0-alpha.2
```

---

## Version Format

### Standard Format

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

**Examples:**
- `1.0.0` - Initial release
- `1.0.1` - Patch release
- `1.1.0` - Minor release
- `2.0.0` - Major release
- `1.2.0-rc.1` - Release candidate
- `1.2.0-beta.1` - Beta version
- `1.2.0-alpha.1` - Alpha version

---

## Repository-Specific Versioning

### codeflow-engine (Python)

- **Location:** `pyproject.toml`
- **Format:** `version = "1.0.1"`
- **Current Version:** Check `pyproject.toml`

### codeflow-desktop (Node.js/Tauri)

- **Location:** `package.json`
- **Format:** `"version": "1.0.0"`
- **Current Version:** Check `package.json`

### codeflow-vscode-extension (Node.js)

- **Location:** `package.json`
- **Format:** `"version": "1.0.0"`
- **Current Version:** Check `package.json`

### codeflow-website (Node.js/Next.js)

- **Location:** `package.json`
- **Format:** `"version": "1.0.0"`
- **Current Version:** Check `package.json`

### codeflow-infrastructure (Bicep)

- **Location:** Parameter files or `version.json`
- **Format:** `"version": "1.0.0"`
- **Current Version:** Check parameter files

### codeflow-azure-setup (PowerShell)

- **Location:** Script header comments or `VERSION.txt`
- **Format:** `# Version: 1.0.0`
- **Current Version:** Check script headers

### codeflow-orchestration (Documentation)

- **Location:** `VERSION.txt` or `package.json` (if applicable)
- **Format:** `1.0.0`
- **Current Version:** Check `VERSION.txt`

---

## Version Synchronization

### Cross-Repo Versioning

For coordinated monorepo prereleases:
- Shipped products should share the same release version
- Internal helper packages may follow independently or remain private
- Use component-prefixed tags to identify which product is being released

**Example:**
- codeflow-engine: `0.2.0-alpha.1`
- codeflow-desktop: `0.2.0-alpha.1`
- codeflow-vscode-extension: `0.2.0-alpha.1`
- codeflow-website: `0.2.0-alpha.1`

### Independent Versioning

For independent releases:
- Each repo can version independently
- Document version compatibility matrix
- Update dependency versions accordingly

---

## Version Bumping Process

### Automated Bumping

Use version bump scripts:
- `scripts/bump-version.sh` (Bash)
- `scripts/bump-version.ps1` (PowerShell)

### Manual Bumping

1. Update version in appropriate file
2. Update CHANGELOG.md
3. Commit changes
4. Create git tag
5. Push tag

---

## Git Tags

### Tag Format

```
<component>-vMAJOR.MINOR.PATCH[-PRERELEASE]
```

**Examples:**
- `engine-v0.2.0-alpha.1`
- `desktop-v0.2.0-alpha.1`
- `website-v0.2.0-alpha.1`
- `vscode-extension-v0.2.0-alpha.1`

### Tag Creation

```bash
# Create tag
git tag -a engine-v0.2.0-alpha.1 -m "Release engine 0.2.0-alpha.1"

# Push tag
git push origin engine-v0.2.0-alpha.1
```

---

## Version Validation

### CI/CD Validation

Version validation checks:
- Format is valid (MAJOR.MINOR.PATCH)
- Version is incremented from previous
- Tag matches version
- CHANGELOG.md is updated

### Pre-release Validation

- Version format is correct
- Pre-release suffix is valid
- Build metadata is valid (if used)

---

## Breaking Change Detection

### Criteria for Breaking Changes

1. **API Changes:**
   - Removed endpoints
   - Changed request/response formats
   - Changed authentication

2. **Configuration Changes:**
   - Removed configuration options
   - Changed configuration format
   - Changed default values

3. **Database Changes:**
   - Schema changes without migration
   - Data format changes

4. **Dependency Changes:**
   - Upgraded dependencies with breaking changes
   - Removed dependencies

---

## Version Compatibility

### Compatibility Matrix

Document version compatibility:
- Which versions work together
- Minimum required versions
- Recommended versions

### Deprecation Policy

- Deprecate features in MINOR version
- Remove deprecated features in next MAJOR version
- Provide migration guides

---

## Release Notes

### Format

- **Breaking Changes:** List all breaking changes
- **New Features:** List all new features
- **Bug Fixes:** List all bug fixes
- **Security:** List security fixes
- **Dependencies:** List dependency updates

---

## Examples

### Example 1: Bug Fix

**Before:** `1.0.0`  
**After:** `1.0.1`  
**Reason:** Fixed bug in PR processing

### Example 2: New Feature

**Before:** `1.0.1`  
**After:** `1.1.0`  
**Reason:** Added new integration with Linear

### Example 3: Breaking Change

**Before:** `1.1.0`  
**After:** `2.0.0`  
**Reason:** Changed API authentication format

---

## Additional Resources

- [Semantic Versioning Specification](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Version Bump Scripts](../scripts/)

---

## Support

For versioning questions:
- GitHub Issues: [codeflow-orchestration/issues](https://github.com/JustAGhosT/codeflow-orchestration/issues)
- Documentation: This policy document

