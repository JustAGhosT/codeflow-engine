"""String formatting utilities."""

import re


def truncate_string(
    value: str,
    max_length: int,
    suffix: str = "...",
    preserve_words: bool = True,
) -> str:
    """
    Truncate string to maximum length.

    Args:
        value: String to truncate
        max_length: Maximum length (including suffix)
        suffix: Suffix to add if truncated
        preserve_words: Whether to preserve word boundaries

    Returns:
        Truncated string
    """
    if len(value) <= max_length:
        return value

    if preserve_words:
        # Try to truncate at word boundary
        truncated = value[:max_length - len(suffix)]
        last_space = truncated.rfind(" ")
        if last_space > max_length * 0.5:  # Only use word boundary if reasonable
            truncated = truncated[:last_space]
        return truncated + suffix

    return value[:max_length - len(suffix)] + suffix


def slugify(value: str, separator: str = "-") -> str:
    """
    Convert string to URL-friendly slug.

    Args:
        value: String to slugify
        separator: Word separator character

    Returns:
        Slugified string
    """
    # Convert to lowercase
    slug = value.lower()

    # Replace spaces and underscores with separator
    slug = re.sub(r"[\s_]+", separator, slug)

    # Remove all non-word characters except separator
    slug = re.sub(r"[^\w\-]+", "", slug)

    # Remove multiple separators
    slug = re.sub(rf"{re.escape(separator)}+", separator, slug)

    # Remove leading/trailing separators
    slug = slug.strip(separator)

    return slug


def camel_to_snake(value: str) -> str:
    """
    Convert camelCase to snake_case.

    Args:
        value: CamelCase string

    Returns:
        snake_case string
    """
    # Insert underscore before uppercase letters
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", value)
    return snake.lower()


def snake_to_camel(value: str, capitalize_first: bool = False) -> str:
    """
    Convert snake_case to camelCase.

    Args:
        value: snake_case string
        capitalize_first: Whether to capitalize first letter (PascalCase)

    Returns:
        camelCase or PascalCase string
    """
    components = value.split("_")

    if capitalize_first:
        return "".join(word.capitalize() for word in components)
    else:
        return components[0] + "".join(word.capitalize() for word in components[1:])
