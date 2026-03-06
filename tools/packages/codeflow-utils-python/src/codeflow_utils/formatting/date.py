"""Date and time formatting utilities."""

from datetime import datetime
from typing import Optional


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime to string.

    Args:
        dt: Datetime object
        format_str: Format string (default: ISO-like format)

    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_str)


def format_iso_datetime(dt: datetime) -> str:
    """
    Format datetime to ISO 8601 string.

    Args:
        dt: Datetime object

    Returns:
        ISO 8601 formatted string
    """
    return dt.isoformat()


def format_relative_time(dt: datetime, now: Optional[datetime] = None) -> str:
    """
    Format datetime as relative time (e.g., "2 hours ago").

    Args:
        dt: Datetime object
        now: Current datetime (defaults to now)

    Returns:
        Relative time string
    """
    if now is None:
        now = datetime.now()

    delta = now - dt

    if delta.total_seconds() < 0:
        # Future time
        delta = dt - now
        if delta.days > 365:
            years = delta.days // 365
            return f"in {years} year{'s' if years > 1 else ''}"
        elif delta.days > 30:
            months = delta.days // 30
            return f"in {months} month{'s' if months > 1 else ''}"
        elif delta.days > 0:
            return f"in {delta.days} day{'s' if delta.days > 1 else ''}"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"in {hours} hour{'s' if hours > 1 else ''}"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"in {minutes} minute{'s' if minutes > 1 else ''}"
        else:
            return "in a moment"

    # Past time
    if delta.days > 365:
        years = delta.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif delta.days > 30:
        months = delta.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif delta.days > 0:
        return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
    elif delta.seconds > 3600:
        hours = delta.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif delta.seconds > 60:
        minutes = delta.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "just now"
