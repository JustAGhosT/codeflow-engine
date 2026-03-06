"""
Mistral AI provider implementation.

Uses BaseLLMProvider with Mistral-specific client handling.
"""

from typing import Any

from codeflow_engine.core.llm import BaseLLMProvider, LLMResponse, LLMProviderRegistry
from codeflow_engine.core.llm.response import ResponseExtractor


class MistralProvider(BaseLLMProvider):
    """
    Mistral AI provider.

    Mistral has its own client library with a different API format.
    """

    DEFAULT_MODEL = "mistral-large-latest"

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.client: Any = None
        self._chat_message_class: Any = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize the Mistral client."""
        try:
            from mistralai.client import MistralClient
            from mistralai.models.chat_completion import ChatMessage

            self.client = MistralClient(api_key=self.api_key)
            self._chat_message_class = ChatMessage
            self.available = True
        except ImportError:
            self.available = False

    def _convert_messages(self, messages: list[dict[str, Any]]) -> list[Any]:
        """
        Convert messages to Mistral ChatMessage format.

        Args:
            messages: List of message dicts with role and content

        Returns:
            List of ChatMessage objects
        """
        mistral_messages = []
        for msg in messages:
            role = str(msg.get("role", "user"))
            content = str(msg.get("content", "")).strip()
            if content and self._chat_message_class:
                mistral_messages.append(
                    self._chat_message_class(role=role, content=content)
                )
        return mistral_messages

    def complete(self, request: dict[str, Any]) -> LLMResponse:
        """Complete a chat conversation using Mistral's API."""
        if not self.client:
            return LLMResponse.from_error(
                "Mistral client not initialized",
                self.get_model(request, self.DEFAULT_MODEL),
            )

        try:
            messages = request.get("messages", [])
            model = self.get_model(request, self.DEFAULT_MODEL)
            max_tokens = request.get("max_tokens", 1024)
            temperature = request.get("temperature", 0.7)

            # Convert messages to Mistral format
            mistral_messages = self._convert_messages(messages)

            if not mistral_messages:
                return LLMResponse.from_error("No valid messages provided", model)

            # Check if chat method exists
            chat_method = getattr(self.client, "chat", None)
            if not callable(chat_method):
                return LLMResponse.from_error(
                    "MistralClient has no 'chat' method", model
                )

            # Call the API
            response = chat_method(
                model=str(model),
                messages=mistral_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            # Extract response using centralized utility
            content, finish_reason, usage = ResponseExtractor.extract_openai_response(response)

            return LLMResponse(
                content=str(content),
                model=str(model),
                finish_reason=str(finish_reason),
                usage=usage,
            )

        except Exception as e:
            return self._create_error_response(e, request, self.DEFAULT_MODEL)


# Register with the provider registry
LLMProviderRegistry.register(
    "mistral",
    MistralProvider,
    default_config={
        "api_key_env": "MISTRAL_API_KEY",
        "default_model": "mistral-large-latest",
    },
)
