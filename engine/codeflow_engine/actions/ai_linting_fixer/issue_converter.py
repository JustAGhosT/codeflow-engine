"""
Issue Converter Utility

This module provides utilities for converting between different LintingIssue representations
to avoid circular imports and schema mismatches.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codeflow_engine.actions.ai_linting_fixer.detection import LintingIssue
    from codeflow_engine.actions.ai_linting_fixer.models import \
        LintingIssue as ModelLintingIssue


def convert_detection_issue_to_model_issue(detection_issue: "LintingIssue") -> "ModelLintingIssue":
    """Convert a LintingIssue from detection module to models module."""
    # Import here to avoid circular imports
    from codeflow_engine.actions.ai_linting_fixer.models import \
        LintingIssue as ModelLintingIssue

    line_number = getattr(detection_issue, "line_number", 0)
    column_number = getattr(detection_issue, "column_number", 0)
    return ModelLintingIssue(
        file_path=detection_issue.file_path,
        line_number=line_number,
        column_number=column_number,
        error_code=detection_issue.error_code,
        message=detection_issue.message,
        line_content=getattr(detection_issue, "line_content", ""),
        column=column_number,
    )


def convert_detection_issues_to_model_issues(
    detection_issues: list["LintingIssue"]
) -> list["ModelLintingIssue"]:
    """Convert a list of LintingIssues from detection module to models module."""
    return [convert_detection_issue_to_model_issue(issue) for issue in detection_issues]
