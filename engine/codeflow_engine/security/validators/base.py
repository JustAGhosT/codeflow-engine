"""
Enterprise Input Validator.

This module provides the EnterpriseInputValidator class that composes
multiple type validators using the new core validation framework.

The implementation follows composition over inheritance, using the
CompositeValidator pattern from codeflow_engine.core.validation.
"""

from typing import Any

import structlog

# Import from core validation framework
from codeflow_engine.core.validation import (
    CompositeValidator,
    SecurityPatterns,
    ValidationResult,
    ValidationSeverity,
)
from codeflow_engine.core.validation.validators import (
    ArrayTypeValidator,
    FileTypeValidator,
    NumberTypeValidator,
    ObjectTypeValidator,
    StringTypeValidator,
)


logger = structlog.get_logger(__name__)


class EnterpriseInputValidator:
    """
    Enterprise-grade input validation and sanitization.

    This class uses the CompositeValidator pattern from the core validation
    framework, providing a unified interface while leveraging type-specific
    validators.

    The validator automatically:
    - Validates key names for safety
    - Detects and blocks security threats (SQL injection, XSS, etc.)
    - Sanitizes input data
    - Validates against optional Pydantic schemas
    """

    def __init__(
        self,
        max_string_length: int = 10000,
        max_array_length: int = 1000,
        allowed_file_extensions: set[str] | None = None,
    ) -> None:
        """
        Initialize the enterprise validator.

        Args:
            max_string_length: Maximum allowed string length
            max_array_length: Maximum allowed array length
            allowed_file_extensions: Set of allowed file extensions
        """
        self.max_string_length = max_string_length
        self.max_array_length = max_array_length
        self.allowed_file_extensions = allowed_file_extensions or {
            ".txt", ".json", ".yaml", ".yml", ".md"
        }

        # Create custom security patterns with stricter enterprise rules
        self._security_patterns = SecurityPatterns(
            sql_injection=[
                r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
                r"(--|#|/\*|\*/)",
                r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
                r"(\bUNION\s+SELECT\b)",
            ],
            xss=[
                r"<script[^>]*>.*?</script>",
                r"javascript:",
                r"on\w+\s*=",
                r"<iframe[^>]*>.*?</iframe>",
                r"<object[^>]*>.*?</object>",
                r"<embed[^>]*>.*?</embed>",
            ],
            command_injection=[
                r"[;&|`$(){}[\]\\]",
                r"\b(rm|del|format|shutdown|reboot|halt)\b",
                r"(>|>>|<|\|)",
            ],
        )

        # Initialize type validators
        string_validator = StringTypeValidator(
            max_length=max_string_length,
            security_patterns=self._security_patterns,
        )
        number_validator = NumberTypeValidator(
            security_patterns=self._security_patterns,
        )
        array_validator = ArrayTypeValidator(
            max_length=max_array_length,
            security_patterns=self._security_patterns,
        )
        object_validator = ObjectTypeValidator(
            security_patterns=self._security_patterns,
        )
        file_validator = FileTypeValidator(
            allowed_extensions=self.allowed_file_extensions,
            security_patterns=self._security_patterns,
        )

        # Create composite validator with all type validators
        self._composite = CompositeValidator(
            security_patterns=self._security_patterns,
            validators=[
                string_validator,
                number_validator,
                array_validator,
                object_validator,
                file_validator,
            ],
        )

        # Wire up recursive validation for nested structures
        array_validator.set_element_validator(self._composite._validate_value)
        object_validator.set_value_validator(self._composite._validate_value)

    def validate_input(
        self, data: dict[str, Any], schema: type | None = None
    ) -> ValidationResult:
        """
        Comprehensive input validation.

        Args:
            data: Dictionary of input data to validate
            schema: Optional Pydantic model for schema validation

        Returns:
            ValidationResult with validation outcome and sanitized data
        """
        return self._composite.validate_input(data, schema)

    def validate_file_upload(
        self, filename: str, content: bytes, max_size: int = 10 * 1024 * 1024
    ) -> ValidationResult:
        """
        Validate file upload.

        Args:
            filename: The uploaded file name
            content: The file content as bytes
            max_size: Maximum allowed file size in bytes

        Returns:
            ValidationResult with validation outcome
        """
        file_validator = FileTypeValidator(
            allowed_extensions=self.allowed_file_extensions,
            max_size=max_size,
            security_patterns=self._security_patterns,
        )
        return file_validator.validate_file_upload(filename, content)

    # Backward compatibility methods for existing code

    def _is_safe_key(self, key: str) -> bool:
        """Check if key name is safe. Delegates to composite validator."""
        return self._composite._is_safe_key(key)

    def _validate_value(self, key: str, value: Any) -> ValidationResult:
        """Validate individual value. Delegates to composite validator."""
        return self._composite._validate_value(key, value)

    # Legacy pattern access for tests/backward compatibility
    @property
    def SQL_INJECTION_PATTERNS(self) -> list[str]:
        """Get SQL injection patterns for backward compatibility."""
        return self._security_patterns.sql_injection

    @property
    def XSS_PATTERNS(self) -> list[str]:
        """Get XSS patterns for backward compatibility."""
        return self._security_patterns.xss

    @property
    def COMMAND_INJECTION_PATTERNS(self) -> list[str]:
        """Get command injection patterns for backward compatibility."""
        return self._security_patterns.command_injection
