"""
Anthropic Claude provider implementation.

Uses BaseLLMProvider with Anthropic-specific message handling.
"""

from typing import Any

from codeflow_engine.core.llm import BaseLLMProvider, LLMResponse, LLMProviderRegistry
from codeflow_engine.core.llm.response import ResponseExtractor


class AnthropicProvider(BaseLLMProvider):
    """
    Anthropic Claude provider.

    Anthropic has a different API format than OpenAI, requiring custom
    message conversion and response extraction.
    """

    DEFAULT_MODEL = "claude-3-sonnet-20240229"

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.client: Any = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize the Anthropic client."""
        try:
            import anthropic

            self.client = anthropic.Anthropic(
                api_key=self.api_key, base_url=self.base_url
            )
            self.available = True
        except ImportError:
            self.available = False

    def _convert_messages(self, messages: list[dict[str, Any]]) -> tuple[str, list[dict[str, str]]]:
        """
        Convert messages to Anthropic format, extracting system prompt.

        Args:
            messages: List of message dicts with role and content

        Returns:
            Tuple of (system_prompt, converted_messages)
        """
        system_prompt = ""
        converted_messages: list[dict[str, str]] = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if not content:
                continue

            if role == "system":
                system_prompt += content + "\n"
            else:
                converted_messages.append({"role": role, "content": content})

        return system_prompt.strip(), converted_messages

    def complete(self, request: dict[str, Any]) -> LLMResponse:
        """Complete a chat conversation using Anthropic's API."""
        if not self.client:
            return LLMResponse.from_error(
                "Anthropic client not initialized",
                self.get_model(request, self.DEFAULT_MODEL),
            )

        try:
            messages = request.get("messages", [])
            model = self.get_model(request, self.DEFAULT_MODEL)
            max_tokens = request.get("max_tokens", 1024)
            temperature = request.get("temperature", 0.7)

            # Convert messages to Anthropic format
            system_prompt, converted_messages = self._convert_messages(messages)

            if not converted_messages:
                return LLMResponse.from_error("No valid messages provided", model)

            # Build API call parameters
            api_params: dict[str, Any] = {
                "model": str(model),
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": converted_messages,
            }

            # Only include system if not empty
            if system_prompt:
                api_params["system"] = system_prompt

            # Call the API
            response = self.client.messages.create(**api_params)

            # Extract response using centralized utility
            content, finish_reason, usage = ResponseExtractor.extract_anthropic_response(response)

            return LLMResponse(
                content=content,
                model=str(model),
                finish_reason=finish_reason,
                usage=usage,
            )

        except Exception as e:
            return self._create_error_response(e, request, self.DEFAULT_MODEL)


# Register with the provider registry
LLMProviderRegistry.register(
    "anthropic",
    AnthropicProvider,
    default_config={
        "api_key_env": "ANTHROPIC_API_KEY",
        "default_model": "claude-3-sonnet-20240229",
    },
)
