"""
CodeFlow Engine - Core Engine Implementation

Main engine class that orchestrates CodeFlow operations.
"""

import logging
from typing import Any

from codeflow_engine.actions.registry import ActionRegistry
from codeflow_engine.ai.core.providers.manager import LLMProviderManager
from codeflow_engine.config import CodeFlowConfig
from codeflow_engine.exceptions import CodeFlowException, ConfigurationError
from codeflow_engine.health import HealthChecker
from codeflow_engine.integrations.registry import IntegrationRegistry
from codeflow_engine.utils.error_handlers import handle_operation_error
from codeflow_engine.workflows.engine import WorkflowEngine

logger = logging.getLogger(__name__)


class CodeFlowEngine:
    """
    Main CodeFlow Engine class that coordinates all automation activities.

    This class serves as the central orchestrator for:
    - Workflow execution
    - Action processing
    - Integration management
    - AI/LLM provider coordination
    """

    def __init__(self, config: CodeFlowConfig | None = None, log_handler: logging.Handler | None = None):
        """
        Initialize the CodeFlow Engine.

        Args:
            config: Configuration object. If None, loads default config.
            log_handler: Optional logging handler to add to the root logger.
        """
        self.config = config or CodeFlowConfig()
        self.workflow_engine = WorkflowEngine(self.config)
        self.action_registry: ActionRegistry = ActionRegistry()
        self.integration_registry = IntegrationRegistry()
        self.llm_manager = LLMProviderManager(self.config)
        self.health_checker = HealthChecker(self)

        if log_handler:
            logging.getLogger().addHandler(log_handler)

        logger.info("CodeFlow Engine initialized successfully")

    async def __aenter__(self) -> "CodeFlowEngine":
        """Async context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.stop()

    async def start(self) -> None:
        """Start the CodeFlow Engine and initialize all components."""
        try:
            # Validate configuration before starting
            if not self.config.validate():
                msg = "Invalid configuration: Missing required authentication or LLM provider keys"
                logger.error(msg)
                raise ConfigurationError(msg)
            
            await self.workflow_engine.start()
            await self.integration_registry.initialize()
            await self.llm_manager.initialize()
            logger.info("CodeFlow Engine started successfully")
        except ConfigurationError:
            raise
        except Exception as e:
            handle_operation_error("Engine startup", e, CodeFlowException)

    async def stop(self) -> None:
        """Stop the CodeFlow Engine and cleanup resources."""
        try:
            await self.workflow_engine.stop()
            await self.integration_registry.cleanup()
            await self.llm_manager.cleanup()
            logger.info("CodeFlow Engine stopped successfully")
        except Exception as e:
            handle_operation_error("Engine shutdown", e, CodeFlowException)

    async def process_event(
        self, event_type: str, event_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Process an incoming event through the workflow engine.

        Args:
            event_type: Type of event (e.g., 'pull_request', 'issue', 'push')
            event_data: Event payload data

        Returns:
            Processing result dictionary
        """
        try:
            result = await self.workflow_engine.process_event(event_type, event_data)
            logger.info(f"Successfully processed {event_type} event")
            return result
        except Exception as e:
            handle_operation_error("Event processing", e, CodeFlowException)

    def get_status(self) -> dict[str, Any]:
        """
        Get the current status of the CodeFlow Engine.

        Returns:
            Status dictionary with component information
        """
        return {
            "engine": "running",
            "workflow_engine": self.workflow_engine.get_status(),
            "actions": len(self.action_registry.get_all_actions()),
            "integrations": len(self.integration_registry.get_all_integrations()),
            "llm_providers": len(self.llm_manager.get_available_providers()),
            "config": self.config.to_dict(),
        }

    def get_version(self) -> str:
        """Get the CodeFlow Engine version."""
        from codeflow_engine import __version__

        return __version__
    
    async def health_check(self) -> dict[str, Any]:
        """
        Perform comprehensive health check on all components.
        
        Returns:
            Health check results including overall status and component details
        """
        try:
            return await self.health_checker.check_all()
        except Exception as e:
            handle_operation_error("Health check", e, CodeFlowException)
