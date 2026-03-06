"""Core Validation Module."""

from codeflow_engine.core.validation.base import BaseTypeValidator
from codeflow_engine.core.validation.composite import CompositeValidator
from codeflow_engine.core.validation.patterns import SecurityPatterns
from codeflow_engine.core.validation.result import (
    ValidationResult,
    ValidationSeverity,
    merge_validation_results,
    update_severity,
)

__all__ = [
    "BaseTypeValidator",
    "CompositeValidator",
    "SecurityPatterns",
    "ValidationResult",
    "ValidationSeverity",
    "merge_validation_results",
    "update_severity",
]