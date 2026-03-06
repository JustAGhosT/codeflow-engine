"""
codeflow-utils - Shared utility functions for CodeFlow Python applications.

This package provides portable utilities that can be used across CodeFlow projects
without tight coupling to any specific application.

Modules:
    logging: Structured logging utilities
    resilience: Circuit breaker and retry patterns
    validation: Input, URL, email, and config validation
    formatting: Date, number, and string formatting
    common: Retry, rate limiting, and error handling
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
from codeflow_utils.validation import (
    validate_config,
    validate_environment_variables,
    sanitize_input,
    validate_input,
    validate_url,
    is_valid_url,
    validate_email,
    is_valid_email,
    extract_email_domain,
    normalize_email,
)
from codeflow_utils.formatting import (
    format_datetime,
    format_iso_datetime,
    format_relative_time,
    format_number,
    format_bytes,
    format_percentage,
    truncate_string,
    slugify,
    camel_to_snake,
    snake_to_camel,
)
from codeflow_utils.common import (
    retry,
    CodeFlowUtilsError,
    format_error_message,
    create_error_response,
    RateLimiter,
    rate_limit,
    PerKeyRateLimiter,
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
    # Validation
    "validate_config",
    "validate_environment_variables",
    "sanitize_input",
    "validate_input",
    "validate_url",
    "is_valid_url",
    "validate_email",
    "is_valid_email",
    "extract_email_domain",
    "normalize_email",
    # Formatting - Date
    "format_datetime",
    "format_iso_datetime",
    "format_relative_time",
    # Formatting - Number
    "format_number",
    "format_bytes",
    "format_percentage",
    # Formatting - String
    "truncate_string",
    "slugify",
    "camel_to_snake",
    "snake_to_camel",
    # Common
    "retry",
    "CodeFlowUtilsError",
    "format_error_message",
    "create_error_response",
    "RateLimiter",
    "rate_limit",
    "PerKeyRateLimiter",
]
