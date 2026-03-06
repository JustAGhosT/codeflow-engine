"""
Object Validator - Backwards compatibility module.

This module re-exports from codeflow_engine.core.validation for backwards compatibility.
New code should import directly from codeflow_engine.core.validation.validators.
"""

# Re-export from core for backwards compatibility
from codeflow_engine.core.validation.validators import ObjectTypeValidator
from codeflow_engine.core.validation import ValidationResult, ValidationSeverity


# Legacy alias for backwards compatibility
ObjectValidator = ObjectTypeValidator

__all__ = ["ObjectValidator", "ObjectTypeValidator", "ValidationResult", "ValidationSeverity"]
