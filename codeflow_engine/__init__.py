"""
CodeFlow Engine - Automated Code Review and Quality Management System

This package provides AI-powered code analysis, automated fixes, and quality assurance workflows.

Main Components:
- CodeFlowEngine: Main orchestrator for all automation activities
- ActionRegistry: Registry for managing action plugins
- WorkflowEngine: Workflow execution engine
- LLMProviderManager: Multi-provider LLM abstraction
- MetricsCollector: Quality metrics collection
"""

import logging
import os
from typing import Any, cast

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

__version__ = "1.0.1"

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


# Configure logging on import
log_level = os.getenv("CODEFLOW_LOG_LEVEL", "INFO")
json_logging = os.getenv("CODEFLOW_JSON_LOGGING", "false").lower() == "true"
configure_logging(level=log_level, format_json=json_logging)
