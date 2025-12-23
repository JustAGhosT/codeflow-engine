"""
OpenAI GPT provider implementation.

Uses the OpenAICompatibleProvider base class for common functionality.
"""

from typing import Any

from codeflow_engine.core.llm import OpenAICompatibleProvider, LLMProviderRegistry


class OpenAIProvider(OpenAICompatibleProvider):
    """
    OpenAI GPT provider.

    Inherits all common functionality from OpenAICompatibleProvider.
    """

    DEFAULT_MODEL = "gpt-4"
    LIBRARY_NAME = "openai"

    def _initialize_client(self) -> None:
        """Initialize the OpenAI client."""
        try:
            import openai

            self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
            self.available = True
        except ImportError:
            self.available = False


# Register with the provider registry
LLMProviderRegistry.register(
    "openai",
    OpenAIProvider,
    default_config={
        "api_key_env": "OPENAI_API_KEY",
        "default_model": "gpt-4",
    },
)
