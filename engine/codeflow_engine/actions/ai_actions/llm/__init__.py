"""CODEFLOW LLM Package - compatibility wrapper under grouped actions."""

from codeflow_engine.actions.ai_actions.llm.manager import (
    ActionLLMProviderManager,
    LLMProviderManager,
)
from codeflow_engine.actions.ai_actions.llm.providers import (
    AnthropicProvider,
    AzureOpenAIProvider,
    GroqProvider,
    MISTRAL_AVAILABLE,
    MistralProvider,
    OpenAIProvider,
    PerplexityProvider,
    TogetherAIProvider,
)
from codeflow_engine.actions.ai_actions.llm.types import (
    LLMConfig,
    LLMProviderType,
    LLMResponse,
    Message,
    MessageRole,
)
from codeflow_engine.core.llm import (
    BaseLLMProvider,
    LLMProviderRegistry,
    OpenAICompatibleProvider,
)


def get_llm_provider_manager() -> ActionLLMProviderManager:
    from codeflow_engine.actions.llm import get_llm_provider_manager as get_manager

    return get_manager()


def complete_chat(*args, **kwargs):
    from codeflow_engine.actions.llm import complete_chat as complete

    return complete(*args, **kwargs)


__all__ = [
    "ActionLLMProviderManager",
    "AnthropicProvider",
    "AzureOpenAIProvider",
    "BaseLLMProvider",
    "GroqProvider",
    "LLMConfig",
    "LLMProviderManager",
    "LLMProviderRegistry",
    "LLMProviderType",
    "LLMResponse",
    "MISTRAL_AVAILABLE",
    "Message",
    "MessageRole",
    "MistralProvider",
    "OpenAICompatibleProvider",
    "OpenAIProvider",
    "PerplexityProvider",
    "TogetherAIProvider",
    "complete_chat",
    "get_llm_provider_manager",
]
