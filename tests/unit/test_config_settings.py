"""Unit tests for CodeFlow settings configuration."""

import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from codeflow_engine.config.settings import CodeFlowSettings


class TestCodeFlowSettings:
    """Test suite for CodeFlowSettings."""

    def test_default_settings(self):
        """Test that default settings are loaded correctly."""
        with patch.dict(os.environ, {}, clear=True):
            settings = CodeFlowSettings()
            assert settings.environment == "development"
            assert settings.log_level == "INFO"
            assert settings.host == "0.0.0.0"
            assert settings.port == 8080

    def test_environment_variable_loading(self):
        """Test loading settings from environment variables."""
        env_vars = {
            "CODEFLOW_ENV": "production",
            "CODEFLOW_LOG_LEVEL": "DEBUG",
            "CODEFLOW_HOST": "127.0.0.1",
            "CODEFLOW_PORT": "9000",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            settings = CodeFlowSettings()
            assert settings.environment == "production"
            assert settings.log_level == "DEBUG"
            assert settings.host == "127.0.0.1"
            assert settings.port == 9000

    def test_github_token_validation(self):
        """Test GitHub token validation."""
        env_vars = {
            "GITHUB_TOKEN": "ghp_test_token_12345",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            settings = CodeFlowSettings()
            assert settings.github_token is not None
            assert settings.github_token.get_secret_value() == "ghp_test_token_12345"

    def test_github_token_optional(self):
        """Test that GitHub token is optional."""
        with patch.dict(os.environ, {}, clear=True):
            settings = CodeFlowSettings()
            assert settings.github_token is None

    def test_database_url_loading(self):
        """Test database URL loading."""
        env_vars = {
            "DATABASE_URL": "postgresql://user:pass@localhost:5432/dbname",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            settings = CodeFlowSettings()
            assert settings.database_url is not None
            assert "postgresql://" in settings.database_url

    def test_redis_url_loading(self):
        """Test Redis URL loading."""
        env_vars = {
            "REDIS_URL": "redis://localhost:6379/0",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            settings = CodeFlowSettings()
            assert settings.redis_url is not None
            assert "redis://" in settings.redis_url

    def test_llm_provider_configuration(self):
        """Test LLM provider configuration."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "ANTHROPIC_API_KEY": "sk-ant-test-key",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            settings = CodeFlowSettings()
            assert settings.openai_api_key is not None
            assert settings.anthropic_api_key is not None

    def test_timeout_validation(self):
        """Test timeout validation."""
        env_vars = {
            "CODEFLOW_TIMEOUT": "30",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            settings = CodeFlowSettings()
            assert settings.timeout == 30

    def test_timeout_validation_negative(self):
        """Test that negative timeout raises validation error."""
        env_vars = {
            "CODEFLOW_TIMEOUT": "-1",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValidationError):
                CodeFlowSettings()

    def test_temperature_validation(self):
        """Test temperature validation."""
        env_vars = {
            "CODEFLOW_TEMPERATURE": "0.7",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            settings = CodeFlowSettings()
            assert settings.temperature == 0.7

    def test_temperature_validation_out_of_range(self):
        """Test that temperature out of range raises validation error."""
        env_vars = {
            "CODEFLOW_TEMPERATURE": "2.0",  # Should be 0-1
        }
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValidationError):
                CodeFlowSettings()

    def test_settings_reload(self):
        """Test settings reload functionality."""
        settings = CodeFlowSettings()
        original_env = settings.environment

        # Change environment variable
        env_vars = {
            "CODEFLOW_ENV": "production",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            settings.reload()
            assert settings.environment == "production"
            assert settings.environment != original_env

    def test_configuration_validation(self):
        """Test configuration validation method."""
        settings = CodeFlowSettings()
        errors = settings.validate_configuration()
        # Should return empty list if valid
        assert isinstance(errors, list)

    def test_environment_specific_config_loading(self):
        """Test loading environment-specific configuration."""
        env_vars = {
            "CODEFLOW_ENV": "production",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            settings = CodeFlowSettings()
            # Should load production-specific config if file exists
            assert settings.environment == "production"

    @patch("codeflow_engine.config.settings.Path.exists")
    @patch("codeflow_engine.config.settings.yaml.safe_load")
    def test_yaml_config_loading(self, mock_yaml_load, mock_path_exists):
        """Test loading configuration from YAML file."""
        mock_path_exists.return_value = True
        mock_yaml_load.return_value = {
            "environment": "staging",
            "log_level": "DEBUG",
        }

        settings = CodeFlowSettings()
        # Should attempt to load YAML config
        mock_path_exists.assert_called()

    def test_custom_config_loading(self):
        """Test loading custom configuration."""
        # This tests the custom config loading logic
        settings = CodeFlowSettings()
        # Should handle custom config gracefully
        assert settings is not None

