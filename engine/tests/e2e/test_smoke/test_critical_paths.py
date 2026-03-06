"""Smoke tests for critical application paths."""

import pytest
from fastapi.testclient import TestClient

from codeflow_engine.server import create_app


@pytest.mark.e2e
@pytest.mark.smoke
def test_smoke_health_check():
    """Smoke test: Health check endpoint is accessible."""
    app = create_app()
    client = TestClient(app)
    
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


@pytest.mark.e2e
@pytest.mark.smoke
def test_smoke_api_root():
    """Smoke test: API root endpoint is accessible."""
    app = create_app()
    client = TestClient(app)
    
    response = client.get("/api")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data


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


@pytest.mark.e2e
@pytest.mark.smoke
def test_smoke_configuration_loading():
    """Smoke test: Configuration can be loaded."""
    from codeflow_engine.config.settings import CodeFlowSettings
    
    settings = CodeFlowSettings()
    assert settings is not None
    assert hasattr(settings, 'environment')

