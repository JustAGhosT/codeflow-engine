"""
OpenAI-Compatible Provider Template.

This module provides a base class for providers that use the OpenAI API format,
eliminating duplication across OpenAI, Groq, Perplexity, Together AI, and other
compatible providers.
"""

import logging
from typing import Any

from codeflow_engine.core.llm.base import BaseLLMProvider
from codeflow_engine.core.llm.response import LLMResponse, ResponseExtractor

logger = logging.getLogger(__name__)


class OpenAICompatibleProvider(BaseLLMProvider):
    """
    Base class for providers that use the OpenAI API format.

    This template class implements the common patterns shared by:
    - OpenAI
    - Azure OpenAI
    - Groq
    - Perplexity
    - Together AI
    - Any other OpenAI-compatible API

    Subclasses only need to implement:
    - _initialize_client(): Set up the specific client
    - Optionally override _get_default_model() and other hooks
    """

    # Class-level defaults that subclasses can override
    DEFAULT_MODEL: str = "gpt-4"
    LIBRARY_NAME: str = "openai"  # For error messages
    CLIENT_CLASS_PATH: str = "openai.OpenAI"  # For documentation

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the provider."""
        super().__init__(config)
        self.client: Any = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        """
        Initialize the API client.

        Subclasses should override this to set up their specific client.
        Must set self.available = True on success, False on failure.
        """
        try:
            import openai

            self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
            self.available = True
        except ImportError:
            logger.debug(f"{self.LIBRARY_NAME} package not installed")
            self.available = False

    def _get_default_model(self) -> str:
        """Get the default model for this provider."""
        return self.default_model or self.DEFAULT_MODEL

    def _prepare_messages(self, messages: list[dict[str, Any]]) -> list[dict[str, str]]:
        """
        Prepare messages for the API call.

        Override in subclasses that need custom message formatting.

        Args:
            messages: Raw messages from the request

        Returns:
            Formatted messages ready for the API
        """
        return ResponseExtractor.filter_messages(messages)

    def _make_api_call(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int | None,
        **kwargs: Any,
    ) -> Any:
        """
        Make the actual API call.

        Override in subclasses that need custom API call logic.

        Args:
            messages: Prepared messages
            model: Model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters

        Returns:
            Raw API response
        """
        call_params: dict[str, Any] = {
            "model": str(model),
            "messages": messages,
            "temperature": temperature,
        }

        if max_tokens is not None:
            call_params["max_tokens"] = max_tokens

        # Add any additional parameters from kwargs
        for key in ["top_p", "frequency_penalty", "presence_penalty", "stop"]:
            if key in kwargs and kwargs[key] is not None:
                call_params[key] = kwargs[key]

        return self.client.chat.completions.create(**call_params)

    def _extract_response(self, response: Any, model: str) -> LLMResponse:
        """
        Extract the LLMResponse from the API response.

        Override in subclasses that have non-standard response formats.

        Args:
            response: Raw API response
            model: Model used for the request

        Returns:
            LLMResponse object
        """
        content, finish_reason, usage = ResponseExtractor.extract_openai_response(response)

        return LLMResponse(
            content=str(content),
            model=str(getattr(response, "model", model)),
            finish_reason=str(finish_reason),
            usage=usage,
        )

    def complete(self, request: dict[str, Any]) -> LLMResponse:
        """
        Complete a chat conversation using the OpenAI-compatible API.

        Args:
            request: Request dictionary with messages and optional parameters

        Returns:
            LLMResponse with the completion result or error
        """
        if not self.client:
            return LLMResponse.from_error(
                f"{self.name} client not initialized",
                self.get_model(request, self._get_default_model()),
            )

        try:
            messages = request.get("messages", [])
            model = self.get_model(request, self._get_default_model())
            temperature = request.get("temperature", 0.7)
            max_tokens = request.get("max_tokens")

            # Prepare messages (can be overridden by subclasses)
            prepared_messages = self._prepare_messages(messages)

            if not prepared_messages:
                return LLMResponse.from_error("No valid messages provided", model)

            # Make the API call
            response = self._make_api_call(
                messages=prepared_messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=request.get("top_p"),
                frequency_penalty=request.get("frequency_penalty"),
                presence_penalty=request.get("presence_penalty"),
                stop=request.get("stop"),
            )

            # Extract and return the response
            return self._extract_response(response, model)

        except Exception as e:
            return self._create_error_response(e, request, self._get_default_model())
