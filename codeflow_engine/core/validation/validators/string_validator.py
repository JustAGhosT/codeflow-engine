"""
String Type Validator.

Validates string inputs for security threats and format requirements.
"""

import html
import re
from typing import Any

from codeflow_engine.core.validation.base import BaseTypeValidator
from codeflow_engine.core.validation.result import ValidationResult, ValidationSeverity
from codeflow_engine.core.validation.patterns import SecurityPatterns


class StringTypeValidator(BaseTypeValidator):
    """
    Validator for string values.

    Performs:
    - Length validation
    - Security threat detection (SQL injection, XSS, command injection)
    - HTML entity sanitization
    - Format validation (email, URL)
    """

    def __init__(
        self,
        max_length: int = 1000,
        security_patterns: SecurityPatterns | None = None,
    ) -> None:
        """
        Initialize the string validator.

        Args:
            max_length: Maximum allowed string length
            security_patterns: Optional custom security patterns
        """
        super().__init__(security_patterns)
        self.max_length = max_length

    def can_validate(self, value: Any) -> bool:
        """Check if this validator handles the value type."""
        return isinstance(value, str)

    def validate(self, key: str, value: Any) -> ValidationResult:
        """Validate a string value."""
        if not isinstance(value, str):
            return ValidationResult.failure(
                f"Expected string for '{key}', got {type(value).__name__}",
                ValidationSeverity.MEDIUM,
            )

        # Length validation
        if len(value) > self.max_length:
            return ValidationResult.failure(
                f"String too long for key '{key}': {len(value)} > {self.max_length}",
                ValidationSeverity.MEDIUM,
            )

        # Security threat check
        threat_result = self._check_security_threats(key, value)
        if not threat_result.is_valid:
            return threat_result

        # Sanitize HTML entities
        sanitized_value = html.escape(value)

        # Format validation for special keys
        format_result = self._validate_format(key, sanitized_value)
        if not format_result.is_valid:
            return format_result

        return ValidationResult.success({"value": sanitized_value})

    def _validate_format(self, key: str, value: str) -> ValidationResult:
        """Validate format for special field types."""
        key_lower = key.lower()

        if "email" in key_lower and not self._is_valid_email(value):
            return ValidationResult.failure(
                f"Invalid email format in '{key}'",
                ValidationSeverity.MEDIUM,
            )

        if "url" in key_lower and not self._is_valid_url(value):
            return ValidationResult.failure(
                f"Invalid URL format in '{key}'",
                ValidationSeverity.MEDIUM,
            )

        return ValidationResult.success()

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email format."""
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_pattern, email))

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """Validate URL format."""
        url_pattern = r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$"
        return bool(re.match(url_pattern, url))
