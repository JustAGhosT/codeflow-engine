"""URL validation utilities."""

from urllib.parse import urlparse


def validate_url(url: str, schemes: list[str] | None = None) -> tuple[bool, str | None]:
    """
    Validate URL format.

    Args:
        url: URL string to validate
        schemes: Allowed URL schemes (None for any)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url or not isinstance(url, str):
        return False, "URL must be a non-empty string"

    try:
        parsed = urlparse(url)

        if not parsed.scheme:
            return False, "URL must include a scheme (e.g., https://)"

        if not parsed.netloc:
            return False, "URL must include a domain"

        if schemes and parsed.scheme not in schemes:
            return False, f"URL scheme must be one of: {', '.join(schemes)}"

        return True, None
    except Exception as e:
        return False, f"Invalid URL format: {str(e)}"


def is_valid_url(url: str, schemes: list[str] | None = None) -> bool:
    """
    Check if URL is valid.

    Args:
        url: URL string to check
        schemes: Allowed URL schemes (None for any)

    Returns:
        True if URL is valid, False otherwise
    """
    is_valid, _ = validate_url(url, schemes)
    return is_valid
