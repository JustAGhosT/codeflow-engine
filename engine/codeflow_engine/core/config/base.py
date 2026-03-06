"""
Base Configuration Utilities.

Provides environment variable helpers and base configuration patterns.
"""

import os
from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TypeVar

import structlog


logger = structlog.get_logger(__name__)

T = TypeVar("T")


def env_var(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name, "").lower()
    if not value:
        return default
    return value in ("1", "true", "yes", "on")


def env_int(name: str, default: int = 0) -> int:
    value = os.getenv(name, "")
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        logger.warning("invalid_env_int", name=name, value=value, default=default)
        return default


def env_float(name: str, default: float = 0.0) -> float:
    value = os.getenv(name, "")
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        logger.warning("invalid_env_float", name=name, value=value, default=default)
        return default


def env_list(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    value = os.getenv(name, "")
    if not value:
        return default or []
    return [item.strip() for item in value.split(separator) if item.strip()]


@dataclass
class BaseConfig(ABC):
    @classmethod
    def from_env(cls, prefix: str = "") -> "BaseConfig":
        raise NotImplementedError("Subclasses must implement from_env")

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def merge(self, overrides: dict[str, Any]) -> "BaseConfig":
        current = self.to_dict()
        current.update(overrides)
        return type(self)(**current)


@dataclass
class ConfigLoader:
    config_paths: list[str] = field(default_factory=lambda: ["pyproject.toml", "config.yaml"])

    def load_toml(self, path: str, section: str | None = None) -> dict[str, Any]:
        if not Path(path).exists():
            return {}

        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib  # type: ignore[import-not-found]
            except ImportError:
                logger.debug("toml_not_available", path=path)
                return {}

        try:
            with open(path, "rb") as f:
                data = tomllib.load(f)

            if section:
                for key in section.split("."):
                    data = data.get(key, {})
                    if not isinstance(data, dict):
                        return {}

            return data
        except Exception as e:
            logger.warning("toml_load_failed", path=path, error=str(e))
            return {}

    def load_yaml(self, path: str) -> dict[str, Any]:
        if not Path(path).exists():
            return {}

        try:
            import yaml
        except ImportError:
            logger.debug("yaml_not_available", path=path)
            return {}

        try:
            with open(path, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.warning("yaml_load_failed", path=path, error=str(e))
            return {}

    def load_json(self, path: str) -> dict[str, Any]:
        if not Path(path).exists():
            return {}

        import json

        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning("json_load_failed", path=path, error=str(e))
            return {}

    def load(self, path: str, section: str | None = None) -> dict[str, Any]:
        path_lower = path.lower()
        if path_lower.endswith(".toml"):
            return self.load_toml(path, section)
        if path_lower.endswith((".yaml", ".yml")):
            return self.load_yaml(path)
        if path_lower.endswith(".json"):
            return self.load_json(path)
        logger.warning("unknown_config_format", path=path)
        return {}

    def load_merged(self, paths: list[str] | None = None, section: str | None = None) -> dict[str, Any]:
        paths = paths or self.config_paths
        merged: dict[str, Any] = {}
        for path in paths:
            config = self.load(path, section)
            merged = self._deep_merge(merged, config)
        return merged

    def _deep_merge(self, base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
        result = dict(base)
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result