# CodeFlow Orchestration

This repository contains orchestration scripts, documentation, infrastructure-as-code, and planning for the CodeFlow project.

> Canonical source: [orchestration](orchestration) in the CodeFlow monorepo.
> Legacy split repo: [JustAGhosT/codeflow-orchestration](https://github.com/JustAGhosT/codeflow-orchestration)

---

## Overview

The CodeFlow Orchestration repository serves as the central hub for:

- **Infrastructure as Code** - Production Azure infrastructure (Bicep, Terraform, Kubernetes)
- **Azure Bootstrap** - Generic reusable Azure environment setup scripts
- **Cross-repository Coordination** - Version management, migration, and deployment
- **Comprehensive Documentation** - Guides, policies, and references

---

## Repository Structure

```
codeflow-orchestration/
├── infrastructure/              # Production Infrastructure (from codeflow-infrastructure)
│   ├── bicep/                  # Azure Bicep templates
│   ├── terraform/              # Terraform configurations
│   ├── kubernetes/             # Kubernetes manifests
│   ├── docker/                 # Docker development environment
│   └── scripts/                # Deployment & monitoring scripts
├── bootstrap/                   # Generic Azure Bootstrap (from codeflow-azure-setup)
│   └── scripts/                # Reusable Azure setup scripts
├── packages/                    # Shared utility packages
│   ├── @codeflow/utils/        # TypeScript utilities (npm)
│   └── codeflow-utils-python/  # Python utilities (PyPI)
├── scripts/                     # Orchestration scripts
│   ├── check-versions.ps1
│   ├── bump-version.ps1
│   ├── sync-versions.ps1
│   └── dev-setup.ps1
└── docs/                        # Documentation
```

---

## Quick Links

### Infrastructure

- [Infrastructure Overview](./infrastructure/README.md) - Production infrastructure guide
- [Bicep Deployment](./infrastructure/bicep/README.md) - Azure Bicep deployment
- [Kubernetes Setup](./infrastructure/kubernetes/) - K8s manifests
- [Docker Development](./infrastructure/docker/docker-compose.yml) - Local development

### Bootstrap (Generic Azure Setup)

- [Bootstrap Scripts](./bootstrap/README.md) - Reusable Azure environment setup

### Migration Documentation

- [Migration Overview](./MIGRATION.md) - Complete migration status and progress (72% complete)
- [Migration Analysis](./MIGRATION_ANALYSIS.md) - Comprehensive analysis, mistakes, and improvements
- [Migration Phases](./MIGRATION_PHASES.md) - Detailed phase descriptions and goals
- [Wave 4 Execution Plan](./WAVE4_EXECUTION_PLAN.md) - Optimization & Enhancement (in progress)
- [Infrastructure Consolidation Plan](./docs/INFRASTRUCTURE_CONSOLIDATION_PLAN.md) - Consolidation migration plan
- [Documentation Index](./docs/README.md) - Central index for all documentation

### Key Documentation

- [Versioning Policy](./docs/VERSIONING_POLICY.md) - Semantic versioning strategy
- [Release Process](./docs/RELEASE_PROCESS.md) - Release automation and process
- [Dependency Management](./docs/DEPENDENCY_MANAGEMENT.md) - Dependency update process
- [Monitoring & Observability](./docs/MONITORING_OBSERVABILITY.md) - Monitoring strategy
- [Full Stack Deployment](./docs/FULL_STACK_DEPLOYMENT.md) - Complete deployment guide
- [Shared Libraries Plan](./docs/SHARED_LIBRARIES_PLAN.md) - Wave 4: Shared libraries strategy
- [Optimization Plan](./docs/OPTIMIZATION_PLAN.md) - Wave 4: Performance and cost optimization
- [Package Publishing Guide](./docs/PACKAGE_PUBLISHING_GUIDE.md) - Publishing shared utility packages
- [Deployment Automation](./docs/DEPLOYMENT_AUTOMATION.md) - Enhanced deployment with rollback and health checks

---

## Migration Progress

### Overall: 72% Complete

| Wave | Status | Progress |
|------|--------|----------|
| Wave 1: Critical Foundation | Complete | 95% |
| Wave 2: Quality & Documentation | Complete | 92% |
| Wave 3: Operations & Infrastructure | Complete | 90% |
| Wave 4: Optimization & Enhancement | In Progress | 65% |

---

## Infrastructure

The `infrastructure/` directory contains production-ready Azure infrastructure definitions:

### Bicep Templates (Recommended)
- `codeflow-engine.bicep` - Container Apps, PostgreSQL, Redis
- `website.bicep` - Static Web Apps
- `main.bicep` - Legacy AKS infrastructure

### Terraform (Alternative)
- Cloud-agnostic infrastructure definitions
- State stored in Azure Blob Storage

### Kubernetes
- Deployment manifests for AKS clusters
- Service, ConfigMap, and Kustomize configs

### Docker
- `docker-compose.yml` - Full local development stack
- Includes PostgreSQL, Redis, Prometheus, Grafana

### Deploy Infrastructure

```bash
# Deploy CodeFlow Engine to Azure
cd infrastructure/bicep
bash deploy-codeflow-engine.sh prod san eastus2

# Or use Terraform
cd infrastructure/terraform
terraform init
terraform apply
```

---

## Bootstrap (Generic Azure Setup)

The `bootstrap/` directory contains generic, reusable Azure environment setup scripts:

### Available Scripts

| Script | Purpose |
|--------|---------|
| `New-AzRepoEnvironment.ps1` | Create core Azure resources (RG, Storage, Log Analytics, App Insights) |
| `New-AzRepoFullEnvironment.ps1` | Full environment with App Service, Container Apps, Managed Identity |
| `Set-GitHubSecretsFromJson.ps1` | Configure GitHub secrets from Azure output |

### Usage

```powershell
# Create basic environment
./bootstrap/scripts/New-AzRepoEnvironment.ps1 `
    -OrgCode "nl" `
    -Environment "dev" `
    -Project "myproject" `
    -RegionShort "san" `
    -Location "southafricanorth"

# Set GitHub secrets
./bootstrap/scripts/Set-GitHubSecretsFromJson.ps1 `
    -JsonPath "./environment.json" `
    -Repo "owner/repo"
```

---

## Orchestration Scripts

### Version Management

```bash
# Check versions across all repos
pwsh scripts/check-versions.ps1

# Bump version in a repo
pwsh scripts/bump-version.ps1 -Type minor

# Sync versions across repos
pwsh scripts/sync-versions.ps1 -Version "1.2.0"
```

### Migration

```bash
# Migrate AutoPR to CodeFlow (dry run)
pwsh scripts/migrate-autopr-to-codeflow.ps1 -DryRun

# Migrate AutoPR to CodeFlow (execute)
pwsh scripts/migrate-autopr-to-codeflow.ps1
```

### Development

```bash
# Set up local development environment
pwsh scripts/dev-setup.ps1
# Or bash version
bash scripts/dev-setup.sh
```

---

## Shared Packages

### TypeScript (@codeflow/utils)

```bash
npm install @codeflow/utils
```

Provides:
- Date/time formatting utilities
- Number formatting utilities
- String formatting utilities
- URL validation

### Python (codeflow-utils-python)

```bash
pip install codeflow-utils-python
```

Provides:
- Error handling utilities
- Retry decorators
- Rate limiting
- Validation helpers

---

## Related Repositories

- [codeflow-engine](https://github.com/JustAGhosT/codeflow-engine) - Core engine (Python, FastAPI)
- [codeflow-desktop](https://github.com/JustAGhosT/codeflow-desktop) - Desktop application (Tauri, React)
- [codeflow-vscode-extension](https://github.com/JustAGhosT/codeflow-vscode-extension) - VS Code extension
- [codeflow-website](https://github.com/JustAGhosT/codeflow-website) - Marketing website (Next.js)

### Archived Repositories

The following repositories have been merged into this one:
- ~~codeflow-infrastructure~~ → `./infrastructure/`
- ~~codeflow-azure-setup~~ → `./bootstrap/`

---

## Getting Started

### For New Contributors

1. **Read the Documentation**
   - Start with [Migration Overview](./MIGRATION.md)
   - Review [Migration Phases](./MIGRATION_PHASES.md) for detailed information

2. **Set Up Local Environment**
   ```bash
   pwsh scripts/dev-setup.ps1
   ```

3. **Check Versions**
   ```bash
   pwsh scripts/check-versions.ps1
   ```

### For Infrastructure Engineers

1. **Review Infrastructure**
   - [Infrastructure README](./infrastructure/README.md)
   - [Bicep Deployment Guide](./infrastructure/bicep/README-CODEFLOW-ENGINE.md)

2. **Deploy**
   ```bash
   cd infrastructure/bicep
   bash deploy-codeflow-engine.sh dev san eastus2
   ```

### For Release Managers

1. **Review Release Process**
   - [Release Process](./docs/RELEASE_PROCESS.md)
   - [Release Coordination](./docs/RELEASE_COORDINATION.md)

2. **Use Version Scripts**
   ```bash
   pwsh scripts/bump-version.ps1 -Type minor
   pwsh scripts/sync-versions.ps1 -Version "1.2.0"
   ```

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

---

## Support

For questions or issues:
- GitHub Issues: [codeflow-orchestration/issues](https://github.com/JustAGhosT/codeflow-orchestration/issues)
- Documentation: See [docs/](./docs/) directory

---

## License

MIT License - See [LICENSE](./LICENSE) file for details.

---

**Last Updated:** 2025-01-XX
