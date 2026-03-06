"""
LLM Providers package - Individual provider implementations.

All providers auto-register themselves with LLMProviderRegistry on import.
"""

from typing import Any

# Import core components
from codeflow_engine.core.llm import (
    BaseLLMProvider,
    LLMProviderRegistry,
    LLMResponse,
    OpenAICompatibleProvider,
)

# Import providers (they auto-register on import)
from codeflow_engine.actions.ai_actions.llm.providers.openai import OpenAIProvider
from codeflow_engine.actions.ai_actions.llm.providers.anthropic import AnthropicProvider
from codeflow_engine.actions.ai_actions.llm.providers.groq import GroqProvider
from codeflow_engine.actions.ai_actions.llm.providers.azure_openai import AzureOpenAIProvider

# Optional providers with graceful fallback
MistralProvider = None
MISTRAL_AVAILABLE = False
try:
    from codeflow_engine.actions.ai_actions.llm.providers.mistral import MistralProvider
    MISTRAL_AVAILABLE = True
except ImportError:
    pass


# OpenAI-compatible providers that only need a custom base URL
class PerplexityProvider(OpenAICompatibleProvider):
    """
    Perplexity AI provider.

    Uses OpenAI-compatible API with custom base URL.
    """

    DEFAULT_MODEL = "llama-3.1-sonar-large-128k-online"
    LIBRARY_NAME = "perplexity"

    def _initialize_client(self) -> None:
        """Initialize the Perplexity client using OpenAI library."""
        try:
            import openai

            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://api.perplexity.ai",
            )
            self.available = True
        except ImportError:
            self.available = False


class TogetherAIProvider(OpenAICompatibleProvider):
    """
    Together AI provider for open source models.

    Uses OpenAI-compatible API with custom base URL.
    """

    DEFAULT_MODEL = "meta-llama/Llama-2-70b-chat-hf"
    LIBRARY_NAME = "together"

    def _initialize_client(self) -> None:
        """Initialize the Together AI client using OpenAI library."""
        try:
            import openai

            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://api.together.xyz/v1",
            )
            self.available = True
        except ImportError:
            self.available = False


# Register the inline providers
LLMProviderRegistry.register(
    "perplexity",
    PerplexityProvider,
    default_config={
        "api_key_env": "PERPLEXITY_API_KEY",
        "default_model": "llama-3.1-sonar-large-128k-online",
    },
)

LLMProviderRegistry.register(
    "together",
    TogetherAIProvider,
    default_config={
        "api_key_env": "TOGETHER_API_KEY",
        "default_model": "meta-llama/Llama-2-70b-chat-hf",
    },
)


# Export all providers
__all__ = [
    "AnthropicProvider",
    "AzureOpenAIProvider",
    "BaseLLMProvider",
    "GroqProvider",
    "LLMProviderRegistry",
    "LLMResponse",
    "OpenAICompatibleProvider",
    "OpenAIProvider",
    "PerplexityProvider",
    "TogetherAIProvider",
]

# Add MistralProvider if available
if MISTRAL_AVAILABLE and MistralProvider is not None:
    __all__.append("MistralProvider")
