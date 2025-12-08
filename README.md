# CodeFlow Orchestration

Central repository for deploying and managing the entire CodeFlow stack.

## Overview

This repository provides orchestration scripts and workflows to deploy, manage, and coordinate all CodeFlow components across the 6 separate repositories.

## Repository Structure

```
codeflow-orchestration/
├── scripts/
│   ├── deploy-all.ps1          # Deploy entire stack (PowerShell)
│   ├── deploy-all.sh            # Deploy entire stack (Bash)
│   ├── setup-dev-environment.ps1 # Setup local development environment
│   └── update-all-repos.sh      # Update all repositories
├── docs/
│   ├── DEPLOYMENT.md            # Full stack deployment guide
│   ├── ARCHITECTURE.md          # System architecture overview
│   └── TROUBLESHOOTING.md       # Common issues and solutions
├── .github/
│   └── workflows/
│       ├── deploy-stack.yml     # CI/CD for full stack deployment
│       └── validate-stack.yml  # Validate all components
└── README.md                    # This file
```

## Quick Start

### Prerequisites

- Azure CLI (`az`) - logged in and configured
- GitHub CLI (`gh`) - for managing secrets
- PowerShell 7+ (for Windows) or Bash (for Linux/Mac)
- Node.js 18+ (for website and desktop)
- Python 3.12+ (for engine)
- Docker (for container builds)

### Deploy Entire Stack

**PowerShell (Windows):**
```powershell
.\scripts\deploy-all.ps1 `
  -OrgCode nl `
  -Environment dev `
  -Project codeflow `
  -RegionShort san `
  -Location southafricanorth `
  -SubscriptionId <your-subscription-id>
```

**Bash (Linux/Mac):**
```bash
./scripts/deploy-all.sh \
  --org-code nl \
  --environment dev \
  --project codeflow \
  --region-short san \
  --location southafricanorth \
  --subscription-id <your-subscription-id>
```

## Deployment Order

The orchestration script deploys components in the following order:

1. **Azure Infrastructure Bootstrap** (`codeflow-azure-setup`)
   - Creates resource group, storage, Log Analytics, App Insights
   - Optionally creates Key Vault

2. **Core Infrastructure** (`codeflow-infrastructure`)
   - Deploys Container Apps environment
   - Creates PostgreSQL database
   - Creates Redis cache
   - Sets up networking and security

3. **CodeFlow Engine** (`codeflow-engine`)
   - Builds and pushes container image
   - Deploys to Container Apps
   - Configures environment variables

4. **Website** (`codeflow-website`)
   - Builds Next.js application
   - Deploys to Azure Static Web Apps

5. **Desktop App** (`codeflow-desktop`)
   - Builds Tauri application
   - Creates release artifacts

6. **VS Code Extension** (`codeflow-vscode-extension`)
   - Builds extension package
   - Creates VSIX file

## Component Repositories

- **[codeflow-azure-setup](https://github.com/JustAGhosT/codeflow-azure-setup)** - Azure bootstrap scripts
- **[codeflow-infrastructure](https://github.com/JustAGhosT/codeflow-infrastructure)** - Production infrastructure (Bicep/Terraform)
- **[codeflow-engine](https://github.com/JustAGhosT/codeflow-engine)** - Core Python engine
- **[codeflow-website](https://github.com/JustAGhosT/codeflow-website)** - Marketing website (Next.js)
- **[codeflow-desktop](https://github.com/JustAGhosT/codeflow-desktop)** - Desktop application (Tauri/React)
- **[codeflow-vscode-extension](https://github.com/JustAGhosT/codeflow-vscode-extension)** - VS Code extension

## Development Workflow

### Local Development Setup

```powershell
.\scripts\setup-dev-environment.ps1
```

This script will:
- Clone all component repositories (if not already present)
- Install dependencies for each component
- Set up local development environment
- Configure inter-component communication

### Update All Repositories

```bash
./scripts/update-all-repos.sh
```

Pulls latest changes from all component repositories.

## CI/CD

The `.github/workflows/deploy-stack.yml` workflow can:
- Deploy the entire stack on demand
- Deploy specific components
- Validate all components before deployment
- Rollback on failure

## Documentation

- [Full Deployment Guide](docs/DEPLOYMENT.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## License

MIT

