"""Validation Result types and utilities."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ValidationSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


SEVERITY_ORDER = {
    ValidationSeverity.LOW: 0,
    ValidationSeverity.MEDIUM: 1,
    ValidationSeverity.HIGH: 2,
    ValidationSeverity.CRITICAL: 3,
}


class ValidationResult(BaseModel):
    is_valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    sanitized_data: dict[str, Any] | None = None
    severity: ValidationSeverity = ValidationSeverity.LOW

    @classmethod
    def success(cls, sanitized_data: dict[str, Any] | None = None) -> "ValidationResult":
        return cls(is_valid=True, sanitized_data=sanitized_data)

    @classmethod
    def failure(cls, error: str, severity: ValidationSeverity = ValidationSeverity.MEDIUM) -> "ValidationResult":
        return cls(is_valid=False, errors=[error], severity=severity)

    def add_error(self, error: str, severity: ValidationSeverity | None = None) -> None:
        self.is_valid = False
        self.errors.append(error)
        if severity:
            self.severity = update_severity(self.severity, severity)

    def add_warning(self, warning: str) -> None:
        self.warnings.append(warning)


def update_severity(current: ValidationSeverity, new: ValidationSeverity) -> ValidationSeverity:
    if SEVERITY_ORDER[new] > SEVERITY_ORDER[current]:
        return new
    return current


def merge_validation_results(results: list[ValidationResult]) -> ValidationResult:
    if not results:
        return ValidationResult(is_valid=True)
    merged = ValidationResult(is_valid=True)
    for result in results:
        if not result.is_valid:
            merged.is_valid = False
        merged.errors.extend(result.errors)
        merged.warnings.extend(result.warnings)
        merged.severity = update_severity(merged.severity, result.severity)
        if result.sanitized_data:
            if merged.sanitized_data is None:
                merged.sanitized_data = {}
            merged.sanitized_data.update(result.sanitized_data)
    return merged