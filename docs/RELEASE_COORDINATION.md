# CodeFlow Release Coordination

This document describes the release coordination process for coordinated releases across multiple CodeFlow repositories.

---

## Release Calendar

### Regular Release Schedule

#### Patch Releases
- **Frequency:** As needed
- **Timing:** Immediate (bug fixes, security)
- **Coordination:** Minimal (single repo)

#### Minor Releases
- **Frequency:** Monthly
- **Timing:** First week of month
- **Coordination:** Moderate (2-3 repos)

#### Major Releases
- **Frequency:** Quarterly
- **Timing:** Beginning of quarter
- **Coordination:** High (all repos)

### Release Freeze Periods

- **End of Quarter:** No major releases
- **Holiday Periods:** Limited releases (emergency only)
- **Critical Bug Fixes:** Always allowed

---

## Release Coordination Process

### Step 1: Release Planning

#### Determine Release Scope
1. **Identify Components**
   - Which repos need updates
   - Dependencies between repos
   - Breaking changes

2. **Set Release Date**
   - Choose release date
   - Account for testing time
   - Consider freeze periods

3. **Assign Responsibilities**
   - Release manager
   - Component owners
   - QA team

### Step 2: Version Synchronization

#### Synchronize Versions
```bash
# Sync all repos to same MAJOR.MINOR version
pwsh scripts/sync-versions.ps1 -Version "1.2.0"
```

#### Version Compatibility Matrix
| Component | Version | Dependencies |
|-----------|---------|--------------|
| codeflow-engine | 1.2.0 | - |
| codeflow-desktop | 1.2.0 | engine >= 1.2.0 |
| codeflow-vscode-extension | 1.2.0 | engine >= 1.2.0 |
| codeflow-website | 1.2.0 | engine >= 1.2.0 |

### Step 3: Release Order

#### Recommended Release Order

1. **codeflow-engine** (Core)
   - Foundation for all other components
   - Release first
   - Wait for deployment

2. **codeflow-desktop** (Desktop App)
   - Depends on engine
   - Release after engine is stable
   - Update engine dependency

3. **codeflow-vscode-extension** (VS Code Extension)
   - Depends on engine
   - Release after engine is stable
   - Update engine dependency

4. **codeflow-website** (Website)
   - Depends on engine
   - Release after engine is stable
   - Update engine dependency

5. **codeflow-infrastructure** (Infrastructure)
   - May depend on engine
   - Release last
   - Update all dependencies

### Step 4: Dependency Updates

#### Update Dependencies
After each component release:

1. **Update Dependency Versions**
   ```json
   // package.json
   {
     "dependencies": {
       "codeflow-engine": "^1.2.0"
     }
   }
   ```

2. **Test Integration**
   - Test with new engine version
   - Verify compatibility
   - Run integration tests

3. **Release Dependent Component**
   - Bump version
   - Create release
   - Deploy

---

## Cross-Repo Dependency Tracking

### Dependency Matrix

| Component | Dependencies | Version Range |
|-----------|--------------|--------------|
| codeflow-engine | - | - |
| codeflow-desktop | codeflow-engine | >= 1.0.0 |
| codeflow-vscode-extension | codeflow-engine | >= 1.0.0 |
| codeflow-website | codeflow-engine | >= 1.0.0 |
| codeflow-infrastructure | codeflow-engine | >= 1.0.0 |

### Breaking Change Tracking

#### Breaking Change Process

1. **Identify Breaking Change**
   - Document in CHANGELOG.md
   - Create migration guide
   - Announce in release notes

2. **Update Dependent Components**
   - Update code
   - Update tests
   - Update documentation

3. **Coordinate Release**
   - Release engine first
   - Update dependencies
   - Release dependent components

---

## Release Checklist

### Pre-Release (1 Week Before)

- [ ] Release plan finalized
- [ ] Versions synchronized
- [ ] Dependencies updated
- [ ] Tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

### Release Day

- [ ] All components ready
- [ ] Release order confirmed
- [ ] Communication plan ready
- [ ] Rollback plan ready

### Release Process

- [ ] Release codeflow-engine
- [ ] Verify deployment
- [ ] Update dependencies
- [ ] Release codeflow-desktop
- [ ] Release codeflow-vscode-extension
- [ ] Release codeflow-website
- [ ] Release codeflow-infrastructure (if needed)

### Post-Release

- [ ] Verify all releases successful
- [ ] Monitor for issues
- [ ] Update documentation
- [ ] Announce release
- [ ] Gather feedback

---

## Communication Plan

### Internal Communication

1. **Release Announcement**
   - Slack/Teams channel
   - Email to team
   - Release notes

2. **Status Updates**
   - Progress updates
   - Issue notifications
   - Completion confirmation

### External Communication

1. **Release Notes**
   - GitHub releases
   - Blog post (if applicable)
   - Community announcements

2. **Breaking Changes**
   - Migration guides
   - Deprecation notices
   - Upgrade instructions

---

## Emergency Releases

### Critical Security Fixes

1. **Immediate Action**
   - Create hotfix branch
   - Apply fix
   - Bump PATCH version
   - Release immediately

2. **Coordination**
   - Notify team immediately
   - Release engine first
   - Update dependencies
   - Release dependent components

3. **Documentation**
   - Update CHANGELOG.md
   - Create security advisory
   - Notify users

---

## Release Rollback Plan

### Rollback Process

1. **Identify Issue**
   - Monitor for errors
   - Check logs
   - Verify issue

2. **Decision**
   - Assess severity
   - Determine rollback need
   - Notify team

3. **Rollback**
   - Revert to previous version
   - Update dependencies
   - Deploy previous version

4. **Post-Rollback**
   - Investigate issue
   - Fix in development
   - Plan re-release

---

## Release Metrics

### Track These Metrics

- **Release Frequency:** Releases per month
- **Release Success Rate:** Successful releases / Total releases
- **Time to Release:** Time from code complete to release
- **Rollback Rate:** Rollbacks / Total releases
- **Issue Rate:** Issues found post-release

---

## Additional Resources

- [Release Process](./RELEASE_PROCESS.md)
- [Versioning Policy](./VERSIONING_POLICY.md)
- [Dependency Management](./DEPENDENCY_MANAGEMENT.md)

---

## Support

For release coordination questions:
- GitHub Issues: [codeflow-orchestration/issues](https://github.com/JustAGhosT/codeflow-orchestration/issues)
- Documentation: This document

