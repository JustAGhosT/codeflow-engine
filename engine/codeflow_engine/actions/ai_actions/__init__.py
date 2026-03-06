"""CodeFlow Engine - AI Actions."""

from codeflow_engine.actions.autogen_implementation import AutoGenImplementation
from codeflow_engine.actions.autogen_multi_agent import AutoGenAgentSystem
from codeflow_engine.actions._module_aliases import register_module_aliases
from codeflow_engine.actions.configurable_llm_provider import (
    LLMProviderManager as ConfigurableLLMProvider,
)
from codeflow_engine.actions.learning_memory_system import LearningMemorySystem
from codeflow_engine.actions.mem0_memory_integration import Mem0MemoryManager
from codeflow_engine.actions.summarize_pr_with_ai import (
    SummarizePrWithAI as SummarizePRWithAI,
)

from . import autogen, llm

register_module_aliases(
    __name__,
    {
        "autogen_implementation": "codeflow_engine.actions.autogen_implementation",
        "autogen_multi_agent": "codeflow_engine.actions.autogen_multi_agent",
        "configurable_llm_provider": "codeflow_engine.actions.configurable_llm_provider",
        "learning_memory_system": "codeflow_engine.actions.learning_memory_system",
        "mem0_memory_integration": "codeflow_engine.actions.mem0_memory_integration",
        "summarize_pr_with_ai": "codeflow_engine.actions.summarize_pr_with_ai",
    },
)

__all__ = [
    "AutoGenAgentSystem",
    "AutoGenImplementation",
    "ConfigurableLLMProvider",
    "LearningMemorySystem",
    "Mem0MemoryManager",
    "SummarizePRWithAI",
    "autogen",
    "llm",
]
