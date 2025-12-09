# CodeFlow Engine - Integration Testing Guide

This guide covers integration testing for CodeFlow Engine, including cross-component tests, API integration tests, and database integration tests.

---

## Table of Contents

- [Overview](#overview)
- [Integration Test Structure](#integration-test-structure)
- [API Integration Tests](#api-integration-tests)
- [Database Integration Tests](#database-integration-tests)
- [External Service Integration](#external-service-integration)
- [Running Integration Tests](#running-integration-tests)
- [Best Practices](#best-practices)

---

## Overview

Integration tests verify that multiple components work together correctly. Unlike unit tests, integration tests:

- Test component interactions
- Use real or test databases
- May use mocked external services
- Test complete workflows
- Are slower than unit tests

### Test Categories

1. **API Integration Tests**: Test HTTP endpoints with real FastAPI app
2. **Database Integration Tests**: Test database operations with test DB
3. **Component Integration Tests**: Test interactions between components
4. **External Service Integration**: Test integrations with mocked external APIs

---

## Integration Test Structure

### Directory Organization

```
tests/integration/
├── __init__.py
├── conftest.py              # Integration-specific fixtures
├── test_api/                # API integration tests
│   ├── test_health.py
│   ├── test_dashboard.py
│   └── test_github_app.py
├── test_database/           # Database integration tests
│   ├── test_models.py
│   ├── test_queries.py
│   └── test_migrations.py
├── test_components/         # Component integration tests
│   ├── test_engine_actions.py
│   ├── test_workflow_execution.py
│   └── test_integrations.py
└── test_external/           # External service integration
    ├── test_github_api.py
    ├── test_linear_api.py
    └── test_slack_api.py
```

---

## API Integration Tests

### Testing FastAPI Endpoints

```python
"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from codeflow_engine.server import create_app

@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_api_status_endpoint(client):
    """Test API status endpoint."""
    response = client.get("/api/status", headers={"X-API-Key": "test-key"})
    assert response.status_code == 200
    data = response.json()
    assert "uptime_seconds" in data
    assert "total_checks" in data


def test_quality_check_endpoint(client):
    """Test quality check endpoint."""
    response = client.post(
        "/api/quality-check",
        headers={"X-API-Key": "test-key"},
        json={
            "mode": "fast",
            "files": ["src/main.py"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "total_issues_found" in data
```

### Testing Authentication

```python
def test_api_requires_authentication(client):
    """Test that API endpoints require authentication."""
    response = client.get("/api/status")
    assert response.status_code == 401


def test_api_with_valid_key(client):
    """Test API with valid API key."""
    response = client.get(
        "/api/status",
        headers={"X-API-Key": "valid-key"}
    )
    assert response.status_code == 200


def test_api_with_invalid_key(client):
    """Test API with invalid API key."""
    response = client.get(
        "/api/status",
        headers={"X-API-Key": "invalid-key"}
    )
    assert response.status_code == 401
```

### Testing Rate Limiting

```python
def test_rate_limiting(client):
    """Test rate limiting on quality check endpoint."""
    headers = {"X-API-Key": "test-key"}
    
    # Make 10 requests (should succeed)
    for i in range(10):
        response = client.post(
            "/api/quality-check",
            headers=headers,
            json={"mode": "fast", "files": []}
        )
        assert response.status_code == 200
    
    # 11th request should be rate limited
    response = client.post(
        "/api/quality-check",
        headers=headers,
        json={"mode": "fast", "files": []}
    )
    assert response.status_code == 429
    assert "Retry-After" in response.headers
```

---

## Database Integration Tests

### Test Database Setup

```python
"""Database integration tests."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from codeflow_engine.database.models import Base, Workflow, WorkflowExecution

@pytest.fixture(scope="module")
def test_db():
    """Create test database."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)


def test_create_workflow(test_db):
    """Test creating a workflow."""
    workflow = Workflow(
        name="test_workflow",
        description="Test workflow",
        enabled=True
    )
    test_db.add(workflow)
    test_db.commit()
    
    assert workflow.id is not None
    assert workflow.name == "test_workflow"


def test_workflow_execution(test_db):
    """Test workflow execution tracking."""
    workflow = Workflow(name="test_workflow", enabled=True)
    test_db.add(workflow)
    test_db.commit()
    
    execution = WorkflowExecution(
        workflow_id=workflow.id,
        status="running"
    )
    test_db.add(execution)
    test_db.commit()
    
    assert execution.id is not None
    assert execution.workflow_id == workflow.id
    assert execution.status == "running"
```

### Testing Transactions

```python
def test_transaction_rollback(test_db):
    """Test transaction rollback."""
    workflow = Workflow(name="test_workflow", enabled=True)
    test_db.add(workflow)
    test_db.flush()
    
    workflow_id = workflow.id
    
    # Rollback
    test_db.rollback()
    
    # Workflow should not exist
    workflow = test_db.query(Workflow).filter_by(id=workflow_id).first()
    assert workflow is None
```

---

## Component Integration Tests

### Testing Engine-Action Integration

```python
"""Integration tests for engine and actions."""

import pytest
from codeflow_engine.engine import CodeFlowEngine
from codeflow_engine.actions.platform_detector import PlatformDetector

@pytest.mark.integration
async def test_engine_executes_platform_detector():
    """Test engine can execute platform detector action."""
    engine = CodeFlowEngine()
    
    result = await engine.execute_action(
        "platform_detector",
        {"repository_path": "tests/fixtures/python_project"}
    )
    
    assert result is not None
    assert "platform" in result
    assert result["platform"] == "Python"


@pytest.mark.integration
async def test_engine_workflow_execution():
    """Test engine executes complete workflow."""
    engine = CodeFlowEngine()
    
    workflow_config = {
        "name": "test_workflow",
        "triggers": ["pr.opened"],
        "actions": [
            {"type": "platform_detector"},
            {"type": "quality_engine", "config": {"mode": "fast"}}
        ]
    }
    
    result = await engine.execute_workflow(
        workflow_config,
        trigger_data={"event": "pr.opened", "pr": {"number": 123}}
    )
    
    assert result is not None
    assert result["success"] is True
```

### Testing Integration Layer

```python
"""Integration tests for integration layer."""

import pytest
from codeflow_engine.integrations.github_app import GitHubAppIntegration

@pytest.mark.integration
async def test_github_app_installation(mock_github_client):
    """Test GitHub App installation flow."""
    integration = GitHubAppIntegration()
    integration.github_client = mock_github_client
    
    result = await integration.install_app(
        installation_id=12345,
        user_id=67890
    )
    
    assert result is not None
    assert result["installed"] is True


@pytest.mark.integration
async def test_github_webhook_processing(mock_github_client):
    """Test GitHub webhook processing."""
    integration = GitHubAppIntegration()
    integration.github_client = mock_github_client
    
    webhook_data = {
        "action": "opened",
        "pull_request": {
            "number": 123,
            "title": "Test PR"
        }
    }
    
    result = await integration.process_webhook(webhook_data)
    
    assert result is not None
    assert result["processed"] is True
```

---

## External Service Integration

### Mocking External APIs

```python
"""Integration tests with mocked external services."""

import pytest
from unittest.mock import patch, AsyncMock

from codeflow_engine.clients.github_client import GitHubClient
from codeflow_engine.clients.linear_client import LinearClient

@pytest.mark.integration
async def test_github_client_integration():
    """Test GitHub client with mocked API."""
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={
            "id": 123,
            "title": "Test PR",
            "state": "open"
        })
        mock_response.status = 200
        mock_get.return_value.__aenter__.return_value = mock_response
        
        client = GitHubClient(token="test_token")
        pr = await client.get_pr("test/repo", 123)
        
        assert pr["id"] == 123
        assert pr["title"] == "Test PR"


@pytest.mark.integration
async def test_linear_client_integration():
    """Test Linear client with mocked API."""
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={
            "data": {
                "issueCreate": {
                    "issue": {
                        "id": "test-issue-id",
                        "title": "Test Issue"
                    }
                }
            }
        })
        mock_response.status = 200
        mock_post.return_value.__aenter__.return_value = mock_response
        
        client = LinearClient(api_key="test_key")
        issue = await client.create_issue(
            team_id="test-team",
            title="Test Issue",
            description="Test description"
        )
        
        assert issue["id"] == "test-issue-id"
        assert issue["title"] == "Test Issue"
```

---

## Running Integration Tests

### Run All Integration Tests

```bash
# Run all integration tests
poetry run pytest tests/integration/

# Run with verbose output
poetry run pytest tests/integration/ -v

# Run specific test file
poetry run pytest tests/integration/test_api/test_health.py
```

### Run by Category

```bash
# API integration tests only
poetry run pytest tests/integration/test_api/

# Database integration tests only
poetry run pytest tests/integration/test_database/

# Component integration tests only
poetry run pytest tests/integration/test_components/
```

### Run with Markers

```bash
# Run tests marked as integration
poetry run pytest -m integration

# Run tests marked as slow
poetry run pytest -m "integration and not slow"
```

---

## Best Practices

### Do's

✅ **Do:**
- Use test databases (in-memory or separate test DB)
- Mock external services (GitHub, Linear, Slack APIs)
- Test complete workflows end-to-end
- Clean up test data after tests
- Use fixtures for common setup
- Test error conditions
- Test edge cases

### Don'ts

❌ **Don't:**
- Use production databases
- Make real API calls to external services
- Rely on test execution order
- Leave test data in database
- Test implementation details
- Make tests dependent on each other

### Test Isolation

Each integration test should:
- Set up its own test data
- Clean up after itself
- Not depend on other tests
- Be able to run independently

### Performance

Integration tests are slower than unit tests:
- Use `@pytest.mark.slow` for long-running tests
- Run integration tests separately in CI/CD
- Consider parallel execution for independent tests

---

## Test Fixtures

### Common Fixtures

```python
# tests/integration/conftest.py

@pytest.fixture
def test_client():
    """Create test FastAPI client."""
    from codeflow_engine.server import create_app
    from fastapi.testclient import TestClient
    app = create_app()
    return TestClient(app)


@pytest.fixture
def test_database():
    """Create test database session."""
    # Setup test database
    # Yield session
    # Cleanup
    pass


@pytest.fixture
def mock_external_services():
    """Mock all external services."""
    with patch('codeflow_engine.clients.github_client.GitHubClient') as mock_github, \
         patch('codeflow_engine.clients.linear_client.LinearClient') as mock_linear:
        yield {
            'github': mock_github,
            'linear': mock_linear
        }
```

---

## CI/CD Integration

### GitHub Actions

Integration tests should run:
- On pull requests
- Before merging to main
- Separately from unit tests (can be slower)

```yaml
# Example in .github/workflows/ci.yml
integration-tests:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: poetry install --with dev
    - name: Run integration tests
      run: poetry run pytest tests/integration/ -m integration
```

---

## Additional Resources

- [Testing Strategy](./TESTING_STRATEGY.md)
- [Coverage Guide](./COVERAGE_GUIDE.md)
- [Unit Testing Guide](./COVERAGE_IMPROVEMENT_PLAN.md)

---

## Support

For integration testing questions:
- GitHub Issues: [codeflow-engine/issues](https://github.com/JustAGhosT/codeflow-engine/issues)
- Testing Documentation: [TESTING_STRATEGY.md](./TESTING_STRATEGY.md)

