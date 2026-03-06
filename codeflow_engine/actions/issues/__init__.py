"""
CodeFlow Engine - Issue/PR Actions

Actions for managing issues, PRs, comments, and labels.
"""

from typing import Any

# Import with error handling for optional dependencies
IssueCreator: type[Any] | None = None
try:
    from codeflow_engine.actions.issues.issue_creator import IssueCreator
except ImportError:
    pass

PRCommentHandler: type[Any] | None = None
try:
    from codeflow_engine.actions.issues.handle_pr_comment import PRCommentHandler
except ImportError:
    pass

CreateOrUpdateIssue: type[Any] | None = None
try:
    from codeflow_engine.actions.issues.create_or_update_issue import CreateOrUpdateIssue
except ImportError:
    pass

PostComment: type[Any] | None = None
try:
    from codeflow_engine.actions.issues.post_comment import PostComment
except ImportError:
    pass

LabelPR: type[Any] | None = None
try:
    from codeflow_engine.actions.issues.label_pr import LabelPR
except ImportError:
    pass

LabelPRBySize: type[Any] | None = None
try:
    from codeflow_engine.actions.issues.label_pr_by_size import LabelPRBySize
except ImportError:
    pass

FindStaleIssuesOrPRs: type[Any] | None = None
try:
    from codeflow_engine.actions.issues.find_stale_issues_or_prs import FindStaleIssuesOrPRs
except ImportError:
    pass

__all__ = [
    "CreateOrUpdateIssue",
    "FindStaleIssuesOrPRs",
    "IssueCreator",
    "LabelPR",
    "LabelPRBySize",
    "PRCommentHandler",
    "PostComment",
]
