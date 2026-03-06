"""
AI Extensions Module

AI extensions and implementation roadmap functionality.
Re-exports from the implementation_roadmap module for backward compatibility.
"""

from typing import Any

# Re-export from implementation_roadmap for backward compatibility
Phase1ExtensionImplementor: type[Any] | None = None
PhaseExecution: type[Any] | None = None
PhaseManager: type[Any] | None = None
ReportGenerator: type[Any] | None = None
Task: type[Any] | None = None
TaskExecution: type[Any] | None = None
TaskExecutor: type[Any] | None = None
TaskRegistry: type[Any] | None = None

try:
    from codeflow_engine.ai.implementation_roadmap import (
        Phase1ExtensionImplementor,
        PhaseExecution,
        PhaseManager,
        ReportGenerator,
        Task,
        TaskExecution,
        TaskExecutor,
        TaskRegistry,
    )
except ImportError:
    pass

__all__ = [
    "Phase1ExtensionImplementor",
    "PhaseExecution",
    "PhaseManager",
    "ReportGenerator",
    "Task",
    "TaskExecution",
    "TaskExecutor",
    "TaskRegistry",
]
