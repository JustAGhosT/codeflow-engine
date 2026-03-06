"""
CodeFlow Engine - Analysis Actions

Actions for analyzing code, PRs, and comments.
"""

from typing import Any

# Import with error handling for optional dependencies
AICommentAnalyzer: type[Any] | None = None
try:
    from codeflow_engine.actions.analysis.ai_comment_analyzer import AICommentAnalyzer
except ImportError:
    pass

PRReviewAnalyzer: type[Any] | None = None
try:
    from codeflow_engine.actions.analysis.pr_review_analyzer import PRReviewAnalyzer
except ImportError:
    pass

__all__ = [
    "AICommentAnalyzer",
    "PRReviewAnalyzer",
]
