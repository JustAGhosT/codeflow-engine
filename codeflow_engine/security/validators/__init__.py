"""
Security Validators package - Backwards compatibility module.

This module provides backwards compatibility for existing code.
New code should import directly from codeflow_engine.core.validation.
"""

# Main enterprise validator
from codeflow_engine.security.validators.base import EnterpriseInputValidator

# Re-export core validation framework
from codeflow_engine.core.validation import (
    BaseTypeValidator,
    CompositeValidator,
    SecurityPatterns,
    ValidationResult,
    ValidationSeverity,
)

# Re-export type validators
from codeflow_engine.core.validation.validators import (
    ArrayTypeValidator,
    FileTypeValidator,
    NumberTypeValidator,
    ObjectTypeValidator,
    StringTypeValidator,
)

# Legacy aliases
from codeflow_engine.security.validators.string_validator import StringValidator
from codeflow_engine.security.validators.number_validator import NumberValidator
from codeflow_engine.security.validators.array_validator import ArrayValidator
from codeflow_engine.security.validators.object_validator import ObjectValidator
from codeflow_engine.security.validators.file_validator import FileValidator


__all__ = [
    # Main validator
    "EnterpriseInputValidator",
    # Core framework
    "BaseTypeValidator",
    "CompositeValidator",
    "SecurityPatterns",
    "ValidationResult",
    "ValidationSeverity",
    # Type validators
    "ArrayTypeValidator",
    "FileTypeValidator",
    "NumberTypeValidator",
    "ObjectTypeValidator",
    "StringTypeValidator",
    # Legacy aliases
    "ArrayValidator",
    "FileValidator",
    "NumberValidator",
    "ObjectValidator",
    "StringValidator",
]
