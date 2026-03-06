# CodeFlow Monorepo

This repository now serves as the consolidated home for the CodeFlow ecosystem. The original Python engine remains at the repository root, while the additional product repositories have been imported with full Git history into dedicated subdirectories.

## Monorepo Layout

- `codeflow_engine/` - Core Python engine package
- `desktop/` - Tauri + React desktop application
- `website/` - Next.js marketing and documentation website
- `orchestration/` - Shared infrastructure, bootstrap assets, and release orchestration
- `vscode-extension/` - VS Code extension
- `docs/` - Shared project documentation
- `templates/` - Shared templates
- `tests/` - Engine test suite

## Migration Status

The first monorepo migration phase is complete:

1. Imported `codeflow-desktop`
2. Imported `codeflow-website`
3. Imported `codeflow-orchestration`
4. Imported `codeflow-vscode-extension`
5. Added shared migration planning and CI scaffolding

The next phase is standardizing tooling, dependency management, and release automation across all components.

## Working with the Repository

### Engine

The Python engine still builds from the repository root:

- `pyproject.toml`
- `setup.py`
- `codeflow_engine/`

### Imported Applications

Each imported application can still be developed independently from its subdirectory using its existing package manager and build scripts.

## Migration Documentation

- [MIGRATION_PLAN.md](MIGRATION_PLAN.md)
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and the component-specific guides inside each imported project.

## License

See [LICENSE](LICENSE).

