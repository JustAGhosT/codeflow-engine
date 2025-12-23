"""
Array Type Validator.

Validates array/list inputs and their elements.
"""

from typing import Any, Callable

from codeflow_engine.core.validation.base import BaseTypeValidator
from codeflow_engine.core.validation.result import (
    ValidationResult,
    ValidationSeverity,
    update_severity,
)
from codeflow_engine.core.validation.patterns import SecurityPatterns


class ArrayTypeValidator(BaseTypeValidator):
    """
    Validator for array/list values.

    Performs:
    - Length validation
    - Element validation (using provided element validator)
    """

    def __init__(
        self,
        max_length: int = 1000,
        element_validator: Callable[[str, Any], ValidationResult] | None = None,
        security_patterns: SecurityPatterns | None = None,
    ) -> None:
        """
        Initialize the array validator.

        Args:
            max_length: Maximum allowed array length
            element_validator: Optional validator function for array elements
            security_patterns: Optional custom security patterns
        """
        super().__init__(security_patterns)
        self.max_length = max_length
        self._element_validator = element_validator

    def set_element_validator(
        self, validator: Callable[[str, Any], ValidationResult]
    ) -> None:
        """
        Set the validator function for array elements.

        This is used by CompositeValidator to inject the composite's
        _validate_value method for recursive validation.

        Args:
            validator: Function that takes (key, value) and returns ValidationResult
        """
        self._element_validator = validator

    def can_validate(self, value: Any) -> bool:
        """Check if this validator handles the value type."""
        return isinstance(value, (list, tuple))

    def validate(self, key: str, value: Any) -> ValidationResult:
        """Validate an array value."""
        if not isinstance(value, (list, tuple)):
            return ValidationResult.failure(
                f"Expected array for '{key}', got {type(value).__name__}",
                ValidationSeverity.MEDIUM,
            )

        # Length validation
        if len(value) > self.max_length:
            return ValidationResult.failure(
                f"Array too long for key '{key}': {len(value)} > {self.max_length}",
                ValidationSeverity.MEDIUM,
            )

        result = ValidationResult(is_valid=True)
        sanitized_array: list[Any] = []

        for i, item in enumerate(value):
            item_key = f"{key}[{i}]"

            # Validate element
            if self._element_validator:
                item_result = self._element_validator(item_key, item)
            else:
                # Default: pass through
                item_result = ValidationResult.success({"value": item})

            if not item_result.is_valid:
                result.is_valid = False
                result.errors.extend(item_result.errors)
                result.warnings.extend(item_result.warnings)
                result.severity = update_severity(result.severity, item_result.severity)
            else:
                # Unwrap single-value dict wrappers
                sanitized_value = self._unwrap_value(item_result.sanitized_data)
                sanitized_array.append(sanitized_value)

        if result.is_valid:
            result.sanitized_data = {"items": sanitized_array}

        return result

    @staticmethod
    def _unwrap_value(data: dict[str, Any] | None) -> Any:
        """Unwrap single-value dict wrappers from element validation."""
        if data is None:
            return None
        if isinstance(data, dict) and len(data) == 1 and "value" in data:
            return data["value"]
        return data
