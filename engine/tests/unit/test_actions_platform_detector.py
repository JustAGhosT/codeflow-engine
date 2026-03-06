"""Unit tests for Platform Detector action."""

from unittest.mock import MagicMock, patch

import pytest

from codeflow_engine.actions.platform_detector import (
    PlatformDetector,
    PlatformDetectorInputs,
    PlatformDetectorOutputs,
)


class TestPlatformDetectorInputs:
    """Test suite for PlatformDetectorInputs."""

    def test_inputs_creation(self):
        """Test creating PlatformDetectorInputs."""
        inputs = PlatformDetectorInputs(
            repository_url="https://github.com/test/repo",
            commit_messages=["Initial commit"],
            workspace_path=".",
        )
        assert inputs.repository_url == "https://github.com/test/repo"
        assert inputs.commit_messages == ["Initial commit"]
        assert inputs.workspace_path == "."

    def test_inputs_defaults(self):
        """Test PlatformDetectorInputs with default values."""
        inputs = PlatformDetectorInputs(repository_url="https://github.com/test/repo")
        assert inputs.commit_messages == []
        assert inputs.workspace_path == "."
        assert inputs.package_json_content is None


class TestPlatformDetectorOutputs:
    """Test suite for PlatformDetectorOutputs."""

    def test_outputs_creation(self):
        """Test creating PlatformDetectorOutputs."""
        outputs = PlatformDetectorOutputs(
            detected_platform="replit",
            confidence_score=0.8,
            platform_specific_config={},
            recommended_workflow="phase2_replit_to_production",
            migration_suggestions=[],
            enhancement_opportunities=[],
        )
        assert outputs.detected_platform == "replit"
        assert outputs.confidence_score == 0.8
        assert isinstance(outputs.platform_specific_config, dict)


class TestPlatformDetector:
    """Test suite for PlatformDetector."""

    @pytest.fixture
    def detector(self):
        """Create a PlatformDetector instance."""
        return PlatformDetector()

    def test_detector_initialization(self, detector):
        """Test detector initialization."""
        assert detector is not None
        assert detector.platform_signatures is not None
        assert len(detector.platform_signatures) > 0

    def test_detect_platform_unknown(self, detector):
        """Test platform detection with no matches."""
        inputs = PlatformDetectorInputs(
            repository_url="https://github.com/test/repo",
            workspace_path=".",
        )
        
        with patch.object(detector, '_scan_workspace', return_value={"files": [], "folders": []}):
            with patch.object(detector, '_parse_package_json', return_value=None):
                result = detector.detect_platform(inputs)
                assert result.detected_platform == "unknown"
                assert result.confidence_score < 0.3

    def test_detect_platform_replit(self, detector):
        """Test platform detection for Replit."""
        inputs = PlatformDetectorInputs(
            repository_url="https://github.com/test/repo",
            commit_messages=["Exported from Replit"],
            workspace_path=".",
        )
        
        file_structure = {
            "files": [".replit", "main.py"],
            "folders": [],
            "file_contents": {".replit": "language=python"},
            "total_files": 2,
        }
        
        with patch.object(detector, '_scan_workspace', return_value=file_structure):
            with patch.object(detector, '_parse_package_json', return_value=None):
                result = detector.detect_platform(inputs)
                assert result.detected_platform == "replit"
                assert result.confidence_score >= 0.3

    def test_detect_platform_lovable(self, detector):
        """Test platform detection for Lovable."""
        inputs = PlatformDetectorInputs(
            repository_url="https://github.com/test/repo",
            workspace_path=".",
            package_json_content='{"dependencies": {"@lovable/core": "^1.0.0"}}',
        )
        
        file_structure = {
            "files": ["lovable.config.js"],
            "folders": [],
            "file_contents": {},
            "total_files": 1,
        }
        
        with patch.object(detector, '_scan_workspace', return_value=file_structure):
            with patch.object(detector, '_parse_package_json', return_value={"dependencies": {"@lovable/core": "^1.0.0"}}):
                result = detector.detect_platform(inputs)
                assert result.detected_platform == "lovable"
                assert result.confidence_score >= 0.3

    def test_scan_workspace(self, detector, tmp_path):
        """Test workspace scanning."""
        # Create test files
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")
        
        result = detector._scan_workspace(str(tmp_path))
        assert "files" in result
        assert "folders" in result
        assert "test.py" in result["files"]

    def test_scan_workspace_nonexistent(self, detector):
        """Test scanning nonexistent workspace."""
        result = detector._scan_workspace("/nonexistent/path")
        assert result["files"] == []
        assert result["total_files"] == 0

    def test_parse_package_json_from_content(self, detector):
        """Test parsing package.json from content."""
        content = '{"name": "test", "version": "1.0.0"}'
        result = detector._parse_package_json(content, ".")
        assert result is not None
        assert result["name"] == "test"

    def test_parse_package_json_invalid(self, detector):
        """Test parsing invalid package.json."""
        result = detector._parse_package_json("invalid json", ".")
        assert result is None

    def test_calculate_platform_score(self, detector):
        """Test platform score calculation."""
        inputs = PlatformDetectorInputs(
            repository_url="https://github.com/test/repo",
            commit_messages=["Replit export"],
        )
        
        signatures = detector.platform_signatures["replit"]
        file_structure = {
            "files": [".replit"],
            "folders": [],
            "file_contents": {},
        }
        
        score, analysis = detector._calculate_platform_score(
            inputs, signatures, file_structure, None
        )
        assert 0.0 <= score <= 1.0
        assert isinstance(analysis, dict)
        assert "file_matches" in analysis

    def test_get_platform_config_replit(self, detector):
        """Test getting Replit platform config."""
        file_structure = {
            "files": ["main.py", ".replit"],
            "folders": [],
            "file_contents": {".replit": "language=python"},
        }
        
        config = detector._get_platform_config("replit", file_structure, None)
        assert isinstance(config, dict)
        assert "deployment_options" in config

    def test_get_recommended_workflow(self, detector):
        """Test getting recommended workflow."""
        workflow = detector._get_recommended_workflow("replit", 0.8)
        assert workflow == "phase2_replit_to_production"
        
        workflow_low = detector._get_recommended_workflow("replit", 0.3)
        assert workflow_low == "phase2_generic_enhancement"

    def test_get_migration_suggestions(self, detector):
        """Test getting migration suggestions."""
        scores = {
            "replit": 0.8,
            "lovable": 0.5,
            "bolt": 0.3,
        }
        suggestions = detector._get_migration_suggestions("replit", scores)
        assert isinstance(suggestions, list)

    def test_get_enhancement_opportunities(self, detector):
        """Test getting enhancement opportunities."""
        analysis = {
            "file_matches": [".replit"],
            "dependency_matches": [],
        }
        opportunities = detector._get_enhancement_opportunities("replit", analysis)
        assert isinstance(opportunities, list)
        assert len(opportunities) > 0

    def test_detect_replit_runtime(self, detector):
        """Test detecting Replit runtime."""
        file_structure = {"files": ["main.py"]}
        runtime = detector._detect_replit_runtime(file_structure)
        assert runtime == "python"
        
        file_structure_js = {"files": ["index.js"]}
        runtime_js = detector._detect_replit_runtime(file_structure_js)
        assert runtime_js == "nodejs"

    def test_check_typescript_usage(self, detector):
        """Test checking TypeScript usage."""
        file_structure = {"files": ["component.tsx"]}
        assert detector._check_typescript_usage(file_structure) is True
        
        file_structure_no_ts = {"files": ["component.jsx"]}
        assert detector._check_typescript_usage(file_structure_no_ts) is False

    def test_detect_database_type(self, detector):
        """Test detecting database type."""
        package_json = {
            "dependencies": {"prisma": "^5.0.0"}
        }
        db_type = detector._detect_database_type({}, package_json)
        assert db_type == "prisma"
        
        package_json_mongo = {
            "dependencies": {"mongoose": "^7.0.0"}
        }
        db_type_mongo = detector._detect_database_type({}, package_json_mongo)
        assert db_type_mongo == "mongodb"

