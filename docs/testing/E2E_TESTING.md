# CodeFlow Engine - End-to-End Testing Guide

This guide covers end-to-end (E2E) testing for CodeFlow Engine, including complete workflow tests, deployment validation, and smoke tests.

---

## Table of Contents

- [Overview](#overview)
- [E2E Test Structure](#e2e-test-structure)
- [Workflow E2E Tests](#workflow-e2e-tests)
- [Deployment Validation](#deployment-validation)
- [Smoke Tests](#smoke-tests)
- [Running E2E Tests](#running-e2e-tests)
- [Best Practices](#best-practices)

---

## Overview

End-to-end tests verify that the entire system works correctly from start to finish. E2E tests:

- Test complete workflows
- Use real or test infrastructure
- May use test external services
- Validate deployment configurations
- Are the slowest type of tests

### Test Categories

1. **Workflow E2E Tests**: Test complete PR processing workflows
2. **Deployment Validation**: Test deployed systems
3. **Smoke Tests**: Quick validation of critical paths
4. **Regression Tests**: Test for known issues

---

## E2E Test Structure

### Directory Organization

```
tests/e2e/
├── __init__.py
├── conftest.py              # E2E-specific fixtures
├── test_workflows/          # Complete workflow tests
│   ├── test_pr_workflow.py
│   ├── test_issue_creation.py
│   └── test_quality_analysis.py
├── test_deployment/          # Deployment validation
│   ├── test_azure_deployment.py
│   ├── test_kubernetes_deployment.py
│   └── test_docker_deployment.py
├── test_smoke/               # Smoke tests
│   ├── test_critical_paths.py
│   └── test_health_checks.py
└── test_regression/          # Regression tests
    ├── test_known_issues.py
    └── test_bug_fixes.py
```

---

## Workflow E2E Tests

### Complete PR Processing Workflow

```python
"""E2E test for complete PR processing workflow."""

import pytest
from tests.utils import create_sample_pr_data

@pytest.mark.e2e
async def test_complete_pr_workflow():
    """Test complete PR processing workflow from webhook to issue creation."""
    from codeflow_engine.engine import CodeFlowEngine
    from codeflow_engine.integrations.github_app import GitHubAppIntegration
    
    # Initialize components
    engine = CodeFlowEngine()
    github_integration = GitHubAppIntegration()
    
    # Simulate PR opened webhook
    pr_data = create_sample_pr_data()
    webhook_event = {
        "action": "opened",
        "pull_request": pr_data
    }
    
    # Process webhook
    result = await github_integration.process_webhook(webhook_event)
    assert result["processed"] is True
    
    # Verify workflow executed
    # Verify actions ran
    # Verify results stored
    # Verify notifications sent
```

### Issue Creation Workflow

```python
"""E2E test for issue creation workflow."""

@pytest.mark.e2e
async def test_issue_creation_workflow():
    """Test complete issue creation workflow."""
    from codeflow_engine.engine import CodeFlowEngine
    from codeflow_engine.actions.issue_creator import IssueCreator
    
    engine = CodeFlowEngine()
    issue_creator = IssueCreator()
    
    # Simulate quality analysis finding issues
    quality_results = {
        "issues_found": 10,
        "critical_issues": 2,
        "files_analyzed": 5
    }
    
    # Create issues
    result = await issue_creator.create_issues(
        repository="test/repo",
        pr_number=123,
        quality_results=quality_results
    )
    
    assert result["issues_created"] > 0
    assert result["github_issues"] > 0 or result["linear_issues"] > 0
```

---

## Deployment Validation

### Azure Deployment Validation

```python
"""E2E tests for Azure deployment validation."""

import pytest
import requests

@pytest.mark.e2e
@pytest.mark.deployment
def test_azure_deployment_health():
    """Test that Azure deployment is healthy."""
    # This would use actual Azure deployment URL in CI/CD
    base_url = os.getenv("AZURE_DEPLOYMENT_URL", "http://localhost:8000")
    
    response = requests.get(f"{base_url}/health", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.e2e
@pytest.mark.deployment
def test_azure_deployment_api():
    """Test that Azure deployment API is accessible."""
    base_url = os.getenv("AZURE_DEPLOYMENT_URL", "http://localhost:8000")
    
    response = requests.get(f"{base_url}/api", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
```

### Kubernetes Deployment Validation

```python
"""E2E tests for Kubernetes deployment validation."""

@pytest.mark.e2e
@pytest.mark.deployment
def test_kubernetes_deployment():
    """Test Kubernetes deployment is accessible."""
    base_url = os.getenv("K8S_DEPLOYMENT_URL", "http://localhost:8000")
    
    # Test health endpoint
    response = requests.get(f"{base_url}/health", timeout=10)
    assert response.status_code == 200
    
    # Test API endpoint
    response = requests.get(f"{base_url}/api", timeout=10)
    assert response.status_code == 200
```

### Docker Deployment Validation

```python
"""E2E tests for Docker deployment validation."""

@pytest.mark.e2e
@pytest.mark.deployment
def test_docker_deployment():
    """Test Docker deployment is working."""
    # This would be run against a Docker container
    base_url = "http://localhost:8000"
    
    response = requests.get(f"{base_url}/health", timeout=10)
    assert response.status_code == 200
```

---

## Smoke Tests

### Critical Path Smoke Tests

```python
"""Smoke tests for critical paths."""

import pytest
from fastapi.testclient import TestClient

from codeflow_engine.server import create_app

@pytest.mark.e2e
@pytest.mark.smoke
def test_smoke_health_check():
    """Smoke test: Health check endpoint."""
    app = create_app()
    client = TestClient(app)
    
    response = client.get("/health")
    assert response.status_code == 200


@pytest.mark.e2e
@pytest.mark.smoke
def test_smoke_api_root():
    """Smoke test: API root endpoint."""
    app = create_app()
    client = TestClient(app)
    
    response = client.get("/api")
    assert response.status_code == 200


@pytest.mark.e2e
@pytest.mark.smoke
def test_smoke_engine_initialization():
    """Smoke test: Engine can be initialized."""
    from codeflow_engine.engine import CodeFlowEngine
    
    engine = CodeFlowEngine()
    assert engine is not None


@pytest.mark.e2e
@pytest.mark.smoke
def test_smoke_action_registry():
    """Smoke test: Actions can be discovered."""
    from codeflow_engine.actions.registry import ActionRegistry
    
    registry = ActionRegistry()
    actions = registry.list_actions()
    assert len(actions) > 0
```

---

## Running E2E Tests

### Run All E2E Tests

```bash
# Run all E2E tests
poetry run pytest tests/e2e/ -m e2e

# Run with verbose output
poetry run pytest tests/e2e/ -m e2e -v

# Run specific E2E test category
poetry run pytest tests/e2e/test_workflows/
```

### Run by Category

```bash
# Smoke tests only (fast)
poetry run pytest tests/e2e/test_smoke/ -m smoke

# Deployment validation (requires deployment)
poetry run pytest tests/e2e/test_deployment/ -m deployment

# Workflow tests
poetry run pytest tests/e2e/test_workflows/ -m e2e

# Regression tests
poetry run pytest tests/e2e/test_regression/ -m e2e
```

### Run in CI/CD

E2E tests should run:
- After successful deployment
- On release candidates
- Separately from unit/integration tests
- With longer timeout

```yaml
# Example in .github/workflows/e2e.yml
e2e-tests:
  runs-on: ubuntu-latest
  timeout-minutes: 30
  steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: poetry install --with dev
    - name: Run E2E tests
      run: poetry run pytest tests/e2e/ -m e2e --timeout=300
```

---

## Best Practices

### Do's

✅ **Do:**
- Test complete user workflows
- Use realistic test data
- Test error scenarios
- Clean up test data
- Use test markers for organization
- Keep tests independent
- Document test scenarios

### Don'ts

❌ **Don't:**
- Test implementation details
- Rely on test execution order
- Use production data
- Make tests dependent on each other
- Skip cleanup steps
- Test third-party library code

### Test Organization

- **Smoke Tests**: Fast, critical paths only
- **Workflow Tests**: Complete workflows
- **Deployment Tests**: Validate deployments
- **Regression Tests**: Prevent known issues

### Performance

E2E tests are the slowest:
- Run separately from unit/integration tests
- Use `@pytest.mark.slow` for long tests
- Consider parallel execution
- Set appropriate timeouts

---

## Test Fixtures

### E2E Fixtures

```python
# tests/e2e/conftest.py

@pytest.fixture(scope="module")
def e2e_client():
    """Create E2E test client."""
    from codeflow_engine.server import create_app
    from fastapi.testclient import TestClient
    app = create_app()
    return TestClient(app)


@pytest.fixture(scope="module")
def e2e_engine():
    """Create E2E test engine."""
    from codeflow_engine.engine import CodeFlowEngine
    return CodeFlowEngine()


@pytest.fixture
def deployment_url():
    """Get deployment URL from environment."""
    return os.getenv("DEPLOYMENT_URL", "http://localhost:8000")
```

---

## CI/CD Integration

### GitHub Actions

E2E tests should run:
- After deployment
- On release candidates
- With appropriate timeouts
- Separately from other tests

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  workflow_dispatch:
  push:
    branches: [main]
    tags:
      - 'v*'

jobs:
  e2e:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - name: Run E2E tests
        run: poetry run pytest tests/e2e/ -m e2e
```

---

## Additional Resources

- [Testing Strategy](./TESTING_STRATEGY.md)
- [Integration Testing](./INTEGRATION_TESTING.md)
- [Coverage Guide](./COVERAGE_GUIDE.md)

---

## Support

For E2E testing questions:
- GitHub Issues: [codeflow-engine/issues](https://github.com/JustAGhosT/codeflow-engine/issues)
- Testing Documentation: [TESTING_STRATEGY.md](./TESTING_STRATEGY.md)

