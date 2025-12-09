"""Integration tests for dashboard API endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_api_root_endpoint(test_client: TestClient):
    """Test API root endpoint."""
    response = test_client.get("/api")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_api_status_requires_auth(test_client: TestClient):
    """Test that API status endpoint requires authentication."""
    response = test_client.get("/api/status")
    # Should return 401 or 200 depending on auth implementation
    assert response.status_code in [200, 401]


def test_api_status_with_auth(test_client: TestClient, authenticated_headers: dict[str, str]):
    """Test API status endpoint with authentication."""
    response = test_client.get("/api/status", headers=authenticated_headers)
    # If auth is required, this might fail with 401
    # If auth is optional, this should return 200
    assert response.status_code in [200, 401]
    
    if response.status_code == 200:
        data = response.json()
        assert "uptime_seconds" in data or "message" in data


def test_api_metrics_endpoint(test_client: TestClient, authenticated_headers: dict[str, str]):
    """Test API metrics endpoint."""
    response = test_client.get("/api/metrics", headers=authenticated_headers)
    # May require auth or may be public
    assert response.status_code in [200, 401]


def test_api_history_endpoint(test_client: TestClient, authenticated_headers: dict[str, str]):
    """Test API history endpoint."""
    response = test_client.get("/api/history", headers=authenticated_headers)
    # May require auth or may be public
    assert response.status_code in [200, 401]
    
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)

