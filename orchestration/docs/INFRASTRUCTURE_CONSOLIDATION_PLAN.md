# Infrastructure & Azure Consolidation Migration Plan

> **Version:** 1.0
> **Status:** Planning
> **Created:** 2025-01-XX
> **Estimated Effort:** 4 Phases, ~2-4 weeks of work

---

## Executive Summary

This document outlines a comprehensive plan to consolidate three repositories:
1. **codeflow-infrastructure** → INTO **codeflow-orchestration**
2. **codeflow-azure-setup** → INTO **codeflow-orchestration**
3. **Utility packages** → DISTRIBUTED to their target repositories

### Target State

```
codeflow-orchestration/          # Renamed or repurposed
├── infrastructure/              # From codeflow-infrastructure
│   ├── bicep/
│   ├── terraform/
│   ├── kubernetes/
│   └── docker/
├── bootstrap/                   # From codeflow-azure-setup
│   └── scripts/
├── packages/                    # Temporary - will be distributed
│   ├── @codeflow/utils/        # → codeflow-desktop (or standalone npm)
│   └── codeflow-utils-python/  # → codeflow-engine
├── scripts/                     # Orchestration scripts (kept)
└── docs/                        # Consolidated documentation
```

### Final Distribution

| Package/Component | Current Location | Target Location |
|-------------------|------------------|-----------------|
| `@codeflow/utils` (TypeScript) | orchestration | codeflow-desktop OR npm registry |
| `codeflow-utils-python` | orchestration | codeflow-engine |
| Version scripts | orchestration | KEEP in orchestration |
| Migration scripts | orchestration | KEEP in orchestration |
| Deploy scripts | orchestration | orchestration/infrastructure |
| Cost/monitoring scripts | orchestration | orchestration/infrastructure |
| Bicep templates | infrastructure | orchestration/infrastructure/bicep |
| Terraform templates | infrastructure | orchestration/infrastructure/terraform |
| K8s manifests | infrastructure | orchestration/infrastructure/kubernetes |
| Docker configs | infrastructure | orchestration/infrastructure/docker |
| Azure bootstrap scripts | azure-setup | orchestration/bootstrap |

---

## Phase 1: Merge codeflow-infrastructure into codeflow-orchestration

### 1.1 Pre-Merge Checklist

- [ ] Ensure all CI/CD workflows pass on infrastructure repo
- [ ] Document current infrastructure deployment state
- [ ] Backup any sensitive configuration
- [ ] Notify team of upcoming changes
- [ ] Freeze infrastructure changes during merge

### 1.2 Directory Structure Creation

Create the following structure in `codeflow-orchestration`:

```bash
# In codeflow-orchestration root
mkdir -p infrastructure/bicep
mkdir -p infrastructure/terraform
mkdir -p infrastructure/kubernetes
mkdir -p infrastructure/docker
mkdir -p infrastructure/.github/workflows
```

### 1.3 File Migration Map

| Source (infrastructure) | Destination (orchestration) |
|------------------------|----------------------------|
| `bicep/*` | `infrastructure/bicep/` |
| `terraform/*` | `infrastructure/terraform/` |
| `kubernetes/*` | `infrastructure/kubernetes/` |
| `docker/*` | `infrastructure/docker/` |
| `.github/workflows/deploy.yml` | `infrastructure/.github/workflows/deploy.yml` |
| `.github/workflows/validate-bicep.yml` | `infrastructure/.github/workflows/validate-bicep.yml` |
| `.github/workflows/validate-terraform.yml` | `infrastructure/.github/workflows/validate-terraform.yml` |
| `README.md` | `infrastructure/README.md` |
| `CONTRIBUTING.md` | Merge into root `CONTRIBUTING.md` |

### 1.4 Migration Commands

```bash
# Clone or navigate to orchestration repo
cd /workspace/repo-faeb9d53-9de5-4245-94d6-f3274bf05f92

# Create infrastructure directory structure
mkdir -p infrastructure/{bicep,terraform,kubernetes,docker}
mkdir -p infrastructure/.github/workflows

# Copy infrastructure files (preserving structure)
cp -r /workspace/repo-d2820966-92b3-4910-92b0-10b690b91f52/bicep/* infrastructure/bicep/
cp -r /workspace/repo-d2820966-92b3-4910-92b0-10b690b91f52/terraform/* infrastructure/terraform/
cp -r /workspace/repo-d2820966-92b3-4910-92b0-10b690b91f52/kubernetes/* infrastructure/kubernetes/
cp -r /workspace/repo-d2820966-92b3-4910-92b0-10b690b91f52/docker/* infrastructure/docker/
cp /workspace/repo-d2820966-92b3-4910-92b0-10b690b91f52/README.md infrastructure/README.md
cp /workspace/repo-d2820966-92b3-4910-92b0-10b690b91f52/.github/workflows/*.yml infrastructure/.github/workflows/

# Copy .gitignore entries
cat /workspace/repo-d2820966-92b3-4910-92b0-10b690b91f52/.gitignore >> .gitignore
```

### 1.5 Update Path References

Files requiring path updates after move:

| File | Changes Required |
|------|------------------|
| `infrastructure/bicep/deploy-codeflow-engine.sh` | Update relative paths to bicep files |
| `infrastructure/bicep/deploy-codeflow-engine.ps1` | Update relative paths to bicep files |
| `infrastructure/.github/workflows/deploy.yml` | Update working-directory to `infrastructure/bicep` |
| `infrastructure/.github/workflows/validate-bicep.yml` | Update glob paths: `infrastructure/bicep/**/*.bicep` |
| `infrastructure/.github/workflows/validate-terraform.yml` | Update working-directory to `infrastructure/terraform` |
| `infrastructure/docker/docker-compose.yml` | Update Dockerfile paths |

### 1.6 CI/CD Workflow Integration

Update the main `.github/workflows/validate.yml` to include infrastructure validation:

```yaml
# Add to existing validate.yml
infrastructure-validation:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    # Bicep validation
    - name: Validate Bicep templates
      run: |
        az bicep build --file infrastructure/bicep/codeflow-engine.bicep --no-restore
        az bicep build --file infrastructure/bicep/website.bicep --no-restore
        az bicep build --file infrastructure/bicep/main.bicep --no-restore

    # Terraform validation
    - name: Validate Terraform
      working-directory: infrastructure/terraform
      run: |
        terraform fmt -check
        terraform init -backend=false
        terraform validate
```

### 1.7 Documentation Updates

1. Update `infrastructure/README.md`:
   - Change repository references from `codeflow-infrastructure` to `codeflow-orchestration/infrastructure`
   - Update clone instructions
   - Update CI/CD badge URLs

2. Update root `README.md`:
   - Add Infrastructure section
   - Link to `infrastructure/README.md`

3. Create `infrastructure/MIGRATION_FROM_SEPARATE_REPO.md`:
   - Document the merge history
   - Provide redirect instructions for old URLs

---

## Phase 2: Merge codeflow-azure-setup into codeflow-orchestration

### 2.1 Pre-Merge Checklist

- [ ] Ensure all CI/CD workflows pass on azure-setup repo
- [ ] Document any active usage of bootstrap scripts
- [ ] Notify dependent teams

### 2.2 Directory Structure Creation

```bash
# In codeflow-orchestration root
mkdir -p bootstrap/scripts
mkdir -p bootstrap/.github/workflows
```

### 2.3 File Migration Map

| Source (azure-setup) | Destination (orchestration) |
|---------------------|----------------------------|
| `scripts/New-AzRepoEnvironment.ps1` | `bootstrap/scripts/` |
| `scripts/New-AzRepoFullEnvironment.ps1` | `bootstrap/scripts/` |
| `scripts/Set-GitHubSecretsFromJson.ps1` | `bootstrap/scripts/` |
| `scripts/README-AZURE-SETUP.md` | `bootstrap/README.md` |
| `.github/workflows/validate.yml` | `bootstrap/.github/workflows/validate.yml` |
| `.github/workflows/validate-powershell.yml` | Merge into main `validate.yml` |
| `README.md` | Reference in `bootstrap/README.md` |
| `CONTRIBUTING.md` | Merge into root `CONTRIBUTING.md` |

### 2.4 Migration Commands

```bash
cd /workspace/repo-faeb9d53-9de5-4245-94d6-f3274bf05f92

# Create bootstrap directory structure
mkdir -p bootstrap/scripts
mkdir -p bootstrap/.github/workflows

# Copy azure-setup files
cp /workspace/repo-e1ed708e-b805-49a1-99b0-a58daef256a1/scripts/*.ps1 bootstrap/scripts/
cp /workspace/repo-e1ed708e-b805-49a1-99b0-a58daef256a1/scripts/README-AZURE-SETUP.md bootstrap/README.md
cp /workspace/repo-e1ed708e-b805-49a1-99b0-a58daef256a1/.github/workflows/*.yml bootstrap/.github/workflows/

# Merge .gitignore entries (deduplicate)
cat /workspace/repo-e1ed708e-b805-49a1-99b0-a58daef256a1/.gitignore >> .gitignore
sort -u .gitignore -o .gitignore
```

### 2.5 Documentation Updates

1. Update `bootstrap/README.md`:
   - Add section explaining this is generic Azure bootstrap (not CodeFlow-specific)
   - Update relative paths to scripts
   - Add link back to main README

2. Update root `README.md`:
   - Add Bootstrap section
   - Clarify difference between `bootstrap/` (generic) and `infrastructure/` (CodeFlow-specific)

### 2.6 CI/CD Integration

Add PowerShell validation to main workflow:

```yaml
# Add to .github/workflows/validate.yml
bootstrap-validation:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - name: Install PSScriptAnalyzer
      shell: pwsh
      run: Install-Module -Name PSScriptAnalyzer -Force -Scope CurrentUser

    - name: Lint Bootstrap Scripts
      shell: pwsh
      run: |
        $scripts = Get-ChildItem -Path "bootstrap/scripts" -Filter "*.ps1"
        foreach ($script in $scripts) {
          Invoke-ScriptAnalyzer -Path $script.FullName -Severity Warning,Error
        }
```

---

## Phase 3: Distribute Utility Packages to Target Repositories

### 3.1 TypeScript Package (@codeflow/utils)

**Decision Required:** Choose one of the following:

#### Option A: Move to codeflow-desktop (Recommended if only desktop uses it)

```bash
# In codeflow-desktop
mkdir -p packages/utils
cp -r /workspace/repo-faeb9d53-9de5-4245-94d6-f3274bf05f92/packages/@codeflow/utils/* packages/utils/
```

Update `package.json` in desktop to use workspace reference:
```json
{
  "workspaces": ["packages/*"],
  "dependencies": {
    "@codeflow/utils": "workspace:*"
  }
}
```

#### Option B: Keep as Standalone NPM Package (Recommended if multiple repos use it)

Keep the package in orchestration but publish to npm registry:

```bash
# Publish to npm (after setting up npm authentication)
cd packages/@codeflow/utils
npm publish --access public
```

Then reference in dependent repos:
```json
{
  "dependencies": {
    "@codeflow/utils": "^0.1.0"
  }
}
```

### 3.2 Python Package (codeflow-utils-python)

**Target:** Move to `codeflow-engine`

```bash
# In codeflow-engine repository
mkdir -p packages/codeflow-utils

# Copy Python utils
cp -r /workspace/repo-faeb9d53-9de5-4245-94d6-f3274bf05f92/packages/codeflow-utils-python/* packages/codeflow-utils/

# Or as a local package in src/
cp -r /workspace/repo-faeb9d53-9de5-4245-94d6-f3274bf05f92/packages/codeflow-utils-python/codeflow_utils src/codeflow_utils
```

Update `pyproject.toml` in engine:
```toml
[tool.poetry.dependencies]
# If using as local package
codeflow-utils = { path = "packages/codeflow-utils", develop = true }

# Or if publishing to PyPI
codeflow-utils-python = "^0.1.0"
```

### 3.3 Migration Scripts Distribution

| Script Category | Current Location | Action |
|----------------|------------------|--------|
| `scripts/deploy-all.ps1` | orchestration | Move to `infrastructure/scripts/` |
| `scripts/deploy-all.sh` | orchestration | Move to `infrastructure/scripts/` |
| `scripts/health-check.ps1` | orchestration | Move to `infrastructure/scripts/` |
| `scripts/automation/*` | orchestration | Move to `infrastructure/scripts/automation/` |
| `scripts/cost/*` | orchestration | Move to `infrastructure/scripts/cost/` |
| `scripts/monitoring/*` | orchestration | Move to `infrastructure/scripts/monitoring/` |
| `scripts/performance/*` | orchestration | Move to `infrastructure/scripts/performance/` |
| `scripts/deployment/*` | orchestration | Move to `infrastructure/scripts/deployment/` |
| `scripts/check-versions.ps1` | orchestration | KEEP in `scripts/` |
| `scripts/bump-version.ps1` | orchestration | KEEP in `scripts/` |
| `scripts/sync-versions.ps1` | orchestration | KEEP in `scripts/` |
| `scripts/migrate-autopr-to-codeflow.ps1` | orchestration | KEEP in `scripts/` as a legacy compatibility migration utility |
| `scripts/dev-setup.ps1` | orchestration | KEEP in `scripts/` |
| `scripts/dev-setup.sh` | orchestration | KEEP in `scripts/` |

### 3.4 Script Relocation Commands

```bash
cd /workspace/repo-faeb9d53-9de5-4245-94d6-f3274bf05f92

# Create infrastructure scripts directory
mkdir -p infrastructure/scripts/{automation,cost,monitoring,performance,deployment}

# Move deployment-related scripts
mv scripts/deploy-all.ps1 infrastructure/scripts/
mv scripts/deploy-all.sh infrastructure/scripts/
mv scripts/health-check.ps1 infrastructure/scripts/

# Move categorized scripts
mv scripts/automation/* infrastructure/scripts/automation/
mv scripts/cost/* infrastructure/scripts/cost/
mv scripts/monitoring/* infrastructure/scripts/monitoring/
mv scripts/performance/* infrastructure/scripts/performance/
mv scripts/deployment/* infrastructure/scripts/deployment/

# Remove empty directories
rmdir scripts/automation scripts/cost scripts/monitoring scripts/performance scripts/deployment
```

---

## Phase 4: Cleanup and Archive Original Repositories

### 4.1 Update References Across All Repos

Update the following files in each CodeFlow repository:

| Repository | Files to Update |
|------------|-----------------|
| codeflow-engine | `README.md`, CI/CD workflows |
| codeflow-desktop | `README.md`, `package.json` |
| codeflow-vscode-extension | `README.md` |
| codeflow-website | `README.md`, deployment configs |
| codeflow-orchestration | All docs, README.md |

### 4.2 Archive codeflow-infrastructure

1. Add deprecation notice to README:

```markdown
# ⚠️ DEPRECATED - Repository Archived

This repository has been merged into [codeflow-orchestration](https://github.com/JustAGhosT/codeflow-orchestration).

## New Location

All infrastructure code is now at:
- **Bicep templates:** `codeflow-orchestration/infrastructure/bicep/`
- **Terraform:** `codeflow-orchestration/infrastructure/terraform/`
- **Kubernetes:** `codeflow-orchestration/infrastructure/kubernetes/`
- **Docker:** `codeflow-orchestration/infrastructure/docker/`

Please update your workflows and bookmarks accordingly.
```

2. Archive repository on GitHub:
   - Settings → General → Danger Zone → Archive this repository

### 4.3 Archive codeflow-azure-setup

1. Add deprecation notice to README:

```markdown
# ⚠️ DEPRECATED - Repository Archived

This repository has been merged into [codeflow-orchestration](https://github.com/JustAGhosT/codeflow-orchestration).

## New Location

All Azure bootstrap scripts are now at:
- **Scripts:** `codeflow-orchestration/bootstrap/scripts/`
- **Documentation:** `codeflow-orchestration/bootstrap/README.md`

Please update your workflows and bookmarks accordingly.
```

2. Archive repository on GitHub

### 4.4 Remove Packages Directory (After Distribution)

Once utility packages are distributed:

```bash
# After confirming packages are working in target repos
rm -rf packages/@codeflow
rm -rf packages/codeflow-utils-python
rmdir packages  # Only if empty
```

---

## Final Repository Structure

After all phases complete:

```
codeflow-orchestration/
├── .github/
│   └── workflows/
│       └── validate.yml           # Combined validation workflow
├── infrastructure/                 # ← From codeflow-infrastructure
│   ├── bicep/
│   │   ├── codeflow-engine.bicep
│   │   ├── website.bicep
│   │   ├── main.bicep
│   │   ├── deploy-*.sh
│   │   ├── deploy-*.ps1
│   │   ├── cleanup-*.sh
│   │   └── README.md
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   └── kustomization.yaml
│   ├── docker/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── nginx/
│   │   ├── postgres/
│   │   ├── redis/
│   │   ├── prometheus/
│   │   └── grafana/
│   ├── scripts/
│   │   ├── deploy-all.ps1
│   │   ├── deploy-all.sh
│   │   ├── health-check.ps1
│   │   ├── automation/
│   │   ├── cost/
│   │   ├── monitoring/
│   │   ├── performance/
│   │   └── deployment/
│   ├── .github/workflows/
│   │   ├── deploy.yml
│   │   ├── validate-bicep.yml
│   │   └── validate-terraform.yml
│   └── README.md
├── bootstrap/                      # ← From codeflow-azure-setup
│   ├── scripts/
│   │   ├── New-AzRepoEnvironment.ps1
│   │   ├── New-AzRepoFullEnvironment.ps1
│   │   └── Set-GitHubSecretsFromJson.ps1
│   ├── .github/workflows/
│   │   └── validate.yml
│   └── README.md
├── scripts/                        # Orchestration scripts (kept)
│   ├── check-versions.ps1
│   ├── bump-version.ps1
│   ├── sync-versions.ps1
│   ├── migrate-autopr-to-codeflow.ps1  # Legacy compatibility migration utility
│   ├── dev-setup.ps1
│   ├── dev-setup.sh
│   └── setup-package-publishing.ps1
├── docs/                           # All documentation
│   ├── README.md
│   ├── VERSIONING_POLICY.md
│   ├── RELEASE_PROCESS.md
│   ├── ... (existing docs)
│   └── INFRASTRUCTURE_CONSOLIDATION_PLAN.md  # This file
├── MIGRATION.md
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## Migration Checklist

### Phase 1: Infrastructure Merge
- [ ] Create directory structure
- [ ] Copy Bicep templates
- [ ] Copy Terraform templates
- [ ] Copy Kubernetes manifests
- [ ] Copy Docker configurations
- [ ] Copy CI/CD workflows
- [ ] Update path references in scripts
- [ ] Update CI/CD workflow paths
- [ ] Update documentation
- [ ] Test Bicep validation
- [ ] Test Terraform validation
- [ ] Test Docker Compose works

### Phase 2: Azure-Setup Merge
- [ ] Create bootstrap directory
- [ ] Copy PowerShell scripts
- [ ] Copy documentation
- [ ] Copy CI/CD workflows
- [ ] Update documentation
- [ ] Test PowerShell validation

### Phase 3: Package Distribution
- [ ] Decide on TypeScript package location
- [ ] Move/publish TypeScript package
- [ ] Move Python package to engine
- [ ] Update dependent repos' dependencies
- [ ] Test packages work in new locations
- [ ] Relocate infrastructure scripts
- [ ] Update script references in docs

### Phase 4: Cleanup
- [ ] Update all cross-repo references
- [ ] Add deprecation notices to old repos
- [ ] Archive codeflow-infrastructure
- [ ] Archive codeflow-azure-setup
- [ ] Remove packages directory (if empty)
- [ ] Final documentation review
- [ ] Announce changes to team

---

## Rollback Plan

If migration causes issues:

1. **Phase 1 Rollback:** Delete `infrastructure/` directory, revert to using `codeflow-infrastructure` repo
2. **Phase 2 Rollback:** Delete `bootstrap/` directory, revert to using `codeflow-azure-setup` repo
3. **Phase 3 Rollback:** Restore `packages/` from git history, revert dependent repo changes
4. **Phase 4 Rollback:** Unarchive original repositories, remove deprecation notices

---

## Benefits of This Consolidation

1. **Single source of truth** for all infrastructure and orchestration
2. **Simplified CI/CD** - one repo to manage all deployment automation
3. **Better discoverability** - contributors find everything in one place
4. **Consistent naming** - unified naming conventions across infra and bootstrap
5. **Reduced context switching** - DevOps work happens in one repo
6. **Cleaner ecosystem** - 7 repos → 5 repos (33% reduction)
7. **Clear separation** - bootstrap (generic) vs infrastructure (CodeFlow-specific) vs orchestration (cross-repo)

---

## Post-Migration Documentation

After migration, update the main README.md to reflect the new structure:

```markdown
## Repository Structure

This repository contains three main areas:

### 1. Infrastructure (`/infrastructure`)
Production infrastructure-as-code for CodeFlow, including:
- Azure Bicep templates
- Terraform configurations
- Kubernetes manifests
- Docker development environment

### 2. Bootstrap (`/bootstrap`)
Generic Azure environment bootstrap scripts (reusable across projects):
- Resource group creation
- Storage and monitoring setup
- GitHub secrets configuration

### 3. Orchestration (`/scripts`, `/docs`)
Cross-repository coordination and documentation:
- Version management scripts
- Migration automation
- Comprehensive documentation
```

---

**Document Owner:** Infrastructure Team
**Last Updated:** 2025-01-XX
**Review Frequency:** After each phase completion
