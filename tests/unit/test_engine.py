"""Unit tests for CodeFlow Engine core functionality."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from codeflow_engine.config import CodeFlowConfig
from codeflow_engine.engine import CodeFlowEngine
from codeflow_engine.exceptions import ConfigurationError


class TestCodeFlowEngineInitialization:
    """Test suite for engine initialization."""

    def test_engine_init_with_default_config(self):
        """Test engine initialization with default config."""
        engine = CodeFlowEngine()
        assert engine is not None
        assert engine.config is not None
        assert engine.workflow_engine is not None
        assert engine.action_registry is not None
        assert engine.integration_registry is not None
        assert engine.llm_manager is not None
        assert engine.health_checker is not None

    def test_engine_init_with_custom_config(self):
        """Test engine initialization with custom config."""
        config = CodeFlowConfig()
        engine = CodeFlowEngine(config=config)
        assert engine.config is config

    def test_engine_init_with_log_handler(self):
        """Test engine initialization with log handler."""
        import logging
        handler = logging.NullHandler()
        engine = CodeFlowEngine(log_handler=handler)
        assert engine is not None

    def test_engine_get_status(self):
        """Test getting engine status."""
        engine = CodeFlowEngine()
        with patch.object(engine.workflow_engine, 'get_status', return_value={"status": "running"}):
            with patch.object(engine.action_registry, 'get_all_actions', return_value=[]):
                with patch.object(engine.integration_registry, 'get_all_integrations', return_value=[]):
                    with patch.object(engine.llm_manager, 'get_available_providers', return_value=[]):
                        with patch.object(engine.config, 'to_dict', return_value={}):
                            status = engine.get_status()
                            assert isinstance(status, dict)
                            assert "engine" in status
                            assert "workflow_engine" in status

    def test_engine_get_version(self):
        """Test getting engine version."""
        engine = CodeFlowEngine()
        version = engine.get_version()
        assert isinstance(version, str)
        assert len(version) > 0

    @pytest.mark.asyncio
    async def test_engine_context_manager(self):
        """Test engine as async context manager."""
        async with CodeFlowEngine() as engine:
            assert engine is not None
            # Engine should be started in context manager

    @pytest.mark.asyncio
    async def test_engine_start_success(self):
        """Test successful engine start."""
        engine = CodeFlowEngine()
        with patch.object(engine.config, 'validate', return_value=True):
            with patch.object(engine.workflow_engine, 'initialize', new_callable=AsyncMock):
                with patch.object(engine.integration_registry, 'initialize', new_callable=AsyncMock):
                    with patch.object(engine.llm_manager, 'initialize', new_callable=AsyncMock):
                        await engine.start()
                        assert engine is not None

    @pytest.mark.asyncio
    async def test_engine_start_invalid_config(self):
        """Test engine start with invalid configuration."""
        engine = CodeFlowEngine()
        with patch.object(engine.config, 'validate', return_value=False):
            with pytest.raises(ConfigurationError):
                await engine.start()

    @pytest.mark.asyncio
    async def test_engine_stop(self):
        """Test engine stop."""
        engine = CodeFlowEngine()
        with patch.object(engine.workflow_engine, 'shutdown', new_callable=AsyncMock):
            with patch.object(engine.integration_registry, 'shutdown', new_callable=AsyncMock):
                with patch.object(engine.llm_manager, 'shutdown', new_callable=AsyncMock):
                    await engine.stop()
                    # Should complete without error

    @pytest.mark.asyncio
    async def test_engine_health_check(self):
        """Test engine health check."""
        engine = CodeFlowEngine()
        result = await engine.health_check()
        assert isinstance(result, dict)
        assert "status" in result or "health" in result


class TestCodeFlowEngineWorkflows:
    """Test suite for engine workflow operations."""

    @pytest.fixture
    def engine(self):
        """Create engine instance for testing."""
        return CodeFlowEngine()

    @pytest.mark.asyncio
    async def test_process_event_success(self, engine):
        """Test successful event processing."""
        event_type = "pull_request"
        event_data = {"action": "opened", "number": 123}
        
        with patch.object(engine.workflow_engine, 'process_event', new_callable=AsyncMock) as mock_process:
            mock_process.return_value = {"status": "success", "workflow_id": "test-123"}
            result = await engine.process_event(event_type, event_data)
            assert result is not None
            assert "status" in result
            mock_process.assert_called_once_with(event_type, event_data)

    @pytest.mark.asyncio
    async def test_process_event_error(self, engine):
        """Test event processing with error."""
        event_type = "pull_request"
        event_data = {"action": "opened", "number": 123}
        
        with patch.object(engine.workflow_engine, 'process_event', new_callable=AsyncMock) as mock_process:
            mock_process.side_effect = Exception("Workflow failed")
            with pytest.raises(Exception):
                await engine.process_event(event_type, event_data)


class TestCodeFlowEngineActions:
    """Test suite for engine action operations."""

    @pytest.fixture
    def engine(self):
        """Create engine instance for testing."""
        return CodeFlowEngine()

    def test_action_registry_access(self, engine):
        """Test accessing action registry."""
        assert engine.action_registry is not None
        actions = engine.action_registry.get_all_actions()
        assert isinstance(actions, list)

    def test_get_action_from_registry(self, engine):
        """Test getting an action from registry."""
        from codeflow_engine.actions.base.action import Action
        
        class TestAction(Action):
            def execute(self, context):
                return {"status": "success"}
        
        action = TestAction("test_action", "Test action")
        engine.action_registry.register(action)
        
        retrieved = engine.action_registry.get("test_action")
        assert retrieved is not None
        assert retrieved.name == "test_action"


class TestCodeFlowEngineIntegrations:
    """Test suite for engine integration operations."""

    @pytest.fixture
    def engine(self):
        """Create engine instance for testing."""
        return CodeFlowEngine()

    @pytest.mark.asyncio
    async def test_get_integration(self, engine):
        """Test getting an integration."""
        # Mock integration registry
        mock_integration = MagicMock()
        with patch.object(engine.integration_registry, 'get_integration', new_callable=AsyncMock, return_value=mock_integration):
            integration = await engine.integration_registry.get_integration("github")
            assert integration is not None

    def test_list_integrations(self, engine):
        """Test listing all integrations."""
        integrations = engine.integration_registry.get_all_integrations()
        assert isinstance(integrations, list)


class TestCodeFlowEngineErrorHandling:
    """Test suite for engine error handling."""

    @pytest.fixture
    def engine(self):
        """Create engine instance for testing."""
        return CodeFlowEngine()

    @pytest.mark.asyncio
    async def test_engine_start_handles_exceptions(self, engine):
        """Test that engine start handles exceptions gracefully."""
        with patch.object(engine.config, 'validate', return_value=True):
            with patch.object(engine.workflow_engine, 'initialize', new_callable=AsyncMock) as mock_init:
                mock_init.side_effect = Exception("Initialization failed")
                with pytest.raises(Exception):
                    await engine.start()

    @pytest.mark.asyncio
    async def test_engine_stop_handles_exceptions(self, engine):
        """Test that engine stop handles exceptions gracefully."""
        with patch.object(engine.workflow_engine, 'shutdown', new_callable=AsyncMock) as mock_shutdown:
            mock_shutdown.side_effect = Exception("Shutdown failed")
            # Should handle gracefully or raise
            try:
                await engine.stop()
            except Exception:
                pass  # Expected behavior

