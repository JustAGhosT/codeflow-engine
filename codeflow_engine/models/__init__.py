"""
CodeFlow Engine Models

This package contains data models and schemas used throughout the CodeFlow system.

Modules:
- artifacts: Prototype enhancement artifacts and I/O models
- base: Base model classes and mixins
- config: Configuration-related models
- events: Event and webhook payload models
"""

from typing import Any

# Import artifact models with error handling
EnhancementType: type[Any] | None = None
PrototypeEnhancerInputs: type[Any] | None = None
PrototypeEnhancerOutputs: type[Any] | None = None

try:
    from codeflow_engine.models.artifacts import (
        EnhancementType,
        PrototypeEnhancerInputs,
        PrototypeEnhancerOutputs,
    )
except ImportError:
    pass

__all__ = [
    "EnhancementType",
    "PrototypeEnhancerInputs",
    "PrototypeEnhancerOutputs",
]
