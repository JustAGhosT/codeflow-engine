"""
Number Validator - Backwards compatibility module.

This module re-exports from codeflow_engine.core.validation for backwards compatibility.
New code should import directly from codeflow_engine.core.validation.validators.
"""

# Re-export from core for backwards compatibility
from codeflow_engine.core.validation.validators import NumberTypeValidator
from codeflow_engine.core.validation import ValidationResult, ValidationSeverity


# Legacy alias for backwards compatibility
NumberValidator = NumberTypeValidator

__all__ = ["NumberValidator", "NumberTypeValidator", "ValidationResult", "ValidationSeverity"]
