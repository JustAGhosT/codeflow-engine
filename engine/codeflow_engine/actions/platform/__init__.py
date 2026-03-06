"""CodeFlow Engine - Platform Actions."""

from .config import PlatformConfigManager
from .detector import PlatformDetector
from .file_analyzer import FileAnalyzer
from .models import PlatformDetectorInputs, PlatformDetectorOutputs
from .patterns import PlatformPatterns
from .scoring import PlatformScoringEngine
from .utils import calculate_confidence_score, get_confidence_level
from .multi_platform_integrator import MultiPlatformIntegrator
from .prototype_enhancer import PrototypeEnhancer

__all__ = [
    "FileAnalyzer",
    "MultiPlatformIntegrator",
    "PlatformConfigManager",
    "PlatformDetector",
    "PlatformDetectorInputs",
    "PlatformDetectorOutputs",
    "PlatformPatterns",
    "PlatformScoringEngine",
    "PrototypeEnhancer",
    "calculate_confidence_score",
    "get_confidence_level",
]