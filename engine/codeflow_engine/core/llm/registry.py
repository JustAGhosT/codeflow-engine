"""LLM Provider Registry."""

import logging
from typing import Any, TypeVar

from codeflow_engine.core.llm.base import BaseLLMProvider

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseLLMProvider)


class LLMProviderRegistry:
    _providers: dict[str, type[BaseLLMProvider]] = {}
    _default_configs: dict[str, dict[str, Any]] = {}

    @classmethod
    def register(cls, name: str, provider_class: type[BaseLLMProvider], default_config: dict[str, Any] | None = None) -> None:
        cls._providers[name.lower()] = provider_class
        if default_config:
            cls._default_configs[name.lower()] = default_config
        logger.debug(f"Registered LLM provider: {name}")

    @classmethod
    def unregister(cls, name: str) -> bool:
        name_lower = name.lower()
        if name_lower in cls._providers:
            del cls._providers[name_lower]
            cls._default_configs.pop(name_lower, None)
            return True
        return False

    @classmethod
    def create(cls, name: str, config: dict[str, Any] | None = None) -> BaseLLMProvider | None:
        name_lower = name.lower()
        provider_class = cls._providers.get(name_lower)
        if provider_class is None:
            logger.warning(f"Provider '{name}' not found in registry")
            return None
        default_config = cls._default_configs.get(name_lower, {})
        merged_config = {**default_config, **(config or {})}
        try:
            return provider_class(merged_config)
        except Exception as e:
            logger.exception(f"Failed to create provider '{name}': {e}")
            return None

    @classmethod
    def get_provider_class(cls, name: str) -> type[BaseLLMProvider] | None:
        return cls._providers.get(name.lower())

    @classmethod
    def get_all(cls) -> dict[str, type[BaseLLMProvider]]:
        return cls._providers.copy()

    @classmethod
    def get_default_config(cls, name: str) -> dict[str, Any]:
        return cls._default_configs.get(name.lower(), {}).copy()

    @classmethod
    def is_registered(cls, name: str) -> bool:
        return name.lower() in cls._providers

    @classmethod
    def list_providers(cls) -> list[str]:
        return list(cls._providers.keys())

    @classmethod
    def clear(cls) -> None:
        cls._providers.clear()
        cls._default_configs.clear()