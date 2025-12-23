"""
Configuration Models

This module contains data models for configuration objects used in the CodeFlow system.
"""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class LogLevel(StrEnum):
    """Logging levels for the application."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Environment(StrEnum):
    """Environment types."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


@dataclass
class DatabaseConfig:
    """Database configuration model."""

    url: str
    pool_size: int = 5
    max_overflow: int = 10
    echo: bool = False
    ssl_required: bool = True


@dataclass
class RedisConfig:
    """Redis configuration model."""

    url: str
    max_connections: int = 10
    ssl: bool = True


@dataclass
class LLMConfig:
    """LLM provider configuration model."""

    provider: str
    api_key: str | None = None
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4096


@dataclass
class GitHubConfig:
    """GitHub integration configuration model."""

    token: str | None = None
    app_id: str | None = None
    private_key: str | None = None
    webhook_secret: str | None = None


@dataclass
class WorkflowConfig:
    """Workflow execution configuration model."""

    max_concurrent: int = 10
    timeout_seconds: int = 300
    retry_attempts: int = 3
    retry_delay_seconds: int = 5


@dataclass
class AppConfig:
    """Main application configuration model."""

    environment: Environment = Environment.DEVELOPMENT
    log_level: LogLevel = LogLevel.INFO
    debug: bool = False
    database: DatabaseConfig | None = None
    redis: RedisConfig | None = None
    llm: LLMConfig | None = None
    github: GitHubConfig | None = None
    workflow: WorkflowConfig = field(default_factory=WorkflowConfig)
    custom_settings: dict[str, Any] = field(default_factory=dict)


__all__ = [
    "AppConfig",
    "DatabaseConfig",
    "Environment",
    "GitHubConfig",
    "LLMConfig",
    "LogLevel",
    "RedisConfig",
    "WorkflowConfig",
]
