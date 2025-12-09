# CodeFlow Developer Experience

Welcome to the CodeFlow Developer Experience documentation! This guide covers all the tools and integrations designed to make CodeFlow seamlessly integrated into your development workflow.

## ðŸš€ Quick Start

### Installation

```bash
# Install CodeFlow Engine with all developer tools
pip install codeflow-engine[full]

# Or install in development mode
git clone https://github.com/CodeFlow/codeflow-engine.git
cd codeflow-engine
pip install -e .
```

### First Steps

1. **CLI Tool**: Run quality checks from command line
2. **VS Code Extension**: Get real-time feedback in your IDE
3. **Git Hooks**: Automate quality checks on commits
4. **Dashboard**: Monitor and configure via web interface

## ðŸ“Ÿ Command Line Interface (CLI)

The CodeFlow CLI provides powerful command-line tools for code quality management.

### Basic Usage

```bash
# Check quality of specific files
CodeFlow check --files file1.py file2.py

# Check entire directory
CodeFlow check --directory ./src --mode comprehensive

# Split large files
CodeFlow split large_file.py --max-lines 100

# Install git hooks
CodeFlow hooks --install

# Start dashboard
CodeFlow dashboard --port 8080
```

### Quality Check Commands

```bash
# Ultra-fast mode (minimal checks)
CodeFlow check --mode ultra-fast --files *.py

# Fast mode (recommended for daily use)
CodeFlow check --mode fast --directory ./src

# Smart mode (context-aware)
CodeFlow check --mode smart --files *.py --volume 500

# Comprehensive mode (all tools)
CodeFlow check --mode comprehensive --directory ./src

# AI-enhanced mode (with AI analysis)
CodeFlow check --mode ai-enhanced --files *.py
```

### File Operations

```bash
# Split large files into manageable components
CodeFlow split large_file.py --max-lines 100 --output-dir ./split

# Dry run to see what would be split
CodeFlow split large_file.py --max-lines 100 --dry-run

# Split with custom function limits
CodeFlow split large_file.py --max-functions 5 --output-dir ./split
```

### Git Hooks Management

```bash
# Install git hooks
CodeFlow hooks --install

# Install with custom configuration
CodeFlow hooks --install --config hooks_config.json

# Uninstall git hooks
CodeFlow hooks --uninstall

# Check hook status
CodeFlow hooks
```

### Configuration

```bash
# Validate configuration
CodeFlow config --file codeflow_config.json

# Auto-fix configuration issues
CodeFlow config --file codeflow_config.json --fix
```

## ðŸ”Œ VS Code Extension

The CodeFlow VS Code extension provides seamless integration with your development environment.

### Installation

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "CodeFlow"
4. Click Install

### Features

#### Commands Available

- **CodeFlow: Run Quality Check** - Check current file or workspace
- **CodeFlow: Check Current File** - Quick check of active file
- **CodeFlow: Check Workspace** - Check entire workspace
- **CodeFlow: Split Large File** - Split current file
- **CodeFlow: Auto-Fix Issues** - Automatically fix detected issues
- **CodeFlow: Show Dashboard** - Open web dashboard
- **CodeFlow: Configure** - Open settings

#### Context Menu Integration

Right-click on files or in the editor to access:
- Quality check options
- Auto-fix functionality
- File splitting tools

#### Real-time Feedback

- **Diagnostics**: Issues appear as squiggly underlines
- **Problems Panel**: All issues listed with details
- **Output Channel**: Detailed analysis results
- **Status Bar**: Quick quality status indicator

#### Configuration

```json
{
    "codeflow.enabled": true,
    "codeflow.qualityMode": "fast",
    "codeflow.autoFixEnabled": false,
    "codeflow.showNotifications": true,
    "codeflow.pythonPath": "python",
    "codeflow.maxFileSize": 10000
}
```

### Usage Examples

#### Quick File Check
1. Open a Python file
2. Press `Ctrl+Shift+P` (Cmd+Shift+P on Mac)
3. Type "CodeFlow: Check Current File"
4. View results in Problems panel

#### Auto-Fix Issues
1. Right-click in editor
2. Select "CodeFlow: Auto-Fix Issues"
3. Review changes in diff view
4. Apply fixes

#### Split Large File
1. Open a large file (>500 lines)
2. Press `Ctrl+Shift+P`
3. Type "CodeFlow: Split Large File"
4. Configure split parameters
5. Review and confirm split

## ðŸ”— Git Hooks

CodeFlow git hooks automate quality checks and ensure code quality standards.

### Available Hooks

#### Pre-commit Hook
- Runs quality checks on staged files
- Prevents commits with quality issues
- Optionally applies auto-fixes
- Configurable quality modes

#### Post-commit Hook
- Collects metrics after successful commits
- Updates quality history
- Runs background analysis

#### Commit-msg Hook
- Validates commit message format
- Ensures conventional commit standards
- Provides helpful error messages

### Installation

```bash
# Install all hooks
CodeFlow hooks --install

# Install with custom configuration
CodeFlow hooks --install --config my_hooks_config.json
```

### Configuration

Create `hooks_config.json`:

```json
{
    "quality_mode": "fast",
    "auto_fix": true,
    "max_file_size": 10000,
    "enabled_hooks": ["pre-commit", "post-commit", "commit-msg"],
    "notifications": {
        "show_success": true,
        "show_warnings": true,
        "show_errors": true
    }
}
```

### Hook Behavior

#### Pre-commit Hook
```bash
# Automatically runs on git commit
git add file.py
git commit -m "feat: add new feature"
# CodeFlow runs quality checks before commit
```

#### Post-commit Hook
```bash
# Runs after successful commit
git commit -m "feat: add new feature"
# CodeFlow collects metrics and updates history
```

#### Commit-msg Hook
```bash
# Validates commit message format
git commit -m "invalid message"
# Error: Invalid commit message format
# Expected: <type>(<scope>): <description>
```

## ðŸ“Š Web Dashboard

The CodeFlow dashboard provides a web-based interface for monitoring and configuration.

### Starting the Dashboard

```bash
# Start with default settings
CodeFlow dashboard

# Custom host and port
CodeFlow dashboard --host 0.0.0.0 --port 9000

# Open browser automatically
CodeFlow dashboard --open-browser
```

### Dashboard Features

#### Real-time Metrics
- Total quality checks performed
- Issues found and resolved
- Success rates and processing times
- Quality mode usage statistics

#### Quick Actions
- **Run Quality Check**: Execute checks from web interface
- **Split Large File**: File splitting with visual feedback
- **Configuration**: Manage CodeFlow settings
- **Refresh Data**: Update metrics in real-time

#### Activity History
- Recent quality check results
- Processing times and issue counts
- Success/failure status
- Timestamp and mode information

#### Configuration Management
- Quality mode settings
- Auto-fix preferences
- File size limits
- Notification settings

### API Endpoints

The dashboard provides RESTful API endpoints:

```bash
# Get dashboard status
GET /api/status

# Get metrics data
GET /api/metrics

# Run quality check
POST /api/quality-check

# Get/set configuration
GET /api/config
POST /api/config

# Get activity history
GET /api/history

# Health check
GET /api/health
```

### Example API Usage

```bash
# Run quality check via API
curl -X POST http://localhost:8080/api/quality-check \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "fast",
    "files": ["file1.py", "file2.py"]
  }'

# Get dashboard status
curl http://localhost:8080/api/status

# Update configuration
curl -X POST http://localhost:8080/api/config \
  -H "Content-Type: application/json" \
  -d '{
    "quality_mode": "smart",
    "auto_fix": true
  }'
```

## ðŸ”§ Configuration

### Global Configuration

Create `~/.codeflow/config.json`:

```json
{
    "quality": {
        "default_mode": "fast",
        "auto_fix": false,
        "max_file_size": 10000,
        "enabled_tools": ["ruff", "mypy", "bandit"]
    },
    "ai": {
        "provider": "openai",
        "model": "gpt-4",
        "temperature": 0.1,
        "max_tokens": 2000
    },
    "dashboard": {
        "host": "localhost",
        "port": 8080,
        "refresh_interval": 30
    },
    "git_hooks": {
        "enabled": true,
        "quality_mode": "fast",
        "auto_fix": true
    }
}
```

### Project Configuration

Create `codeflow.yaml` in your project root:

```yaml
quality:
  default_mode: smart
  auto_fix: true
  max_file_size: 5000
  enabled_tools:
    - ruff
    - mypy
    - bandit

ai:
  provider: anthropic
  model: claude-3-sonnet
  temperature: 0.1

git_hooks:
  enabled: true
  pre_commit:
    mode: fast
    auto_fix: true
  post_commit:
    collect_metrics: true
  commit_msg:
    validate_format: true

file_splitting:
  max_lines: 100
  max_functions: 10
  max_classes: 5
  output_directory: ./split
```

## ðŸš€ Integration Examples

### CI/CD Pipeline Integration

```yaml
# GitHub Actions example
name: CodeFlow Quality Check
on: [push, pull_request]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install CodeFlow
        run: pip install codeflow-engine[full]
      - name: Run quality check
        run: CodeFlow check --mode comprehensive --directory ./src
```

### Pre-commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: codeflow-quality-check
        name: CodeFlow Quality Check
        entry: CodeFlow check --mode fast --files
        language: system
        types: [python]
        pass_filenames: true
```

### VS Code Workspace Settings

```json
// .vscode/settings.json
{
    "codeflow.enabled": true,
    "codeflow.qualityMode": "smart",
    "codeflow.autoFixEnabled": true,
    "codeflow.showNotifications": true,
    "codeflow.pythonPath": "python",
    "codeflow.maxFileSize": 10000
}
```

## ðŸ› Troubleshooting

### Common Issues

#### CLI Not Found
```bash
# Ensure CodeFlow is installed
pip install codeflow-engine[full]

# Check installation
which CodeFlow

# Reinstall if needed
pip uninstall codeflow-engine
pip install codeflow-engine[full]
```

#### VS Code Extension Issues
1. Check Python path in settings
2. Ensure CodeFlow CLI is accessible
3. Restart VS Code after installation
4. Check Output panel for error messages

#### Git Hooks Not Working
```bash
# Check hook installation
ls -la .git/hooks/

# Reinstall hooks
CodeFlow hooks --uninstall
CodeFlow hooks --install

# Check permissions
chmod +x .git/hooks/pre-commit
```

#### Dashboard Won't Start
```bash
# Check port availability
netstat -an | grep 8080

# Try different port
CodeFlow dashboard --port 9000

# Check dependencies
pip install flask flask-cors
```

### Getting Help

- **Documentation**: [https://codeflow.dev/docs](https://codeflow.dev/docs)
- **Issues**: [GitHub Issues](https://github.com/CodeFlow/codeflow-engine/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CodeFlow/codeflow-engine/discussions)
- **Discord**: [CodeFlow Community](https://discord.gg/CodeFlow)

## ðŸŽ¯ Best Practices

### Development Workflow

1. **Daily Development**:
   - Use VS Code extension for real-time feedback
   - Run `CodeFlow check --mode fast` before commits
   - Enable auto-fix for common issues

2. **Code Reviews**:
   - Use `CodeFlow check --mode comprehensive` for thorough analysis
   - Review AI-enhanced suggestions
   - Check file splitting recommendations

3. **CI/CD Integration**:
   - Run quality checks in CI pipeline
   - Use git hooks for pre-commit validation
   - Monitor metrics via dashboard

### Configuration Management

1. **Global Settings**: Use `~/.codeflow/config.json` for personal preferences
2. **Project Settings**: Use `codeflow.yaml` for project-specific configuration
3. **Team Standards**: Share configuration files in version control

### Performance Optimization

1. **Fast Mode**: Use for daily development and quick checks
2. **Smart Mode**: Use for balanced speed and thoroughness
3. **Comprehensive Mode**: Use for final reviews and CI/CD
4. **AI-Enhanced Mode**: Use for complex analysis and suggestions

---

*For more information, visit [https://codeflow.dev](https://codeflow.dev) or join our [Discord community](https://discord.gg/CodeFlow).*
