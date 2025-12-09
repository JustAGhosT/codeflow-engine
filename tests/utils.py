"""Test utilities and helpers for CodeFlow Engine tests."""

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, Mock

import pytest


# =============================================================================
# Test Data Helpers
# =============================================================================

def get_test_data_path(filename: str) -> Path:
    """Get path to test data file."""
    return Path(__file__).parent / "fixtures" / filename


def load_test_data(filename: str) -> dict[str, Any]:
    """Load test data from JSON file."""
    path = get_test_data_path(filename)
    if not path.exists():
        raise FileNotFoundError(f"Test data file not found: {path}")
    with open(path) as f:
        return json.load(f)


def create_sample_pr_data(
    repo: str = "test/repo",
    number: int = 123,
    title: str = "Test PR",
    **kwargs: Any,
) -> dict[str, Any]:
    """Create sample PR data for testing."""
    default_data = {
        "repository": repo,
        "number": number,
        "title": title,
        "body": "Test PR description",
        "state": "open",
        "user": {"login": "testuser"},
        "head": {"ref": "feature-branch", "sha": "abc123"},
        "base": {"ref": "main", "sha": "def456"},
        "files": [
            {"filename": "src/main.py", "status": "modified", "additions": 10, "deletions": 5},
        ],
    }
    default_data.update(kwargs)
    return default_data


def create_sample_issue_data(
    repo: str = "test/repo",
    number: int = 1,
    title: str = "Test Issue",
    **kwargs: Any,
) -> dict[str, Any]:
    """Create sample issue data for testing."""
    default_data = {
        "repository": repo,
        "number": number,
        "title": title,
        "body": "Test issue description",
        "state": "open",
        "user": {"login": "testuser"},
        "labels": [],
    }
    default_data.update(kwargs)
    return default_data


def create_sample_workflow_config(
    name: str = "test_workflow",
    triggers: list[str] | None = None,
    actions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Create sample workflow configuration for testing."""
    if triggers is None:
        triggers = ["pr.opened"]
    if actions is None:
        actions = [{"type": "platform_detector"}]
    
    return {
        "name": name,
        "triggers": triggers,
        "actions": actions,
        "enabled": True,
    }


# =============================================================================
# Mock Helpers
# =============================================================================

def create_mock_github_client() -> Mock:
    """Create a mock GitHub client for testing."""
    mock_client = Mock()
    
    # Mock common methods
    mock_client.get_pr.return_value = create_sample_pr_data()
    mock_client.create_issue.return_value = create_sample_issue_data()
    mock_client.post_comment.return_value = {"id": 1, "body": "Test comment"}
    mock_client.get_repository.return_value = {"name": "test-repo", "full_name": "test/repo"}
    
    return mock_client


def create_mock_linear_client() -> Mock:
    """Create a mock Linear client for testing."""
    mock_client = Mock()
    
    # Mock common methods
    mock_client.create_issue.return_value = {
        "id": "test-issue-id",
        "title": "Test Issue",
        "state": "open",
    }
    mock_client.get_team.return_value = {"id": "test-team-id", "name": "Test Team"}
    
    return mock_client


def create_mock_slack_client() -> Mock:
    """Create a mock Slack client for testing."""
    mock_client = Mock()
    
    # Mock common methods
    mock_client.send_message.return_value = {"ok": True, "ts": "1234567890.123456"}
    mock_client.post_webhook.return_value = {"ok": True}
    
    return mock_client


def create_mock_llm_provider() -> Mock:
    """Create a mock LLM provider for testing."""
    mock_provider = Mock()
    
    # Mock common methods
    mock_provider.generate.return_value = "Mocked LLM response"
    mock_provider.generate_stream.return_value = iter(["Mocked", " streamed", " response"])
    mock_provider.estimate_tokens.return_value = 100
    
    return mock_provider


# =============================================================================
# Database Helpers
# =============================================================================

def create_test_database_url() -> str:
    """Create a test database URL."""
    return "postgresql://test:test@localhost:5432/test_codeflow"


def create_test_redis_url() -> str:
    """Create a test Redis URL."""
    return "redis://localhost:6379/1"  # Use DB 1 for tests


# =============================================================================
# Assertion Helpers
# =============================================================================

def assert_pr_data_valid(pr_data: dict[str, Any]) -> None:
    """Assert that PR data has required fields."""
    required_fields = ["repository", "number", "title", "state"]
    for field in required_fields:
        assert field in pr_data, f"Missing required field: {field}"


def assert_issue_data_valid(issue_data: dict[str, Any]) -> None:
    """Assert that issue data has required fields."""
    required_fields = ["repository", "number", "title", "state"]
    for field in required_fields:
        assert field in issue_data, f"Missing required field: {field}"


# =============================================================================
# File Helpers
# =============================================================================

def create_temp_file(content: str, suffix: str = ".py") -> Path:
    """Create a temporary file for testing."""
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False) as f:
        f.write(content)
        return Path(f.name)


def create_temp_directory() -> Path:
    """Create a temporary directory for testing."""
    import tempfile
    return Path(tempfile.mkdtemp())


# =============================================================================
# Async Helpers
# =============================================================================

async def run_async_test(coro) -> Any:
    """Run an async test coroutine."""
    import asyncio
    return await coro


# =============================================================================
# Configuration Helpers
# =============================================================================

def create_test_config(
    environment: str = "testing",
    **overrides: Any,
) -> dict[str, Any]:
    """Create test configuration."""
    config = {
        "environment": environment,
        "debug": True,
        "database": {
            "url": create_test_database_url(),
        },
        "redis": {
            "url": create_test_redis_url(),
        },
        "github": {
            "token": "test_token",
        },
        "llm": {
            "default_provider": "openai",
            "openai_api_key": "test_key",
        },
    }
    config.update(overrides)
    return config

