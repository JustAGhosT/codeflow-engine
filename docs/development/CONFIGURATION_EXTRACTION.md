# Configuration and Template Extraction

This document describes the systematic extraction and organization of embedded JSON and YAML
configurations from the CodeFlow engine codebase into a clean, maintainable directory structure.

## Overview

All embedded JSON and YAML configuration data has been extracted from Python files and organized
into two main directories:

- `configs/` - Reusable configuration files for platforms, packages, workflows, and triggers
- `templates/` - File generation templates for builds, deployments, testing, and monitoring

## Directory Structure

### Configs/ (Reusable Configuration Files)

````text
configs/
â”œâ”€â”€ README.md                    # Configuration directory overview
â”œâ”€â”€ platforms/                  # Platform-specific configurations
â”‚   â”œâ”€â”€ replit.json             # Replit platform config
â”‚   â”œâ”€â”€ lovable.json            # Lovable.dev platform config
â”‚   â”œâ”€â”€ bolt.json               # Bolt.new platform config
â”‚   â”œâ”€â”€ same.json               # Same.new platform config
â”‚   â””â”€â”€ emergent.json           # Emergent.sh platform config
â”œâ”€â”€ packages/                   # Package dependency configurations
â”‚   â”œâ”€â”€ security.json           # Security-related packages
â”‚   â”œâ”€â”€ testing.json            # Testing framework packages
â”‚   â”œâ”€â”€ performance.json        # Performance optimization packages
â”‚   â”œâ”€â”€ development.json        # Development tool packages
â”‚   â””â”€â”€ monitoring.json         # Monitoring and logging packages
â”œâ”€â”€ workflows/                  # Workflow YAML files (21 files)
â”‚   â”œâ”€â”€ phase1_pr_review_workflow.yaml
â”‚   â”œâ”€â”€ phase2-rapid-prototyping.yaml
â”‚   â”œâ”€â”€ magic-fix.yaml
â”‚   â”œâ”€â”€ automated_dependency_update.yaml
â”‚   â”œâ”€â”€ branch_cleanup.yaml
â”‚   â”œâ”€â”€ changelog_updater.yaml
â”‚   â”œâ”€â”€ dead_code_report.yaml
â”‚   â”œâ”€â”€ enhanced_pr_comment_handler.yaml
â”‚   â”œâ”€â”€ onboard_contributor.yaml
â”‚   â”œâ”€â”€ pr_comment_handler.yaml
â”‚   â”œâ”€â”€ pr_size_labeler.yaml
â”‚   â”œâ”€â”€ quality_gate.yaml
â”‚   â”œâ”€â”€ release_drafter.yaml
â”‚   â”œâ”€â”€ scaffold_component_workflow.yaml
â”‚   â”œâ”€â”€ screenshot_gallery.yaml
â”‚   â”œâ”€â”€ security_audit.yaml
â”‚   â”œâ”€â”€ stale_issue_closer.yaml
â”‚   â”œâ”€â”€ tech_debt_report.yaml
â”‚   â”œâ”€â”€ update_documentation.yaml
â”‚   â””â”€â”€ ...
â””â”€â”€ triggers/                   # Trigger configurations
    â””â”€â”€ main-triggers.yaml      # Main workflow triggers

```text

### templates/ (File Generation Templates)

``` text
templates/
â”œâ”€â”€ README.md                   # Template directory overview
â”œâ”€â”€ typescript/                # TypeScript configuration templates
â”‚   â”œâ”€â”€ react-tsconfig.json    # React TypeScript config
â”‚   â”œâ”€â”€ vite-tsconfig.json     # Vite TypeScript config
â”‚   â””â”€â”€ basic-tsconfig.json    # Basic TypeScript config
â”œâ”€â”€ build/                     # Build configuration templates
â”‚   â”œâ”€â”€ vite.config.js         # Vite build configuration
â”‚   â”œâ”€â”€ vitest.config.js       # Vitest testing configuration
â”‚   â”œâ”€â”€ next.config.js         # Next.js configuration
â”‚   â””â”€â”€ pm2.config.js          # PM2 process manager config
â”œâ”€â”€ docker/                    # Dockerfile templates
â”‚   â”œâ”€â”€ react.dockerfile       # React application Dockerfile
â”‚   â”œâ”€â”€ node.dockerfile        # Node.js application Dockerfile
â”‚   â””â”€â”€ generic.dockerfile     # Generic application Dockerfile
â”œâ”€â”€ testing/                   # Testing setup templates
â”‚   â”œâ”€â”€ test-setup.js          # Common test setup
â”‚   â”œâ”€â”€ jest.config.js         # Jest configuration
â”‚   â”œâ”€â”€ setupTests.ts          # React testing setup
â”‚   â”œâ”€â”€ App.test.tsx           # Sample React test
â”‚   â””â”€â”€ playwright.config.ts   # Playwright E2E config
â”œâ”€â”€ deployment/                # Deployment configuration templates
â”‚   â”œâ”€â”€ azure-static-web-app.json  # Azure Static Web Apps config
â”‚   â””â”€â”€ github-actions-test.yml    # GitHub Actions test workflow
â””â”€â”€ monitoring/                # Monitoring and backup scripts
    â”œâ”€â”€ health-check.sh        # Health check script
    â”œâ”€â”€ monitor.sh             # System monitoring script
    â”œâ”€â”€ backup.sh              # Backup script
    â””â”€â”€ restore.sh             # Restore script
````

## Extraction Sources

### Python Files Processed

1. **file_generators.py** (873 lines) - Contains JSON templates for TypeScript configs, Dockerfiles,
   deployment configs, monitoring and backup scripts
2. **enhancement_strategies.py** (548 lines) - Contains build configs (Vite, Vitest), PM2 process
   manager config, and other template strings
3. **platform_configs.py** (572 lines) - Contains platform definitions, package dependency lists,
   deployment configurations, and production checklists

### YAML Files Organized

- **22 workflow YAML files** moved from `CodeFlow/workflows/` to `configs/workflows/`
- **triggers.yaml** moved to `configs/triggers/main-triggers.yaml`

## Benefits Achieved

### Maintainability

- **Clear separation** between configuration data and business logic
- **Organized structure** with logical grouping of related files
- **Easy to find** and modify specific configurations
- **Version control friendly** with individual files for each configuration

### Reusability

- **Platform configurations** can be reused across different enhancement strategies
- **Package dependencies** organized by category for easy selection
- **Template files** can be used independently or combined
- **Workflow configurations** can be shared and customized

### Extensibility

- **Easy to add** new platforms by creating new JSON files in `configs/platforms/`
- **Simple to extend** package categories in `configs/packages/`
- **Straightforward** to add new templates in appropriate `templates/` subdirectories
- **Clear pattern** for adding new workflow configurations

### Developer Experience

- **IDE support** with proper JSON/YAML syntax highlighting and validation
- **Documentation** embedded in README files for each directory
- **Consistent structure** makes it easy to understand and navigate
- **Type safety** maintained through structured JSON schemas

## Next Steps

1. **Refactor Python modules** to load configurations from files instead of embedded literals
2. **Add configuration validation** to ensure loaded configs match expected schemas
3. **Create utility functions** for loading and caching configuration files
4. **Add unit tests** to verify correct loading and usage of externalized configs
5. **Update documentation** to reflect the new configuration management approach

## Usage Examples

### Loading Platform Configuration

```python
import json
from pathlib import Path

def load_platform_config(platform_name: str) -> dict:
    config_path = Path(f"configs/platforms/{platform_name}.json")
    with open(config_path, 'r') as f:
        return json.load(f)

# Usage
replit_config = load_platform_config("replit")
```

### Loading Package Dependencies

```python
def load_package_dependencies(category: str) -> dict:
    config_path = Path(f"configs/packages/{category}.json")
    with open(config_path, 'r') as f:
        return json.load(f)

# Usage
security_packages = load_package_dependencies("security")
```

### Loading Templates

```python
def load_template(category: str, template_name: str) -> str:
    template_path = Path(f"templates/{category}/{template_name}")
    with open(template_path, 'r') as f:
        return f.read()

# Usage
dockerfile_content = load_template("docker", "react.dockerfile")
tsconfig_content = load_template("typescript", "react-tsconfig.json")
```

This extraction significantly improves the maintainability, reusability, and clarity of
configuration management in the CodeFlow engine while preserving all original functionality.
