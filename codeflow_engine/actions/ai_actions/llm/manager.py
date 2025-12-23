"""
LLM Provider Manager - Manages multiple LLM providers with fallback support.

Uses LLMProviderRegistry for dynamic provider creation (Open/Closed principle).
"""

import logging
import os
from typing import Any

from codeflow_engine.core.llm import BaseLLMProvider, LLMProviderRegistry, LLMResponse

# Import providers to trigger their registration
from codeflow_engine.actions.ai_actions.llm import providers as _  # noqa: F401

logger = logging.getLogger(__name__)


class ActionLLMProviderManager:
    """
    Manages multiple LLM providers with fallback support for action-driven use cases.

    Uses LLMProviderRegistry for dynamic provider instantiation, following the
    Open/Closed principle - new providers can be added without modifying this class.
    """

    # Default provider configurations (can be extended via registry)
    DEFAULT_PROVIDER_CONFIGS: dict[str, dict[str, Any]] = {
        "openai": {
            "api_key_env": "OPENAI_API_KEY",
            "default_model": "gpt-4",
        },
        "azure_openai": {
            "api_key_env": "AZURE_OPENAI_API_KEY",
            "default_model": "gpt-5-chat",
            "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            "api_version": "2024-02-01",
            "deployment_name": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-chat"),
        },
        "anthropic": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "default_model": "claude-3-sonnet-20240229",
        },
        "mistral": {
            "api_key_env": "MISTRAL_API_KEY",
            "default_model": "mistral-large-latest",
        },
        "groq": {
            "api_key_env": "GROQ_API_KEY",
            "default_model": "mixtral-8x7b-32768",
        },
        "perplexity": {
            "api_key_env": "PERPLEXITY_API_KEY",
            "default_model": "llama-3.1-sonar-large-128k-online",
        },
        "together": {
            "api_key_env": "TOGETHER_API_KEY",
            "default_model": "meta-llama/Llama-2-70b-chat-hf",
        },
    }

    def __init__(self, config: dict[str, Any], display=None) -> None:
        """
        Initialize the manager with configuration.

        Args:
            config: Configuration dictionary containing:
                - fallback_order: List of provider names to try as fallbacks
                - default_provider: Name of the default provider
                - providers: Dict of provider-specific configurations
            display: Optional display object for user feedback
        """
        self.providers: dict[str, BaseLLMProvider] = {}
        self.fallback_order: list[str] = config.get(
            "fallback_order", ["azure_openai", "openai", "anthropic", "mistral"]
        )
        self.default_provider: str = config.get("default_provider", "azure_openai")
        self.display = display

        # Get user-provided provider configs
        provider_configs: dict[str, dict[str, Any]] = config.get("providers", {})

        # Initialize providers using registry (Open/Closed principle)
        self._initialize_providers(provider_configs)

    def _initialize_providers(self, user_configs: dict[str, dict[str, Any]]) -> None:
        """
        Initialize all registered providers.

        Args:
            user_configs: User-provided configuration overrides
        """
        # Get all providers from registry plus defaults
        provider_names = set(LLMProviderRegistry.list_providers()) | set(self.DEFAULT_PROVIDER_CONFIGS.keys())

        for provider_name in provider_names:
            # Merge configs: defaults -> registry defaults -> user config
            default_config = self.DEFAULT_PROVIDER_CONFIGS.get(provider_name, {})
            registry_config = LLMProviderRegistry.get_default_config(provider_name)
            user_config = user_configs.get(provider_name, {})
            merged_config = {**default_config, **registry_config, **user_config}

            try:
                # Create provider using registry
                provider = LLMProviderRegistry.create(provider_name, merged_config)
                if provider is not None:
                    self.providers[provider_name] = provider
            except Exception as e:
                self._handle_provider_init_error(provider_name, e)

    def _handle_provider_init_error(self, provider_name: str, error: Exception) -> None:
        """Handle provider initialization errors with appropriate logging."""
        logger.debug(f"Failed to initialize {provider_name} provider: {error}")

        # Only show warning if this provider is important
        if provider_name in self.fallback_order or provider_name == self.default_provider:
            if self.display:
                self.display.error.show_warning(
                    f"Provider {provider_name} not available: {error!s}"
                )
            else:
                logger.warning(f"Failed to initialize {provider_name} provider: {error}")

    def get_provider(self, provider_name: str) -> BaseLLMProvider | None:
        """
        Get a provider by name.

        Args:
            provider_name: Name of the provider to retrieve

        Returns:
            The provider instance if found and available, None otherwise
        """
        provider = self.providers.get(provider_name.lower())
        if provider is not None and provider.is_available():
            return provider
        return None

    def get_llm(self, provider_name: str) -> BaseLLMProvider | None:
        """Alias for get_provider to satisfy older code/tests."""
        return self.get_provider(provider_name)

    def complete(self, request: dict[str, Any]) -> LLMResponse:
        """
        Complete a chat conversation using the specified or default provider with fallback.

        Args:
            request: Dictionary containing:
                - provider: Optional provider name to use
                - model: Optional model name
                - messages: List of message dictionaries
                - Other provider-specific parameters

        Returns:
            LLMResponse containing the completion response or error
        """
        request = request.copy()

        # Get the requested provider or use default
        provider_name = request.pop("provider", self.default_provider)
        if not provider_name:
            return LLMResponse.from_error(
                "No provider specified and no default provider configured",
                request.get("model") or "unknown",
            )

        # Try to get the requested provider
        provider = self.get_provider(provider_name)
        if provider is None:
            provider = self._get_fallback_provider(provider_name)

        if provider is None:
            return LLMResponse.from_error(
                f"Provider '{provider_name}' not found or not available, and no fallback providers available",
                request.get("model") or "unknown",
            )

        # Validate request
        if "messages" not in request:
            return LLMResponse.from_error(
                "Missing required field 'messages' in request",
                request.get("model") or "unknown",
            )

        # Set default model if not specified
        if "model" not in request and hasattr(provider, "default_model"):
            request["model"] = provider.default_model

        try:
            return provider.complete(request)
        except Exception as e:
            error_msg = f"Error calling provider '{provider_name}': {e!s}"
            logger.exception(error_msg)
            return LLMResponse.from_error(error_msg, request.get("model") or "unknown")

    def _get_fallback_provider(self, failed_provider: str) -> BaseLLMProvider | None:
        """
        Get a fallback provider when the requested one fails.

        Args:
            failed_provider: Name of the provider that failed

        Returns:
            A working fallback provider or None
        """
        for fallback_name in self.fallback_order:
            if fallback_name != failed_provider:
                fallback_provider = self.get_provider(fallback_name)
                if fallback_provider is not None:
                    logger.info(
                        f"Using fallback provider '{fallback_name}' instead of '{failed_provider}'"
                    )
                    return fallback_provider
        return None

    def get_available_providers(self) -> list[str]:
        """Get list of available providers."""
        return [
            name for name, provider in self.providers.items() if provider.is_available()
        ]

    def get_provider_info(self) -> dict[str, Any]:
        """Get information about all providers."""
        info: dict[str, Any] = {
            "available_providers": self.get_available_providers(),
            "default_provider": self.default_provider,
            "fallback_order": self.fallback_order,
            "providers": {},
        }

        for name, provider in self.providers.items():
            info["providers"][name] = {
                "available": provider.is_available(),
                "default_model": getattr(provider, "default_model", "unknown"),
            }

        return info


# Backward compatibility alias
LLMProviderManager = ActionLLMProviderManager
