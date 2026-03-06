# CodeFlow Engine

This directory contains the Python engine for the CodeFlow monorepo.

## Canonical Location

- Repository: [JustAGhosT/codeflow-engine](https://github.com/JustAGhosT/codeflow-engine)
- Project path: [engine](https://github.com/JustAGhosT/codeflow-engine/tree/master/engine)

## Development

From the repository root:

```bash
cd engine
poetry install --with dev
poetry run pytest
```

## Package Contents

- `codeflow_engine/` - application package
- `configs/` - engine configuration files
- `templates/` - engine templates
- `tests/` - engine tests
- `alembic/` - database migrations

See the monorepo [README.md](../README.md) for the full repository layout.
