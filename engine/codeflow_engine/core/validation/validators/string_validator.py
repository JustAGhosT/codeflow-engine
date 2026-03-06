"""String Type Validator."""

import html
import re
from typing import Any

from codeflow_engine.core.validation.base import BaseTypeValidator
from codeflow_engine.core.validation.patterns import SecurityPatterns
from codeflow_engine.core.validation.result import ValidationResult, ValidationSeverity


class StringTypeValidator(BaseTypeValidator):
    def __init__(
        self, max_length: int = 1000, security_patterns: SecurityPatterns | None = None
    ) -> None:
        super().__init__(security_patterns)
        self.max_length = max_length

    def can_validate(self, value: Any) -> bool:
        return isinstance(value, str)

    def validate(self, key: str, value: Any) -> ValidationResult:
        if not isinstance(value, str):
            return ValidationResult.failure(
                f"Expected string for '{key}', got {type(value).__name__}",
                ValidationSeverity.MEDIUM,
            )
        if len(value) > self.max_length:
            return ValidationResult.failure(
                f"String too long for key '{key}': {len(value)} > {self.max_length}",
                ValidationSeverity.MEDIUM,
            )
        threat_result = self._check_security_threats(key, value)
        if not threat_result.is_valid:
            return threat_result
        sanitized_value = html.escape(value)
        format_result = self._validate_format(key, sanitized_value)
        if not format_result.is_valid:
            return format_result
        return ValidationResult.success({"value": sanitized_value})

    def _validate_format(self, key: str, value: str) -> ValidationResult:
        key_lower = key.lower()
        if "email" in key_lower and not self._is_valid_email(value):
            return ValidationResult.failure(
                f"Invalid email format in '{key}'", ValidationSeverity.MEDIUM
            )
        if "url" in key_lower and not self._is_valid_url(value):
            return ValidationResult.failure(
                f"Invalid URL format in '{key}'", ValidationSeverity.MEDIUM
            )
        return ValidationResult.success()

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        return bool(
            re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        )

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        return bool(re.match(r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$", url))
