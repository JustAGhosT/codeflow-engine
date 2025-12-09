# Migration History Preservation Decision

## Decision: Fresh Start Approach

For this migration, we are using a **fresh start** approach for all repositories:

- **Option Selected**: Fresh start with new initial commits
- **Rationale**: 
  - Cleaner separation between repositories
  - Avoids complexity of git filter-repo/subtree split
  - Each repo starts with a clean history focused on its purpose
  - Original monorepo history preserved via tag `legacy-codeflow-monorepo-final`

## History Preservation by Repository

| Repository | Strategy | Notes |
|------------|----------|-------|
| `codeflow-azure-setup` | Fresh start | New scripts, minimal history needed |
| `codeflow-infrastructure` | Fresh start | IaC files, clean history preferred |
| `codeflow-engine` | Fresh start | Core engine, clean slate for new structure |
| `codeflow-desktop` | Fresh start | Desktop app, independent history |
| `codeflow-vscode-extension` | Fresh start | Extension, independent history |
| `codeflow-website` | Fresh start | Marketing site, independent history |

## Accessing Original History

To access the original monorepo history:

```bash
git checkout legacy-codeflow-monorepo-final
```

Or view the tag:
```bash
git show legacy-codeflow-monorepo-final
```

## Migration Date

Migration completed: 2025-01-XX

