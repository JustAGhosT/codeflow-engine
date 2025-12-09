"""Integration tests for health check endpoint."""

import pytest
from fastapi.testclient import TestClient


def test_health_endpoint_basic(test_client: TestClient):
    """Test basic health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data


def test_health_endpoint_detailed(test_client: TestClient):
    """Test detailed health check endpoint."""
    response = test_client.get("/health?detailed=true")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data or "version" in data


def test_health_endpoint_returns_version(test_client: TestClient):
    """Test health endpoint returns version."""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert isinstance(data["version"], str)

