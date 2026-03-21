# 21. Repository Structure: Monorepo vs Multi-Repo Decision

## Status

Accepted

## Date

2025-12-08

## Updated

2026-03-21

## Context

The CodeFlow project grew to span multiple distinct concerns across several archived
`codeflow-*` repositories under the `JustAGhosT` GitHub organization:

| Repository | Status before migration |
|---|---|
| `codeflow-engine` | Active (this repo) |
| `codeflow-orchestration` | Archived |
| `codeflow-infrastructure` | Archived |
| `codeflow-desktop` | Archived |
| `codeflow-azure-setup` | Archived |
| `codeflow-website` | Archived |
| `codeflow-vscode-extension` | Archived |

The discussion ([GitHub Issue #21](https://github.com/JustAGhosT/codeflow-engine/issues/21))
asked two related questions:

1. Should the `codeflow-*` repositories be reintegrated into a monorepo?
2. How do the `codeflow-*` repositories fit into the broader `phoenixvc/*` and
   `justaghost/*` ecosystem?

This ADR records the decision made and the reasoning behind it.

---

## Component Summary

Before deciding on structure, the components were analysed for purpose and coupling:

| Component | Type | Direct code deps |
|---|---|---|
| `engine/` | Python library + service | None (only external APIs) |
| `desktop/` | Tauri + React app | `engine/` via HTTP/WebSocket sidecar only |
| `vscode-extension/` | VS Code extension (TypeScript) | `engine/` via HTTP REST only |
| `website/` | Next.js marketing/docs site | None (fully standalone) |
| `orchestration/` | Azure IaC + shared utility packages | None |

Key observation: `desktop/` and `vscode-extension/` communicate with `engine/` through
well-defined API contracts, not direct imports. They are **loosely coupled at the code
level** and can be built, released, and deployed independently.

---

## Options Evaluated

### Option 1 — Keep monorepo with path-aware CI ✅ (Chosen)

Consolidate all `codeflow-*` repositories into this repo; use path filters in CI so
only the affected component builds on each change.

**Pros:**
- Archived repos need no ongoing maintenance in isolation.
- Atomic cross-component changes remain easy (e.g. API shape change + client update in
  one PR).
- Single source of truth for linting configs, licences, and contribution guides.
- Path-aware CI (`dorny/paths-filter`) eliminates the full-build penalty.
- Small team; cross-repo coordination overhead is not justified.

**Cons:**
- Larger clone size (mitigated by sparse checkout or shallow clone).
- Granular per-component access control is not possible (not a current requirement).

### Option 2 — Split into 3–4 focused repositories

Extract engine, UI clients, infrastructure, and templates into separate repos.

**Pros:** Independent release cycles, focused pipelines, smaller clones.

**Cons:**
- The component repos were already archived; re-splitting re-creates maintenance burden.
- Cross-repo version coordination is non-trivial for a small team.
- No immediate access-control requirement justifies the overhead.

### Option 3 — Full microrepo (one repo per component)

Maximum independence but maximum coordination overhead. Not appropriate for the team
size.

---

## Decision

**Consolidate all `codeflow-*` repositories into this monorepo (Option 1).**

All formerly separate repositories have been imported with git history preserved:

| Legacy repository | Monorepo path |
|---|---|
| `codeflow-engine` | `engine/` |
| `codeflow-desktop` | `desktop/` |
| `codeflow-website` | `website/` |
| `codeflow-orchestration` | `orchestration/` |
| `codeflow-vscode-extension` | `vscode-extension/` |

The canonical layout is:

```
codeflow-engine/
├── engine/            # Python core package (codeflow_engine)
├── desktop/           # Tauri + React desktop application
├── vscode-extension/  # VS Code extension
├── website/           # Next.js marketing and documentation site
├── orchestration/     # Azure IaC, bootstrap scripts, shared utility packages
├── docs/              # Shared project documentation and ADRs
└── tools/             # Shared development tooling and helper scripts
```

---

## Was the Monorepo the Right Decision?

Short answer: **yes, for the current stage of the project**.

### Rationale

1. **Most component repos were already archived.** Re-splitting means creating and
   maintaining new repos for code that was intentionally deprioritised.
2. **Loose API coupling means monorepo risk is low.** Because `desktop/` and
   `vscode-extension/` integrate with `engine/` through HTTP/WebSocket APIs and not
   direct imports, independent release cadences are preserved even inside the same repo.
3. **Path-aware CI eliminates the main monorepo penalty.** The
   `.github/workflows/monorepo-ci.yml` workflow uses `dorny/paths-filter` so only
   the changed component's jobs run.
4. **Small team; cross-repo overhead is a real cost.** Version matrix management,
   cross-repo PR coordination, and duplicated tooling configs are disproportionately
   costly.
5. **History is preserved.** `git subtree` imports keep blame and history intact
   without requiring any git tricks at development time.

### What Could Reasonably Be Extracted Later

The decision is **correct now** but two components warrant review as the project scales:

#### `website/` — borderline case

- The marketing/docs site has **zero code dependencies** on the engine or any other
  component. It is a fully standalone Next.js application.
- It could be extracted to a dedicated repo (e.g. `codeflow-website`) if:
  - A content team without engine write access needs to contribute, or
  - The deployment cadence diverges significantly from the engine.
- **Recommendation:** Keep in the monorepo for now. If contributor access-control
  needs arise, extract at that point.

#### `orchestration/bootstrap/` — generic Azure tooling

- The PowerShell scripts in `orchestration/bootstrap/` are deliberately generic (they
  create Azure resource groups, storage accounts, and Log Analytics workspaces for
  any project).
- If a shared `justaghost/*` or `phoenixvc/*` infrastructure repo is established,
  these scripts are good candidates to contribute upstream.
- **Recommendation:** Keep here until a target shared repo exists. Do not extract
  speculatively.

---

## Ecosystem Fit: `phoenixvc/*` and `justaghost/*`

As of this decision there are **no code-level references** to `phoenixvc` anywhere in
this repository. The CodeFlow components relate to the broader organisation ecosystem
as follows:

| Component | Role in the ecosystem |
|---|---|
| `engine/` | Authoritative backend for AI-powered PR automation; exposed as both a PyPI package and a self-hosted service. Any `justaghost/*` or `phoenixvc/*` project can consume it as a dependency. |
| `desktop/` | Local developer tooling for managing CodeFlow without a browser. Targets individual developers and small teams; no org-specific coupling. |
| `vscode-extension/` | IDE integration surface; publishes to the VS Code Marketplace. Usable by any developer regardless of org. |
| `website/` | Public-facing marketing and documentation. Not org-specific in content. |
| `orchestration/` | Azure IaC and bootstrap tooling for CodeFlow deployments. The generic bootstrap scripts could serve as a template for other `justaghost/*` or `phoenixvc/*` projects that run on Azure. |

### Integration path if a shared org repo is created

If a `justaghost/shared-infra` or `phoenixvc/platform-bootstrap` repository is
created in future, the recommended migration is:

1. Extract `orchestration/bootstrap/` scripts to the shared repo.
2. Extract the generic utility packages (`@codeflow/utils`,
   `codeflow-utils-python`) if other org projects will reuse them.
3. Keep CodeFlow-specific IaC (`orchestration/infrastructure/`) here.

No extraction is warranted until a concrete target repo exists.

---

## Implementation Status

### Completed

- All `codeflow-*` repositories imported with git history preserved.
- Path-aware monorepo CI workflow (`.github/workflows/monorepo-ci.yml`).
- Shared documentation under `docs/`.
- Archive and redirect guidance in `docs/LEGACY_REPO_REDIRECTS.md`.
- Migration documentation in `MIGRATION_PLAN.md` and `MIGRATION_GUIDE.md`.

### Remaining Work

1. Normalise dependency management across Python and Node.js components.
2. Add path-aware release automation for each component.
3. Consolidate duplicate `README`, `LICENSE`, and `CONTRIBUTING` files.
4. Archive legacy split repositories and update their READMEs to redirect here.

---

## Consequences

### Positive

- Single clone gives a contributor everything they need.
- Atomic cross-component changes require only one PR.
- Linting, formatting, and CI standards are enforced centrally.
- No ongoing maintenance of multiple archived repositories.

### Negative

- Repository clone size is larger than any individual component (mitigated by sparse
  checkout or shallow clone).
- Granular per-component access control is not possible inside GitHub's permission
  model (not a current requirement).

---

## Related Decisions

- [ADR-0019: Python-Only Architecture](0019-python-only-architecture.md)
- [ADR-0020: Package Naming Convention](0020-package-naming.md)
- [ADR-0012: Deployment Strategy](0012-deployment-strategy.md)
- [ADR-0015: Testing Strategy](0015-testing-strategy.md)

## References

- Monorepo vs Multi-Repo: <https://monorepo.tools/>
- Google's Monorepo Experience: <https://cacm.acm.org/magazines/2016/7/204032-why-google-stores-billions-of-lines-of-code-in-a-single-repository/>
- Migration Plan: [MIGRATION_PLAN.md](../../MIGRATION_PLAN.md)
- Legacy Redirects: [docs/LEGACY_REPO_REDIRECTS.md](../LEGACY_REPO_REDIRECTS.md)
