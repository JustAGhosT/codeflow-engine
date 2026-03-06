"""Tests for validation utilities."""

import os
from unittest.mock import patch

import pytest

from codeflow_utils.validation import (
    validate_config,
    validate_environment_variables,
    sanitize_input,
    validate_input,
    validate_url,
    is_valid_url,
)


def test_validate_config():
    """Test configuration validation."""
    config = {"key1": "value1", "key2": "value2"}
    is_valid, missing = validate_config(config, ["key1", "key2"])
    assert is_valid
    assert len(missing) == 0
    
    is_valid, missing = validate_config(config, ["key1", "key3"])
    assert not is_valid
    assert "key3" in missing


def test_validate_config_invalid_type():
    """Test configuration validation with invalid type."""
    is_valid, missing = validate_config("not a dict", ["key1"])
    assert not is_valid
    assert len(missing) > 0


def test_validate_environment_variables():
    """Test environment variable validation."""
    with patch.dict(os.environ, {"TEST_VAR": "test_value"}, clear=False):
        result = validate_environment_variables(["TEST_VAR"])
        assert result["valid"]
        assert len(result["missing"]) == 0
        assert "TEST_VAR" in result["found"]
    
    with patch.dict(os.environ, {}, clear=True):
        result = validate_environment_variables(["MISSING_VAR"])
        assert not result["valid"]
        assert "MISSING_VAR" in result["missing"]


def test_sanitize_input():
    """Test input sanitization."""
    assert sanitize_input("  test  ") == "test"
    assert sanitize_input("test\x00null") == "testnull"
    assert sanitize_input("test" * 10, max_length=10) == "test" * 2 + "te"


def test_validate_input():
    """Test input validation."""
    is_valid, error = validate_input("test", str)
    assert is_valid
    assert error is None
    
    is_valid, error = validate_input(123, str)
    assert not is_valid
    assert error is not None
    
    is_valid, error = validate_input(None, str, required=False)
    assert is_valid
    
    is_valid, error = validate_input(None, str, required=True)
    assert not is_valid


def test_validate_url():
    """Test URL validation."""
    is_valid, error = validate_url("https://example.com")
    assert is_valid
    assert error is None
    
    is_valid, error = validate_url("invalid-url")
    assert not is_valid
    assert error is not None
    
    is_valid, error = validate_url("https://example.com", schemes=["https"])
    assert is_valid
    
    is_valid, error = validate_url("http://example.com", schemes=["https"])
    assert not is_valid


def test_is_valid_url():
    """Test is_valid_url helper."""
    assert is_valid_url("https://example.com")
    assert not is_valid_url("invalid-url")
    assert is_valid_url("https://example.com", schemes=["https"])
    assert not is_valid_url("http://example.com", schemes=["https"])

