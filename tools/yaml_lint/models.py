"""Data models for the YAML linter.

This module re-exports the shared lint models from tools.core.models
for backwards compatibility.
"""

from tools.core.models import FileReport, IssueSeverity, LintIssue

__all__ = ["IssueSeverity", "LintIssue", "FileReport"]
