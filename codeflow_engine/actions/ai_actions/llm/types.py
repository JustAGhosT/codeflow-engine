"""
Base types, enums, and data classes for LLM providers.

This module maintains backwards compatibility while re-exporting LLMResponse from core.
"""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel

# Re-export LLMResponse from core for backwards compatibility
from codeflow_engine.core.llm.response import LLMResponse


class MessageRole(StrEnum):
    """Role of a message in a chat conversation."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(BaseModel):
    """A message in a chat conversation."""

    role: MessageRole
    content: str
    name: str | None = None
    tool_calls: list[dict[str, Any]] | None = None
    tool_call_id: str | None = None


class LLMProviderType(StrEnum):
    """Supported LLM providers."""

    GROQ = "groq"
    MISTRAL = "mistral"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    PERPLEXITY = "perplexity"
    TOGETHER = "together"


class LLMConfig(BaseModel):
    """Configuration for an LLM provider."""

    provider: LLMProviderType
    model: str
    api_key: str | None = None
    base_url: str | None = None
    temperature: float = 0.7
    max_tokens: int | None = None
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: list[str] | None = None


__all__ = [
    "LLMConfig",
    "LLMProviderType",
    "LLMResponse",
    "Message",
    "MessageRole",
]
