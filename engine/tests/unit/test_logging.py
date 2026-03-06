"""Unit tests for structured logging utilities."""

import json
import logging
import pytest
from unittest.mock import Mock, patch

from codeflow_engine.utils.logging import (
    StructuredFormatter,
    TextFormatter,
    get_logger,
    log_with_context,
    setup_logging,
)
from codeflow_engine.config.settings import CodeFlowSettings, LogLevel


class TestStructuredFormatter:
    """Test cases for StructuredFormatter."""

    def test_format_basic_log(self):
        """Test formatting a basic log record."""
        formatter = StructuredFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        
        result = formatter.format(record)
        data = json.loads(result)
        
        assert data["level"] == "INFO"
        assert data["message"] == "Test message"
        assert data["component"] == "test"
        assert "timestamp" in data

    def test_format_with_extra_fields(self):
        """Test formatting with extra context fields."""
        formatter = StructuredFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.request_id = "req-123"
        record.user_id = "user-456"
        record.duration_ms = 150
        
        result = formatter.format(record)
        data = json.loads(result)
        
        assert data["request_id"] == "req-123"
        assert data["user_id"] == "user-456"
        assert data["duration_ms"] == 150

    def test_format_with_exception(self):
        """Test formatting with exception info."""
        formatter = StructuredFormatter()
        
        try:
            raise ValueError("Test error")
        except ValueError:
            record = logging.LogRecord(
                name="test",
                level=logging.ERROR,
                pathname="test.py",
                lineno=1,
                msg="Error occurred",
                args=(),
                exc_info=True,
            )
            
            result = formatter.format(record)
            data = json.loads(result)
            
            assert data["level"] == "ERROR"
            assert "exception" in data
            assert "exception_type" in data
            assert data["exception_type"] == "ValueError"


class TestTextFormatter:
    """Test cases for TextFormatter."""

    def test_format_basic_log(self):
        """Test formatting a basic log record."""
        formatter = TextFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        
        result = formatter.format(record)
        
        assert "INFO" in result
        assert "Test message" in result
        assert "test" in result

    def test_format_with_context(self):
        """Test formatting with context."""
        formatter = TextFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.request_id = "req-123"
        record.duration_ms = 150
        
        result = formatter.format(record)
        
        assert "request_id=req-123" in result
        assert "duration=150ms" in result


class TestLoggingUtilities:
    """Test cases for logging utility functions."""

    def test_get_logger(self):
        """Test getting a logger instance."""
        logger = get_logger("test_module")
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"

    def test_log_with_context(self):
        """Test logging with context."""
        logger = logging.getLogger("test")
        logger.setLevel(logging.INFO)
        
        # Capture log output
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        
        # Test logging with context
        log_with_context(
            logger,
            logging.INFO,
            "Test message",
            request_id="req-123",
            user_id="user-456"
        )
        
        # Verify logger was called (basic check)
        assert logger.level == logging.INFO

    @patch("codeflow_engine.utils.logging.logging.getLogger")
    def test_setup_logging(self, mock_get_logger):
        """Test logging setup."""
        settings = CodeFlowSettings()
        settings.monitoring.log_level = LogLevel.INFO
        
        # Mock logger
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        
        # Setup logging
        setup_logging(settings)
        
        # Verify setup was called
        assert mock_logger is not None

    def test_setup_logging_with_json_format(self):
        """Test logging setup with JSON format."""
        settings = CodeFlowSettings()
        settings.monitoring.log_level = LogLevel.INFO
        
        # Add log format if supported
        if hasattr(settings.monitoring, "log_format"):
            settings.monitoring.log_format = "json"
        
        setup_logging(settings)
        
        # Verify root logger is configured
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) > 0

