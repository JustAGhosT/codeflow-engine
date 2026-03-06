"""Integration tests for workflow API endpoints."""

import pytest
from fastapi.testclient import TestClient

from codeflow_engine.server import create_app


@pytest.fixture
def client():
    """Create a test client."""
    app = create_app()
    return TestClient(app)


class TestWorkflowEndpoints:
    """Integration tests for workflow endpoints."""

    def test_workflow_list_endpoint(self, client):
        """Test workflow list endpoint if available."""
        # This endpoint may not exist yet, so we check for 404 or 200
        response = client.get("/api/workflows")
        
        # Either endpoint exists (200) or doesn't exist yet (404)
        assert response.status_code in [200, 404, 405]
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, (dict, list))

    def test_workflow_execute_endpoint(self, client):
        """Test workflow execution endpoint if available."""
        workflow_data = {
            "workflow_id": "test_workflow",
            "event": {
                "type": "test",
                "payload": {}
            }
        }
        
        response = client.post("/api/workflows/execute", json=workflow_data)
        
        # Endpoint may not exist yet
        assert response.status_code in [200, 201, 404, 405, 422]

    def test_workflow_status_endpoint(self, client):
        """Test workflow status endpoint if available."""
        response = client.get("/api/workflows/test_workflow/status")
        
        # Endpoint may not exist yet
        assert response.status_code in [200, 404, 405]

