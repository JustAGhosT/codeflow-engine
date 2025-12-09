"""Tests for number formatting utilities."""

import pytest

from codeflow_utils.formatting.number import (
    format_number,
    format_bytes,
    format_percentage,
)


def test_format_number():
    """Test number formatting."""
    assert format_number(1234.56) == "1,234.56"
    assert format_number(1234.56, decimals=0) == "1,235"
    assert format_number(1234567.89, decimals=2) == "1,234,567.89"


def test_format_bytes():
    """Test bytes formatting."""
    assert format_bytes(0) == "0 B"
    assert format_bytes(1024) == "1.00 KB"
    assert format_bytes(1048576) == "1.00 MB"
    assert format_bytes(1024, binary=True) == "1.00 KiB"
    assert format_bytes(1048576, binary=True) == "1.00 MiB"


def test_format_percentage():
    """Test percentage formatting."""
    assert format_percentage(0.5) == "50.0%"
    assert format_percentage(0.123, decimals=2) == "12.30%"
    assert format_percentage(75) == "75.0%"

