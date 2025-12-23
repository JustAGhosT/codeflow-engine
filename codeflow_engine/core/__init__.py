"""
CodeFlow Core Module - Shared base classes, utilities, and patterns.

This module provides common infrastructure used across the codeflow_engine package:
- Base classes for managers, validators, and handlers
- Common patterns (Registry, Factory, etc.)
- Configuration utilities
- Shared utilities
"""

from codeflow_engine.core.llm import (
    BaseLLMProvider,
    LLMProviderRegistry,
    LLMResponse,
    OpenAICompatibleProvider,
)

from codeflow_engine.core.managers import (
    BaseManager,
    ManagerConfig,
    SessionMixin,
    StatsMixin,
)

from codeflow_engine.core.validation import (
    BaseTypeValidator,
    CompositeValidator,
    SecurityPatterns,
    ValidationResult,
    ValidationSeverity,
)

from codeflow_engine.core.config import (
    AppSettings,
    BaseConfig,
    ConfigLoader,
    DatabaseSettings,
    LLMSettings,
    LoggingSettings,
    env_var,
    env_bool,
    env_int,
    env_float,
    env_list,
)

from codeflow_engine.core.files import (
    BackupService,
    ContentValidator,
    ContentValidationResult,
    FileBackup,
    FileIO,
)

__all__ = [
    # LLM
    "BaseLLMProvider",
    "LLMProviderRegistry",
    "LLMResponse",
    "OpenAICompatibleProvider",
    # Managers
    "BaseManager",
    "ManagerConfig",
    "SessionMixin",
    "StatsMixin",
    # Validation
    "BaseTypeValidator",
    "CompositeValidator",
    "SecurityPatterns",
    "ValidationResult",
    "ValidationSeverity",
    # Configuration
    "AppSettings",
    "BaseConfig",
    "ConfigLoader",
    "DatabaseSettings",
    "LLMSettings",
    "LoggingSettings",
    "env_var",
    "env_bool",
    "env_int",
    "env_float",
    "env_list",
    # Files
    "BackupService",
    "ContentValidator",
    "ContentValidationResult",
    "FileBackup",
    "FileIO",
]
