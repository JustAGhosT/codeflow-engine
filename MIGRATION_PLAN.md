# CodeFlow Monorepo Migration Plan

This document tracks the migration of all CodeFlow-related repositories into a unified
monorepo structure. The decision to consolidate is recorded in
[docs/adr/0021-repository-structure.md](docs/adr/0021-repository-structure.md).

## Structure

```
engine/            # Python core engine project
desktop/           # Tauri + React desktop application
vscode-extension/  # VS Code extension
website/           # Next.js marketing and documentation site
orchestration/     # Azure IaC, bootstrap scripts, and shared utility packages
docs/              # Shared project documentation
tools/             # Shared development tooling and helper scripts
```

## Current Status

### Phase 1 — Code Consolidation ✅ Complete

1. Added monorepo migration scaffolding and shared documentation.
2. Imported `codeflow-desktop` into `desktop/`.
3. Imported `codeflow-website` into `website/`.
4. Imported `codeflow-orchestration` into `orchestration/`.
5. Imported `codeflow-vscode-extension` into `vscode-extension/`.
6. Added path-aware CI workflow (`.github/workflows/monorepo-ci.yml`).
7. Added archive and redirect guidance (`docs/LEGACY_REPO_REDIRECTS.md`).
8. Finalised repository structure decision (ADR-0021 accepted).

### Phase 2 — Tooling Standardisation ⏳ In Progress

1. Normalise dependency management across Python and Node.js projects.
2. Add path-aware release automation for each component.
3. Consolidate duplicate `README`, `LICENSE`, and `CONTRIBUTING` files.
4. Archive legacy split repositories and update their READMEs to redirect here.

## Future Extraction Candidates

The following components *could* be extracted to separate repositories in future if
specific conditions are met (see ADR-0021 for full rationale):

| Component | Condition for extraction |
|---|---|
| `website/` | Content team needs write access without engine write access |
| `orchestration/bootstrap/` | A shared `justaghost/*` or `phoenixvc/*` infra repo is created |

No extraction is recommended at this stage.

## Migration Steps (Reference)

1. Import code from each repo, preserving git history (`git subtree`).
2. Resolve conflicts and update imports.
3. Centralise CI/CD workflows with path-aware filtering.
4. Update documentation and onboarding.
5. Archive legacy split repositories.
6. Announce migration and monitor feedback.

---

For detailed instructions, see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md).
