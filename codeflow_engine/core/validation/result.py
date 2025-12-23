"""
Validation Result types and utilities.

This module provides the standard ValidationResult class and helper functions
for consistent validation result handling across all validators.
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ValidationSeverity(Enum):
    """Severity levels for validation issues."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Severity ordering for comparisons
SEVERITY_ORDER = {
    ValidationSeverity.LOW: 0,
    ValidationSeverity.MEDIUM: 1,
    ValidationSeverity.HIGH: 2,
    ValidationSeverity.CRITICAL: 3,
}


class ValidationResult(BaseModel):
    """
    Result of input validation.

    Attributes:
        is_valid: Whether the validation passed
        errors: List of error messages
        warnings: List of warning messages
        sanitized_data: Sanitized version of the validated data
        severity: The highest severity of any issue found
    """

    is_valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    sanitized_data: dict[str, Any] | None = None
    severity: ValidationSeverity = ValidationSeverity.LOW

    @classmethod
    def success(cls, sanitized_data: dict[str, Any] | None = None) -> "ValidationResult":
        """Create a successful validation result."""
        return cls(is_valid=True, sanitized_data=sanitized_data)

    @classmethod
    def failure(
        cls,
        error: str,
        severity: ValidationSeverity = ValidationSeverity.MEDIUM,
    ) -> "ValidationResult":
        """Create a failed validation result."""
        return cls(is_valid=False, errors=[error], severity=severity)

    def add_error(self, error: str, severity: ValidationSeverity | None = None) -> None:
        """Add an error to the result and update validity."""
        self.is_valid = False
        self.errors.append(error)
        if severity:
            self.severity = update_severity(self.severity, severity)

    def add_warning(self, warning: str) -> None:
        """Add a warning to the result."""
        self.warnings.append(warning)


def update_severity(
    current: ValidationSeverity, new: ValidationSeverity
) -> ValidationSeverity:
    """
    Update severity to the higher of the two values.

    This helper function eliminates the duplicated severity comparison logic
    that was spread across multiple validators.

    Args:
        current: The current severity level
        new: The new severity level to consider

    Returns:
        The higher of the two severity levels
    """
    if SEVERITY_ORDER[new] > SEVERITY_ORDER[current]:
        return new
    return current


def merge_validation_results(results: list[ValidationResult]) -> ValidationResult:
    """
    Merge multiple validation results into one.

    Args:
        results: List of ValidationResult objects to merge

    Returns:
        A single ValidationResult combining all results
    """
    if not results:
        return ValidationResult(is_valid=True)

    merged = ValidationResult(is_valid=True)

    for result in results:
        if not result.is_valid:
            merged.is_valid = False
        merged.errors.extend(result.errors)
        merged.warnings.extend(result.warnings)
        merged.severity = update_severity(merged.severity, result.severity)

        # Merge sanitized data
        if result.sanitized_data:
            if merged.sanitized_data is None:
                merged.sanitized_data = {}
            merged.sanitized_data.update(result.sanitized_data)

    return merged
