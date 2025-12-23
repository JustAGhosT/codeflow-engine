"""
Core Manager Framework.

Provides base classes and utilities for building manager components
with consistent patterns for logging, configuration, and lifecycle.
"""

from codeflow_engine.core.managers.base import (
    BaseManager,
    ManagerConfig,
    SessionMixin,
    StatsMixin,
)

__all__ = [
    "BaseManager",
    "ManagerConfig",
    "SessionMixin",
    "StatsMixin",
]
