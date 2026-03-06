"""OpenAI-Compatible Provider Template."""

import logging
from typing import Any

from codeflow_engine.core.llm.base import BaseLLMProvider
from codeflow_engine.core.llm.response import LLMResponse, ResponseExtractor

logger = logging.getLogger(__name__)


class OpenAICompatibleProvider(BaseLLMProvider):
    DEFAULT_MODEL: str = "gpt-4"
    LIBRARY_NAME: str = "openai"
    CLIENT_CLASS_PATH: str = "openai.OpenAI"

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.client: Any = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        try:
            import openai

            self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
            self.available = True
        except ImportError:
            logger.debug(f"{self.LIBRARY_NAME} package not installed")
            self.available = False

    def _get_default_model(self) -> str:
        return self.default_model or self.DEFAULT_MODEL

    def _prepare_messages(self, messages: list[dict[str, Any]]) -> list[dict[str, str]]:
        return ResponseExtractor.filter_messages(messages)

    def _make_api_call(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int | None,
        **kwargs: Any,
    ) -> Any:
        call_params: dict[str, Any] = {
            "model": str(model),
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            call_params["max_tokens"] = max_tokens
        for key in ["top_p", "frequency_penalty", "presence_penalty", "stop"]:
            if key in kwargs and kwargs[key] is not None:
                call_params[key] = kwargs[key]
        return self.client.chat.completions.create(**call_params)

    def _extract_response(self, response: Any, model: str) -> LLMResponse:
        content, finish_reason, usage = ResponseExtractor.extract_openai_response(
            response
        )
        return LLMResponse(
            content=str(content),
            model=str(getattr(response, "model", model)),
            finish_reason=str(finish_reason),
            usage=usage,
        )

    def complete(self, request: dict[str, Any]) -> LLMResponse:
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
            prepared_messages = self._prepare_messages(messages)
            if not prepared_messages:
                return LLMResponse.from_error("No valid messages provided", model)
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
            return self._extract_response(response, model)
        except Exception as e:
            return self._create_error_response(e, request, self._get_default_model())
