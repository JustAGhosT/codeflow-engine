"""
Structured logging utilities for CodeFlow Engine.

Provides JSON-formatted structured logging with correlation IDs,
contextual information, and Azure Log Analytics integration.
"""

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from codeflow_engine.config.settings import CodeFlowSettings, LogLevel


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.

        Args:
            record: Log record to format

        Returns:
            JSON-formatted log string
        """
        log_data: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": "codeflow-engine",
            "component": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields from record
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        if hasattr(record, "correlation_id"):
            log_data["correlation_id"] = record.correlation_id

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            log_data["exception_type"] = record.exc_info[0].__name__ if record.exc_info[0] else None

        # Add any additional extra fields
        for key, value in record.__dict__.items():
            if key not in {
                "name",
                "msg",
                "args",
                "created",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "thread",
                "threadName",
                "exc_info",
                "exc_text",
                "stack_info",
            }:
                if not key.startswith("_"):
                    log_data[key] = value

        return json.dumps(log_data, default=str)


class TextFormatter(logging.Formatter):
    """Human-readable text formatter for development."""

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as human-readable text.

        Args:
            record: Log record to format

        Returns:
            Formatted log string
        """
        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )
        level = record.levelname.ljust(8)
        component = record.name
        message = record.getMessage()

        # Build context string
        context_parts = []
        if hasattr(record, "request_id"):
            context_parts.append(f"request_id={record.request_id}")
        if hasattr(record, "user_id"):
            context_parts.append(f"user_id={record.user_id}")
        if hasattr(record, "duration_ms"):
            context_parts.append(f"duration={record.duration_ms}ms")

        context = f" [{', '.join(context_parts)}]" if context_parts else ""

        log_line = f"{timestamp} | {level} | {component} | {message}{context}"

        # Add exception if present
        if record.exc_info:
            log_line += f"\n{self.formatException(record.exc_info)}"

        return log_line


def setup_logging(settings: CodeFlowSettings) -> None:
    """
    Configure structured logging based on settings.

    Args:
        settings: CodeFlowSettings instance with logging configuration
    """
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.monitoring.log_level.upper(), logging.INFO))

    # Remove existing handlers
    root_logger.handlers.clear()

    # Determine log format
    log_format = getattr(settings.monitoring, "log_format", "json")
    if log_format == "json":
        formatter = StructuredFormatter()
    else:
        formatter = TextFormatter()

    # Configure output handlers
    log_output = getattr(settings.monitoring, "log_output", "stdout")

    if log_output in ("stdout", "both"):
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        stdout_handler.setLevel(getattr(logging, settings.monitoring.log_level.upper(), logging.INFO))
        root_logger.addHandler(stdout_handler)

    if log_output in ("file", "both"):
        log_file = getattr(settings.monitoring, "log_file", "/app/logs/codeflow.log")
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(getattr(logging, settings.monitoring.log_level.upper(), logging.INFO))
        root_logger.addHandler(file_handler)

    # Configure Azure Log Analytics if configured
    workspace_id = getattr(settings.monitoring, "log_analytics_workspace_id", None)
    workspace_key = getattr(settings.monitoring, "log_analytics_workspace_key", None)

    if workspace_id and workspace_key:
        try:
            from azure.monitor.opencensus import AzureLogHandler  # type: ignore[import-untyped]

            azure_handler = AzureLogHandler(
                connection_string=f"InstrumentationKey={workspace_key}"
            )
            azure_handler.setFormatter(StructuredFormatter())
            root_logger.addHandler(azure_handler)
        except ImportError:
            logger = logging.getLogger(__name__)
            logger.warning(
                "Azure Log Analytics handler not available. Install with: pip install opencensus-ext-azure"
            )

    # Set specific logger levels
    logging.getLogger("codeflow_engine").setLevel(
        getattr(logging, settings.monitoring.log_level.upper(), logging.INFO)
    )

    # Reduce noise from third-party libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def log_with_context(
    logger: logging.Logger,
    level: int,
    message: str,
    **context: Any,
) -> None:
    """
    Log a message with additional context.

    Args:
        logger: Logger instance
        level: Log level (logging.INFO, etc.)
        message: Log message
        **context: Additional context fields
    """
    logger.log(level, message, extra=context)

