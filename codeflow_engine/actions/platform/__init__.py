"""
CodeFlow Engine - Platform Actions

Actions for platform detection, integration, and prototype enhancement.
Includes file analysis and scoring utilities.
"""

from typing import Any

from .config import PlatformConfigManager
from .detector import PlatformDetector
from .file_analyzer import FileAnalyzer
from .models import PlatformDetectorInputs, PlatformDetectorOutputs
from .patterns import PlatformPatterns
from .scoring import PlatformScoringEngine
from .utils import calculate_confidence_score, get_confidence_level

# Import additional platform-related actions with error handling
MultiPlatformIntegrator: type[Any] | None = None
try:
    from codeflow_engine.actions.platform.multi_platform_integrator import (
        MultiPlatformIntegrator,
    )
except ImportError:
    pass

PrototypeEnhancer: type[Any] | None = None
try:
    from codeflow_engine.actions.platform.prototype_enhancer import PrototypeEnhancer
except ImportError:
    pass

__all__ = [
    # Core platform detection
    "FileAnalyzer",
    "PlatformConfigManager",
    "PlatformDetector",
    "PlatformDetectorInputs",
    "PlatformDetectorOutputs",
    "PlatformPatterns",
    "PlatformScoringEngine",
    # Platform integration
    "MultiPlatformIntegrator",
    "PrototypeEnhancer",
    # Utilities
    "calculate_confidence_score",
    "get_confidence_level",
]
