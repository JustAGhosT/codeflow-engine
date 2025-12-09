"""Tests for common utilities."""

import asyncio
import pytest

from codeflow_utils.common.retry import retry


def test_retry_success():
    """Test retry decorator with successful call."""
    call_count = 0
    
    @retry(max_attempts=3)
    def successful_call():
        nonlocal call_count
        call_count += 1
        return "success"
    
    result = successful_call()
    assert result == "success"
    assert call_count == 1


def test_retry_failure():
    """Test retry decorator with failures."""
    call_count = 0
    
    @retry(max_attempts=3, delay=0.1)
    def failing_call():
        nonlocal call_count
        call_count += 1
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        failing_call()
    
    assert call_count == 3


def test_retry_success_after_retry():
    """Test retry decorator that succeeds after retry."""
    call_count = 0
    
    @retry(max_attempts=3, delay=0.1)
    def eventually_successful():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise ValueError("Test error")
        return "success"
    
    result = eventually_successful()
    assert result == "success"
    assert call_count == 2


@pytest.mark.asyncio
async def test_retry_async():
    """Test retry decorator with async function."""
    call_count = 0
    
    @retry(max_attempts=3, delay=0.1)
    async def async_call():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise ValueError("Test error")
        return "success"
    
    result = await async_call()
    assert result == "success"
    assert call_count == 2

