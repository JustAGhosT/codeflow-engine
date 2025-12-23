"""
Validation Models - Backwards compatibility module.

This module re-exports from codeflow_engine.core.validation for backwards compatibility.
New code should import directly from codeflow_engine.core.validation.
"""

# Re-export from core for backwards compatibility
from codeflow_engine.core.validation.result import (
    ValidationResult,
    ValidationSeverity,
)

__all__ = ["ValidationResult", "ValidationSeverity"]
