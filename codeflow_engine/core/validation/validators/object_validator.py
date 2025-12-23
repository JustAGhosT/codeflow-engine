"""
Object/Dict Type Validator.

Validates dictionary/object inputs and their nested values.
"""

import re
from typing import Any, Callable

from codeflow_engine.core.validation.base import BaseTypeValidator
from codeflow_engine.core.validation.result import (
    ValidationResult,
    ValidationSeverity,
    update_severity,
)
from codeflow_engine.core.validation.patterns import SecurityPatterns


# Constants
MAX_KEY_LENGTH = 100
SAFE_KEY_PATTERN = re.compile(r"^[a-zA-Z0-9_\-\.]+$")


class ObjectTypeValidator(BaseTypeValidator):
    """
    Validator for dictionary/object values.

    Performs:
    - Key name validation
    - Nested value validation (using provided value validator)
    """

    def __init__(
        self,
        value_validator: Callable[[str, Any], ValidationResult] | None = None,
        security_patterns: SecurityPatterns | None = None,
    ) -> None:
        """
        Initialize the object validator.

        Args:
            value_validator: Optional validator function for nested values
            security_patterns: Optional custom security patterns
        """
        super().__init__(security_patterns)
        self._value_validator = value_validator

    def set_value_validator(
        self, validator: Callable[[str, Any], ValidationResult]
    ) -> None:
        """
        Set the validator function for nested values.

        This is used by CompositeValidator to inject the composite's
        _validate_value method for recursive validation.

        Args:
            validator: Function that takes (key, value) and returns ValidationResult
        """
        self._value_validator = validator

    def can_validate(self, value: Any) -> bool:
        """Check if this validator handles the value type."""
        return isinstance(value, dict)

    def validate(self, key: str, value: Any) -> ValidationResult:
        """Validate a dictionary value."""
        if not isinstance(value, dict):
            return ValidationResult.failure(
                f"Expected object for '{key}', got {type(value).__name__}",
                ValidationSeverity.MEDIUM,
            )

        result = ValidationResult(is_valid=True)
        sanitized_object: dict[str, Any] = {}

        for obj_key, obj_value in value.items():
            # Validate nested key name
            if not self._is_safe_key(str(obj_key)):
                result.add_error(
                    f"Invalid nested key name: {key}.{obj_key}",
                    ValidationSeverity.HIGH,
                )
                continue

            nested_key = f"{key}.{obj_key}"

            # Validate nested value
            if self._value_validator:
                obj_result = self._value_validator(nested_key, obj_value)
            else:
                # Default: pass through
                obj_result = ValidationResult.success({"value": obj_value})

            if not obj_result.is_valid:
                result.is_valid = False
                result.errors.extend(obj_result.errors)
                result.warnings.extend(obj_result.warnings)
                result.severity = update_severity(result.severity, obj_result.severity)
            else:
                # Unwrap single-value dict wrappers
                sanitized_value = self._unwrap_value(obj_result.sanitized_data)
                sanitized_object[obj_key] = sanitized_value

        if result.is_valid:
            result.sanitized_data = sanitized_object

        return result

    @staticmethod
    def _is_safe_key(key: str) -> bool:
        """Check if a key name is safe."""
        return bool(SAFE_KEY_PATTERN.match(key)) and len(key) <= MAX_KEY_LENGTH

    @staticmethod
    def _unwrap_value(data: dict[str, Any] | None) -> Any:
        """Unwrap single-value dict wrappers from value validation."""
        if data is None:
            return None
        if isinstance(data, dict) and len(data) == 1 and "value" in data:
            return data["value"]
        return data
