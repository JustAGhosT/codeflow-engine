"""
CodeFlow Engine Utility Modules

Core utilities for logging, error handling, resilience, and other common operations.

Modules:
- logging: Structured logging configuration
- error_handlers: Standardized error handling patterns
- resilience: Circuit breaker and retry patterns
- volume_utils: Volume management utilities
"""

from typing import Any

# Logging utilities
get_logger: Any = None
log_with_context: Any = None
setup_logging: Any = None
try:
    from codeflow_engine.utils.logging import (
        get_logger,
        log_with_context,
        setup_logging,
    )
except ImportError:
    pass

# Resilience utilities
CircuitBreaker: type[Any] | None = None
CircuitBreakerOpenError: type[Any] | None = None
CircuitBreakerState: type[Any] | None = None
try:
    from codeflow_engine.utils.resilience import (
        CircuitBreaker,
        CircuitBreakerOpenError,
        CircuitBreakerState,
    )
except ImportError:
    pass

# Error handling utilities
handle_operation_error: Any = None
handle_workflow_error: Any = None
try:
    from codeflow_engine.utils.error_handlers import (
        handle_operation_error,
        handle_workflow_error,
    )
except ImportError:
    pass

__all__ = [
    # Logging
    "get_logger",
    "log_with_context",
    "setup_logging",
    # Resilience
    "CircuitBreaker",
    "CircuitBreakerOpenError",
    "CircuitBreakerState",
    # Error handling
    "handle_operation_error",
    "handle_workflow_error",
]
