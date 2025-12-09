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
            status=HealthStatus.HEALTHY,
            message="All good",
            details={"key": "value"},
        )
        assert health.status == HealthStatus.HEALTHY
        assert health.message == "All good"
        assert health.details == {"key": "value"}

    def test_component_health_defaults(self):
        """Test ComponentHealth with default values."""
        health = ComponentHealth(status=HealthStatus.HEALTHY)
        assert health.status == HealthStatus.HEALTHY
        assert health.message == ""
        assert health.details == {}


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
        with patch.object(health_checker, "_check_database", return_value=ComponentHealth(HealthStatus.HEALTHY)):
            with patch.object(health_checker, "_check_llm_providers", return_value=ComponentHealth(HealthStatus.HEALTHY)):
                with patch.object(health_checker, "_check_integrations", return_value=ComponentHealth(HealthStatus.HEALTHY)):
                    with patch.object(health_checker, "_check_system_resources", return_value=ComponentHealth(HealthStatus.HEALTHY)):
                        with patch.object(health_checker, "_check_workflow_engine", return_value=ComponentHealth(HealthStatus.HEALTHY)):
                            result = await health_checker.check_health()
                            assert result["status"] == HealthStatus.HEALTHY
                            assert "components" in result

    @pytest.mark.asyncio
    async def test_check_health_with_degraded_component(self, health_checker):
        """Test health check with degraded component."""
        with patch.object(health_checker, "_check_database", return_value=ComponentHealth(HealthStatus.HEALTHY)):
            with patch.object(health_checker, "_check_llm_providers", return_value=ComponentHealth(HealthStatus.DEGRADED, message="Some providers unavailable")):
                with patch.object(health_checker, "_check_integrations", return_value=ComponentHealth(HealthStatus.HEALTHY)):
                    with patch.object(health_checker, "_check_system_resources", return_value=ComponentHealth(HealthStatus.HEALTHY)):
                        with patch.object(health_checker, "_check_workflow_engine", return_value=ComponentHealth(HealthStatus.HEALTHY)):
                            result = await health_checker.check_health()
                            assert result["status"] == HealthStatus.DEGRADED
                            assert "components" in result
                            assert result["components"]["llm_providers"]["status"] == HealthStatus.DEGRADED

    @pytest.mark.asyncio
    async def test_check_health_with_unhealthy_component(self, health_checker):
        """Test health check with unhealthy component."""
        with patch.object(health_checker, "_check_database", return_value=ComponentHealth(HealthStatus.UNHEALTHY, message="Database connection failed")):
            with patch.object(health_checker, "_check_llm_providers", return_value=ComponentHealth(HealthStatus.HEALTHY)):
                with patch.object(health_checker, "_check_integrations", return_value=ComponentHealth(HealthStatus.HEALTHY)):
                    with patch.object(health_checker, "_check_system_resources", return_value=ComponentHealth(HealthStatus.HEALTHY)):
                        with patch.object(health_checker, "_check_workflow_engine", return_value=ComponentHealth(HealthStatus.HEALTHY)):
                            result = await health_checker.check_health()
                            assert result["status"] == HealthStatus.UNHEALTHY
                            assert "components" in result
                            assert result["components"]["database"]["status"] == HealthStatus.UNHEALTHY

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
            "database": ComponentHealth(HealthStatus.HEALTHY),
            "llm_providers": ComponentHealth(HealthStatus.HEALTHY),
            "integrations": ComponentHealth(HealthStatus.HEALTHY),
            "system_resources": ComponentHealth(HealthStatus.HEALTHY),
            "workflow_engine": ComponentHealth(HealthStatus.HEALTHY),
        }
        result = health_checker._determine_overall_health(components)
        assert result == HealthStatus.HEALTHY

    def test_determine_overall_health_with_degraded(self, health_checker):
        """Test overall health determination with degraded components."""
        components = {
            "database": ComponentHealth(HealthStatus.HEALTHY),
            "llm_providers": ComponentHealth(HealthStatus.DEGRADED),
            "integrations": ComponentHealth(HealthStatus.HEALTHY),
            "system_resources": ComponentHealth(HealthStatus.HEALTHY),
            "workflow_engine": ComponentHealth(HealthStatus.HEALTHY),
        }
        result = health_checker._determine_overall_health(components)
        assert result == HealthStatus.DEGRADED

    def test_determine_overall_health_with_unhealthy(self, health_checker):
        """Test overall health determination with unhealthy components."""
        components = {
            "database": ComponentHealth(HealthStatus.UNHEALTHY),
            "llm_providers": ComponentHealth(HealthStatus.HEALTHY),
            "integrations": ComponentHealth(HealthStatus.HEALTHY),
            "system_resources": ComponentHealth(HealthStatus.HEALTHY),
            "workflow_engine": ComponentHealth(HealthStatus.HEALTHY),
        }
        result = health_checker._determine_overall_health(components)
        assert result == HealthStatus.UNHEALTHY

    def test_determine_overall_health_with_unknown(self, health_checker):
        """Test overall health determination with unknown status."""
        components = {
            "database": ComponentHealth(HealthStatus.UNKNOWN),
            "llm_providers": ComponentHealth(HealthStatus.HEALTHY),
            "integrations": ComponentHealth(HealthStatus.HEALTHY),
            "system_resources": ComponentHealth(HealthStatus.HEALTHY),
            "workflow_engine": ComponentHealth(HealthStatus.HEALTHY),
        }
        result = health_checker._determine_overall_health(components)
        assert result in [HealthStatus.DEGRADED, HealthStatus.UNKNOWN]

