"""Data models for linting tools.

This module provides shared data structures used across all linting tools
(markdown, YAML, etc.) to eliminate code duplication and ensure consistency.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path


class IssueSeverity(Enum):
    """Severity levels for linting issues.

    Severity levels are ordered from most severe to least severe:
    - ERROR: Critical issues that must be fixed
    - WARNING: Issues that should be addressed
    - STYLE: Stylistic issues that are optional to fix
    """

    ERROR = auto()
    WARNING = auto()
    STYLE = auto()


@dataclass
class LintIssue:
    """Represents a single linting issue.

    Attributes:
        line: The line number where the issue was found (1-indexed)
        column: The column number where the issue was found (0-indexed)
        code: A short code identifying the rule (e.g., "MD022", "YML001")
        message: A human-readable description of the issue
        severity: The severity level of the issue
        fixable: Whether this issue can be automatically fixed
        fix: An optional function that takes the line content and returns the fixed content
        context: Additional context about the issue (e.g., the problematic line)
    """

    line: int
    column: int = 0
    code: str = ""
    message: str = ""
    severity: IssueSeverity = IssueSeverity.WARNING
    fixable: bool = False
    fix: Callable[[str], str] | None = None
    context: str = ""

    def __str__(self) -> str:
        """Return a string representation of the issue."""
        return f"{self.severity.name}:{self.code} - {self.message} (line {self.line}, col {self.column})"


@dataclass
class FileReport:
    """Collection of lint issues for a single file.

    Attributes:
        path: The path to the file that was linted
        issues: A list of LintIssue objects found in the file
        fixed_content: The content of the file after fixes have been applied (if any)
    """

    path: Path
    issues: list[LintIssue] = field(default_factory=list)
    fixed_content: list[str] | None = None

    @property
    def has_issues(self) -> bool:
        """Return True if there are any issues."""
        return bool(self.issues)

    @property
    def has_errors(self) -> bool:
        """Return True if there are any error-level issues."""
        return any(issue.severity == IssueSeverity.ERROR for issue in self.issues)

    @property
    def has_warnings(self) -> bool:
        """Return True if there are any warning-level issues."""
        return any(issue.severity == IssueSeverity.WARNING for issue in self.issues)

    @property
    def has_fixable_issues(self) -> bool:
        """Return True if there are any fixable issues."""
        return any(issue.fixable for issue in self.issues)

    def add_issue(self, issue: LintIssue) -> None:
        """Add an issue to the report."""
        self.issues.append(issue)

    def get_issues_by_severity(self, severity: IssueSeverity) -> list[LintIssue]:
        """Get all issues with the given severity."""
        return [issue for issue in self.issues if issue.severity == severity]

    def get_error_count(self) -> int:
        """Get the count of error-level issues."""
        return len(self.get_issues_by_severity(IssueSeverity.ERROR))

    def get_warning_count(self) -> int:
        """Get the count of warning-level issues."""
        return len(self.get_issues_by_severity(IssueSeverity.WARNING))

    def get_style_count(self) -> int:
        """Get the count of style-level issues."""
        return len(self.get_issues_by_severity(IssueSeverity.STYLE))
