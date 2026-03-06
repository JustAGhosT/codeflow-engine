"""
CodeFlow Engine Security Module

Comprehensive security functionality including:
- Authentication and authorization
- Input validation
- Rate limiting
- Encryption utilities
- Exception handling with secure error messages
- Zero-trust security model
"""

from collections.abc import Callable
from typing import Any

# Authorization
EnterpriseAuthorizationManager: type[Any] | None = None
try:
    from codeflow_engine.security.authorization.enterprise_manager import (
        EnterpriseAuthorizationManager,
    )
except ImportError:
    pass

# Authentication
EnterpriseAuthManager: type[Any] | None = None
try:
    from codeflow_engine.security.auth import EnterpriseAuthManager
except ImportError:
    pass


def authenticate(manager: Any, token: str) -> dict[str, Any]:
    """Compatibility wrapper around `EnterpriseAuthManager.verify_token()`."""
    return manager.verify_token(token)


def verify_token(manager: Any, token: str) -> dict[str, Any]:
    """Compatibility wrapper around `EnterpriseAuthManager.verify_token()`."""
    return manager.verify_token(token)


# Rate limiting
RateLimiter: type[Any] | None = None
rate_limit: Callable[..., Any] | None = None
try:
    from codeflow_engine.security.rate_limiting import RateLimiter, rate_limit
except ImportError:
    pass

# Encryption
EnterpriseEncryptionManager: type[Any] | None = None
try:
    from codeflow_engine.security.encryption import EnterpriseEncryptionManager
except ImportError:
    pass


def encrypt(manager: Any, value: str) -> str:
    """Compatibility wrapper around `EnterpriseEncryptionManager.encrypt_data()`."""
    return manager.encrypt_data(value)


def decrypt(manager: Any, value: str) -> str:
    """Compatibility wrapper around `EnterpriseEncryptionManager.decrypt_data()`."""
    return manager.decrypt_data(value)


# Input validation
EnterpriseInputValidator: type[Any] | None = None
try:
    from codeflow_engine.security.input_validation import EnterpriseInputValidator
except ImportError:
    pass


def validate_input(
    validator: Any, data: dict[str, Any], schema: type | None = None
) -> Any:
    """Compatibility wrapper around `EnterpriseInputValidator.validate_input()`."""
    return validator.validate_input(data, schema)


def sanitize_input(
    validator: Any, data: dict[str, Any], schema: type | None = None
) -> dict[str, Any] | None:
    """Return sanitized data from validation results when available."""
    result = validator.validate_input(data, schema)
    return result.sanitized_data


__all__ = [
    # Authorization
    "EnterpriseAuthorizationManager",
    "EnterpriseAuthManager",
    "EnterpriseEncryptionManager",
    "EnterpriseInputValidator",
    # Authentication
    "authenticate",
    "verify_token",
    # Rate limiting
    "RateLimiter",
    "rate_limit",
    # Encryption
    "decrypt",
    "encrypt",
    # Validation
    "sanitize_input",
    "validate_input",
]
