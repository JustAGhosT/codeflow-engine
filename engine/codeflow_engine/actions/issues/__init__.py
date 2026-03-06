"""CodeFlow Engine - Issue/PR Actions."""

from codeflow_engine.actions.create_or_update_issue import CreateOrUpdateIssue
from codeflow_engine.actions.find_stale_issues_or_prs import FindStaleIssuesOrPRs
from codeflow_engine.actions.handle_pr_comment import PRCommentHandler
from codeflow_engine.actions._module_aliases import register_module_aliases
from codeflow_engine.actions.issue_creator import IssueCreator
from codeflow_engine.actions.label_pr import LabelPR
from codeflow_engine.actions.label_pr_by_size import LabelPRBySize
from codeflow_engine.actions.post_comment import PostComment

register_module_aliases(
    __name__,
    {
        "create_or_update_issue": "codeflow_engine.actions.create_or_update_issue",
        "find_stale_issues_or_prs": "codeflow_engine.actions.find_stale_issues_or_prs",
        "handle_pr_comment": "codeflow_engine.actions.handle_pr_comment",
        "issue_creator": "codeflow_engine.actions.issue_creator",
        "label_pr": "codeflow_engine.actions.label_pr",
        "label_pr_by_size": "codeflow_engine.actions.label_pr_by_size",
        "post_comment": "codeflow_engine.actions.post_comment",
    },
)

__all__ = [
    "CreateOrUpdateIssue",
    "FindStaleIssuesOrPRs",
    "IssueCreator",
    "LabelPR",
    "LabelPRBySize",
    "PRCommentHandler",
    "PostComment",
]
