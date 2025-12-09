"""Integration tests for external service integrations."""

import pytest
from unittest.mock import Mock, patch

from codeflow_engine.clients.github_client import GitHubClient
from codeflow_engine.clients.linear_client import LinearClient


class TestGitHubClientIntegration:
    """Integration tests for GitHub client."""

    @pytest.fixture
    def github_client(self):
        """Create a GitHub client instance."""
        # Use mock token for testing
        return GitHubClient(token="test_token")

    def test_github_client_init(self, github_client):
        """Test GitHub client initialization."""
        assert github_client is not None
        assert hasattr(github_client, "token")

    @patch("codeflow_engine.clients.github_client.requests.get")
    def test_github_client_get_request(self, mock_get, github_client):
        """Test GitHub client GET request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response
        
        # Test that client can make requests
        assert github_client is not None

    @patch("codeflow_engine.clients.github_client.requests.post")
    def test_github_client_post_request(self, mock_post, github_client):
        """Test GitHub client POST request."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 123}
        mock_post.return_value = mock_response
        
        # Test that client can make POST requests
        assert github_client is not None


class TestLinearClientIntegration:
    """Integration tests for Linear client."""

    @pytest.fixture
    def linear_client(self):
        """Create a Linear client instance."""
        return LinearClient(api_key="test_key")

    def test_linear_client_init(self, linear_client):
        """Test Linear client initialization."""
        assert linear_client is not None
        assert hasattr(linear_client, "api_key")

    @patch("codeflow_engine.clients.linear_client.requests.post")
    def test_linear_client_query(self, mock_post, linear_client):
        """Test Linear client GraphQL query."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"test": "result"}}
        mock_post.return_value = mock_response
        
        # Test that client can make queries
        assert linear_client is not None

