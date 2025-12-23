"""Output formatting utilities for linting tools.

This module provides consistent formatting for linting output across all
linting tools, supporting both text and JSON output formats.
"""

import json
import sys
from pathlib import Path
from typing import Any

from tools.core.models import FileReport, IssueSeverity, LintIssue

# ANSI color codes for terminal output
COLORS = {
    IssueSeverity.ERROR: "\033[31m",  # Red
    IssueSeverity.WARNING: "\033[33m",  # Yellow
    IssueSeverity.STYLE: "\033[36m",  # Cyan
}
RESET = "\033[0m"


def format_issue_text(
    issue: LintIssue,
    file_path: Path,
    use_color: bool = True,
    verbose: int = 0,
    omit_file: bool = False,
) -> str:
    """Format a single issue for text output.

    Args:
        issue: The LintIssue to format
        file_path: The path to the file containing the issue
        use_color: Whether to use ANSI color codes
        verbose: Verbosity level (0=minimal, 1+=detailed)
        omit_file: Whether to omit the file path from the output (useful when
            file path is already displayed as a header)

    Returns:
        A formatted string representation of the issue
    """
    severity_color = COLORS.get(issue.severity, "") if use_color else ""
    reset = RESET if use_color else ""
    severity_name = issue.severity.name.lower()

    if omit_file:
        location = f"{issue.line}:{issue.column}"
    else:
        location = f"{file_path}:{issue.line}:{issue.column}"

    if verbose >= 1:
        # Detailed format with context
        code_part = f": {issue.code}" if issue.code else ""
        result = f"{location}: {severity_color}{severity_name}{reset}{code_part}: {issue.message}"
        if issue.context:
            result += f"\n  {issue.context}"
        return result

    # Standard format
    if issue.code:
        return f"{location}: {severity_color}{severity_name}{reset}: {issue.message} [{issue.code}]"
    return f"{location}: {severity_color}{severity_name}{reset}: {issue.message}"


def format_issue_json(issue: LintIssue) -> dict[str, Any]:
    """Format a single issue for JSON output.

    Args:
        issue: The LintIssue to format

    Returns:
        A dictionary representation of the issue
    """
    return {
        "line": issue.line,
        "column": issue.column,
        "code": issue.code,
        "message": issue.message,
        "severity": issue.severity.name.lower(),
        "fixable": issue.fixable,
    }


def format_report_text(
    reports: dict[Path, FileReport],
    use_color: bool | None = None,
    verbose: int = 0,
    min_severity: IssueSeverity | None = None,
) -> str:
    """Format multiple file reports for text output.

    Args:
        reports: Dictionary mapping file paths to FileReport objects
        use_color: Whether to use ANSI colors (None = auto-detect from TTY)
        verbose: Verbosity level (0=minimal, 1+=detailed)
        min_severity: Minimum severity level to include (None = include all)

    Returns:
        A formatted string representation of all reports
    """
    if use_color is None:
        use_color = sys.stdout.isatty()

    lines: list[str] = []
    total_issues = 0
    total_files = 0

    for file_path, report in sorted(reports.items()):
        if not report.has_issues:
            continue

        # Filter by severity if specified
        issues = report.issues
        if min_severity is not None:
            issues = [i for i in issues if i.severity.value <= min_severity.value]

        if not issues:
            continue

        total_files += 1
        total_issues += len(issues)

        lines.append(f"\n{file_path}:")
        for issue in sorted(issues, key=lambda x: (x.line, x.column)):
            lines.append(f"  {format_issue_text(issue, file_path, use_color, verbose, omit_file=True)}")

    if total_issues > 0 or verbose > 0:
        lines.append(format_summary(total_issues, total_files))

    return "\n".join(lines)


def format_report_json(
    reports: dict[Path, FileReport],
    min_severity: IssueSeverity | None = None,
    indent: int = 2,
) -> str:
    """Format multiple file reports for JSON output.

    Args:
        reports: Dictionary mapping file paths to FileReport objects
        min_severity: Minimum severity level to include (None = include all)
        indent: JSON indentation level

    Returns:
        A JSON string representation of all reports
    """
    output: list[dict[str, Any]] = []

    for file_path, report in reports.items():
        if not report.has_issues:
            continue

        # Filter by severity if specified
        issues = report.issues
        if min_severity is not None:
            issues = [i for i in issues if i.severity.value <= min_severity.value]

        if not issues:
            continue

        file_data = {
            "file": str(file_path),
            "issues": [format_issue_json(issue) for issue in issues],
        }
        output.append(file_data)

    return json.dumps(output, indent=indent)


def format_summary(issue_count: int, file_count: int) -> str:
    """Format a summary line for the report.

    Args:
        issue_count: Total number of issues found
        file_count: Total number of files with issues

    Returns:
        A formatted summary string
    """
    issue_word = "issue" if issue_count == 1 else "issues"
    file_word = "file" if file_count == 1 else "files"

    if issue_count == 0:
        return "\nNo issues found"
    return f"\nFound {issue_count} {issue_word} in {file_count} {file_word}"
