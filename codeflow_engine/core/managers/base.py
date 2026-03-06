"""
Base Manager Framework.

Provides common patterns for manager classes including:
- Structured logging
- Configuration management
- Session handling
- Statistics collection
"""

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any, TypeVar

import structlog


T = TypeVar("T", bound="ManagerConfig")


@dataclass
class ManagerConfig:
    """
    Base configuration for managers.

    Subclass this to add manager-specific configuration options.
    """

    name: str = "manager"
    enabled: bool = True
    log_level: str = "INFO"
    metadata: dict[str, Any] = field(default_factory=dict)

    def merge(self: T, overrides: dict[str, Any]) -> T:
        """
        Create a new config with overrides applied.

        Args:
            overrides: Dictionary of values to override

        Returns:
            New config instance with overrides applied
        """
        current = {k: v for k, v in self.__dict__.items()}
        current.update(overrides)
        return type(self)(**current)


class BaseManager(ABC):
    """
    Abstract base class for manager components.

    Provides:
    - Structured logging via structlog
    - Configuration handling
    - Lifecycle management (startup/shutdown)

    Usage:
        class MyManager(BaseManager):
            def __init__(self, config: MyConfig | None = None):
                super().__init__(config or MyConfig())

            def _on_startup(self) -> None:
                # Custom initialization
                pass
    """

    def __init__(self, config: ManagerConfig | None = None) -> None:
        """
        Initialize the manager.

        Args:
            config: Optional configuration object
        """
        self._config = config or ManagerConfig()
        self._logger = structlog.get_logger(self._config.name)
        self._started = False
        self._start_time: datetime | None = None

    @property
    def config(self) -> ManagerConfig:
        """Get the manager configuration."""
        return self._config

    @property
    def logger(self) -> structlog.stdlib.BoundLogger:
        """Get the bound logger for this manager."""
        return self._logger

    @property
    def is_started(self) -> bool:
        """Check if the manager has been started."""
        return self._started

    @property
    def uptime_seconds(self) -> float:
        """Get the uptime in seconds since startup."""
        if not self._start_time:
            return 0.0
        return (datetime.now(UTC) - self._start_time).total_seconds()

    def startup(self) -> None:
        """
        Start the manager.

        Calls _on_startup() for subclass initialization.
        """
        if self._started:
            self._logger.warning("manager_already_started", name=self._config.name)
            return

        self._logger.info("manager_starting", name=self._config.name)
        self._start_time = datetime.now(UTC)
        self._on_startup()
        self._started = True
        self._logger.info("manager_started", name=self._config.name)

    def shutdown(self) -> None:
        """
        Shutdown the manager.

        Calls _on_shutdown() for subclass cleanup.
        """
        if not self._started:
            return

        self._logger.info("manager_shutting_down", name=self._config.name)
        self._on_shutdown()
        self._started = False
        self._logger.info("manager_shutdown", name=self._config.name)

    def _on_startup(self) -> None:
        """
        Hook for subclass startup initialization.

        Override in subclasses to perform custom startup logic.
        """
        pass

    def _on_shutdown(self) -> None:
        """
        Hook for subclass shutdown cleanup.

        Override in subclasses to perform custom cleanup logic.
        """
        pass


class SessionMixin:
    """
    Mixin providing session management capabilities.

    Add this to managers that need to track operations within sessions.
    """

    def __init__(self) -> None:
        """Initialize session tracking."""
        self._sessions: dict[str, dict[str, Any]] = {}
        self._current_session: str | None = None

    @property
    def current_session_id(self) -> str | None:
        """Get the current session ID."""
        return self._current_session

    @property
    def active_sessions(self) -> list[str]:
        """Get list of active session IDs."""
        return [
            sid for sid, data in self._sessions.items()
            if data.get("is_active", False)
        ]

    def start_session(self, session_id: str, metadata: dict[str, Any] | None = None) -> None:
        """
        Start a new session.

        Args:
            session_id: Unique identifier for the session
            metadata: Optional metadata to attach to the session
        """
        self._sessions[session_id] = {
            "start_time": datetime.now(UTC),
            "is_active": True,
            "metadata": metadata or {},
            "data": {},
        }
        self._current_session = session_id

    def end_session(self, session_id: str | None = None) -> None:
        """
        End a session.

        Args:
            session_id: Session to end, defaults to current session
        """
        sid = session_id or self._current_session
        if sid and sid in self._sessions:
            self._sessions[sid]["is_active"] = False
            self._sessions[sid]["end_time"] = datetime.now(UTC)

            if self._current_session == sid:
                self._current_session = None

    def get_session_data(self, session_id: str | None = None) -> dict[str, Any]:
        """
        Get session data.

        Args:
            session_id: Session to get data for, defaults to current session

        Returns:
            Session data dictionary
        """
        sid = session_id or self._current_session
        if sid and sid in self._sessions:
            return self._sessions[sid].get("data", {})
        return {}

    def set_session_data(self, key: str, value: Any, session_id: str | None = None) -> None:
        """
        Set session data.

        Args:
            key: Data key
            value: Data value
            session_id: Session to set data for, defaults to current session
        """
        sid = session_id or self._current_session
        if sid and sid in self._sessions:
            self._sessions[sid].setdefault("data", {})[key] = value


class StatsMixin:
    """
    Mixin providing statistics collection capabilities.

    Add this to managers that need to track operational metrics.
    """

    def __init__(self) -> None:
        """Initialize statistics tracking."""
        self._stats: dict[str, int | float] = {}
        self._stats_history: list[dict[str, Any]] = []

    def increment_stat(self, name: str, amount: int = 1) -> None:
        """
        Increment a counter statistic.

        Args:
            name: Statistic name
            amount: Amount to increment by
        """
        self._stats[name] = self._stats.get(name, 0) + amount

    def set_stat(self, name: str, value: int | float) -> None:
        """
        Set a statistic value.

        Args:
            name: Statistic name
            value: Value to set
        """
        self._stats[name] = value

    def get_stat(self, name: str, default: int | float = 0) -> int | float:
        """
        Get a statistic value.

        Args:
            name: Statistic name
            default: Default value if stat doesn't exist

        Returns:
            Statistic value
        """
        return self._stats.get(name, default)

    def get_all_stats(self) -> dict[str, int | float]:
        """
        Get all statistics.

        Returns:
            Dictionary of all statistics
        """
        return self._stats.copy()

    def record_event(self, event_type: str, data: dict[str, Any] | None = None) -> None:
        """
        Record an event in statistics history.

        Args:
            event_type: Type of event
            data: Optional event data
        """
        self._stats_history.append({
            "timestamp": datetime.now(UTC).isoformat(),
            "event_type": event_type,
            "data": data or {},
        })

    def get_stats_history(
        self,
        event_type: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get statistics history.

        Args:
            event_type: Optional filter by event type
            limit: Optional limit on number of events

        Returns:
            List of recorded events
        """
        history = self._stats_history
        if event_type:
            history = [e for e in history if e["event_type"] == event_type]
        if limit:
            history = history[-limit:]
        return history

    def clear_stats(self) -> None:
        """Clear all statistics and history."""
        self._stats.clear()
        self._stats_history.clear()
