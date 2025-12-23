"""
Abstract base class for LLM providers.

This module re-exports from codeflow_engine.core.llm for backwards compatibility.
New code should import directly from codeflow_engine.core.llm.
"""

# Re-export from core for backwards compatibility
from codeflow_engine.core.llm.base import BaseLLMProvider

__all__ = ["BaseLLMProvider"]
