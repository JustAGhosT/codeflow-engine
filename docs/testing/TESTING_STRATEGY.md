# CodeFlow Engine - Testing Strategy

This document outlines the testing strategy for CodeFlow Engine, including unit testing, integration testing, end-to-end testing, and quality gates.

---

## Table of Contents

- [Testing Philosophy](#testing-philosophy)
- [Test Structure](#test-structure)
- [Test Coverage Goals](#test-coverage-goals)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Test Utilities](#test-utilities)
- [CI/CD Integration](#cicd-integration)
- [Quality Gates](#quality-gates)

---

## Testing Philosophy

### Principles

1. **Test Pyramid**: More unit tests, fewer integration tests, minimal E2E tests
2. **Fast Feedback**: Unit tests should run in seconds
3. **Isolation**: Tests should be independent and not rely on external services
4. **Maintainability**: Tests should be easy to read and maintain
5. **Coverage**: Focus on critical paths and business logic

### Test Types

- **Unit Tests**: Test individual functions/classes in isolation
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete workflows
- **Security Tests**: Test security features
- **Performance Tests**: Test performance characteristics

---

## Test Structure

### Directory Organization

```
tests/
├── unit/              # Unit tests (fast, isolated)
├── integration/       # Integration tests (moderate speed)
├── e2e/              # End-to-end tests (slower)
├── security/          # Security-focused tests
├── comprehensive/     # Comprehensive test suites
├── clients/          # Client integration tests
├── agents/           # Agent tests
└── conftest.py       # Pytest configuration and fixtures
```

### Test Naming Convention

- Unit tests: `test_<module>_<functionality>.py`
- Integration tests: `test_<component>_integration.py`
- E2E tests: `test_<workflow>_e2e.py`

---

## Test Coverage Goals

### Overall Targets

| Component | Target Coverage | Priority |
|-----------|----------------|----------|
| **Core Engine** | >90% | Critical |
| **Actions** | >80% | High |
| **Integrations** | >80% | High |
| **API Endpoints** | >85% | Critical |
| **Workflows** | >75% | Medium |
| **Configuration** | >70% | Medium |
| **Utilities** | >60% | Low |

### Current Status

To measure current coverage:

```bash
# Install coverage tools
poetry add --group dev pytest-cov coverage

# Run tests with coverage
poetry run pytest --cov=codeflow_engine --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

---

## Running Tests

### All Tests

```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run with coverage
poetry run pytest --cov=codeflow_engine --cov-report=term
```

### By Category

```bash
# Unit tests only
poetry run pytest tests/unit/

# Integration tests only
poetry run pytest tests/integration/

# E2E tests only
poetry run pytest tests/e2e/

# Security tests
poetry run pytest tests/security/
```

### By Marker

```bash
# Run tests marked as "slow"
poetry run pytest -m slow

# Run tests marked as "integration"
poetry run pytest -m integration

# Skip slow tests
poetry run pytest -m "not slow"
```

### Specific Test Files

```bash
# Run specific test file
poetry run pytest tests/unit/test_agents.py

# Run specific test function
poetry run pytest tests/unit/test_agents.py::test_agent_creation
```

---

## Writing Tests

### Unit Test Example

```python
import pytest
from codeflow_engine.actions.platform_detector import PlatformDetector

def test_platform_detector_detects_python():
    """Test that PlatformDetector correctly identifies Python projects."""
    detector = PlatformDetector()
    result = detector.detect("tests/fixtures/python_project")
    
    assert result.platform == "Python"
    assert result.confidence > 0.8
    assert "requirements.txt" in result.indicators
```

### Integration Test Example

```python
import pytest
from codeflow_engine.engine import CodeFlowEngine

@pytest.mark.integration
async def test_engine_processes_pr():
    """Test that engine can process a PR end-to-end."""
    engine = CodeFlowEngine()
    
    pr_data = {
        "repository": "test/repo",
        "number": 123,
        "title": "Test PR"
    }
    
    result = await engine.process_pr(pr_data)
    
    assert result.success is True
    assert result.issues_found > 0
```

### Using Fixtures

```python
import pytest

@pytest.fixture
def sample_pr_data():
    """Fixture providing sample PR data."""
    return {
        "repository": "test/repo",
        "number": 123,
        "title": "Test PR",
        "files": ["src/main.py"]
    }

def test_process_pr(sample_pr_data):
    """Test PR processing with fixture."""
    engine = CodeFlowEngine()
    result = engine.process_pr(sample_pr_data)
    assert result is not None
```

### Mocking External Services

```python
from unittest.mock import Mock, patch

@patch('codeflow_engine.clients.github_client.GitHubClient.get_pr')
def test_analyze_pr_with_mock(mock_get_pr):
    """Test PR analysis with mocked GitHub API."""
    mock_get_pr.return_value = {
        "title": "Test PR",
        "body": "Test description"
    }
    
    analyzer = PRAnalyzer()
    result = analyzer.analyze("test/repo", 123)
    
    assert result is not None
    mock_get_pr.assert_called_once_with("test/repo", 123)
```

---

## Test Utilities

### Fixtures

Common fixtures are defined in `tests/conftest.py`:

```python
# Example fixture
@pytest.fixture
def mock_github_client():
    """Mock GitHub client for testing."""
    with patch('codeflow_engine.clients.github_client.GitHubClient') as mock:
        yield mock
```

### Test Data

Test data should be stored in `tests/fixtures/`:

```
tests/fixtures/
├── sample_pr.json
├── sample_issue.json
├── sample_workflow.yaml
└── sample_repos/
    ├── python_project/
    └── javascript_project/
```

### Helpers

Test helper functions in `tests/utils.py`:

```python
def create_test_pr(repo="test/repo", number=1):
    """Helper to create test PR data."""
    return {
        "repository": repo,
        "number": number,
        "title": f"Test PR #{number}"
    }
```

---

## CI/CD Integration

### GitHub Actions

Tests run automatically on:
- Push to `main` or `develop`
- Pull requests
- Manual workflow dispatch

### Coverage Reporting

Coverage is reported to:
- GitHub Actions summary
- Codecov (if configured)
- HTML reports (artifacts)

### Quality Gates

CI/CD enforces:
- All tests must pass
- Coverage must not decrease
- Coverage must be >80% for critical components
- No linting errors
- No type errors

---

## Quality Gates

### Coverage Requirements

```yaml
# .github/workflows/ci.yml
- name: Check coverage
  run: |
    poetry run pytest --cov=codeflow_engine --cov-report=term --cov-report=xml
    poetry run coverage report --fail-under=80
```

### Coverage Configuration

Create `.coveragerc`:

```ini
[run]
source = codeflow_engine
omit = 
    */tests/*
    */__pycache__/*
    */migrations/*
    */venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
```

---

## Test Categories

### Unit Tests

**Location:** `tests/unit/`

**Focus:**
- Individual functions and classes
- Business logic
- Data transformations
- Utility functions

**Speed:** Fast (< 1 second per test)

**Examples:**
- `test_platform_detector.py`
- `test_volume_control.py`
- `test_agents.py`

### Integration Tests

**Location:** `tests/integration/`

**Focus:**
- Component interactions
- API endpoints
- Database operations
- External service integration (mocked)

**Speed:** Moderate (1-5 seconds per test)

**Examples:**
- `test_simple.py`
- `test_volume_control_e2e.py`

### E2E Tests

**Location:** `tests/e2e/`

**Focus:**
- Complete workflows
- Real API calls (test environment)
- Full system integration

**Speed:** Slow (5-30 seconds per test)

**Examples:**
- `test_full_pr_workflow_e2e.py`
- `test_issue_creation_e2e.py`

### Security Tests

**Location:** `tests/security/`

**Focus:**
- Authentication
- Authorization
- Input validation
- Rate limiting
- Secret handling

**Examples:**
- `test_rate_limiting.py`
- `test_exception_handling.py`
- `test_dashboard_security.py`

---

## Best Practices

### Do's

✅ **Do:**
- Write tests before fixing bugs (TDD when possible)
- Use descriptive test names
- Keep tests independent
- Use fixtures for common setup
- Mock external dependencies
- Test edge cases and error conditions
- Keep tests fast
- Document complex test logic

### Don'ts

❌ **Don't:**
- Test implementation details
- Rely on test execution order
- Use real external services in unit tests
- Create tests that depend on other tests
- Write tests that are hard to understand
- Skip tests without good reason
- Test third-party library code

---

## Measuring Coverage

### Generate Coverage Report

```bash
# Terminal report
poetry run pytest --cov=codeflow_engine --cov-report=term

# HTML report
poetry run pytest --cov=codeflow_engine --cov-report=html
open htmlcov/index.html

# XML report (for CI/CD)
poetry run pytest --cov=codeflow_engine --cov-report=xml
```

### Coverage by Module

```bash
# Show coverage by module
poetry run coverage report --show-missing

# Show only uncovered lines
poetry run coverage report --show-missing | grep -E "^\s+[0-9]+\s+[0-9]+\s+[0-9]+%"
```

---

## Continuous Improvement

### Coverage Tracking

1. **Baseline**: Measure current coverage
2. **Target**: Set coverage goals per component
3. **Monitor**: Track coverage in CI/CD
4. **Improve**: Add tests for uncovered code
5. **Maintain**: Prevent coverage regression

### Test Review Process

1. **New Code**: Must include tests
2. **Bug Fixes**: Must include regression tests
3. **Refactoring**: Update tests as needed
4. **Coverage**: Must not decrease

---

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [coverage.py Documentation](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Mocking Guide](https://docs.python.org/3/library/unittest.mock.html)

---

## Support

For testing questions:
- GitHub Issues: [codeflow-engine/issues](https://github.com/JustAGhosT/codeflow-engine/issues)
- Documentation: [README.md](../../README.md)

