"""
LLM Response types and extraction utilities.

This module centralizes response handling to eliminate duplication across providers.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class LLMResponse:
    """Response from an LLM provider."""

    content: str
    model: str
    finish_reason: str
    usage: dict[str, int] | None = None
    error: str | None = None

    @classmethod
    def from_error(cls, error: str, model: str = "unknown") -> "LLMResponse":
        """Create an error response."""
        return cls(content="", model=model, finish_reason="error", error=error)


class ResponseExtractor:
    """
    Utility class for extracting responses from various LLM API formats.

    Centralizes response extraction logic to eliminate duplication (DRY principle).
    """

    @staticmethod
    def extract_openai_response(response: Any, default_model: str = "unknown") -> tuple[str, str, dict[str, int] | None]:
        """
        Extract content, finish_reason, and usage from OpenAI-compatible responses.

        Works with: OpenAI, Azure OpenAI, Groq, Perplexity, Together AI.

        Args:
            response: The API response object
            default_model: Fallback model name if not in response

        Returns:
            Tuple of (content, finish_reason, usage)
        """
        content = ""
        finish_reason = "stop"
        usage = None

        # Extract content and finish_reason from choices
        if hasattr(response, "choices") and response.choices and len(response.choices) > 0:
            choice = response.choices[0]
            if hasattr(choice, "message") and hasattr(choice.message, "content"):
                content = choice.message.content or ""
            finish_reason = getattr(choice, "finish_reason", "stop") or "stop"

        # Extract usage information
        if hasattr(response, "usage") and response.usage:
            if hasattr(response.usage, "dict"):
                usage = response.usage.dict()
            else:
                usage = {
                    "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
                    "completion_tokens": getattr(response.usage, "completion_tokens", 0),
                    "total_tokens": getattr(response.usage, "total_tokens", 0),
                }

        return content, finish_reason, usage

    @staticmethod
    def extract_anthropic_response(response: Any) -> tuple[str, str, dict[str, int] | None]:
        """
        Extract content, finish_reason, and usage from Anthropic responses.

        Args:
            response: The Anthropic API response object

        Returns:
            Tuple of (content, finish_reason, usage)
        """
        content = ""
        if hasattr(response, "content") and response.content:
            content = "\n".join(
                block.text for block in response.content if hasattr(block, "text")
            )

        finish_reason = getattr(response, "stop_reason", "stop")

        usage = None
        if hasattr(response, "usage"):
            response_usage = response.usage
            input_tokens = getattr(response_usage, "input_tokens", 0) if hasattr(response_usage, "input_tokens") else response_usage.get("input_tokens", 0) if isinstance(response_usage, dict) else 0
            output_tokens = getattr(response_usage, "output_tokens", 0) if hasattr(response_usage, "output_tokens") else response_usage.get("output_tokens", 0) if isinstance(response_usage, dict) else 0
            usage = {
                "prompt_tokens": input_tokens,
                "completion_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
            }

        return content, finish_reason, usage

    @staticmethod
    def filter_messages(messages: list[dict[str, Any]]) -> list[dict[str, str]]:
        """
        Filter and normalize messages, removing empty content.

        Args:
            messages: List of message dictionaries

        Returns:
            Filtered list of messages with role and content
        """
        return [
            {"role": msg.get("role", "user"), "content": msg.get("content", "")}
            for msg in messages
            if msg.get("content", "").strip()
        ]
