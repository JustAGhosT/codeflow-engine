"""
Groq provider implementation.

Uses the OpenAICompatibleProvider base class for common functionality.
"""

from typing import Any

from codeflow_engine.core.llm import OpenAICompatibleProvider, LLMProviderRegistry


class GroqProvider(OpenAICompatibleProvider):
    """
    Groq provider for fast inference.

    Groq uses an OpenAI-compatible API format.
    """

    DEFAULT_MODEL = "mixtral-8x7b-32768"
    LIBRARY_NAME = "groq"

    def _initialize_client(self) -> None:
        """Initialize the Groq client."""
        try:
            from groq import Groq

            self.client = Groq(api_key=self.api_key)
            self.available = True
        except ImportError:
            self.available = False


# Register with the provider registry
LLMProviderRegistry.register(
    "groq",
    GroqProvider,
    default_config={
        "api_key_env": "GROQ_API_KEY",
        "default_model": "mixtral-8x7b-32768",
    },
)
