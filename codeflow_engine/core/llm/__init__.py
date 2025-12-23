"""
Core LLM Module - Base classes and utilities for LLM providers.

This module provides:
- BaseLLMProvider: Abstract base class for all LLM providers
- OpenAICompatibleProvider: Template for OpenAI API-compatible providers
- LLMProviderRegistry: Dynamic provider registration (Open/Closed principle)
- ResponseExtractor: Common response extraction utilities (DRY)
"""

from codeflow_engine.core.llm.base import BaseLLMProvider
from codeflow_engine.core.llm.registry import LLMProviderRegistry
from codeflow_engine.core.llm.response import LLMResponse, ResponseExtractor
from codeflow_engine.core.llm.openai_compatible import OpenAICompatibleProvider

__all__ = [
    "BaseLLMProvider",
    "LLMProviderRegistry",
    "LLMResponse",
    "OpenAICompatibleProvider",
    "ResponseExtractor",
]
