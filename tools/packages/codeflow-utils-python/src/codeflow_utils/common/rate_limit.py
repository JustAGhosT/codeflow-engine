"""Rate limiting utilities."""

import time
from collections import defaultdict
from threading import Lock
from typing import Callable, Any


class RateLimiter:
    """Simple rate limiter using token bucket algorithm."""

    def __init__(self, max_calls: int, period: float):
        """
        Initialize rate limiter.

        Args:
            max_calls: Maximum number of calls allowed
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls: list[float] = []
        self.lock = Lock()

    def acquire(self) -> bool:
        """
        Try to acquire a rate limit token.

        Returns:
            True if token acquired, False if rate limit exceeded
        """
        with self.lock:
            now = time.time()

            # Remove old calls outside the period
            self.calls = [call_time for call_time in self.calls if now - call_time < self.period]

            # Check if we can make another call
            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return True

            return False

    def wait_time(self) -> float:
        """
        Get the wait time until next call can be made.

        Returns:
            Wait time in seconds, or 0 if no wait needed
        """
        with self.lock:
            if len(self.calls) < self.max_calls:
                return 0.0

            oldest_call = min(self.calls)
            wait = self.period - (time.time() - oldest_call)
            return max(0.0, wait)


def rate_limit(max_calls: int, period: float):
    """
    Decorator to rate limit function calls.

    Args:
        max_calls: Maximum number of calls allowed
        period: Time period in seconds

    Returns:
        Decorated function with rate limiting
    """
    limiter = RateLimiter(max_calls, period)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not limiter.acquire():
                wait = limiter.wait_time()
                if wait > 0:
                    time.sleep(wait)
                    limiter.acquire()

            return func(*args, **kwargs)

        return wrapper

    return decorator


class PerKeyRateLimiter:
    """Rate limiter that tracks limits per key."""

    def __init__(self, max_calls: int, period: float):
        """
        Initialize per-key rate limiter.

        Args:
            max_calls: Maximum number of calls allowed per key
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.limiters: dict[str, RateLimiter] = defaultdict(
            lambda: RateLimiter(max_calls, period)
        )
        self.lock = Lock()

    def acquire(self, key: str) -> bool:
        """
        Try to acquire a rate limit token for a key.

        Args:
            key: Rate limit key

        Returns:
            True if token acquired, False if rate limit exceeded
        """
        with self.lock:
            return self.limiters[key].acquire()

    def wait_time(self, key: str) -> float:
        """
        Get the wait time for a key.

        Args:
            key: Rate limit key

        Returns:
            Wait time in seconds
        """
        with self.lock:
            return self.limiters[key].wait_time()
