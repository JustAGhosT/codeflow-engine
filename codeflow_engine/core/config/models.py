"""
Configuration Models.

Centralized configuration models for the codeflow_engine.
Uses dataclasses for simplicity; can be migrated to Pydantic if needed.
"""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from codeflow_engine.core.config.base import (
    BaseConfig,
    env_var,
    env_bool,
    env_int,
    env_float,
)


class Environment(StrEnum):
    """Application environment types."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class LogLevel(StrEnum):
    """Logging levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LoggingSettings(BaseConfig):
    """Logging configuration."""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    json_format: bool = False

    @classmethod
    def from_env(cls, prefix: str = "") -> "LoggingSettings":
        """Load from environment variables."""
        p = f"{prefix}_" if prefix else ""
        return cls(
            level=env_var(f"{p}LOG_LEVEL", "INFO").upper(),
            format=env_var(f"{p}LOG_FORMAT", cls.format),
            json_format=env_bool(f"{p}LOG_JSON"),
        )


@dataclass
class DatabaseSettings(BaseConfig):
    """Database configuration."""

    url: str = "sqlite:///:memory:"
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600
    pool_pre_ping: bool = True
    echo: bool = False
    ssl_required: bool = False

    @classmethod
    def from_env(cls, prefix: str = "") -> "DatabaseSettings":
        """Load from environment variables."""
        p = f"{prefix}_" if prefix else ""
        return cls(
            url=env_var(f"{p}DATABASE_URL", "sqlite:///:memory:"),
            pool_size=env_int(f"{p}DB_POOL_SIZE", 5),
            max_overflow=env_int(f"{p}DB_MAX_OVERFLOW", 10),
            pool_timeout=env_int(f"{p}DB_POOL_TIMEOUT", 30),
            pool_recycle=env_int(f"{p}DB_POOL_RECYCLE", 3600),
            pool_pre_ping=env_bool(f"{p}DB_POOL_PRE_PING", True),
            echo=env_bool(f"{p}DB_ECHO"),
            ssl_required=env_bool(f"{p}DB_SSL_REQUIRED"),
        )


@dataclass
class LLMSettings(BaseConfig):
    """LLM provider configuration."""

    provider: str = "openai"
    api_key: str = ""
    api_key_env: str = ""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4096
    base_url: str | None = None

    @classmethod
    def from_env(cls, prefix: str = "") -> "LLMSettings":
        """Load from environment variables."""
        p = f"{prefix}_" if prefix else ""
        provider = env_var(f"{p}LLM_PROVIDER", "openai")

        # Determine API key env var based on provider
        api_key_env_map = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "groq": "GROQ_API_KEY",
            "mistral": "MISTRAL_API_KEY",
            "azure": "AZURE_OPENAI_API_KEY",
        }
        api_key_env = api_key_env_map.get(provider, f"{provider.upper()}_API_KEY")

        return cls(
            provider=provider,
            api_key=env_var(api_key_env, ""),
            api_key_env=api_key_env,
            model=env_var(f"{p}LLM_MODEL", "gpt-4"),
            temperature=env_float(f"{p}LLM_TEMPERATURE", 0.7),
            max_tokens=env_int(f"{p}LLM_MAX_TOKENS", 4096),
            base_url=env_var(f"{p}LLM_BASE_URL") or None,
        )


@dataclass
class AppSettings(BaseConfig):
    """Main application settings."""

    environment: Environment = Environment.DEVELOPMENT
    debug: bool = False
    app_name: str = "codeflow_engine"
    version: str = "0.1.0"

    logging: LoggingSettings = field(default_factory=LoggingSettings)
    database: DatabaseSettings = field(default_factory=DatabaseSettings)
    llm: LLMSettings = field(default_factory=LLMSettings)

    custom: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_env(cls, prefix: str = "") -> "AppSettings":
        """Load all settings from environment variables."""
        p = f"{prefix}_" if prefix else ""

        env_str = env_var(f"{p}ENVIRONMENT", "development").lower()
        try:
            environment = Environment(env_str)
        except ValueError:
            environment = Environment.DEVELOPMENT

        return cls(
            environment=environment,
            debug=env_bool(f"{p}DEBUG"),
            app_name=env_var(f"{p}APP_NAME", "codeflow_engine"),
            version=env_var(f"{p}VERSION", "0.1.0"),
            logging=LoggingSettings.from_env(prefix),
            database=DatabaseSettings.from_env(prefix),
            llm=LLMSettings.from_env(prefix),
        )

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == Environment.PRODUCTION

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == Environment.DEVELOPMENT

    @property
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.environment == Environment.TESTING
