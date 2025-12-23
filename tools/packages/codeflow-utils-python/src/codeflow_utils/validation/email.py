"""Email validation utilities."""

import re
from typing import Optional


# RFC 5322 compliant email regex (simplified)
EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)


def validate_email(email: str) -> bool:
    """
    Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        True if email is valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False

    email = email.strip()

    if not email:
        return False

    # Basic format check
    if not EMAIL_PATTERN.match(email):
        return False

    # Additional checks
    if email.count('@') != 1:
        return False

    local, domain = email.split('@', 1)

    # Local part checks
    if len(local) > 64:
        return False

    if local.startswith('.') or local.endswith('.'):
        return False

    if '..' in local:
        return False

    # Domain part checks
    if len(domain) > 255:
        return False

    if domain.startswith('.') or domain.endswith('.'):
        return False

    if '..' in domain:
        return False

    return True


def is_valid_email(email: str) -> bool:
    """
    Alias for validate_email for consistency.

    Args:
        email: Email address to validate

    Returns:
        True if email is valid, False otherwise
    """
    return validate_email(email)


def extract_email_domain(email: str) -> Optional[str]:
    """
    Extract domain from email address.

    Args:
        email: Email address

    Returns:
        Domain name or None if invalid
    """
    if not validate_email(email):
        return None

    return email.split('@', 1)[1]


def normalize_email(email: str) -> Optional[str]:
    """
    Normalize email address (lowercase, trim).

    Args:
        email: Email address to normalize

    Returns:
        Normalized email or None if invalid
    """
    if not email or not isinstance(email, str):
        return None

    email = email.strip().lower()

    if not validate_email(email):
        return None

    return email
