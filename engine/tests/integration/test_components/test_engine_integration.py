"""Integration tests for engine component interactions."""

import pytest


@pytest.mark.integration
def test_engine_initialization():
    """Test that engine can be initialized."""
    from codeflow_engine.engine import CodeFlowEngine
    
    engine = CodeFlowEngine()
    assert engine is not None


@pytest.mark.integration
async def test_engine_action_registry():
    """Test that engine can discover and use actions."""
    from codeflow_engine.engine import CodeFlowEngine
    from codeflow_engine.actions.registry import ActionRegistry
    
    engine = CodeFlowEngine()
    registry = ActionRegistry()
    
    # Check that actions are registered
    actions = registry.list_actions()
    assert len(actions) > 0
    
    # Check that engine can access actions
    assert hasattr(engine, 'execute_action') or hasattr(engine, 'actions')


@pytest.mark.integration
def test_engine_configuration_loading():
    """Test that engine can load configuration."""
    from codeflow_engine.engine import CodeFlowEngine
    from codeflow_engine.config.settings import CodeFlowSettings
    
    # Test that settings can be loaded
    settings = CodeFlowSettings()
    assert settings is not None
    assert hasattr(settings, 'environment')

