"""
Abstract base class for LLM providers.

Provides common functionality and defines the interface that all providers must implement.
"""

import logging
import os
from abc import ABC, abstractmethod
from typing import Any

from codeflow_engine.core.llm.response import LLMResponse

logger = logging.getLogger(__name__)


class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    This class defines the interface and provides common functionality for all LLM providers.

    Attributes:
        config: Configuration dictionary for the provider
        api_key: API key for authentication
        base_url: Optional custom base URL for the API
        default_model: Default model to use for completions
        name: Human-readable name of the provider
        available: Whether the provider is properly initialized
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialize the provider with configuration.

        Args:
            config: Configuration dictionary containing:
                - api_key: Direct API key (optional)
                - api_key_env: Environment variable name for API key
                - base_url: Custom API base URL (optional)
                - default_model: Default model name
                - name: Provider name (optional, defaults to class name)
        """
        self.config = config
        self.api_key = config.get("api_key") or os.getenv(config.get("api_key_env", ""))
        self.base_url = config.get("base_url")
        self.default_model = config.get("default_model")
        self.name = config.get("name", self.__class__.__name__.lower().replace("provider", ""))
        self.available = False  # Subclasses set this during initialization

    @abstractmethod
    def complete(self, request: dict[str, Any]) -> LLMResponse:
        """
        Complete a chat conversation.

        Args:
            request: Request dictionary containing:
                - messages: List of message dicts with 'role' and 'content'
                - model: Model name (optional, uses default_model if not specified)
                - temperature: Sampling temperature (optional)
                - max_tokens: Maximum tokens in response (optional)
                - Additional provider-specific parameters

        Returns:
            LLMResponse with the completion result or error
        """

    def is_available(self) -> bool:
        """
        Check if the provider is properly configured and available.

        Returns:
            True if the provider can accept requests
        """
        return self.available and bool(self.api_key)

    def get_model(self, request: dict[str, Any], fallback: str = "unknown") -> str:
        """
        Get the model to use from request, config, or fallback.

        Args:
            request: Request dictionary that may contain 'model' key
            fallback: Fallback model name if none specified

        Returns:
            Model name to use
        """
        return request.get("model") or self.default_model or fallback

    def _create_error_response(self, error: Exception | str, request: dict[str, Any], fallback_model: str = "unknown") -> LLMResponse:
        """
        Create an error response with consistent formatting.

        Args:
            error: The error that occurred
            request: The original request
            fallback_model: Fallback model name for the response

        Returns:
            LLMResponse with error information
        """
        error_msg = str(error) if isinstance(error, Exception) else error
        model = self.get_model(request, fallback_model)
        return LLMResponse.from_error(f"Error calling {self.name} API: {error_msg}", model)
