# CodeFlow Engine Agent Guide

## Build/Test/Lint Commands

- **Run all tests**: `pytest`
- **Single test file**: `pytest tests/unit/test_file.py`
- **Single test function**: `pytest tests/unit/test_file.py::test_function`
- **Tests with coverage**: `pytest --cov=CodeFlow --cov-report=html`
- **Unit tests only**: `pytest tests/unit/`
- **Integration tests**: `pytest tests/integration/`
- **Volume control tests**: `python tests/unit/test_volume_control_clean.py`
- **Code formatting**: `black CodeFlow tests` (check: `black --check --diff .`)
- **Import sorting**: `isort CodeFlow tests` (check: `isort --check-only --diff .`)
- **Type checking**: `mypy CodeFlow` (very permissive config)
- **Install dev deps**: `pip install -e ".[dev]"`

## Architecture

- **Main package**: `CodeFlow/` - Core engine with actions, workflows, integrations, AI providers
- **Actions**: 50+ automation actions in `CodeFlow/actions/` (PR analysis, issue creation, quality
  gates)
- **Workflows**: Pre-built workflow definitions in `CodeFlow/workflows/`
- **Integrations**: External services (GitHub, Linear, Slack, AI providers) in
  `CodeFlow/integrations/`
- **AI/LLM**: Multi-provider AI system in `CodeFlow/ai/` (OpenAI, Anthropic, Mistral, Groq)
- **Quality System**: AI-powered code analysis and quality gates in `CodeFlow/quality/`
- **Volume Control**: HiFi-style volume control system in `scripts/volume-control/` (dev & commit
  knobs)

## Code Style & Conventions

- **Python 3.13** required
- **Type hints**: Optional (mypy configured to ignore most errors)
- **Line length**: Effectively unlimited (flake8 disabled)
- **Error handling**: Use CodeFlowException base class and subclasses
- **Imports**: Use absolute imports, organize by category (stdlib, 3rd party, local)
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Async/await**: Preferred for I/O operations
- **Pydantic**: Used for configuration and data models
- **Logging**: Structured logging with configurable JSON output

_Context improved by Giga AI, using cursorrules and windsurfrules development guidelines._
