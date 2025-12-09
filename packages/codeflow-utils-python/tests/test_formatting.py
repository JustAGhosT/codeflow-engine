"""Tests for formatting utilities."""

from datetime import datetime, timedelta

import pytest

from codeflow_utils.formatting.date import (
    format_datetime,
    format_iso_datetime,
    format_relative_time,
)


def test_format_datetime():
    """Test datetime formatting."""
    dt = datetime(2025, 1, 15, 10, 30, 45)
    formatted = format_datetime(dt)
    assert "2025-01-15" in formatted
    assert "10:30:45" in formatted
    
    custom_format = format_datetime(dt, "%Y/%m/%d")
    assert custom_format == "2025/01/15"


def test_format_iso_datetime():
    """Test ISO datetime formatting."""
    dt = datetime(2025, 1, 15, 10, 30, 45)
    formatted = format_iso_datetime(dt)
    assert formatted.startswith("2025-01-15T10:30:45")


def test_format_relative_time():
    """Test relative time formatting."""
    now = datetime.now()
    
    # Just now
    assert format_relative_time(now) == "just now"
    
    # Minutes ago
    two_minutes_ago = now - timedelta(minutes=2)
    assert "minute" in format_relative_time(two_minutes_ago)
    
    # Hours ago
    two_hours_ago = now - timedelta(hours=2)
    assert "hour" in format_relative_time(two_hours_ago)
    
    # Days ago
    two_days_ago = now - timedelta(days=2)
    assert "day" in format_relative_time(two_days_ago)
    
    # Future time
    future = now + timedelta(minutes=5)
    assert "in" in format_relative_time(future, now)

