"""Configuration and fixtures for E2E tests."""

import os

import pytest
from fastapi.testclient import TestClient

from codeflow_engine.server import create_app


@pytest.fixture(scope="module")
def e2e_client():
    """Create E2E test client."""
    app = create_app()
    return TestClient(app)


@pytest.fixture(scope="module")
def e2e_engine():
    """Create E2E test engine."""
    from codeflow_engine.engine import CodeFlowEngine
    return CodeFlowEngine()


@pytest.fixture
def deployment_url() -> str:
    """Get deployment URL from environment."""
    return os.getenv("DEPLOYMENT_URL", "http://localhost:8000")

