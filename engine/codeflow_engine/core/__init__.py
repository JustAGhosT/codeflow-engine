"""
CodeFlow Core Module - Shared base classes, utilities, and patterns.

This module provides common infrastructure used across the codeflow_engine package:
- Base classes for managers, validators, and handlers
- Common patterns (Registry, Factory, etc.)
- Configuration utilities
- Shared utilities
"""

from codeflow_engine.core.config import (
    AppSettings,
    BaseConfig,
    ConfigLoader,
    DatabaseSettings,
    LLMSettings,
    LoggingSettings,
    env_bool,
    env_float,
    env_int,
    env_list,
    env_var,
)
from codeflow_engine.core.files import (
    BackupService,
    ContentValidationResult,
    ContentValidator,
    FileBackup,
    FileIO,
)
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

__all__ = [
    "AppSettings",
    "BackupService",
    "BaseConfig",
    "BaseLLMProvider",
    "BaseManager",
    "BaseTypeValidator",
    "CompositeValidator",
    "ConfigLoader",
    "ContentValidationResult",
    "ContentValidator",
    "DatabaseSettings",
    "FileBackup",
    "FileIO",
    "LLMProviderRegistry",
    "LLMResponse",
    "LLMSettings",
    "LoggingSettings",
    "ManagerConfig",
    "OpenAICompatibleProvider",
    "SecurityPatterns",
    "SessionMixin",
    "StatsMixin",
    "ValidationResult",
    "ValidationSeverity",
    "env_bool",
    "env_float",
    "env_int",
    "env_list",
    "env_var",
]
