"""
Core Validation Module - Base classes and utilities for input validation.

This module provides:
- SecurityPatterns: Centralized security threat patterns (DRY)
- ValidationResult: Standard validation result structure
- BaseTypeValidator: Abstract base for type-specific validators
- CompositeValidator: Composition-based validator (SOLID principles)
"""

from codeflow_engine.core.validation.patterns import SecurityPatterns
from codeflow_engine.core.validation.result import (
    ValidationResult,
    ValidationSeverity,
    merge_validation_results,
    update_severity,
)
from codeflow_engine.core.validation.base import BaseTypeValidator
from codeflow_engine.core.validation.composite import CompositeValidator

__all__ = [
    "BaseTypeValidator",
    "CompositeValidator",
    "SecurityPatterns",
    "ValidationResult",
    "ValidationSeverity",
    "merge_validation_results",
    "update_severity",
]
