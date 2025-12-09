"""Tests for rate limiting utilities."""

import time
import pytest

from codeflow_utils.common.rate_limit import (
    RateLimiter,
    rate_limit,
    PerKeyRateLimiter,
)


def test_rate_limiter_acquire():
    """Test rate limiter token acquisition."""
    limiter = RateLimiter(max_calls=2, period=1.0)
    
    assert limiter.acquire() is True
    assert limiter.acquire() is True
    assert limiter.acquire() is False  # Rate limit exceeded


def test_rate_limiter_wait_time():
    """Test rate limiter wait time calculation."""
    limiter = RateLimiter(max_calls=1, period=1.0)
    
    limiter.acquire()
    wait = limiter.wait_time()
    
    assert wait > 0
    assert wait <= 1.0


def test_rate_limit_decorator():
    """Test rate limit decorator."""
    call_count = 0
    
    @rate_limit(max_calls=2, period=1.0)
    def test_function():
        nonlocal call_count
        call_count += 1
        return call_count
    
    # First two calls should succeed
    assert test_function() == 1
    assert test_function() == 2
    
    # Third call should wait and then succeed
    result = test_function()
    assert result == 3


def test_per_key_rate_limiter():
    """Test per-key rate limiter."""
    limiter = PerKeyRateLimiter(max_calls=1, period=1.0)
    
    # Different keys can acquire independently
    assert limiter.acquire("key1") is True
    assert limiter.acquire("key2") is True
    
    # Same key is rate limited
    assert limiter.acquire("key1") is False
    assert limiter.acquire("key2") is False

