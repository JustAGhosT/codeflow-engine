# CodeFlow Monorepo Migration Guide

This guide provides step-by-step instructions for migrating CodeFlow repositories into a single monorepo.

## 1. Preparation
- List all repositories to migrate.
- Define the target directory for each repo in the monorepo.

## 2. Import Repositories
- Use `git subtree` or `git filter-repo` to import each repo, preserving history.
- Example (using git subtree):

```
git remote add codeflow-desktop <repo-url>
git fetch codeflow-desktop

git subtree add --prefix=desktop codeflow-desktop master --squash
```

- Repeat for each repository.

## 3. Resolve Conflicts
- Deduplicate files and resolve naming conflicts.
- Update import paths and dependencies as needed.

## 4. Centralize CI/CD
- Move CI/CD workflows to `.github/workflows/`.
- Set up matrix builds for Python, Node.js, and infrastructure.

## 5. Update Documentation
- Update `README.md` and docs to reflect new structure.
- Document onboarding and contribution guidelines.

## 6. Deprecate Old Repositories
- Archive or mark old repositories as read-only.

## 7. Announce Migration
- Communicate changes to contributors and users.

---

For questions, see MIGRATION_PLAN.md or contact the maintainers.
