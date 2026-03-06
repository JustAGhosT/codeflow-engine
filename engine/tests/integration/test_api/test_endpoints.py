"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
def test_root_endpoint(test_client: TestClient):
    """Test root endpoint."""
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data or "name" in data


@pytest.mark.integration
def test_favicon_endpoint(test_client: TestClient):
    """Test favicon endpoint."""
    response = test_client.get("/favicon.ico")
    # Should return 204 or 404, not 500
    assert response.status_code in [200, 204, 404]


@pytest.mark.integration
def test_version_endpoint(test_client: TestClient):
    """Test version endpoint."""
    response = test_client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert isinstance(data["version"], str)


@pytest.mark.integration
def test_dashboard_home_endpoint(test_client: TestClient):
    """Test dashboard home endpoint."""
    response = test_client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


@pytest.mark.integration
def test_dashboard_status_endpoint(test_client: TestClient):
    """Test dashboard status endpoint."""
    response = test_client.get("/api/dashboard/status")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


@pytest.mark.integration
def test_dashboard_metrics_endpoint(test_client: TestClient):
    """Test dashboard metrics endpoint."""
    response = test_client.get("/api/dashboard/metrics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


@pytest.mark.integration
def test_dashboard_history_endpoint(test_client: TestClient):
    """Test dashboard history endpoint."""
    response = test_client.get("/api/dashboard/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (dict, list))


@pytest.mark.integration
def test_health_endpoint_with_query_params(test_client: TestClient):
    """Test health endpoint with query parameters."""
    response = test_client.get("/health?detailed=false")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


@pytest.mark.integration
def test_api_error_handling(test_client: TestClient):
    """Test API error handling for invalid endpoints."""
    response = test_client.get("/api/nonexistent")
    assert response.status_code == 404


@pytest.mark.integration
def test_api_response_format(test_client: TestClient):
    """Test that API responses are properly formatted JSON."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)

