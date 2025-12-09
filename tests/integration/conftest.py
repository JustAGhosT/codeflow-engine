"""Configuration and fixtures for integration tests."""

import pytest
from fastapi.testclient import TestClient

from codeflow_engine.server import create_app


@pytest.fixture
def test_client():
    """Create test FastAPI client for integration tests."""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def api_key() -> str:
    """Provide test API key for authenticated requests."""
    return "test-api-key-for-integration-tests"


@pytest.fixture
def authenticated_headers(api_key: str) -> dict[str, str]:
    """Provide authenticated headers for API requests."""
    return {"X-API-Key": api_key}

