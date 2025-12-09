"""Integration tests for database connectivity and operations."""

import pytest


@pytest.mark.integration
def test_database_connection_available():
    """Test that database connection can be established."""
    from codeflow_engine.config.settings import CodeFlowSettings
    
    settings = CodeFlowSettings()
    # If DATABASE_URL is set, connection should be possible
    if settings.database.url:
        # This would require actual database connection
        # For now, just check that URL is valid format
        assert settings.database.url.startswith(("postgresql://", "mysql://", "sqlite://"))


@pytest.mark.integration
def test_database_pool_configuration():
    """Test database pool configuration."""
    from codeflow_engine.config.settings import CodeFlowSettings
    
    settings = CodeFlowSettings()
    assert settings.database.pool_size > 0
    assert settings.database.max_overflow >= 0
    assert settings.database.pool_timeout > 0


@pytest.mark.integration
def test_redis_connection_available():
    """Test that Redis connection can be established."""
    from codeflow_engine.config.settings import CodeFlowSettings
    
    settings = CodeFlowSettings()
    # If REDIS_URL is set, connection should be possible
    if settings.redis.url:
        # This would require actual Redis connection
        # For now, just check that URL is valid format
        assert settings.redis.url.startswith(("redis://", "rediss://"))


@pytest.mark.integration
def test_redis_configuration():
    """Test Redis configuration."""
    from codeflow_engine.config.settings import CodeFlowSettings
    
    settings = CodeFlowSettings()
    assert 1 <= settings.redis.port <= 65535
    assert 0 <= settings.redis.db <= 15
    assert settings.redis.max_connections > 0


@pytest.mark.integration
def test_database_settings_validation():
    """Test that database settings pass validation."""
    from codeflow_engine.config.settings import CodeFlowSettings
    from codeflow_engine.config.validation import validate_configuration
    
    settings = CodeFlowSettings()
    # Set valid database URL if not set
    if not settings.database.url:
        settings.database.url = "postgresql://user:pass@localhost/db"
    
    result = validate_configuration(settings)
    # Database config should not have errors (warnings are OK)
    db_errors = [e for e in result["errors"] if "database" in e.lower() or "pool" in e.lower()]
    assert len(db_errors) == 0


@pytest.mark.integration
def test_redis_settings_validation():
    """Test that Redis settings pass validation."""
    from codeflow_engine.config.settings import CodeFlowSettings
    from codeflow_engine.config.validation import validate_configuration
    
    settings = CodeFlowSettings()
    result = validate_configuration(settings)
    # Redis config should not have errors (warnings are OK)
    redis_errors = [e for e in result["errors"] if "redis" in e.lower()]
    assert len(redis_errors) == 0

