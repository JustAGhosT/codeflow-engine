"""
Base Type Validator.

This module provides the abstract base class for type-specific validators,
following the Single Responsibility Principle.
"""

from abc import ABC, abstractmethod
from typing import Any

from codeflow_engine.core.validation.result import ValidationResult, ValidationSeverity
from codeflow_engine.core.validation.patterns import SecurityPatterns, DEFAULT_SECURITY_PATTERNS


class BaseTypeValidator(ABC):
    """
    Abstract base class for type-specific validators.

    Each validator is responsible for validating a single type of data,
    following the Single Responsibility Principle.

    Subclasses must implement:
    - can_validate(): Check if this validator handles the given type
    - validate(): Perform the validation

    Attributes:
        security_patterns: Security patterns to use for threat detection
    """

    def __init__(self, security_patterns: SecurityPatterns | None = None) -> None:
        """
        Initialize the validator.

        Args:
            security_patterns: Optional custom security patterns. Uses defaults if not provided.
        """
        self.security_patterns = security_patterns or DEFAULT_SECURITY_PATTERNS

    @abstractmethod
    def can_validate(self, value: Any) -> bool:
        """
        Check if this validator can handle the given value type.

        Args:
            value: The value to check

        Returns:
            True if this validator can validate the value
        """

    @abstractmethod
    def validate(self, key: str, value: Any) -> ValidationResult:
        """
        Validate the given value.

        Args:
            key: The key/name of the field being validated
            value: The value to validate

        Returns:
            ValidationResult with validation outcome and sanitized data
        """

    def _check_security_threats(self, key: str, value: str) -> ValidationResult:
        """
        Check for common security threats in a string value.

        This is a helper method that subclasses can use for threat detection.

        Args:
            key: The field key for error messages
            value: The string value to check

        Returns:
            ValidationResult with threat detection outcome
        """
        has_threat, threat_type = self.security_patterns.check_all_threats(value)

        if has_threat:
            return ValidationResult.failure(
                f"Potential {threat_type} detected in '{key}'",
                ValidationSeverity.CRITICAL,
            )

        return ValidationResult.success()
