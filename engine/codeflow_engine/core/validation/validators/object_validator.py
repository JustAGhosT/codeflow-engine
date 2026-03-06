"""Object/Dict Type Validator."""

import re
from typing import Any, Callable

from codeflow_engine.core.validation.base import BaseTypeValidator
from codeflow_engine.core.validation.patterns import SecurityPatterns
from codeflow_engine.core.validation.result import ValidationResult, ValidationSeverity, update_severity

MAX_KEY_LENGTH = 100
SAFE_KEY_PATTERN = re.compile(r"^[a-zA-Z0-9_\-\.]+$")


class ObjectTypeValidator(BaseTypeValidator):
    def __init__(self, value_validator: Callable[[str, Any], ValidationResult] | None = None, security_patterns: SecurityPatterns | None = None) -> None:
        super().__init__(security_patterns)
        self._value_validator = value_validator

    def set_value_validator(self, validator: Callable[[str, Any], ValidationResult]) -> None:
        self._value_validator = validator

    def can_validate(self, value: Any) -> bool:
        return isinstance(value, dict)

    def validate(self, key: str, value: Any) -> ValidationResult:
        if not isinstance(value, dict):
            return ValidationResult.failure(f"Expected object for '{key}', got {type(value).__name__}", ValidationSeverity.MEDIUM)
        result = ValidationResult(is_valid=True)
        sanitized_object: dict[str, Any] = {}
        for obj_key, obj_value in value.items():
            if not self._is_safe_key(str(obj_key)):
                result.add_error(f"Invalid nested key name: {key}.{obj_key}", ValidationSeverity.HIGH)
                continue
            nested_key = f"{key}.{obj_key}"
            obj_result = self._value_validator(nested_key, obj_value) if self._value_validator else ValidationResult.success({"value": obj_value})
            if not obj_result.is_valid:
                result.is_valid = False
                result.errors.extend(obj_result.errors)
                result.warnings.extend(obj_result.warnings)
                result.severity = update_severity(result.severity, obj_result.severity)
            else:
                sanitized_object[obj_key] = self._unwrap_value(obj_result.sanitized_data)
        if result.is_valid:
            result.sanitized_data = sanitized_object
        return result

    @staticmethod
    def _is_safe_key(key: str) -> bool:
        return bool(SAFE_KEY_PATTERN.match(key)) and len(key) <= MAX_KEY_LENGTH

    @staticmethod
    def _unwrap_value(data: dict[str, Any] | None) -> Any:
        if data is None:
            return None
        if isinstance(data, dict) and len(data) == 1 and "value" in data:
            return data["value"]
        return data