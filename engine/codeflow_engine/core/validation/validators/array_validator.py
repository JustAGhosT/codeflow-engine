"""Array Type Validator."""

from typing import Any, Callable

from codeflow_engine.core.validation.base import BaseTypeValidator
from codeflow_engine.core.validation.patterns import SecurityPatterns
from codeflow_engine.core.validation.result import (
    ValidationResult,
    ValidationSeverity,
    update_severity,
)


class ArrayTypeValidator(BaseTypeValidator):
    def __init__(
        self,
        max_length: int = 1000,
        element_validator: Callable[[str, Any], ValidationResult] | None = None,
        security_patterns: SecurityPatterns | None = None,
    ) -> None:
        super().__init__(security_patterns)
        self.max_length = max_length
        self._element_validator = element_validator

    def set_element_validator(
        self, validator: Callable[[str, Any], ValidationResult]
    ) -> None:
        self._element_validator = validator

    def can_validate(self, value: Any) -> bool:
        return isinstance(value, (list, tuple))

    def validate(self, key: str, value: Any) -> ValidationResult:
        if not isinstance(value, (list, tuple)):
            return ValidationResult.failure(
                f"Expected array for '{key}', got {type(value).__name__}",
                ValidationSeverity.MEDIUM,
            )
        if len(value) > self.max_length:
            return ValidationResult.failure(
                f"Array too long for key '{key}': {len(value)} > {self.max_length}",
                ValidationSeverity.MEDIUM,
            )
        result = ValidationResult(is_valid=True)
        sanitized_array: list[Any] = []
        for i, item in enumerate(value):
            item_key = f"{key}[{i}]"
            item_result = (
                self._element_validator(item_key, item)
                if self._element_validator
                else ValidationResult.success({"value": item})
            )
            if not item_result.is_valid:
                result.is_valid = False
                result.errors.extend(item_result.errors)
                result.warnings.extend(item_result.warnings)
                result.severity = update_severity(result.severity, item_result.severity)
            else:
                sanitized_array.append(self._unwrap_value(item_result.sanitized_data))
        if result.is_valid:
            result.sanitized_data = {"items": sanitized_array}
        return result

    @staticmethod
    def _unwrap_value(data: dict[str, Any] | None) -> Any:
        if data is None:
            return None
        if isinstance(data, dict) and len(data) == 1 and "value" in data:
            return data["value"]
        return data
