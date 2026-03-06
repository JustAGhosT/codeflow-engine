"""Unit tests for configuration validation."""

import os
from unittest.mock import patch

import pytest

from codeflow_engine.config.settings import CodeFlowSettings, Environment, LLMProvider
from codeflow_engine.config.validation import (
    ConfigurationValidator,
    check_environment_variables,
    generate_config_report,
    validate_configuration,
)


class TestConfigurationValidator:
    """Test suite for ConfigurationValidator."""

    @pytest.fixture
    def settings(self):
        """Create a basic CodeFlowSettings instance."""
        return CodeFlowSettings()

    @pytest.fixture
    def validator(self, settings):
        """Create a ConfigurationValidator instance."""
        return ConfigurationValidator(settings)

    def test_validator_initialization(self, validator):
        """Test validator initialization."""
        assert validator is not None
        assert validator.errors == []
        assert validator.warnings == []

    def test_validate_all_returns_tuple(self, validator):
        """Test that validate_all returns errors and warnings."""
        errors, warnings = validator.validate_all()
        assert isinstance(errors, list)
        assert isinstance(warnings, list)

    def test_validate_github_config_missing_auth(self, validator):
        """Test GitHub config validation with missing authentication."""
        validator.settings.github.token = None
        validator.settings.github.app_id = None
        validator._validate_github_config()
        assert len(validator.errors) > 0
        assert any("GitHub authentication required" in error for error in validator.errors)

    def test_validate_github_config_app_id_without_key(self, validator):
        """Test GitHub config validation with app_id but no private_key."""
        validator.settings.github.app_id = "12345"
        validator.settings.github.private_key = None
        validator._validate_github_config()
        assert any("GITHUB_PRIVATE_KEY is required" in error for error in validator.errors)

    def test_validate_github_config_invalid_url(self, validator):
        """Test GitHub config validation with invalid URL."""
        validator.settings.github.base_url = "not-a-url"
        validator._validate_github_config()
        assert any("Invalid GitHub base URL" in error for error in validator.errors)

    def test_validate_github_config_timeout_validation(self, validator):
        """Test GitHub timeout validation."""
        validator.settings.github.timeout = -1
        validator._validate_github_config()
        assert any("timeout must be positive" in error for error in validator.errors)

        validator.errors.clear()
        validator.settings.github.timeout = 3
        validator._validate_github_config()
        assert any("timeout is very low" in warning for warning in validator.warnings)

    def test_validate_github_config_retries_validation(self, validator):
        """Test GitHub retries validation."""
        validator.settings.github.max_retries = -1
        validator._validate_github_config()
        assert any("max_retries cannot be negative" in error for error in validator.errors)

        validator.errors.clear()
        validator.settings.github.max_retries = 15
        validator._validate_github_config()
        assert any("max_retries is very high" in warning for warning in validator.warnings)

    def test_validate_llm_config_no_providers(self, validator):
        """Test LLM config validation with no providers."""
        validator.settings.llm.openai_api_key = None
        validator.settings.llm.anthropic_api_key = None
        validator.settings.llm.mistral_api_key = None
        validator.settings.llm.groq_api_key = None
        validator.settings.llm.perplexity_api_key = None
        validator.settings.llm.together_api_key = None
        validator._validate_llm_config()
        assert any("At least one LLM provider API key is required" in error for error in validator.errors)

    def test_validate_llm_config_default_provider_no_key(self, validator):
        """Test LLM config validation with default provider missing key."""
        validator.settings.llm.default_provider = LLMProvider.OPENAI
        validator.settings.llm.openai_api_key = None
        validator.settings.llm.anthropic_api_key = "test-key"
        validator._validate_llm_config()
        assert any("has no API key configured" in warning for warning in validator.warnings)

    def test_validate_llm_config_max_tokens_validation(self, validator):
        """Test LLM max_tokens validation."""
        validator.settings.llm.max_tokens = -1
        validator._validate_llm_config()
        assert any("max_tokens must be positive" in error for error in validator.errors)

        validator.errors.clear()
        validator.settings.llm.max_tokens = 50000
        validator._validate_llm_config()
        assert any("max_tokens is very high" in warning for warning in validator.warnings)

    def test_validate_llm_config_temperature_validation(self, validator):
        """Test LLM temperature validation."""
        validator.settings.llm.temperature = -1
        validator._validate_llm_config()
        assert any("temperature must be between 0 and 2" in error for error in validator.errors)

        validator.errors.clear()
        validator.settings.llm.temperature = 3
        validator._validate_llm_config()
        assert any("temperature must be between 0 and 2" in error for error in validator.errors)

    def test_validate_database_config_pool_size(self, validator):
        """Test database pool_size validation."""
        validator.settings.database.pool_size = 0
        validator._validate_database_config()
        assert any("pool_size must be positive" in error for error in validator.errors)

        validator.errors.clear()
        validator.settings.database.pool_size = 150
        validator._validate_database_config()
        assert any("pool_size is very high" in warning for warning in validator.warnings)

    def test_validate_database_config_max_overflow(self, validator):
        """Test database max_overflow validation."""
        validator.settings.database.max_overflow = -1
        validator._validate_database_config()
        assert any("max_overflow cannot be negative" in error for error in validator.errors)

    def test_validate_redis_config_port_validation(self, validator):
        """Test Redis port validation."""
        validator.settings.redis.port = 0
        validator._validate_redis_config()
        assert any("port must be between 1 and 65535" in error for error in validator.errors)

        validator.errors.clear()
        validator.settings.redis.port = 70000
        validator._validate_redis_config()
        assert any("port must be between 1 and 65535" in error for error in validator.errors)

    def test_validate_redis_config_db_validation(self, validator):
        """Test Redis database number validation."""
        validator.settings.redis.db = -1
        validator._validate_redis_config()
        assert any("database number must be between 0 and 15" in error for error in validator.errors)

        validator.errors.clear()
        validator.settings.redis.db = 20
        validator._validate_redis_config()
        assert any("database number must be between 0 and 15" in error for error in validator.errors)

    def test_validate_security_config_production_secret_key(self, validator):
        """Test security config validation for production secret key."""
        validator.settings.environment = Environment.PRODUCTION
        validator.settings.security.secret_key = None
        validator._validate_security_config()
        assert any("SECRET_KEY is required in production" in error for error in validator.errors)

        validator.errors.clear()
        validator.settings.security.secret_key = "short"
        validator._validate_security_config()
        assert any("SECRET_KEY should be at least 32 characters" in error for error in validator.errors)

    def test_validate_security_config_jwt_validation(self, validator):
        """Test JWT validation."""
        validator.settings.security.jwt_secret = "short"
        validator._validate_security_config()
        assert any("JWT_SECRET should be at least 32 characters" in warning for warning in validator.warnings)

        validator.warnings.clear()
        validator.settings.security.jwt_expiry = 0
        validator._validate_security_config()
        assert any("JWT expiry must be positive" in error for error in validator.errors)

    def test_validate_security_config_cors_production(self, validator):
        """Test CORS validation in production."""
        validator.settings.environment = Environment.PRODUCTION
        validator.settings.security.enable_cors = True
        validator.settings.security.allowed_origins = []
        validator._validate_security_config()
        assert any("CORS allowed_origins must be specified in production" in error for error in validator.errors)

    def test_validate_environment_specific_production(self, validator):
        """Test environment-specific validation for production."""
        validator.settings.environment = Environment.PRODUCTION
        validator.settings.debug = True
        validator._validate_environment_specific()
        assert any("Debug mode should be disabled in production" in error for error in validator.errors)

        validator.errors.clear()
        validator.settings.debug = False
        validator.settings.monitoring.log_level = "DEBUG"
        validator._validate_environment_specific()
        assert any("Debug logging should be avoided in production" in warning for warning in validator.warnings)

    def test_validate_environment_specific_development(self, validator):
        """Test environment-specific validation for development."""
        validator.settings.environment = Environment.DEVELOPMENT
        validator.settings.debug = False
        validator._validate_environment_specific()
        assert any("Debug mode is typically enabled in development" in warning for warning in validator.warnings)

    def test_validate_environment_specific_testing(self, validator):
        """Test environment-specific validation for testing."""
        validator.settings.environment = Environment.TESTING
        validator.settings.workflow.max_concurrent = 5
        validator._validate_environment_specific()
        assert any("Sequential execution is recommended for testing" in warning for warning in validator.warnings)


class TestValidateConfiguration:
    """Test suite for validate_configuration function."""

    def test_validate_configuration_valid(self):
        """Test validation with valid configuration."""
        settings = CodeFlowSettings()
        settings.github.token = "test-token"
        settings.llm.openai_api_key = "test-key"
        
        result = validate_configuration(settings)
        assert isinstance(result, dict)
        assert "valid" in result
        assert "errors" in result
        assert "warnings" in result

    def test_validate_configuration_invalid(self):
        """Test validation with invalid configuration."""
        settings = CodeFlowSettings()
        settings.github.token = None
        settings.github.app_id = None
        
        result = validate_configuration(settings)
        assert result["valid"] is False
        assert len(result["errors"]) > 0


class TestCheckEnvironmentVariables:
    """Test suite for check_environment_variables function."""

    def test_check_environment_variables(self):
        """Test environment variable checking."""
        with patch.dict(os.environ, {}, clear=True):
            result = check_environment_variables()
            assert isinstance(result, dict)
            assert "issues" in result
            assert "recommendations" in result
            assert "missing_important_vars" in result

    def test_check_environment_variables_missing_vars(self):
        """Test checking for missing environment variables."""
        with patch.dict(os.environ, {}, clear=True):
            result = check_environment_variables()
            assert len(result["missing_important_vars"]) > 0

    def test_check_environment_variables_short_secrets(self):
        """Test detection of short secret values."""
        with patch.dict(os.environ, {"GITHUB_TOKEN": "short"}):
            result = check_environment_variables()
            assert len(result["issues"]) > 0
            assert any("too short" in issue.lower() for issue in result["issues"])


class TestGenerateConfigReport:
    """Test suite for generate_config_report function."""

    def test_generate_config_report(self):
        """Test config report generation."""
        settings = CodeFlowSettings()
        settings.github.token = "test-token"
        
        report = generate_config_report(settings)
        assert isinstance(report, str)
        assert "CodeFlow Configuration Report" in report
        assert "Environment:" in report

    def test_generate_config_report_includes_errors(self):
        """Test that report includes errors."""
        settings = CodeFlowSettings()
        settings.github.token = None
        settings.github.app_id = None
        
        report = generate_config_report(settings)
        assert "Errors:" in report or "Configuration has errors" in report

    def test_generate_config_report_includes_warnings(self):
        """Test that report includes warnings."""
        settings = CodeFlowSettings()
        settings.github.timeout = 3
        
        report = generate_config_report(settings)
        assert "Warnings:" in report or "warning" in report.lower()

