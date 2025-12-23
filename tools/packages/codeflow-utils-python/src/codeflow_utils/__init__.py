"""
codeflow-utils - Shared utility functions for CodeFlow Python applications.

This package provides portable utilities that can be used across CodeFlow projects
without tight coupling to any specific application.

Modules:
    logging: Structured logging utilities
    resilience: Circuit breaker and retry patterns
"""

from codeflow_utils.logging import (
    JsonFormatter,
    TextFormatter,
    get_logger,
    log_with_context,
)
from codeflow_utils.resilience import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerOpenError,
    CircuitBreakerState,
    CircuitBreakerStats,
)

__version__ = "0.1.0"

__all__ = [
    # Logging
    "JsonFormatter",
    "TextFormatter",
    "get_logger",
    "log_with_context",
    # Resilience
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitBreakerOpenError",
    "CircuitBreakerState",
    "CircuitBreakerStats",
]
