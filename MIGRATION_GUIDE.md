# CodeFlow Monorepo Migration Guide

This guide provides step-by-step instructions for migrating CodeFlow repositories into a single monorepo.

## 1. Preparation

- List all repositories to migrate.
- Define the target directory for each repo in the monorepo.
- Reserve `engine/` as the canonical home for the Python engine project.

## 2. Import Repositories

- Use `git subtree` or `git filter-repo` to import each repo, preserving history.
- Example (using git subtree):

```bash
git remote add codeflow-desktop <repo-url>
git fetch codeflow-desktop

git subtree add --prefix=desktop codeflow-desktop master --squash
```

- Repeat for each repository.

### Imported in this repository

- `codeflow-engine` -> `engine/`
- `codeflow-desktop` -> `desktop/`
- `codeflow-website` -> `website/`
- `codeflow-orchestration` -> `orchestration/`
- `codeflow-vscode-extension` -> `vscode-extension/`

## 3. Resolve Conflicts

- Deduplicate files and resolve naming conflicts.
- Update import paths and dependencies as needed.
- Reconcile duplicate root files such as `README.md`, `LICENSE`, `CONTRIBUTING.md`, and CI workflows.
- Keep component-local documentation inside each imported directory until shared standards are finalized.
- Move engine-specific build files under `engine/` and update workflows to use path-aware working directories.

## 4. Centralize CI/CD

- Move CI/CD workflows to `.github/workflows/`.
- Set up component-aware builds for:
  - root engine (Python)
  - `desktop/`
  - `website/`
  - `orchestration/packages/@codeflow/utils`
  - `vscode-extension/`

## 5. Update Documentation

- Update `README.md` and docs to reflect new structure.
- Document onboarding and contribution guidelines.
- Explicitly document which parts of the repository still retain their pre-monorepo layout.
- Add archive/redirect instructions for the old split repositories.

## 6. Deprecate Old Repositories

- Archive or mark old repositories as read-only.
- Update each legacy repository README to point contributors to this monorepo.

## 7. Announce Migration

- Communicate changes to contributors and users.
- Publish a follow-up plan for workspace tooling standardization.

---

For questions, see MIGRATION_PLAN.md or contact the maintainers.
