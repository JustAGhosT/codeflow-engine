# CodeFlow Monorepo Migration Plan

This document tracks the migration of all CodeFlow-related repositories into a unified monorepo structure.

## Structure

- engine/           # Python core engine project
- desktop/          # Electron/Tauri app
- vscode-extension/ # VS Code extension
- website/          # Docs/marketing
- orchestration/    # Infra, bootstrap, and shared orchestration assets
- templates/        # Workflow templates
- tools/            # Dev tools/scripts
- tests/            # Unified test suite for engine
- docs/             # Shared documentation

## Current Status

Completed:

1. Added monorepo migration scaffolding and shared documentation.
2. Imported `codeflow-desktop` into `desktop/`.
3. Imported `codeflow-website` into `website/`.
4. Imported `codeflow-orchestration` into `orchestration/`.
5. Imported `codeflow-vscode-extension` into `vscode-extension/`.

Pending:

1. Normalize dependency management across Python and Node-based projects.
2. Add path-aware CI and release automation.
3. Consolidate duplicate docs, licenses, and contribution guidance.
4. Complete archive and redirect steps for the former split repositories.

## Migration Steps

1. Import code from each repo, preserving git history.
2. Resolve conflicts and update imports.
3. Centralize CI/CD workflows.
4. Update documentation and onboarding.
5. Deprecate old repositories.
6. Announce migration and monitor feedback.

---

For detailed instructions, see MIGRATION_GUIDE.md.
