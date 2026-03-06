# Legacy Repository Redirects

Use this checklist when archiving the split repositories after the monorepo cutover.

## Archive Settings Links

- [codeflow-desktop settings](https://github.com/JustAGhosT/codeflow-desktop/settings)
- [codeflow-website settings](https://github.com/JustAGhosT/codeflow-website/settings)
- [codeflow-orchestration settings](https://github.com/JustAGhosT/codeflow-orchestration/settings)
- [codeflow-vscode-extension settings](https://github.com/JustAGhosT/codeflow-vscode-extension/settings)

GitHub does not expose a separate public archive URL. Use each repository's Settings page and archive it from the Danger Zone.

## Suggested Redirect README

```md
# Repository Archived

This repository has moved into the CodeFlow monorepo.

- Canonical repository: https://github.com/JustAGhosT/codeflow-engine
- Component path: https://github.com/JustAGhosT/codeflow-engine/tree/master/<component>

This split repository is now read-only and kept only for historical reference.
```

## Component Paths

- Desktop: [monorepo desktop path](https://github.com/JustAGhosT/codeflow-engine/tree/master/desktop)
- Website: [monorepo website path](https://github.com/JustAGhosT/codeflow-engine/tree/master/website)
- Orchestration: [monorepo orchestration path](https://github.com/JustAGhosT/codeflow-engine/tree/master/orchestration)
- VS Code extension: [monorepo VS Code extension path](https://github.com/JustAGhosT/codeflow-engine/tree/master/vscode-extension)
- Engine: [monorepo engine path](https://github.com/JustAGhosT/codeflow-engine/tree/master/engine)