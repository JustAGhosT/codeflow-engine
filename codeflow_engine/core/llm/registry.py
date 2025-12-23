"""
LLM Provider Registry - Dynamic provider registration following Open/Closed principle.

This registry allows new providers to be added without modifying existing code.
"""

import logging
from typing import Any, TypeVar

from codeflow_engine.core.llm.base import BaseLLMProvider

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseLLMProvider)


class LLMProviderRegistry:
    """
    Registry for LLM providers following the Open/Closed principle.

    Allows providers to be registered dynamically without modifying manager code.

    Usage:
        # Register a provider
        LLMProviderRegistry.register("openai", OpenAIProvider)

        # Create a provider instance
        provider = LLMProviderRegistry.create("openai", config)

        # Get all registered providers
        providers = LLMProviderRegistry.get_all()
    """

    _providers: dict[str, type[BaseLLMProvider]] = {}
    _default_configs: dict[str, dict[str, Any]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        provider_class: type[BaseLLMProvider],
        default_config: dict[str, Any] | None = None,
    ) -> None:
        """
        Register a provider class with the registry.

        Args:
            name: Unique identifier for the provider (e.g., 'openai', 'anthropic')
            provider_class: The provider class to register
            default_config: Optional default configuration for this provider
        """
        cls._providers[name.lower()] = provider_class
        if default_config:
            cls._default_configs[name.lower()] = default_config
        logger.debug(f"Registered LLM provider: {name}")

    @classmethod
    def unregister(cls, name: str) -> bool:
        """
        Remove a provider from the registry.

        Args:
            name: The provider name to remove

        Returns:
            True if the provider was removed, False if not found
        """
        name_lower = name.lower()
        if name_lower in cls._providers:
            del cls._providers[name_lower]
            cls._default_configs.pop(name_lower, None)
            return True
        return False

    @classmethod
    def create(cls, name: str, config: dict[str, Any] | None = None) -> BaseLLMProvider | None:
        """
        Create a provider instance by name.

        Args:
            name: The provider name to instantiate
            config: Configuration to pass to the provider (merged with defaults)

        Returns:
            Provider instance or None if provider not found
        """
        name_lower = name.lower()
        provider_class = cls._providers.get(name_lower)

        if provider_class is None:
            logger.warning(f"Provider '{name}' not found in registry")
            return None

        # Merge default config with provided config
        default_config = cls._default_configs.get(name_lower, {})
        merged_config = {**default_config, **(config or {})}

        try:
            return provider_class(merged_config)
        except Exception as e:
            logger.exception(f"Failed to create provider '{name}': {e}")
            return None

    @classmethod
    def get_provider_class(cls, name: str) -> type[BaseLLMProvider] | None:
        """
        Get a provider class by name without instantiating it.

        Args:
            name: The provider name

        Returns:
            Provider class or None if not found
        """
        return cls._providers.get(name.lower())

    @classmethod
    def get_all(cls) -> dict[str, type[BaseLLMProvider]]:
        """
        Get all registered providers.

        Returns:
            Dictionary mapping provider names to their classes
        """
        return cls._providers.copy()

    @classmethod
    def get_default_config(cls, name: str) -> dict[str, Any]:
        """
        Get the default configuration for a provider.

        Args:
            name: The provider name

        Returns:
            Default configuration dictionary (empty if none registered)
        """
        return cls._default_configs.get(name.lower(), {}).copy()

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """
        Check if a provider is registered.

        Args:
            name: The provider name to check

        Returns:
            True if the provider is registered
        """
        return name.lower() in cls._providers

    @classmethod
    def list_providers(cls) -> list[str]:
        """
        List all registered provider names.

        Returns:
            List of provider names
        """
        return list(cls._providers.keys())

    @classmethod
    def clear(cls) -> None:
        """Clear all registered providers. Mainly useful for testing."""
        cls._providers.clear()
        cls._default_configs.clear()
