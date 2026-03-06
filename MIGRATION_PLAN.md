# CodeFlow Monorepo Migration Plan

This document tracks the migration of all CodeFlow-related repositories into a unified monorepo structure.

## Structure

- engine/           # Python core
- desktop/          # Electron/Tauri app
- vscode-extension/ # VS Code extension
- website/          # Docs/marketing
- infrastructure/   # K8s, Terraform, Docker
- templates/        # Workflow templates
- tools/            # Dev tools/scripts
- tests/            # Unified test suite
- docs/             # Documentation

## Migration Steps

1. Import code from each repo, preserving git history.
2. Resolve conflicts and update imports.
3. Centralize CI/CD workflows.
4. Update documentation and onboarding.
5. Deprecate old repositories.
6. Announce migration and monitor feedback.

---

For detailed instructions, see MIGRATION_GUIDE.md.
