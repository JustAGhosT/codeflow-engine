# Testing Quick Start Guide

Get started with testing CodeFlow Engine in 5 minutes.

---

## Prerequisites

- Python 3.12+
- Poetry installed
- Dependencies installed: `poetry install --with dev`

---

## Quick Start

### 1. Run All Tests

```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run specific test file
poetry run pytest tests/unit/test_agents.py
```

### 2. Run Tests with Coverage

```bash
# Run tests with coverage report
poetry run pytest --cov=codeflow_engine --cov-report=term

# Generate HTML coverage report
poetry run pytest --cov=codeflow_engine --cov-report=html
open htmlcov/index.html

# Or use the measurement script
./tools/coverage/measure-coverage.sh
```

### 3. Run by Category

```bash
# Unit tests only
poetry run pytest tests/unit/

# Integration tests only
poetry run pytest tests/integration/ -m integration

# E2E tests only
poetry run pytest tests/e2e/ -m e2e

# Smoke tests (fast)
poetry run pytest tests/e2e/test_smoke/ -m smoke
```

---

## Writing Your First Test

### Unit Test Example

```python
# tests/unit/test_example.py
import pytest
from codeflow_engine.actions.platform_detector import PlatformDetector

def test_platform_detector():
    """Test platform detector."""
    detector = PlatformDetector()
    result = detector.detect("tests/fixtures/python_project")
    
    assert result.platform == "Python"
    assert result.confidence > 0.8
```

### Integration Test Example

```python
# tests/integration/test_example.py
import pytest
from fastapi.testclient import TestClient

from codeflow_engine.server import create_app

@pytest.mark.integration
def test_health_endpoint():
    """Test health endpoint."""
    app = create_app()
    client = TestClient(app)
    
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

---

## Using Test Utilities

### Mock Clients

```python
from tests.utils import create_mock_github_client

def test_with_mock_github(mock_github_client):
    """Test with mocked GitHub client."""
    # Use mock_github_client fixture
    result = mock_github_client.get_pr("test/repo", 123)
    assert result is not None
```

### Test Data

```python
from tests.utils import create_sample_pr_data

def test_with_sample_data():
    """Test with sample PR data."""
    pr_data = create_sample_pr_data(
        repo="test/repo",
        number=123,
        title="Test PR"
    )
    assert pr_data["repository"] == "test/repo"
```

---

## Coverage Goals

- **Overall Target:** 80%
- **Critical Components:** 90%+
- **Current Baseline:** ~30%

### Check Coverage

```bash
# Check if coverage meets threshold
./tools/coverage/check-coverage.sh 70

# Or PowerShell
.\tools\coverage\check-coverage.ps1 -CoverageThreshold 70
```

---

## Next Steps

1. **Read Testing Strategy:** [TESTING_STRATEGY.md](./TESTING_STRATEGY.md)
2. **Check Coverage Plan:** [COVERAGE_IMPROVEMENT_PLAN.md](./COVERAGE_IMPROVEMENT_PLAN.md)
3. **Write Tests:** Use utilities and fixtures
4. **Measure Progress:** Use coverage scripts

---

## Additional Resources

- [Testing Strategy](./TESTING_STRATEGY.md)
- [Coverage Guide](./COVERAGE_GUIDE.md)
- [Integration Testing](./INTEGRATION_TESTING.md)
- [E2E Testing](./E2E_TESTING.md)

---

## Support

For testing questions:
- GitHub Issues: [codeflow-engine/issues](https://github.com/JustAGhosT/codeflow-engine/issues)
- Testing Documentation: [TESTING_STRATEGY.md](./TESTING_STRATEGY.md)

