"""Number Type Validator."""

from typing import Any

from codeflow_engine.core.validation.base import BaseTypeValidator
from codeflow_engine.core.validation.patterns import SecurityPatterns
from codeflow_engine.core.validation.result import ValidationResult, ValidationSeverity


class NumberTypeValidator(BaseTypeValidator):
    INT_MIN = -(2**31)
    INT_MAX = 2**31 - 1
    FLOAT_ABS_MAX = 1e308

    def __init__(self, int_min: int | None = None, int_max: int | None = None, float_abs_max: float | None = None, security_patterns: SecurityPatterns | None = None) -> None:
        super().__init__(security_patterns)
        self.int_min = int_min if int_min is not None else self.INT_MIN
        self.int_max = int_max if int_max is not None else self.INT_MAX
        self.float_abs_max = float_abs_max if float_abs_max is not None else self.FLOAT_ABS_MAX

    def can_validate(self, value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    def validate(self, key: str, value: Any) -> ValidationResult:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return ValidationResult.failure(
                f"Expected number for '{key}', got {type(value).__name__}",
                ValidationSeverity.MEDIUM,
            )
        if isinstance(value, int) and (value < self.int_min or value > self.int_max):
            return ValidationResult.failure(f"Integer out of safe range for key '{key}': {value}", ValidationSeverity.MEDIUM)
        if isinstance(value, float) and abs(value) > self.float_abs_max:
            return ValidationResult.failure(f"Float out of safe range for key '{key}': {value}", ValidationSeverity.MEDIUM)
        return ValidationResult.success({"value": value})