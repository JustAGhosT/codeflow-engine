"""Unit tests for data models."""

import pytest
from datetime import datetime

from codeflow_engine.models.artifacts import (
    PrototypeEnhancerInputs,
    PrototypeEnhancerOutputs,
    EnhancementType,
)


class TestPrototypeEnhancerInputs:
    """Test cases for PrototypeEnhancerInputs model."""

    def test_prototype_enhancer_inputs_creation(self):
        """Test prototype enhancer inputs creation."""
        inputs = PrototypeEnhancerInputs(
            platform="python",
            enhancement_type=EnhancementType.PRODUCTION,
            project_path="/path/to/project"
        )
        
        assert inputs.platform == "python"
        assert inputs.enhancement_type == EnhancementType.PRODUCTION
        assert inputs.project_path == "/path/to/project"
        assert inputs.config is None
        assert inputs.dry_run is False

    def test_prototype_enhancer_inputs_with_config(self):
        """Test prototype enhancer inputs with config."""
        config = {"key": "value"}
        inputs = PrototypeEnhancerInputs(
            platform="python",
            enhancement_type=EnhancementType.PRODUCTION,
            project_path="/path/to/project",
            config=config
        )
        
        assert inputs.config == config

    def test_prototype_enhancer_inputs_dry_run(self):
        """Test prototype enhancer inputs with dry_run."""
        inputs = PrototypeEnhancerInputs(
            platform="python",
            enhancement_type=EnhancementType.PRODUCTION,
            project_path="/path/to/project",
            dry_run=True
        )
        
        assert inputs.dry_run is True


class TestPrototypeEnhancerOutputs:
    """Test cases for PrototypeEnhancerOutputs model."""

    def test_prototype_enhancer_outputs_creation(self):
        """Test prototype enhancer outputs creation."""
        outputs = PrototypeEnhancerOutputs(
            success=True,
            message="Enhancement completed",
            generated_files=["file1.py"],
            modified_files=["file2.py"],
            next_steps=["Step 1", "Step 2"]
        )
        
        assert outputs.success is True
        assert outputs.message == "Enhancement completed"
        assert len(outputs.generated_files) == 1
        assert len(outputs.modified_files) == 1
        assert len(outputs.next_steps) == 2
        assert outputs.metadata is None

    def test_prototype_enhancer_outputs_with_metadata(self):
        """Test prototype enhancer outputs with metadata."""
        metadata = {"key": "value"}
        outputs = PrototypeEnhancerOutputs(
            success=True,
            message="Test",
            generated_files=[],
            modified_files=[],
            next_steps=[],
            metadata=metadata
        )
        
        assert outputs.metadata == metadata


class TestEnhancementType:
    """Test cases for EnhancementType enum."""

    def test_enhancement_type_values(self):
        """Test enhancement type enum values."""
        assert EnhancementType.PRODUCTION == "production"
        assert EnhancementType.TESTING == "testing"
        assert EnhancementType.SECURITY == "security"

