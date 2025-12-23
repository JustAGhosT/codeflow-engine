"""Configuration validation utilities."""

import os
from typing import Any


def validate_config(config: dict[str, Any], required_keys: list[str]) -> tuple[bool, list[str]]:
    """
    Validate configuration dictionary.

    Args:
        config: Configuration dictionary to validate
        required_keys: List of required keys

    Returns:
        Tuple of (is_valid, missing_keys)
    """
    if not isinstance(config, dict):
        return False, ["Configuration must be a dictionary"]

    missing_keys = [key for key in required_keys if key not in config or config[key] is None]
    return len(missing_keys) == 0, missing_keys


def validate_environment_variables(required_vars: list[str]) -> dict[str, Any]:
    """
    Check for required environment variables.

    Args:
        required_vars: List of required environment variable names

    Returns:
        Dictionary with validation results:
        - valid: bool - Whether all variables are present
        - missing: list[str] - List of missing variable names
        - found: list[str] - List of found variable names
    """
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    found_vars = [var for var in required_vars if var not in missing_vars]

    return {
        "valid": len(missing_vars) == 0,
        "missing": missing_vars,
        "found": found_vars,
    }
