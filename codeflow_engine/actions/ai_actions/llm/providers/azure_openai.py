"""
Azure OpenAI Provider for CodeFlow LLM system.

Supports Azure OpenAI endpoints with custom configurations.
Uses OpenAICompatibleProvider as base with Azure-specific initialization.
"""

import logging
import os
from typing import Any

from codeflow_engine.core.llm import OpenAICompatibleProvider, LLMResponse, LLMProviderRegistry

logger = logging.getLogger(__name__)


class AzureOpenAIProvider(OpenAICompatibleProvider):
    """
    Azure OpenAI provider implementation.

    Extends OpenAICompatibleProvider with Azure-specific configuration:
    - Azure endpoint
    - API version
    - Deployment name
    """

    DEFAULT_MODEL = "gpt-35-turbo"
    LIBRARY_NAME = "openai (Azure)"

    def __init__(self, config: dict[str, Any]) -> None:
        # Azure-specific configuration - set before super().__init__
        self.azure_endpoint = config.get("azure_endpoint") or os.getenv(
            "AZURE_OPENAI_ENDPOINT"
        )
        self.api_version = config.get("api_version", "2024-02-01")
        self.deployment_name = config.get("deployment_name", "gpt-35-turbo")

        # Use Azure-specific API key environment variable
        azure_api_key = config.get("api_key") or os.getenv("AZURE_OPENAI_API_KEY")
        if azure_api_key:
            config["api_key"] = azure_api_key

        # Use deployment name as default model
        config["default_model"] = self.deployment_name

        super().__init__(config)
        self.name = "azure_openai"

    def _initialize_client(self) -> None:
        """Initialize the Azure OpenAI client."""
        if not self.azure_endpoint:
            logger.warning("Azure OpenAI endpoint not configured")
            self.available = False
            return

        try:
            from openai import AzureOpenAI

            self.client = AzureOpenAI(
                api_key=self.api_key,
                api_version=self.api_version,
                azure_endpoint=self.azure_endpoint,
            )
            self.available = True
            logger.info(f"Initialized Azure OpenAI client with endpoint: {self.azure_endpoint}")
        except ImportError:
            logger.debug("openai package not installed")
            self.available = False
        except Exception as e:
            logger.exception(f"Failed to initialize Azure OpenAI client: {e}")
            self.available = False

    def is_available(self) -> bool:
        """Check if Azure OpenAI is properly configured."""
        return bool(self.api_key and self.azure_endpoint and self.client)


# Register with the provider registry
LLMProviderRegistry.register(
    "azure_openai",
    AzureOpenAIProvider,
    default_config={
        "api_key_env": "AZURE_OPENAI_API_KEY",
        "default_model": "gpt-35-turbo",
        "api_version": "2024-02-01",
    },
)
