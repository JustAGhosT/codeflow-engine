"""Tests for email validation utilities."""

import pytest

from codeflow_utils.validation.email import (
    validate_email,
    is_valid_email,
    extract_email_domain,
    normalize_email,
)


def test_validate_email_valid():
    """Test valid email addresses."""
    assert validate_email("test@example.com") is True
    assert validate_email("user.name@example.co.uk") is True
    assert validate_email("user+tag@example.com") is True
    assert validate_email("user_name@example-domain.com") is True


def test_validate_email_invalid():
    """Test invalid email addresses."""
    assert validate_email("invalid") is False
    assert validate_email("@example.com") is False
    assert validate_email("user@") is False
    assert validate_email("user@.com") is False
    assert validate_email("user..name@example.com") is False
    assert validate_email("") is False
    assert validate_email(None) is False


def test_is_valid_email():
    """Test is_valid_email alias."""
    assert is_valid_email("test@example.com") is True
    assert is_valid_email("invalid") is False


def test_extract_email_domain():
    """Test domain extraction."""
    assert extract_email_domain("test@example.com") == "example.com"
    assert extract_email_domain("user@sub.example.co.uk") == "sub.example.co.uk"
    assert extract_email_domain("invalid") is None


def test_normalize_email():
    """Test email normalization."""
    assert normalize_email("Test@Example.COM") == "test@example.com"
    assert normalize_email("  USER@EXAMPLE.COM  ") == "user@example.com"
    assert normalize_email("invalid") is None

