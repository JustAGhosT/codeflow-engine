"""
Base Models

This module contains base model classes and mixins for the CodeFlow system.
"""

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class BaseModel(ABC):
    """Base class for all CodeFlow models with common functionality."""

    id: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary representation."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif hasattr(value, "to_dict"):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result


@dataclass
class TimestampMixin:
    """Mixin for models that need timestamp tracking."""

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None

    def touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()


@dataclass
class MetadataMixin:
    """Mixin for models that support arbitrary metadata."""

    metadata: dict[str, Any] = field(default_factory=dict)

    def set_metadata(self, key: str, value: Any) -> None:
        """Set a metadata key-value pair."""
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get a metadata value by key."""
        return self.metadata.get(key, default)


__all__ = [
    "BaseModel",
    "MetadataMixin",
    "TimestampMixin",
]
