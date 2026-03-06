"""Input validation and sanitization utilities."""

from typing import Any


def sanitize_input(value: str, max_length: int | None = None) -> str:
    """
    Sanitize input string.

    Args:
        value: Input string to sanitize
        max_length: Maximum length (None for no limit)

    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        value = str(value)

    # Remove leading/trailing whitespace
    sanitized = value.strip()

    # Remove null bytes
    sanitized = sanitized.replace("\x00", "")

    # Truncate if needed
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized


def validate_input(value: Any, input_type: type, required: bool = True) -> tuple[bool, str | None]:
    """
    Validate input value.

    Args:
        value: Value to validate
        input_type: Expected type
        required: Whether value is required

    Returns:
        Tuple of (is_valid, error_message)
    """
    if value is None:
        if required:
            return False, "Value is required"
        return True, None

    if not isinstance(value, input_type):
        return False, f"Expected {input_type.__name__}, got {type(value).__name__}"

    return True, None
