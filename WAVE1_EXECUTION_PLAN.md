# Wave 1 Execution Plan: Critical Foundation

## Overview

Wave 1 focuses on fixing critical issues and establishing the foundation for all future work.

**Duration:** Week 2-3  
**Phases:** 1, 2, 3

---

## Wave 1 Phases

### Phase 1: Critical Fixes & Security (Week 2, Days 1-3)
**Priority:** CRITICAL

#### 1.1 Security Fixes
- [ ] Remove credentials from git history (all repos)
- [ ] Add `.credentials-*.json` to `.gitignore` (all repos)
- [ ] Add `deployment-output.json` to `.gitignore`
- [ ] Implement Azure Key Vault integration
- [ ] Remove hardcoded passwords
- [ ] Add security scanning to CI/CD

#### 1.2 Fix Deployment Scripts
- [ ] Fix `deploy-codeflow-engine.ps1` structure
- [ ] Add PowerShell linting (PSScriptAnalyzer)
- [ ] Add script validation tests
- [ ] Improve error handling
- [ ] Add rollback capabilities
- [ ] Document script structure

#### 1.3 Fix Critical Bugs
- [ ] Verify certificate creation logic
- [ ] Fix database name inconsistencies
- [ ] Fix environment variable naming
- [ ] Verify all Bicep templates compile
- [ ] Test all deployment scripts end-to-end

**Success Criteria:**
- Zero credentials in git
- All scripts pass linting
- All deployments succeed
- Security scan passes

---

### Phase 2: Naming Consistency & Branding (Week 2, Days 4-5)
**Priority:** HIGH

#### 2.1 Package & Command Names
- [ ] Update `codeflow-engine/pyproject.toml`:
  - [ ] `CodeFlow` â†’ `codeflow`
  - [ ] `codeflow-server` â†’ `codeflow-server`
  - [ ] `codeflow-worker` â†’ `codeflow-worker`
  - [ ] Update entry points `codeflow.*` â†’ `codeflow.*`
- [ ] Update `codeflow-vscode-extension/package.json`:
  - [ ] All `codeflow.*` commands â†’ `codeflow.*`
  - [ ] Update configuration keys
- [ ] Update all internal code references

#### 2.2 Documentation Updates
- [ ] Update all README files
- [ ] Update code comments
- [ ] Update error messages
- [ ] Update log messages
- [ ] Update API documentation

#### 2.3 Database & Configuration
- [ ] Standardize database names to `codeflow`
- [ ] Update all environment variables
- [ ] Update configuration files
- [ ] Update connection strings

#### 2.4 Create Migration Script
- [ ] Create automated search/replace script
- [ ] Test on one repo first
- [ ] Apply to all repos
- [ ] Verify no broken references

**Success Criteria:**
- Zero "CodeFlow" references
- All commands use `codeflow.*`
- All packages named consistently

---

### Phase 3: Basic CI/CD Foundation (Week 3)
**Priority:** HIGH

#### 3.1 Core CI/CD Workflows
- [ ] **codeflow-engine:**
  - [ ] Build workflow (Poetry)
  - [ ] Test workflow (pytest)
  - [ ] Lint workflow (ruff, mypy)
  - [ ] Security scan workflow
- [ ] **codeflow-desktop:**
  - [ ] Build workflow (npm + Tauri)
  - [ ] Test workflow
  - [ ] Lint workflow
- [ ] **codeflow-vscode-extension:**
  - [ ] Build workflow (npm)
  - [ ] Test workflow
  - [ ] Package workflow (.vsix)
  - [ ] Release workflow
- [ ] **codeflow-website:**
  - [ ] Build workflow (Next.js)
  - [ ] Test workflow
  - [ ] Lint workflow
  - [ ] Deploy workflow (Azure Static Web Apps)
- [ ] **codeflow-infrastructure:**
  - [ ] Bicep validation workflow
  - [ ] Terraform validation workflow
  - [ ] Deployment workflow (manual trigger)
- [ ] **codeflow-azure-setup:**
  - [ ] PowerShell validation workflow
  - [ ] Script testing workflow
- [ ] **codeflow-orchestration:**
  - [ ] Validation workflow
  - [ ] Deployment workflow

#### 3.2 Shared Workflow Templates
- [ ] Create reusable workflow templates
- [ ] Standardize workflow structure
- [ ] Add common steps (checkout, setup, cache)

#### 3.3 Basic Testing
- [ ] Add unit tests where missing
- [ ] Add build verification tests
- [ ] Add smoke tests for deployments

**Success Criteria:**
- All repos have working CI/CD
- All builds pass
- All tests pass
- Deployments automated

---

## Execution Strategy

### Day-by-Day Plan

**Week 2:**
- **Day 1:** Phase 1.1 (Security fixes)
- **Day 2:** Phase 1.2 (Deployment scripts)
- **Day 3:** Phase 1.3 (Critical bugs) + Phase 2.1 start
- **Day 4:** Phase 2.1-2.2 (Naming consistency)
- **Day 5:** Phase 2.3-2.4 (Database/config + migration script)

**Week 3:**
- **Day 1:** Phase 3.1 (CI/CD workflows - engine, desktop)
- **Day 2:** Phase 3.1 (CI/CD workflows - extension, website)
- **Day 3:** Phase 3.1 (CI/CD workflows - infrastructure, setup, orchestration)
- **Day 4:** Phase 3.2 (Shared workflow templates)
- **Day 5:** Phase 3.3 (Basic testing) + Wave 1 review

---

## Dependencies

- **Phase 1** must complete before Phase 2 (security first)
- **Phase 2** can start after Phase 1.1 (security fixes)
- **Phase 3** depends on Phase 1.2 (script fixes)
- All phases can be worked on in parallel where possible

---

## Risk Mitigation

1. **Test in one repo first** before applying to all
2. **Create backups** before major changes
3. **Use feature branches** for all changes
4. **Have rollback plans** for each phase
5. **Review after each phase** before proceeding

---

## Success Metrics

- **Security:** Zero credentials in git, security scan passes
- **Naming:** Zero "CodeFlow" references, all commands consistent
- **CI/CD:** All repos have working workflows, all builds pass
- **Quality:** All scripts linted, all tests pass

---

## Next Steps After Wave 1

1. **Review Wave 1** completion
2. **Plan Wave 2** (Documentation & Testing)
3. **Celebrate** foundation completion! ðŸŽ‰

