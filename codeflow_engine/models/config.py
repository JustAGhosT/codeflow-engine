"""
Configuration Models

This module contains data models for configuration objects used in the CodeFlow system.
"""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, SecretStr, field_validator, model_validator


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


class DatabaseConfig(BaseModel):
    """Database configuration model with validation."""

    url: str
    pool_size: int = Field(default=5, ge=0)
    max_overflow: int = Field(default=10, ge=0)
    echo: bool = False
    ssl_required: bool = True

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v:
            raise ValueError("Database URL cannot be empty")
        # Basic URL validation - must contain ://
        if "://" not in v:
            raise ValueError(
                "Invalid database URL format. Expected format: dialect://user:password@host:port/database"
            )
        return v


class RedisConfig(BaseModel):
    """Redis configuration model with validation."""

    url: str
    max_connections: int = Field(default=10, ge=0)
    ssl: bool = True

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate Redis URL format."""
        if not v:
            raise ValueError("Redis URL cannot be empty")
        # Basic URL validation - must contain ://
        if "://" not in v:
            raise ValueError(
                "Invalid Redis URL format. Expected format: redis://host:port or rediss://host:port"
            )
        return v


class LLMConfig(BaseModel):
    """LLM provider configuration model with validation."""

    provider: str
    api_key: SecretStr | None = None
    model: str  # Required; provider-specific (e.g., gpt-4, claude-3-opus, mistral-large)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, gt=0)

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        """Validate temperature is within sensible range."""
        if not 0.0 <= v <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v


class GitHubConfig(BaseModel):
    """GitHub integration configuration model with secrets protection."""

    token: SecretStr | None = None
    app_id: str | None = None
    private_key: SecretStr | None = None
    webhook_secret: SecretStr | None = None


class WorkflowConfig(BaseModel):
    """Workflow execution configuration model with validation."""

    max_concurrent: int = Field(default=10, gt=0)
    timeout_seconds: int = Field(default=300, gt=0)
    retry_attempts: int = Field(default=3, ge=0)
    retry_delay_seconds: int = Field(default=5, gt=0)

    @field_validator("max_concurrent", "timeout_seconds")
    @classmethod
    def validate_positive(cls, v: int) -> int:
        """Validate that values are positive."""
        if v <= 0:
            raise ValueError("Value must be positive")
        return v


class AppConfig(BaseModel):
    """Main application configuration model."""

    environment: Environment = Environment.DEVELOPMENT
    log_level: LogLevel = LogLevel.INFO
    debug: bool = False
    database: DatabaseConfig | None = None
    redis: RedisConfig | None = None
    llm: LLMConfig | None = None
    github: GitHubConfig | None = None
    workflow: WorkflowConfig = Field(default_factory=WorkflowConfig)
    custom_settings: dict[str, Any] = Field(default_factory=dict)


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
