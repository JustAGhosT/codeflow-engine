# Contributing to CodeFlow Orchestration

Thank you for your interest in contributing to CodeFlow Orchestration! This document provides guidelines for orchestration and tooling contributions.

---

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up development environment**:
   - PowerShell 7+ or Bash
   - Git
   - VS Code (recommended)
4. **Create a branch** for your changes

---

## Development Workflow

### Prerequisites

- PowerShell 7+ (for .ps1 scripts)
- Bash (for .sh scripts)
- Git
- VS Code (recommended)

### Code Style

**PowerShell:**
- Follow PSScriptAnalyzer rules
- Use approved verbs
- Add comprehensive help
- Use proper error handling

**Bash:**
- Use `set -e` for error handling
- Follow shellcheck recommendations
- Add comments for complex logic

**Before committing:**
```powershell
# PowerShell
Invoke-ScriptAnalyzer -Path .\scripts\*.ps1

# Bash
shellcheck scripts/*.sh
```

---

## Pull Request Process

1. **Validate scripts** before submitting
2. **Test scripts** if possible
3. **Update documentation** as needed
4. **Create a pull request** with a clear description

### PR Checklist

- [ ] Scripts validated (PSScriptAnalyzer/shellcheck)
- [ ] Documentation updated
- [ ] No hardcoded credentials
- [ ] Error handling implemented

---

## Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(orchestration): add health check script

Create health-check.ps1 for monitoring all services.
Add retry logic and detailed error reporting.

Closes #123
```

---

## Reporting Issues

Use GitHub Issues with:
- Clear description
- Affected script/tool
- Steps to reproduce
- Error messages
- Environment details

---

## Questions?

- GitHub Discussions: For questions
- GitHub Issues: For bugs and features
- See [CONTRIBUTING template](./docs/CONTRIBUTING_TEMPLATE.md) for more details

---

Thank you for contributing! 🎉

