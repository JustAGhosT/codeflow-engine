"""CodeFlow Engine public package API.

The canonical package lives under ``engine/codeflow_engine`` in the monorepo.
Keep this module lightweight so submodule imports such as
``codeflow_engine.actions.analysis.ai_comment_analyzer`` do not eagerly import
optional runtime dependencies during package initialization.
"""

from __future__ import annotations

import importlib
import logging
import os
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from codeflow_engine.actions.registry import ActionRegistry
    from codeflow_engine.ai.core.base import LLMProvider
    from codeflow_engine.ai.core.providers.manager import LLMProviderManager
    from codeflow_engine.config import CodeFlowConfig
    from codeflow_engine.engine import CodeFlowEngine
    from codeflow_engine.exceptions import (
        ActionError,
        AuthenticationError,
        CodeFlowException,
        CodeFlowPermissionError,
        ConfigurationError,
        IntegrationError,
        LLMProviderError,
        RateLimitError,
        ValidationError,
        WorkflowError,
    )
    from codeflow_engine.integrations.base import Integration
    from codeflow_engine.quality.metrics_collector import MetricsCollector
    from codeflow_engine.security.authorization.enterprise_manager import (
        EnterpriseAuthorizationManager,
    )
    from codeflow_engine.workflows.base import Workflow
    from codeflow_engine.workflows.engine import WorkflowEngine

# Import structlog with error handling
STRUCTLOG_AVAILABLE: bool
try:
    import structlog

    STRUCTLOG_AVAILABLE = True
    structlog_module = cast("Any", structlog)
except ImportError:
    STRUCTLOG_AVAILABLE = False
    structlog_module = None

__version__ = "0.2.0-alpha.1"

_LAZY_EXPORTS = {
    "CodeFlowEngine": "codeflow_engine.engine:CodeFlowEngine",
    "CodeFlowConfig": "codeflow_engine.config:CodeFlowConfig",
    "ActionRegistry": "codeflow_engine.actions.registry:ActionRegistry",
    "LLMProvider": "codeflow_engine.ai.core.base:LLMProvider",
    "LLMProviderManager": "codeflow_engine.ai.core.providers.manager:LLMProviderManager",
    "Integration": "codeflow_engine.integrations.base:Integration",
    "Workflow": "codeflow_engine.workflows.base:Workflow",
    "WorkflowEngine": "codeflow_engine.workflows.engine:WorkflowEngine",
    "MetricsCollector": "codeflow_engine.quality.metrics_collector:MetricsCollector",
    "EnterpriseAuthorizationManager": "codeflow_engine.security.authorization.enterprise_manager:EnterpriseAuthorizationManager",
    "ActionError": "codeflow_engine.exceptions:ActionError",
    "AuthenticationError": "codeflow_engine.exceptions:AuthenticationError",
    "CodeFlowException": "codeflow_engine.exceptions:CodeFlowException",
    "CodeFlowPermissionError": "codeflow_engine.exceptions:CodeFlowPermissionError",
    "ConfigurationError": "codeflow_engine.exceptions:ConfigurationError",
    "IntegrationError": "codeflow_engine.exceptions:IntegrationError",
    "LLMProviderError": "codeflow_engine.exceptions:LLMProviderError",
    "RateLimitError": "codeflow_engine.exceptions:RateLimitError",
    "ValidationError": "codeflow_engine.exceptions:ValidationError",
    "WorkflowError": "codeflow_engine.exceptions:WorkflowError",
}

# Public API exports
__all__ = [
    # Core engine
    "CodeFlowEngine",
    "CodeFlowConfig",
    # Registries
    "ActionRegistry",
    # AI/LLM
    "LLMProvider",
    "LLMProviderManager",
    # Integrations
    "Integration",
    # Workflows
    "Workflow",
    "WorkflowEngine",
    # Quality
    "MetricsCollector",
    # Security
    "EnterpriseAuthorizationManager",
    # Exceptions
    "ActionError",
    "AuthenticationError",
    "CodeFlowException",
    "CodeFlowPermissionError",
    "ConfigurationError",
    "IntegrationError",
    "LLMProviderError",
    "RateLimitError",
    "ValidationError",
    "WorkflowError",
    # Utilities
    "configure_logging",
]


def configure_logging(level: str = "INFO", *, format_json: bool = False) -> None:
    """
    Configure default logging for CodeFlow Engine.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_json: If True and structlog is available, use JSON logging
    """
    if format_json and STRUCTLOG_AVAILABLE and structlog_module:
        # Structured JSON logging
        structlog_module.configure(
            processors=[
                structlog_module.processors.TimeStamper(fmt="iso"),
                structlog_module.processors.add_log_level,
                structlog_module.processors.JSONRenderer(),
            ],
            context_class=dict,
            logger_factory=structlog_module.WriteLoggerFactory(),
            wrapper_class=structlog_module.make_filtering_bound_logger(
                getattr(logging, level.upper())
            ),
            cache_logger_on_first_use=True,
        )
    else:
        # Standard logging
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


def __getattr__(name: str) -> Any:
    """Lazily load public exports to avoid importing optional dependencies."""
    target = _LAZY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module_name, attribute_name = target.split(":", 1)
    try:
        module = importlib.import_module(module_name)
        value = getattr(module, attribute_name)
    except (ImportError, OSError):
        if name == "EnterpriseAuthorizationManager":
            value = None
        else:
            raise

    globals()[name] = value
    return value


def __dir__() -> list[str]:
    """Return module attributes including lazy exports for interactive tooling."""
    return sorted(set(globals()) | set(__all__))


# Configure logging on import
log_level = os.getenv("CODEFLOW_LOG_LEVEL", "INFO")
json_logging = os.getenv("CODEFLOW_JSON_LOGGING", "false").lower() == "true"
configure_logging(level=log_level, format_json=json_logging)
