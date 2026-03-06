# CodeFlow Quality Engine

A comprehensive, cross-platform code quality analysis engine with AI-enhanced capabilities and
Windows compatibility.

## Features

- **Cross-Platform Support**: Works on Windows, Linux, and macOS with automatic platform detection
- **Comprehensive Tool Integration**: Integrates multiple quality analysis tools
- **AI-Enhanced Analysis**: Optional AI-powered code review and suggestions
- **Windows Adaptations**: Automatic tool substitutions and alternatives for Windows compatibility
- **Extensible Architecture**: Easy to add new tools and analysis capabilities

## Directory Structure

```text
quality_engine/
â”œâ”€â”€ __init__.py                 # Main package initialization
â”œâ”€â”€ engine.py                   # Core quality engine implementation
â”œâ”€â”€ cli.py                      # Command-line interface
â”œâ”€â”€ models.py                   # Data models and enums
â”œâ”€â”€ config.py                   # Configuration management
â”œâ”€â”€ platform_detector.py        # Platform detection and adaptations
â”œâ”€â”€ tool_runner.py              # Tool execution and result processing
â”œâ”€â”€ summary.py                  # Result summarization
â”œâ”€â”€ di.py                       # Dependency injection container
â”œâ”€â”€ handler_registry.py         # Result handler management
â”œâ”€â”€ handler_base.py             # Base handler classes
â”œâ”€â”€ result_wrapper.py           # Result wrapping utilities
â”œâ”€â”€ example_usage.py            # Usage examples
â”œâ”€â”€ README.md                   # This file
â”‚
â”œâ”€â”€ tools/                      # Quality analysis tools
â”‚   â”œâ”€â”€ __init__.py            # Tool discovery and registration
â”‚   â”œâ”€â”€ tool_base.py           # Base tool interface
â”‚   â”œâ”€â”€ registry.py            # Tool registry
â”‚   â”œâ”€â”€ ruff_tool.py           # Python linting and formatting
â”‚   â”œâ”€â”€ mypy_tool.py           # Python type checking
â”‚   â”œâ”€â”€ bandit_tool.py         # Python security scanning
â”‚   â”œâ”€â”€ semgrep_tool.py        # Cross-platform static analysis (NEW)
â”‚   â”œâ”€â”€ interrogate_tool.py    # Python docstring coverage
â”‚   â”œâ”€â”€ pytest_tool.py         # Python testing
â”‚   â”œâ”€â”€ radon_tool.py          # Python complexity analysis
â”‚   â”œâ”€â”€ codeql_tool.py         # GitHub CodeQL (Linux/macOS)
â”‚   â”œâ”€â”€ windows_security_tool.py # Windows security scanner
â”‚   â”œâ”€â”€ eslint_tool.py         # JavaScript/TypeScript linting
â”‚   â”œâ”€â”€ sonarqube_tool.py      # SonarQube integration
â”‚   â”œâ”€â”€ dependency_scanner_tool.py # Dependency analysis
â”‚   â””â”€â”€ performance_analyzer_tool.py # Performance analysis
â”‚
â”œâ”€â”€ handlers/                   # Result handlers
â”‚   â”œâ”€â”€ __init__.py            # Handler discovery
â”‚   â”œâ”€â”€ base.py                # Base handler classes
â”‚   â””â”€â”€ ...                    # Specific handlers
â”‚
â”œâ”€â”€ ai/                        # AI-enhanced analysis
â”‚   â”œâ”€â”€ ai_modes.py            # AI analysis modes
â”‚   â”œâ”€â”€ ai_analyzer.py         # AI code analyzer
â”‚   â””â”€â”€ ai_handler.py          # AI result handling
â”‚
â””â”€â”€ __tests__/                 # Test files
    â””â”€â”€ test_*.py              # Unit tests
```

## Available Tools

### Cross-Platform Tools (Recommended)

- **Semgrep**: Comprehensive static analysis for security and code quality
- **Ruff**: Fast Python linting and formatting
- **Bandit**: Python security vulnerability scanning
- **Safety**: Dependency vulnerability scanning
- **MyPy**: Python type checking
- **Pytest**: Python testing framework

### Platform-Specific Tools

- **CodeQL**: Advanced security analysis (Linux/macOS only)
- **Windows Security Tool**: Comprehensive Windows security scanner
- **ESLint**: JavaScript/TypeScript linting
- **SonarQube**: Enterprise code quality analysis

### Analysis Tools

- **Interrogate**: Python docstring coverage
- **Radon**: Python code complexity analysis
- **Dependency Scanner**: Package dependency analysis
- **Performance Analyzer**: Code performance analysis

## Windows Compatibility

The Quality Engine automatically detects Windows and provides:

1. **Tool Substitutions**: CodeQL â†’ Semgrep (recommended cross-platform alternative)
2. **Windows Security Tool**: Comprehensive security scanning for Windows
3. **Platform Warnings**: Clear information about limitations and alternatives
4. **User Confirmation**: Optional confirmation before running on Windows

## Usage

### Command Line Interface

```bash
# Basic usage (smart mode is default)
python -m codeflow.actions.quality_engine

# Fast mode - quick analysis with essential tools
python -m codeflow.actions.quality_engine --mode=fast

# Smart mode - intelligent tool selection based on file types (default)
python -m codeflow.actions.quality_engine --mode=smart

# Comprehensive mode - full analysis with all available tools
python -m codeflow.actions.quality_engine --mode=comprehensive

# AI-enhanced analysis (experimental)
python -m codeflow.actions.quality_engine --mode=ai_enhanced --ai-provider openai --ai-model gpt-4

# Auto-fix mode - automatically fix issues using AI
python -m codeflow.actions.quality_engine --mode=comprehensive --auto-fix --ai-provider openai --ai-model gpt-4

# Auto-fix with specific issue types
python -m codeflow.actions.quality_engine --auto-fix --fix-types E501 F401 F841 --max-fixes 25

# Dry-run auto-fix (preview changes without applying)
python -m codeflow.actions.quality_engine --auto-fix --dry-run

# Windows mode (with confirmation)
python -m codeflow.actions.quality_engine.cli --files <files> --mode comprehensive

# Skip Windows check
python -m codeflow.actions.quality_engine.cli --files <files> --skip-windows-check
```

### Available Modes

- **smart** (default): Intelligent tool selection based on file types - fastest for daily use
- **fast**: Quick analysis with essential tools (Ruff, Bandit) - minimal checks
- **comprehensive**: Full analysis with all available tools - thorough but slower
- **ai_enhanced**: AI-powered analysis with code suggestions - requires AI provider and model
  configuration (experimental)

### Pre-commit Integration

The Quality Engine is **disabled by default** in pre-commit hooks due to performance considerations.

#### Current Pre-commit Workflow

1. **Black** - Python code formatting
2. **isort** - Import sorting
3. **Prettier** - JSON/YAML/Markdown formatting
4. **Handle Unstaged Changes** - Automatically adds formatting changes
5. **âœ… Commit completes successfully**

#### Manual Quality Checks

```bash
# Run comprehensive analysis when needed
python -m codeflow.actions.quality_engine --mode=comprehensive

# Run smart analysis for quick checks
python -m codeflow.actions.quality_engine --mode=smart

# Run fast analysis for essential checks
python -m codeflow.actions.quality_engine --mode=fast
```

#### Re-enabling Quality Engine in Pre-commit

If you want to add Quality Engine back to pre-commit, uncomment the section in
`.pre-commit-config.yaml`:

```yaml
# Quality Engine (uncomment to enable)
- repo: local
  hooks:
    - id: quality-engine
      name: CodeFlow Quality Engine
      entry: python -m codeflow.actions.quality_engine
      language: system
      types: [python]
      args: [--mode=smart] # Use smart mode for pre-commit
      stages: [pre-commit]
      verbose: true
      pass_filenames: false
```

**Note**: Enabling Quality Engine in pre-commit will significantly increase commit time (60-90
seconds).

### CLI Options

```bash
python -m codeflow.actions.quality_engine [OPTIONS]

Options:
  --mode {fast,comprehensive,ai_enhanced,smart}  Quality check mode (default: smart)
  --files [FILES ...]                            Files to check (supports glob patterns)
  --config CONFIG                                Path to configuration file (default: pyproject.toml)
  --verbose                                      Enable verbose output
  --ai-provider AI_PROVIDER                      AI provider to use for AI-enhanced mode
  --ai-model AI_MODEL                           AI model to use for AI-enhanced mode
  --auto-fix                                     Automatically fix issues using AI
  --fix-types [FIX_TYPES ...]                    Types of issues to fix (e.g., E501 F401 F841)
  --max-fixes MAX_FIXES                          Maximum number of fixes to apply (default: 50)
  --dry-run                                      Show what would be fixed without making changes
  -h, --help                                     Show help message
```

### Auto-Fix Features

The Quality Engine now includes **AI-powered auto-fix capabilities** that can automatically resolve
common code quality issues:

#### Supported Fix Types

- **E501**: Line too long - Break long lines at natural points
- **F401**: Unused imports - Remove unnecessary imports
- **F841**: Unused variables - Remove or rename with underscore
- **E722**: Bare except - Specify appropriate exception types
- **E302**: Expected 2 blank lines - Fix import spacing
- **E305**: Expected 2 blank lines after class - Fix class spacing

#### Auto-Fix Examples

```bash
# Basic auto-fix with default settings
python -m codeflow.actions.quality_engine --auto-fix

# Auto-fix with specific issue types
python -m codeflow.actions.quality_engine --auto-fix --fix-types E501 F401 F841

# Limit the number of fixes applied
python -m codeflow.actions.quality_engine --auto-fix --max-fixes 25

# Preview changes without applying them
python -m codeflow.actions.quality_engine --auto-fix --dry-run

# Combine with comprehensive analysis
python -m codeflow.actions.quality_engine --mode=comprehensive --auto-fix
```

#### Safety Features

- **Backup Creation**: Automatically creates backups before making changes
- **Dry-Run Mode**: Preview changes without applying them
- **Confidence Scoring**: Only applies fixes the AI is confident about
- **Error Handling**: Graceful fallback if auto-fix fails
- **Detailed Logging**: Comprehensive logs of all changes made

### Performance Characteristics

#### Mode Comparison

- **Fast Mode**: ~2-5 seconds - Essential tools only
- **Smart Mode**: ~10-30 seconds - Intelligent tool selection
- **Comprehensive Mode**: ~60-120 seconds - All tools, thorough analysis

#### Typical Results (CodeFlow Engine Codebase)

- **Fast Mode**: ~50-100 issues found
- **Smart Mode**: ~500-1000 issues found
- **Comprehensive Mode**: ~3000-4000 issues found across 250+ files

#### Tool Execution Times (Comprehensive Mode)

- **Ruff**: ~1.1s (3,762 issues found)
- **Semgrep**: ~45s (security analysis)
- **Windows Security**: ~43s (Windows-specific)
- **Radon**: ~60s (complexity analysis)
- **MyPy**: ~3s (type checking)
- **Bandit**: ~1.1s (security scanning)

### Programmatic Usage

```python
from codeflow.actions.quality_engine.engine import QualityEngine
from codeflow.actions.quality_engine.models import QualityInputs
from codeflow.utils.volume_utils import QualityMode

# Create engine
engine = QualityEngine()

# Run analysis
inputs = QualityInputs(
    mode=QualityMode.COMPREHENSIVE,
    files=["src/"],
    enable_ai_agents=True
)

result = await engine.run(inputs)
print(f"Found {result.total_issues_found} issues")
```

## Configuration

The engine can be configured via `pyproject.toml`:

```toml
[tool.codeflow.quality_engine]
default_mode = "smart"
enable_ai = false

[tool.codeflow.quality_engine.tools]
ruff = { enabled = true, config = {} }
semgrep = { enabled = true, rules = "auto", severity = "INFO,WARNING,ERROR" }
bandit = { enabled = true, config = {} }
```

## Adding New Tools

To add a new quality analysis tool:

1. Create a new tool class in `tools/` directory
2. Inherit from `Tool` base class
3. Implement required methods (`name`, `description`, `run`)
4. Register the tool in `tools/__init__.py`

Example:

```python
from .tool_base import Tool

class MyCustomTool(Tool):
    @property
    def name(self) -> str:
        return "my_custom_tool"

    @property
    def description(self) -> str:
        return "My custom quality analysis tool"

    async def run(self, files: List[str], config: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Implement tool logic here
        return []
```

## Contributing

1. Follow the existing code structure and patterns
2. Add appropriate tests for new tools
3. Update documentation for new features
4. Ensure cross-platform compatibility
5. Add Windows adaptations if needed

## License

Part of the CodeFlow project. See main project license.
