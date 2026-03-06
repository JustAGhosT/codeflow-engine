"""Unit tests for workflow components."""

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock

from codeflow_engine.workflows.engine import WorkflowEngine
from codeflow_engine.config import CodeFlowConfig


class TestWorkflowEngine:
    """Test cases for WorkflowEngine."""

    @pytest.fixture
    def config(self):
        """Create a mock config."""
        config = Mock(spec=CodeFlowConfig)
        config.workflow_timeout = 300
        config.workflow_retry_attempts = 3
        config.workflow_retry_delay = 5
        return config

    @pytest.fixture
    def engine(self, config):
        """Create a workflow engine instance."""
        return WorkflowEngine(config)

    def test_workflow_engine_init(self, engine):
        """Test workflow engine initialization."""
        assert engine is not None
        assert hasattr(engine, "workflows")
        assert hasattr(engine, "running_workflows")
        assert hasattr(engine, "workflow_history")
        assert engine._is_running is False

    @pytest.mark.asyncio
    async def test_start_engine(self, engine):
        """Test starting the workflow engine."""
        await engine.start()
        assert engine._is_running is True

    @pytest.mark.asyncio
    async def test_stop_engine(self, engine):
        """Test stopping the workflow engine."""
        await engine.start()
        await engine.stop()
        assert engine._is_running is False

    def test_register_workflow(self, engine):
        """Test workflow registration."""
        from codeflow_engine.workflows.base import Workflow
        
        mock_workflow = Mock(spec=Workflow)
        mock_workflow.name = "test_workflow"
        
        engine.register_workflow(mock_workflow)
        assert "test_workflow" in engine.workflows
        assert engine.workflows["test_workflow"] == mock_workflow

    def test_unregister_workflow(self, engine):
        """Test unregistering a workflow."""
        from codeflow_engine.workflows.base import Workflow
        
        mock_workflow = Mock(spec=Workflow)
        mock_workflow.name = "test_workflow"
        
        engine.register_workflow(mock_workflow)
        assert "test_workflow" in engine.workflows
        
        engine.unregister_workflow("test_workflow")
        assert "test_workflow" not in engine.workflows

    @pytest.mark.asyncio
    async def test_get_status(self, engine):
        """Test getting engine status."""
        status = await engine.get_status()
        
        assert "running" in status
        assert "registered_workflows" in status
        assert "running_workflows" in status
        assert "total_executions" in status
        assert "workflows" in status
        assert "metrics" in status

    @pytest.mark.asyncio
    async def test_get_metrics(self, engine):
        """Test getting engine metrics."""
        metrics = await engine.get_metrics()
        
        assert "total_executions" in metrics
        assert "successful_executions" in metrics
        assert "failed_executions" in metrics
        assert "timeout_executions" in metrics
        assert "success_rate_percent" in metrics

    def test_get_workflow_history(self, engine):
        """Test getting workflow history."""
        history = engine.get_workflow_history()
        assert isinstance(history, list)

    def test_get_running_workflows(self, engine):
        """Test getting running workflows."""
        running = engine.get_running_workflows()
        assert isinstance(running, list)

