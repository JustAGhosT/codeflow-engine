"""Unit tests for Issue Creator action."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from codeflow_engine.actions.issue_creator import (
    IssueCreator,
    IssueCreatorInputs,
    IssueCreatorOutputs,
)


class TestIssueCreatorInputs:
    """Test suite for IssueCreatorInputs."""

    def test_inputs_creation(self):
        """Test creating IssueCreatorInputs."""
        inputs = IssueCreatorInputs(
            repository="test/repo",
            github_issues=[{"title": "Test issue"}],
        )
        assert inputs.repository == "test/repo"
        assert len(inputs.github_issues) == 1
        assert inputs.create_github is True
        assert inputs.create_linear is True

    def test_inputs_defaults(self):
        """Test IssueCreatorInputs with default values."""
        inputs = IssueCreatorInputs(repository="test/repo")
        assert inputs.github_issues == []
        assert inputs.linear_tickets == []
        assert inputs.ai_assignments == {}


class TestIssueCreatorOutputs:
    """Test suite for IssueCreatorOutputs."""

    def test_outputs_creation(self):
        """Test creating IssueCreatorOutputs."""
        outputs = IssueCreatorOutputs(
            success_count=2,
            github_issues_created=[{"number": 1}],
            linear_tickets_created=[{"id": "ticket-1"}],
        )
        assert outputs.success_count == 2
        assert len(outputs.github_issues_created) == 1
        assert len(outputs.linear_tickets_created) == 1


class TestIssueCreator:
    """Test suite for IssueCreator."""

    @pytest.fixture
    def creator(self):
        """Create an IssueCreator instance."""
        with patch.dict("os.environ", {
            "GITHUB_TOKEN": "test-token",
            "LINEAR_API_KEY": "test-linear-key",
        }):
            return IssueCreator()

    def test_creator_initialization(self, creator):
        """Test creator initialization."""
        assert creator is not None
        assert creator.github_token == "test-token"
        assert creator.linear_token == "test-linear-key"

    def test_create_issues_and_tickets_github_only(self, creator):
        """Test creating GitHub issues only."""
        inputs = IssueCreatorInputs(
            repository="test/repo",
            github_issues=[{
                "title": "Test issue",
                "body": "Test body",
                "labels": ["bug"],
            }],
            create_github=True,
            create_linear=False,
        )
        
        with patch.object(creator, '_create_github_issue', return_value={"number": 1, "url": "https://github.com/test/repo/issues/1"}):
            result = creator.create_issues_and_tickets(inputs)
            assert result.success_count == 1
            assert len(result.github_issues_created) == 1
            assert len(result.linear_tickets_created) == 0

    def test_create_issues_and_tickets_linear_only(self, creator):
        """Test creating Linear tickets only."""
        inputs = IssueCreatorInputs(
            repository="test/repo",
            linear_tickets=[{
                "title": "Test ticket",
                "description": "Test description",
                "priority": 2,
            }],
            create_github=False,
            create_linear=True,
        )
        
        with patch.object(creator, '_create_linear_ticket', return_value={"id": "ticket-1", "number": 1}):
            result = creator.create_issues_and_tickets(inputs)
            assert result.success_count == 1
            assert len(result.github_issues_created) == 0
            assert len(result.linear_tickets_created) == 1

    def test_create_issues_and_tickets_error_handling(self, creator):
        """Test error handling when creating issues."""
        inputs = IssueCreatorInputs(
            repository="test/repo",
            github_issues=[{"title": "Test issue"}],
        )
        
        with patch.object(creator, '_create_github_issue', side_effect=Exception("API error")):
            result = creator.create_issues_and_tickets(inputs)
            assert result.success_count == 0
            assert len(result.errors) == 1
            assert "Failed to create GitHub issue" in result.errors[0]

    @patch('codeflow_engine.actions.issue_creator.requests.post')
    def test_create_github_issue_success(self, mock_post, creator):
        """Test successful GitHub issue creation."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "number": 123,
            "html_url": "https://github.com/test/repo/issues/123",
            "title": "Test issue",
            "labels": [{"name": "bug"}],
            "created_at": "2025-01-01T00:00:00Z",
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        issue_data = {
            "title": "Test issue",
            "body": "Test body",
            "labels": ["bug"],
        }
        
        with patch.object(creator, '_add_ai_specific_comments'):
            result = creator._create_github_issue(issue_data, "test/repo")
            assert result["number"] == 123
            assert "url" in result

    @patch('codeflow_engine.actions.issue_creator.requests.post')
    def test_create_github_issue_api_error(self, mock_post, creator):
        """Test GitHub issue creation with API error."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("API error")
        mock_post.return_value = mock_response
        
        issue_data = {"title": "Test issue", "body": "Test body"}
        
        with pytest.raises(requests.HTTPError):
            creator._create_github_issue(issue_data, "test/repo")

    @patch('codeflow_engine.actions.issue_creator.requests.post')
    def test_create_linear_ticket_success(self, mock_post, creator):
        """Test successful Linear ticket creation."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "issueCreate": {
                    "success": True,
                    "issue": {
                        "id": "ticket-123",
                        "number": 123,
                        "url": "https://linear.app/ticket-123",
                        "title": "Test ticket",
                        "priority": 2,
                        "labels": {"nodes": [{"name": "bug"}]},
                        "team": {"name": "development"},
                    }
                }
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        ticket_data = {
            "title": "Test ticket",
            "description": "Test description",
            "priority": 2,
        }
        
        with patch.object(creator, '_get_team_id', return_value="team-id"):
            with patch.object(creator, '_get_label_ids', return_value=["label-id"]):
                with patch.object(creator, '_notify_charlie_linear'):
                    result = creator._create_linear_ticket(ticket_data)
                    assert result["id"] == "ticket-123"
                    assert result["number"] == 123

    @patch('codeflow_engine.actions.issue_creator.requests.post')
    def test_create_linear_ticket_graphql_error(self, mock_post, creator):
        """Test Linear ticket creation with GraphQL error."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "errors": [{"message": "GraphQL error"}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        ticket_data = {"title": "Test ticket", "description": "Test"}
        
        with patch.object(creator, '_get_team_id', return_value="team-id"):
            with patch.object(creator, '_get_label_ids', return_value=[]):
                with pytest.raises(Exception, match="Linear API error"):
                    creator._create_linear_ticket(ticket_data)

    def test_notify_ai_tool_charlie(self, creator):
        """Test notifying Charlie AI tool."""
        github_issues = []
        linear_tickets = [{"labels": ["typescript"], "url": "https://linear.app/ticket-1", "title": "TS issue"}]
        
        with patch.object(creator, '_send_slack_notification'):
            result = creator._notify_charlie("key", github_issues, linear_tickets)
            assert result["ai_tool"] == "charlie"
            assert result["status"] == "notified"

    def test_notify_ai_tool_snyk(self, creator):
        """Test notifying Snyk."""
        github_issues = [{"labels": ["security"]}]
        linear_tickets = []
        
        result = creator._notify_snyk("key", github_issues, linear_tickets)
        assert result["ai_tool"] == "snyk"
        assert result["status"] == "scan_triggered"

    def test_notify_ai_tool_unknown(self, creator):
        """Test notifying unknown AI tool."""
        result = creator._notify_ai_tool("key", "unknown_tool", [], [])
        assert result["status"] == "no_notification_method"

    def test_get_team_id(self, creator):
        """Test getting Linear team ID."""
        team_id = creator._get_team_id("frontend")
        assert team_id == "team_frontend_id"
        
        team_id_default = creator._get_team_id("unknown")
        assert team_id_default == "team_dev_id"

    def test_get_label_ids(self, creator):
        """Test getting Linear label IDs."""
        label_ids = creator._get_label_ids(["typescript", "security"])
        assert len(label_ids) == 2
        assert all(isinstance(id, str) for id in label_ids)

