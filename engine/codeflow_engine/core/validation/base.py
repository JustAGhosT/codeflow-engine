"""Base Type Validator."""

from abc import ABC, abstractmethod
from typing import Any

from codeflow_engine.core.validation.patterns import (
    DEFAULT_SECURITY_PATTERNS,
    SecurityPatterns,
)
from codeflow_engine.core.validation.result import ValidationResult, ValidationSeverity


class BaseTypeValidator(ABC):
    def __init__(self, security_patterns: SecurityPatterns | None = None) -> None:
        self.security_patterns = security_patterns or DEFAULT_SECURITY_PATTERNS

    @abstractmethod
    def can_validate(self, value: Any) -> bool:
        pass

    @abstractmethod
    def validate(self, key: str, value: Any) -> ValidationResult:
        pass

    def _check_security_threats(self, key: str, value: str) -> ValidationResult:
        has_threat, threat_type = self.security_patterns.check_all_threats(value)
        if has_threat:
            return ValidationResult.failure(
                f"Potential {threat_type} detected in '{key}'",
                ValidationSeverity.CRITICAL,
            )
        return ValidationResult.success()
