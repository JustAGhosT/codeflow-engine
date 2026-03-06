"""
Number Type Validator.

Validates numeric inputs for safe ranges.
"""

from typing import Any

from codeflow_engine.core.validation.base import BaseTypeValidator
from codeflow_engine.core.validation.result import ValidationResult, ValidationSeverity
from codeflow_engine.core.validation.patterns import SecurityPatterns


class NumberTypeValidator(BaseTypeValidator):
    """
    Validator for numeric values (int and float).

    Performs:
    - Integer range validation (within 32-bit signed range)
    - Float range validation (within safe float range)
    """

    # Safe ranges for numeric types
    INT_MIN = -(2**31)
    INT_MAX = 2**31 - 1
    FLOAT_ABS_MAX = 1e308

    def __init__(
        self,
        int_min: int | None = None,
        int_max: int | None = None,
        float_abs_max: float | None = None,
        security_patterns: SecurityPatterns | None = None,
    ) -> None:
        """
        Initialize the number validator.

        Args:
            int_min: Minimum integer value (defaults to -(2^31))
            int_max: Maximum integer value (defaults to 2^31-1)
            float_abs_max: Maximum absolute float value (defaults to 1e308)
            security_patterns: Optional custom security patterns
        """
        super().__init__(security_patterns)
        self.int_min = int_min if int_min is not None else self.INT_MIN
        self.int_max = int_max if int_max is not None else self.INT_MAX
        self.float_abs_max = float_abs_max if float_abs_max is not None else self.FLOAT_ABS_MAX

    def can_validate(self, value: Any) -> bool:
        """Check if this validator handles the value type."""
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    def validate(self, key: str, value: Any) -> ValidationResult:
        """Validate a numeric value."""
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return ValidationResult.failure(
                f"Expected number for '{key}', got {type(value).__name__}",
                ValidationSeverity.MEDIUM,
            )

        # Integer range validation
        if isinstance(value, int):
            if value < self.int_min or value > self.int_max:
                return ValidationResult.failure(
                    f"Integer out of safe range for key '{key}': {value}",
                    ValidationSeverity.MEDIUM,
                )

        # Float range validation
        if isinstance(value, float):
            if abs(value) > self.float_abs_max:
                return ValidationResult.failure(
                    f"Float out of safe range for key '{key}': {value}",
                    ValidationSeverity.MEDIUM,
                )

        return ValidationResult.success({"value": value})
