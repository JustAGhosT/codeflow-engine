"""Severity handling utilities for CLI tools."""

from tools.core.models import IssueSeverity

# Mapping from severity string names to enum values
SEVERITY_MAPPING: dict[str, IssueSeverity] = {
    "error": IssueSeverity.ERROR,
    "warning": IssueSeverity.WARNING,
    "style": IssueSeverity.STYLE,
}


def get_severity_threshold(severity_name: str) -> IssueSeverity:
    """Convert severity name to IssueSeverity enum.

    Args:
        severity_name: The name of the severity level (case-insensitive)

    Returns:
        The corresponding IssueSeverity enum value

    Raises:
        KeyError: If the severity name is not recognized
    """
    return SEVERITY_MAPPING[severity_name.lower()]


def filter_issues_by_severity(issues: list, min_severity: IssueSeverity) -> list:
    """Filter issues to only include those at or above the minimum severity.

    Args:
        issues: List of LintIssue objects
        min_severity: The minimum severity level to include

    Returns:
        Filtered list of issues
    """
    return [issue for issue in issues if issue.severity.value <= min_severity.value]
