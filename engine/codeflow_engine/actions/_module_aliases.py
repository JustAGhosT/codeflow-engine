"""Helpers for preserving legacy module import paths within the canonical package."""

from __future__ import annotations

import importlib
import sys


def register_module_aliases(package_name: str, aliases: dict[str, str]) -> None:
    """Register legacy submodule paths as aliases to canonical modules."""
    for alias, target in aliases.items():
        full_alias = f"{package_name}.{alias}"
        if full_alias in sys.modules:
            continue

        try:
            sys.modules[full_alias] = importlib.import_module(target)
        except (ImportError, OSError):
            continue
