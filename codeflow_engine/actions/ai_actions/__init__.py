"""
CodeFlow Engine - AI Actions

Actions for AI/LLM-powered features including AutoGen, memory systems, and summarization.
"""

from typing import Any

# Import with error handling for optional dependencies
AutoGenImplementation: type[Any] | None = None
try:
    from codeflow_engine.actions.ai_actions.autogen_implementation import AutoGenImplementation
except ImportError:
    pass

AutoGenAgentSystem: type[Any] | None = None
try:
    from codeflow_engine.actions.ai_actions.autogen_multi_agent import AutoGenAgentSystem
except ImportError:
    pass

Mem0MemoryManager: type[Any] | None = None
try:
    from codeflow_engine.actions.ai_actions.mem0_memory_integration import Mem0MemoryManager
except ImportError:
    pass

LearningMemorySystem: type[Any] | None = None
try:
    from codeflow_engine.actions.ai_actions.learning_memory_system import LearningMemorySystem
except ImportError:
    pass

ConfigurableLLMProvider: type[Any] | None = None
try:
    from codeflow_engine.actions.ai_actions.configurable_llm_provider import ConfigurableLLMProvider
except ImportError:
    pass

# Submodule exports with guarded imports
autogen = None
try:
    from codeflow_engine.actions.ai_actions import autogen
except (ImportError, OSError):
    pass

llm = None
try:
    from codeflow_engine.actions.ai_actions import llm
except (ImportError, OSError):
    pass

__all__ = [
    "AutoGenAgentSystem",
    "AutoGenImplementation",
    "ConfigurableLLMProvider",
    "LearningMemorySystem",
    "Mem0MemoryManager",
    "autogen",
    "llm",
]
