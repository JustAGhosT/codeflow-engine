"""Composite Validator."""

import re
from typing import Any

import structlog

from codeflow_engine.core.validation.base import BaseTypeValidator
from codeflow_engine.core.validation.patterns import DEFAULT_SECURITY_PATTERNS, SecurityPatterns
from codeflow_engine.core.validation.result import ValidationResult, ValidationSeverity, update_severity

logger = structlog.get_logger(__name__)

MAX_KEY_LENGTH = 100
SAFE_KEY_PATTERN = re.compile(r"^[a-zA-Z0-9_\-\.]+$")


class CompositeValidator:
    def __init__(self, security_patterns: SecurityPatterns | None = None, validators: list[BaseTypeValidator] | None = None) -> None:
        self.security_patterns = security_patterns or DEFAULT_SECURITY_PATTERNS
        self._validators: list[BaseTypeValidator] = validators or []

    def register(self, validator: BaseTypeValidator) -> "CompositeValidator":
        self._validators.append(validator)
        return self

    def unregister(self, validator_type: type[BaseTypeValidator]) -> bool:
        original_count = len(self._validators)
        self._validators = [v for v in self._validators if not isinstance(v, validator_type)]
        return len(self._validators) < original_count

    def validate_input(self, data: dict[str, Any], schema: type | None = None) -> ValidationResult:
        result = ValidationResult(is_valid=True)
        sanitized_data: dict[str, Any] = {}
        try:
            for key, value in data.items():
                if not self._is_safe_key(key):
                    result.add_error(f"Invalid key name: {key}", ValidationSeverity.HIGH)
                    continue
                value_result = self._validate_value(key, value)
                self._merge_result(result, value_result)
                if value_result.is_valid and value_result.sanitized_data is not None:
                    sanitized_data[key] = self._unwrap_sanitized(value_result.sanitized_data)
            if schema and result.is_valid:
                result = self._apply_schema(schema, sanitized_data, result)
            else:
                result.sanitized_data = sanitized_data
            self._log_validation_result(result, data)
            return result
        except Exception:
            logger.exception("Input validation error")
            return ValidationResult.failure("Validation system error", ValidationSeverity.CRITICAL)

    def _validate_value(self, key: str, value: Any) -> ValidationResult:
        for validator in self._validators:
            if validator.can_validate(value):
                return validator.validate(key, value)
        return ValidationResult.success({"value": value})

    def _is_safe_key(self, key: str) -> bool:
        return bool(SAFE_KEY_PATTERN.match(key)) and len(key) <= MAX_KEY_LENGTH

    def _merge_result(self, target: ValidationResult, source: ValidationResult) -> None:
        if not source.is_valid:
            target.is_valid = False
            target.errors.extend(source.errors)
            target.warnings.extend(source.warnings)
            target.severity = update_severity(target.severity, source.severity)

    def _unwrap_sanitized(self, sanitized_data: dict[str, Any]) -> Any:
        if isinstance(sanitized_data, dict) and len(sanitized_data) == 1 and "value" in sanitized_data:
            return sanitized_data["value"]
        if isinstance(sanitized_data, dict) and "items" in sanitized_data:
            return sanitized_data["items"]
        return sanitized_data

    def _apply_schema(self, schema: type, sanitized_data: dict[str, Any], current_result: ValidationResult) -> ValidationResult:
        try:
            validated = schema(**sanitized_data)
            if hasattr(validated, "dict"):
                current_result.sanitized_data = validated.dict()
            elif hasattr(validated, "model_dump"):
                current_result.sanitized_data = validated.model_dump()
            else:
                current_result.sanitized_data = sanitized_data
        except Exception as e:
            current_result.add_error(f"Schema validation failed: {e!s}", ValidationSeverity.HIGH)
        return current_result

    def _log_validation_result(self, result: ValidationResult, data: dict[str, Any]) -> None:
        if not result.is_valid:
            logger.warning("Input validation failed", errors=result.errors, severity=result.severity.value, data_keys=list(data.keys()))
        else:
            logger.debug("Input validation passed", data_keys=list(data.keys()))