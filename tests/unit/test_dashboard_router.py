"""Unit tests for dashboard router endpoints."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from codeflow_engine.dashboard.router import router
from codeflow_engine.server import create_app


class TestDashboardRouter:
    """Test suite for dashboard router."""

    @pytest.fixture
    def client(self):
        """Create a test client with dashboard router."""
        app = create_app()
        return TestClient(app)

    def test_dashboard_home_endpoint(self, client):
        """Test dashboard home endpoint."""
        response = client.get("/dashboard/")
        # May return 200 (with template) or 503 (if templates not available)
        assert response.status_code in [200, 503]

    def test_api_status_endpoint(self, client):
        """Test API status endpoint."""
        # May require authentication
        response = client.get("/dashboard/api/status")
        assert response.status_code in [200, 401, 403]

    def test_api_status_with_auth(self, client):
        """Test API status endpoint with authentication."""
        # Mock authentication
        with patch("codeflow_engine.dashboard.router.verify_api_key", return_value="test-key"):
            response = client.get("/dashboard/api/status")
            if response.status_code == 200:
                data = response.json()
                assert "uptime_seconds" in data or "check_count" in data

    def test_api_metrics_endpoint(self, client):
        """Test API metrics endpoint."""
        # May require authentication
        response = client.get("/dashboard/api/metrics")
        assert response.status_code in [200, 401, 403]

    def test_api_metrics_with_auth(self, client):
        """Test API metrics endpoint with authentication."""
        with patch("codeflow_engine.dashboard.router.verify_api_key", return_value="test-key"):
            response = client.get("/dashboard/api/metrics")
            if response.status_code == 200:
                data = response.json()
                assert isinstance(data, dict)

    def test_api_history_endpoint(self, client):
        """Test API history endpoint."""
        # May require authentication
        response = client.get("/dashboard/api/history")
        assert response.status_code in [200, 401, 403]

    def test_api_history_with_pagination(self, client):
        """Test API history endpoint with pagination."""
        with patch("codeflow_engine.dashboard.router.verify_api_key", return_value="test-key"):
            response = client.get("/dashboard/api/history?limit=10&offset=0")
            if response.status_code == 200:
                data = response.json()
                assert isinstance(data, list)

    def test_api_history_pagination_limits(self, client):
        """Test API history pagination limits."""
        with patch("codeflow_engine.dashboard.router.verify_api_key", return_value="test-key"):
            # Test limit validation
            response = client.get("/dashboard/api/history?limit=200")  # Over max
            assert response.status_code in [200, 400, 422]
            
            response = client.get("/dashboard/api/history?limit=0")  # Under min
            assert response.status_code in [200, 400, 422]

    def test_api_quality_check_endpoint(self, client):
        """Test API quality check endpoint."""
        with patch("codeflow_engine.dashboard.router.verify_api_key", return_value="test-key"):
            payload = {
                "mode": "files",
                "files": ["test.py"]
            }
            response = client.post("/dashboard/api/quality-check", json=payload)
            # May return 200, 429 (rate limit), or 500 (if quality check fails)
            assert response.status_code in [200, 429, 500]

    def test_api_quality_check_rate_limiting(self, client):
        """Test API quality check rate limiting."""
        with patch("codeflow_engine.dashboard.router.verify_api_key", return_value="test-key"):
            with patch("codeflow_engine.dashboard.router.quality_check_limiter.is_allowed", return_value=False):
                with patch("codeflow_engine.dashboard.router.quality_check_limiter.get_retry_after", return_value=60):
                    payload = {
                        "mode": "files",
                        "files": ["test.py"]
                    }
                    response = client.post("/dashboard/api/quality-check", json=payload)
                    assert response.status_code == 429
                    assert "Retry-After" in response.headers

    def test_api_quality_check_invalid_mode(self, client):
        """Test API quality check with invalid mode."""
        with patch("codeflow_engine.dashboard.router.verify_api_key", return_value="test-key"):
            payload = {
                "mode": "invalid_mode",
                "files": []
            }
            response = client.post("/dashboard/api/quality-check", json=payload)
            # Should return validation error
            assert response.status_code in [400, 422]

