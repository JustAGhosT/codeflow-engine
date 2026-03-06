"""Abstract base class for LLM providers."""

import logging
import os
from abc import ABC, abstractmethod
from typing import Any

from codeflow_engine.core.llm.response import LLMResponse

logger = logging.getLogger(__name__)


class BaseLLMProvider(ABC):
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.api_key = config.get("api_key") or os.getenv(config.get("api_key_env", ""))
        self.base_url = config.get("base_url")
        self.default_model = config.get("default_model")
        self.name = config.get("name", self.__class__.__name__.lower().replace("provider", ""))
        self.available = False

    @abstractmethod
    def complete(self, request: dict[str, Any]) -> LLMResponse:
        pass

    def is_available(self) -> bool:
        return self.available and bool(self.api_key)

    def get_model(self, request: dict[str, Any], fallback: str = "unknown") -> str:
        return request.get("model") or self.default_model or fallback

    def _create_error_response(self, error: Exception | str, request: dict[str, Any], fallback_model: str = "unknown") -> LLMResponse:
        error_msg = str(error) if isinstance(error, Exception) else error
        model = self.get_model(request, fallback_model)
        return LLMResponse.from_error(f"Error calling {self.name} API: {error_msg}", model)