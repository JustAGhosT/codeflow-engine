"""CodeFlow Engine - Platform Actions."""

from codeflow_engine.actions._module_aliases import register_module_aliases

from .config import PlatformConfigManager
from .detector import PlatformDetector
from .file_analyzer import FileAnalyzer
from .models import PlatformDetectorInputs, PlatformDetectorOutputs
from .multi_platform_integrator import MultiPlatformIntegrator
from .patterns import PlatformPatterns
from .prototype_enhancer import PrototypeEnhancer
from .scoring import PlatformScoringEngine
from .utils import calculate_confidence_score, get_confidence_level

register_module_aliases(
    __name__,
    {
        "config": "codeflow_engine.actions.platform.config",
        "detector": "codeflow_engine.actions.platform.detector",
        "file_analyzer": "codeflow_engine.actions.platform.file_analyzer",
        "inputs": "codeflow_engine.actions.platform_detection.inputs",
        "models": "codeflow_engine.actions.platform.models",
        "multi_platform_integrator": "codeflow_engine.actions.multi_platform_integrator",
        "patterns": "codeflow_engine.actions.platform.patterns",
        "platform_detector": "codeflow_engine.actions.platform_detector",
        "prototype_enhancer": "codeflow_engine.actions.platform.prototype_enhancer",
        "schema": "codeflow_engine.actions.platform.schema",
        "scoring": "codeflow_engine.actions.platform.scoring",
        "utils": "codeflow_engine.actions.platform.utils",
    },
)

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
