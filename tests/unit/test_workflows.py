"""Unit tests for workflow components."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from codeflow_engine.workflows.engine import WorkflowEngine
from codeflow_engine.models.events import WorkflowEvent


class TestWorkflowEngine:
    """Test cases for WorkflowEngine."""

    def test_workflow_engine_init(self):
        """Test workflow engine initialization."""
        engine = WorkflowEngine()
        assert engine is not None
        assert hasattr(engine, "workflows")

    def test_register_workflow(self):
        """Test workflow registration."""
        engine = WorkflowEngine()
        
        def test_workflow(event):
            return {"status": "success"}
        
        engine.register_workflow("test_workflow", test_workflow)
        assert "test_workflow" in engine.workflows

    def test_execute_workflow_success(self):
        """Test successful workflow execution."""
        engine = WorkflowEngine()
        
        def test_workflow(event):
            return {"status": "success", "result": "completed"}
        
        engine.register_workflow("test_workflow", test_workflow)
        
        event = WorkflowEvent(
            type="test",
            payload={"data": "test"}
        )
        
        result = engine.execute_workflow("test_workflow", event)
        assert result["status"] == "success"
        assert result["result"] == "completed"

    def test_execute_workflow_not_found(self):
        """Test workflow execution with non-existent workflow."""
        engine = WorkflowEngine()
        
        event = WorkflowEvent(
            type="test",
            payload={"data": "test"}
        )
        
        with pytest.raises(ValueError, match="Workflow not found"):
            engine.execute_workflow("non_existent", event)

    def test_execute_workflow_with_error(self):
        """Test workflow execution with error handling."""
        engine = WorkflowEngine()
        
        def failing_workflow(event):
            raise ValueError("Workflow error")
        
        engine.register_workflow("failing_workflow", failing_workflow)
        
        event = WorkflowEvent(
            type="test",
            payload={"data": "test"}
        )
        
        with pytest.raises(ValueError, match="Workflow error"):
            engine.execute_workflow("failing_workflow", event)

    def test_workflow_event_creation(self):
        """Test workflow event creation."""
        event = WorkflowEvent(
            type="test_event",
            payload={"key": "value"}
        )
        
        assert event.type == "test_event"
        assert event.payload == {"key": "value"}

    def test_list_workflows(self):
        """Test listing registered workflows."""
        engine = WorkflowEngine()
        
        def workflow1(event):
            return {}
        
        def workflow2(event):
            return {}
        
        engine.register_workflow("workflow1", workflow1)
        engine.register_workflow("workflow2", workflow2)
        
        workflows = engine.list_workflows()
        assert "workflow1" in workflows
        assert "workflow2" in workflows
        assert len(workflows) == 2

