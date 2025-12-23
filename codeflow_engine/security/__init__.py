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
try:
    from codeflow_engine.security.auth import authenticate, verify_token
except ImportError:
    authenticate = None
    verify_token = None

# Rate limiting
try:
    from codeflow_engine.security.rate_limiting import RateLimiter, rate_limit
except ImportError:
    RateLimiter = None
    rate_limit = None

# Encryption
try:
    from codeflow_engine.security.encryption import decrypt, encrypt
except ImportError:
    encrypt = None
    decrypt = None

# Input validation
try:
    from codeflow_engine.security.input_validation import (
        sanitize_input,
        validate_input,
    )
except ImportError:
    validate_input = None
    sanitize_input = None

__all__ = [
    # Authorization
    "EnterpriseAuthorizationManager",
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
