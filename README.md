# CodeFlow Engine

AI-Powered GitHub PR Automation and Issue Management

[![PyPI version](https://badge.fury.io/py/codeflow-engine.svg)](https://badge.fury.io/py/codeflow-engine)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

CodeFlow Engine is a comprehensive AI-powered automation platform that transforms GitHub pull request workflows through intelligent analysis, issue creation, and multi-agent collaboration.

## Features

### AI-Powered PR Analysis
- **Multi-Agent Review**: CodeRabbit, GitHub Copilot, AI TypeScript Check integration
- **Platform Detection**: Detects 25+ development platforms
- **Intelligent Issue Classification**: Security, performance, bugs, features
- **Quality Gates**: Automated validation before merge

### Smart Integrations
- **Communication**: Slack (Axolo), Microsoft Teams, Discord, Notion
- **Project Management**: Linear, GitHub Issues, Jira
- **AI Tools**: AutoGen multi-agent, configurable LLM providers
- **Monitoring**: Sentry, DataDog, Prometheus metrics

### Advanced Automation
- **Issue Auto-Creation**: GitHub Issues and Linear tickets
- **AI Tool Assignment**: Route issues to specialized AI tools
- **Workflow Orchestration**: 20+ pre-built workflows
- **Memory System**: Learn from past interactions and patterns

## Quick Start

### Installation

```bash
# Install from PyPI
pip install codeflow-engine

# Or install with all features
pip install "codeflow-engine[full]"
```

### Docker Deployment

```bash
docker build -t codeflow-engine:latest .
docker run -d \
  -e GITHUB_TOKEN=your_token \
  -e OPENAI_API_KEY=your_key \
  -p 8080:8080 \
  codeflow-engine:latest
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/your-org/codeflow-engine.git
cd codeflow-engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

### Project Structure

```
codeflow-engine/
├── codeflow_engine/     # Main package
├── tests/              # Test suite
├── docs/               # Documentation
├── configs/            # Configuration templates
├── templates/          # Template system
├── .github/
│   └── workflows/      # CI/CD workflows
├── pyproject.toml
└── poetry.lock
```

## Configuration

The engine uses configuration via:
- **Environment variables**: `GITHUB_TOKEN`, `OPENAI_API_KEY`, etc.
- **Config files**: `configs/config.yaml`
- **CLI arguments**: Command-line options

**Important**: The engine has no hard-coded infrastructure paths. All configuration is externalized.

## Documentation

- [Getting Started Guide](docs/getting-started/)
- [Architecture Documentation](docs/architecture/)
- [Development Guide](docs/development/)
- [API Reference](docs/api/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

MIT - See [LICENSE](LICENSE) for details.

## Related Repositories

- [`codeflow-infrastructure`](../codeflow-infrastructure) - Production infrastructure as code
- [`codeflow-desktop`](../codeflow-desktop) - Desktop application
- [`codeflow-vscode-extension`](../codeflow-vscode-extension) - VS Code extension
- [`codeflow-azure-setup`](../codeflow-azure-setup) - Azure bootstrap scripts

