"""Base Manager Framework."""

from abc import ABC
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, TypeVar

import structlog


T = TypeVar("T", bound="ManagerConfig")


@dataclass
class ManagerConfig:
    name: str = "manager"
    enabled: bool = True
    log_level: str = "INFO"
    metadata: dict[str, Any] = field(default_factory=dict)

    def merge(self: T, overrides: dict[str, Any]) -> T:
        current = {k: v for k, v in self.__dict__.items()}
        current.update(overrides)
        return type(self)(**current)


class BaseManager(ABC):
    def __init__(self, config: ManagerConfig | None = None) -> None:
        self._config = config or ManagerConfig()
        self._logger = structlog.get_logger(self._config.name)
        self._started = False
        self._start_time: datetime | None = None

    @property
    def config(self) -> ManagerConfig:
        return self._config

    @property
    def logger(self) -> structlog.stdlib.BoundLogger:
        return self._logger

    @property
    def is_started(self) -> bool:
        return self._started

    @property
    def uptime_seconds(self) -> float:
        if not self._start_time:
            return 0.0
        return (datetime.now(UTC) - self._start_time).total_seconds()

    def startup(self) -> None:
        if self._started:
            self._logger.warning("manager_already_started", name=self._config.name)
            return
        self._logger.info("manager_starting", name=self._config.name)
        self._start_time = datetime.now(UTC)
        self._on_startup()
        self._started = True
        self._logger.info("manager_started", name=self._config.name)

    def shutdown(self) -> None:
        if not self._started:
            return
        self._logger.info("manager_shutting_down", name=self._config.name)
        self._on_shutdown()
        self._started = False
        self._logger.info("manager_shutdown", name=self._config.name)

    def _on_startup(self) -> None:
        pass

    def _on_shutdown(self) -> None:
        pass


class SessionMixin:
    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, Any]] = {}
        self._current_session: str | None = None

    @property
    def current_session_id(self) -> str | None:
        return self._current_session

    @property
    def active_sessions(self) -> list[str]:
        return [
            sid for sid, data in self._sessions.items() if data.get("is_active", False)
        ]

    def start_session(
        self, session_id: str, metadata: dict[str, Any] | None = None
    ) -> None:
        self._sessions[session_id] = {
            "start_time": datetime.now(UTC),
            "is_active": True,
            "metadata": metadata or {},
            "data": {},
        }
        self._current_session = session_id

    def end_session(self, session_id: str | None = None) -> None:
        sid = session_id or self._current_session
        if sid and sid in self._sessions:
            self._sessions[sid]["is_active"] = False
            self._sessions[sid]["end_time"] = datetime.now(UTC)
            if self._current_session == sid:
                self._current_session = None

    def get_session_data(self, session_id: str | None = None) -> dict[str, Any]:
        sid = session_id or self._current_session
        if sid and sid in self._sessions:
            return self._sessions[sid].get("data", {})
        return {}

    def set_session_data(
        self, key: str, value: Any, session_id: str | None = None
    ) -> None:
        sid = session_id or self._current_session
        if sid and sid in self._sessions:
            self._sessions[sid].setdefault("data", {})[key] = value


class StatsMixin:
    def __init__(self) -> None:
        self._stats: dict[str, int | float] = {}
        self._stats_history: list[dict[str, Any]] = []

    def increment_stat(self, name: str, amount: int = 1) -> None:
        self._stats[name] = self._stats.get(name, 0) + amount

    def set_stat(self, name: str, value: int | float) -> None:
        self._stats[name] = value

    def get_stat(self, name: str, default: int | float = 0) -> int | float:
        return self._stats.get(name, default)

    def get_all_stats(self) -> dict[str, int | float]:
        return self._stats.copy()

    def record_event(self, event_type: str, data: dict[str, Any] | None = None) -> None:
        self._stats_history.append(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "event_type": event_type,
                "data": data or {},
            }
        )

    def get_stats_history(
        self, event_type: str | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        history = self._stats_history
        if event_type:
            history = [e for e in history if e["event_type"] == event_type]
        if limit:
            history = history[-limit:]
        return history

    def clear_stats(self) -> None:
        self._stats.clear()
        self._stats_history.clear()
