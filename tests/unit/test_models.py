"""Unit tests for data models."""

import pytest
from datetime import datetime

from codeflow_engine.models.events import WorkflowEvent
from codeflow_engine.models.artifacts import Artifact
from codeflow_engine.models.config import WorkflowConfig


class TestWorkflowEvent:
    """Test cases for WorkflowEvent model."""

    def test_workflow_event_creation(self):
        """Test workflow event creation with required fields."""
        event = WorkflowEvent(
            type="test_event",
            payload={"key": "value"}
        )
        
        assert event.type == "test_event"
        assert event.payload == {"key": "value"}

    def test_workflow_event_with_timestamp(self):
        """Test workflow event with timestamp."""
        timestamp = datetime.now()
        event = WorkflowEvent(
            type="test_event",
            payload={},
            timestamp=timestamp
        )
        
        assert event.timestamp == timestamp

    def test_workflow_event_validation(self):
        """Test workflow event validation."""
        # Valid event
        event = WorkflowEvent(
            type="test",
            payload={}
        )
        assert event.type == "test"
        
        # Empty payload is valid
        event = WorkflowEvent(
            type="test",
            payload={}
        )
        assert event.payload == {}


class TestArtifact:
    """Test cases for Artifact model."""

    def test_artifact_creation(self):
        """Test artifact creation."""
        artifact = Artifact(
            name="test_artifact",
            content="test content",
            type="text"
        )
        
        assert artifact.name == "test_artifact"
        assert artifact.content == "test content"
        assert artifact.type == "text"

    def test_artifact_with_metadata(self):
        """Test artifact with metadata."""
        metadata = {"key": "value"}
        artifact = Artifact(
            name="test",
            content="content",
            type="text",
            metadata=metadata
        )
        
        assert artifact.metadata == metadata


class TestWorkflowConfig:
    """Test cases for WorkflowConfig model."""

    def test_workflow_config_creation(self):
        """Test workflow config creation."""
        config = WorkflowConfig(
            name="test_workflow",
            enabled=True
        )
        
        assert config.name == "test_workflow"
        assert config.enabled is True

    def test_workflow_config_defaults(self):
        """Test workflow config defaults."""
        config = WorkflowConfig(name="test")
        
        # Check default values if any
        assert config.name == "test"

