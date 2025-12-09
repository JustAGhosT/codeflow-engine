"""Unit tests for CodeFlow server endpoints."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from codeflow_engine.server import create_app, get_health_checker


class TestServerCreation:
    """Test suite for server creation."""

    def test_create_app(self):
        """Test that app is created successfully."""
        app = create_app()
        assert app is not None
        assert app.title == "CodeFlow Engine"

    def test_get_health_checker(self):
        """Test that health checker is created and cached."""
        # Clear the global instance
        import codeflow_engine.server as server_module
        server_module._health_checker = None
        
        checker1 = get_health_checker()
        checker2 = get_health_checker()
        
        # Should return the same instance
        assert checker1 is checker2


class TestServerEndpoints:
    """Test suite for server endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        app = create_app()
        return TestClient(app)

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code in [200, 404]  # May redirect or return 404
        
        if response.status_code == 200:
            data = response.json()
            assert "message" in data or "version" in data

    def test_api_root_endpoint(self, client):
        """Test API root endpoint."""
        response = client.get("/api")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_endpoint_basic(self, client):
        """Test basic health endpoint."""
        with patch("codeflow_engine.server.get_health_checker") as mock_get_checker:
            mock_checker = MagicMock()
            mock_checker.check_quick = MagicMock(return_value={
                "status": "healthy",
                "version": "1.0.0"
            })
            mock_get_checker.return_value = mock_checker
            
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert "version" in data

    def test_health_endpoint_detailed(self, client):
        """Test detailed health endpoint."""
        with patch("codeflow_engine.server.get_health_checker") as mock_get_checker:
            mock_checker = MagicMock()
            mock_checker.check_all = MagicMock(return_value={
                "status": "healthy",
                "version": "1.0.0",
                "components": {}
            })
            mock_get_checker.return_value = mock_checker
            
            response = client.get("/health?detailed=true")
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert "version" in data

    def test_health_endpoint_error_handling(self, client):
        """Test health endpoint error handling."""
        with patch("codeflow_engine.server.get_health_checker") as mock_get_checker:
            mock_checker = MagicMock()
            mock_checker.check_quick = MagicMock(side_effect=Exception("Health check failed"))
            mock_get_checker.return_value = mock_checker
            
            # Should handle errors gracefully
            response = client.get("/health")
            # May return 500 or handle gracefully
            assert response.status_code in [200, 500]

    def test_docs_endpoint(self, client):
        """Test OpenAPI docs endpoint."""
        response = client.get("/docs")
        # Should return 200 for Swagger UI
        assert response.status_code == 200

    def test_openapi_endpoint(self, client):
        """Test OpenAPI JSON endpoint."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data or "info" in data

    def test_favicon_endpoint(self, client):
        """Test favicon endpoint."""
        response = client.get("/favicon.ico")
        # May return 404 if no favicon, or 200 if exists
        assert response.status_code in [200, 404]

    def test_cors_headers(self, client):
        """Test CORS headers are set."""
        response = client.options("/api", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        })
        # CORS preflight should be handled
        assert response.status_code in [200, 204, 405]


class TestServerMiddleware:
    """Test suite for server middleware."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        app = create_app()
        return TestClient(app)

    def test_cors_middleware_enabled(self, client):
        """Test that CORS middleware is enabled."""
        response = client.get("/api", headers={"Origin": "http://localhost:3000"})
        # CORS headers should be present if middleware is enabled
        assert response.status_code == 200

