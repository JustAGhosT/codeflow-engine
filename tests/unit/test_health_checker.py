"""Unit tests for health checker component."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from codeflow_engine.health.health_checker import (
    ComponentHealth,
    HealthChecker,
    HealthStatus,
)


class TestHealthStatus:
    """Test suite for HealthStatus enum."""

    def test_health_status_values(self):
        """Test that HealthStatus has expected values."""
        assert HealthStatus.HEALTHY == "healthy"
        assert HealthStatus.DEGRADED == "degraded"
        assert HealthStatus.UNHEALTHY == "unhealthy"
        assert HealthStatus.UNKNOWN == "unknown"


class TestComponentHealth:
    """Test suite for ComponentHealth class."""

    def test_component_health_creation(self):
        """Test creating a ComponentHealth instance."""
        health = ComponentHealth(
            name="test",
            status=HealthStatus.HEALTHY,
            message="All good",
            response_time_ms=10.0,
            details={"key": "value"},
        )
        assert health.name == "test"
        assert health.status == HealthStatus.HEALTHY
        assert health.message == "All good"
        assert health.response_time_ms == 10.0
        assert health.details == {"key": "value"}

    def test_component_health_defaults(self):
        """Test ComponentHealth with default values."""
        health = ComponentHealth(
            name="test",
            status=HealthStatus.HEALTHY,
            message="",
            response_time_ms=0.0,
        )
        assert health.name == "test"
        assert health.status == HealthStatus.HEALTHY
        assert health.message == ""
        assert health.response_time_ms == 0.0
        assert health.details is None


class TestHealthChecker:
    """Test suite for HealthChecker class."""

    @pytest.fixture
    def health_checker(self):
        """Create a HealthChecker instance for testing."""
        with patch("codeflow_engine.health.health_checker.CodeFlowSettings") as mock_settings:
            mock_settings.return_value = MagicMock()
            checker = HealthChecker()
            return checker

    @pytest.mark.asyncio
    async def test_check_health_basic(self, health_checker):
        """Test basic health check."""
        healthy_component = ComponentHealth("test", HealthStatus.HEALTHY, "", 0.0)
        with patch.object(health_checker, "_check_database", return_value=healthy_component):
            with patch.object(health_checker, "_check_llm_providers", return_value=healthy_component):
                with patch.object(health_checker, "_check_integrations", return_value=healthy_component):
                    with patch.object(health_checker, "_check_system_resources", return_value=healthy_component):
                        with patch.object(health_checker, "_check_workflow_engine", return_value=healthy_component):
                            result = await health_checker.check_all()
                            assert result["status"] == HealthStatus.HEALTHY.value
                            assert "components" in result

    @pytest.mark.asyncio
    async def test_check_health_with_degraded_component(self, health_checker):
        """Test health check with degraded component."""
        healthy = ComponentHealth("database", HealthStatus.HEALTHY, "", 0.0)
        degraded = ComponentHealth("llm_providers", HealthStatus.DEGRADED, "Some providers unavailable", 0.0)
        with patch.object(health_checker, "_check_database", return_value=healthy):
            with patch.object(health_checker, "_check_llm_providers", return_value=degraded):
                with patch.object(health_checker, "_check_integrations", return_value=healthy):
                    with patch.object(health_checker, "_check_system_resources", return_value=healthy):
                        with patch.object(health_checker, "_check_workflow_engine", return_value=healthy):
                            result = await health_checker.check_all()
                            assert result["status"] == HealthStatus.DEGRADED.value
                            assert "components" in result
                            assert result["components"]["llm_providers"]["status"] == HealthStatus.DEGRADED.value

    @pytest.mark.asyncio
    async def test_check_health_with_unhealthy_component(self, health_checker):
        """Test health check with unhealthy component."""
        healthy = ComponentHealth("test", HealthStatus.HEALTHY, "", 0.0)
        unhealthy = ComponentHealth("database", HealthStatus.UNHEALTHY, "Database connection failed", 0.0)
        with patch.object(health_checker, "_check_database", return_value=unhealthy):
            with patch.object(health_checker, "_check_llm_providers", return_value=healthy):
                with patch.object(health_checker, "_check_integrations", return_value=healthy):
                    with patch.object(health_checker, "_check_system_resources", return_value=healthy):
                        with patch.object(health_checker, "_check_workflow_engine", return_value=healthy):
                            result = await health_checker.check_all()
                            assert result["status"] == HealthStatus.UNHEALTHY.value
                            assert "components" in result
                            assert result["components"]["database"]["status"] == HealthStatus.UNHEALTHY.value

    @pytest.mark.asyncio
    async def test_check_database_healthy(self, health_checker):
        """Test database health check when healthy."""
        with patch("codeflow_engine.health.health_checker.get_db") as mock_get_db:
            mock_db = AsyncMock()
            mock_get_db.return_value = mock_db
            mock_db.execute = AsyncMock(return_value=MagicMock())
            
            result = await health_checker._check_database()
            assert result.status == HealthStatus.HEALTHY
            assert "database" in result.message.lower() or result.message == ""

    @pytest.mark.asyncio
    async def test_check_database_unhealthy(self, health_checker):
        """Test database health check when unhealthy."""
        with patch("codeflow_engine.health.health_checker.get_db") as mock_get_db:
            mock_get_db.side_effect = Exception("Connection failed")
            
            result = await health_checker._check_database()
            assert result.status == HealthStatus.UNHEALTHY
            assert "error" in result.message.lower() or "failed" in result.message.lower()

    @pytest.mark.asyncio
    async def test_check_llm_providers_healthy(self, health_checker):
        """Test LLM providers health check when healthy."""
        with patch("codeflow_engine.health.health_checker.CodeFlowSettings") as mock_settings:
            mock_settings.return_value.llm = MagicMock()
            mock_settings.return_value.llm.openai_api_key = MagicMock()
            mock_settings.return_value.llm.openai_api_key.get_secret_value.return_value = "test-key"
            
            result = await health_checker._check_llm_providers()
            assert result.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNKNOWN]

    @pytest.mark.asyncio
    async def test_check_llm_providers_no_keys(self, health_checker):
        """Test LLM providers health check when no API keys configured."""
        with patch("codeflow_engine.health.health_checker.CodeFlowSettings") as mock_settings:
            mock_settings.return_value.llm = MagicMock()
            mock_settings.return_value.llm.openai_api_key = None
            mock_settings.return_value.llm.anthropic_api_key = None
            
            result = await health_checker._check_llm_providers()
            assert result.status in [HealthStatus.DEGRADED, HealthStatus.UNHEALTHY, HealthStatus.UNKNOWN]

    @pytest.mark.asyncio
    async def test_check_integrations_healthy(self, health_checker):
        """Test integrations health check when healthy."""
        with patch("codeflow_engine.health.health_checker.IntegrationRegistry") as mock_registry:
            mock_registry_instance = MagicMock()
            mock_registry_instance.health_check_all = AsyncMock(return_value={
                "github": {"status": "healthy"},
                "linear": {"status": "healthy"},
            })
            mock_registry.return_value = mock_registry_instance
            
            result = await health_checker._check_integrations()
            assert result.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNKNOWN]

    @pytest.mark.asyncio
    async def test_check_system_resources_healthy(self, health_checker):
        """Test system resources health check when healthy."""
        with patch("codeflow_engine.health.health_checker.psutil") as mock_psutil:
            mock_psutil.cpu_percent.return_value = 50.0
            mock_psutil.virtual_memory.return_value = MagicMock(percent=60.0)
            mock_psutil.disk_usage.return_value = MagicMock(percent=50.0)
            
            result = await health_checker._check_system_resources()
            assert result.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED]

    @pytest.mark.asyncio
    async def test_check_system_resources_high_usage(self, health_checker):
        """Test system resources health check when usage is high."""
        with patch("codeflow_engine.health.health_checker.psutil") as mock_psutil:
            mock_psutil.cpu_percent.return_value = 95.0
            mock_psutil.virtual_memory.return_value = MagicMock(percent=95.0)
            mock_psutil.disk_usage.return_value = MagicMock(percent=95.0)
            
            result = await health_checker._check_system_resources()
            assert result.status in [HealthStatus.DEGRADED, HealthStatus.UNHEALTHY]

    @pytest.mark.asyncio
    async def test_check_workflow_engine_healthy(self, health_checker):
        """Test workflow engine health check when healthy."""
        with patch("codeflow_engine.health.health_checker.WorkflowEngine") as mock_engine:
            mock_engine_instance = MagicMock()
            mock_engine_instance.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_engine.return_value = mock_engine_instance
            
            result = await health_checker._check_workflow_engine()
            assert result.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNKNOWN]

    def test_determine_overall_health_all_healthy(self, health_checker):
        """Test overall health determination when all components are healthy."""
        components = {
            "database": ComponentHealth("database", HealthStatus.HEALTHY, "", 0.0),
            "llm_providers": ComponentHealth("llm_providers", HealthStatus.HEALTHY, "", 0.0),
            "integrations": ComponentHealth("integrations", HealthStatus.HEALTHY, "", 0.0),
            "system_resources": ComponentHealth("system_resources", HealthStatus.HEALTHY, "", 0.0),
            "workflow_engine": ComponentHealth("workflow_engine", HealthStatus.HEALTHY, "", 0.0),
        }
        result = health_checker._determine_overall_health(components)
        assert result == HealthStatus.HEALTHY

    def test_determine_overall_health_with_degraded(self, health_checker):
        """Test overall health determination with degraded components."""
        components = {
            "database": ComponentHealth("database", HealthStatus.HEALTHY, "", 0.0),
            "llm_providers": ComponentHealth("llm_providers", HealthStatus.DEGRADED, "", 0.0),
            "integrations": ComponentHealth("integrations", HealthStatus.HEALTHY, "", 0.0),
            "system_resources": ComponentHealth("system_resources", HealthStatus.HEALTHY, "", 0.0),
            "workflow_engine": ComponentHealth("workflow_engine", HealthStatus.HEALTHY, "", 0.0),
        }
        result = health_checker._determine_overall_health(components)
        assert result == HealthStatus.DEGRADED

    def test_determine_overall_health_with_unhealthy(self, health_checker):
        """Test overall health determination with unhealthy components."""
        components = {
            "database": ComponentHealth("database", HealthStatus.UNHEALTHY, "", 0.0),
            "llm_providers": ComponentHealth("llm_providers", HealthStatus.HEALTHY, "", 0.0),
            "integrations": ComponentHealth("integrations", HealthStatus.HEALTHY, "", 0.0),
            "system_resources": ComponentHealth("system_resources", HealthStatus.HEALTHY, "", 0.0),
            "workflow_engine": ComponentHealth("workflow_engine", HealthStatus.HEALTHY, "", 0.0),
        }
        result = health_checker._determine_overall_health(components)
        assert result == HealthStatus.UNHEALTHY

    def test_determine_overall_health_with_unknown(self, health_checker):
        """Test overall health determination with unknown status."""
        components = {
            "database": ComponentHealth("database", HealthStatus.UNKNOWN, "", 0.0),
            "llm_providers": ComponentHealth("llm_providers", HealthStatus.HEALTHY, "", 0.0),
            "integrations": ComponentHealth("integrations", HealthStatus.HEALTHY, "", 0.0),
            "system_resources": ComponentHealth("system_resources", HealthStatus.HEALTHY, "", 0.0),
            "workflow_engine": ComponentHealth("workflow_engine", HealthStatus.HEALTHY, "", 0.0),
        }
        result = health_checker._determine_overall_health(components)
        assert result in [HealthStatus.DEGRADED, HealthStatus.UNKNOWN]

