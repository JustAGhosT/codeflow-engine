"""CodeFlow Engine - Analysis Actions."""

from codeflow_engine.actions.ai_comment_analyzer import AICommentAnalyzer
from codeflow_engine.actions.pr_review_analyzer import PRReviewAnalyzer

from codeflow_engine.actions._module_aliases import register_module_aliases

register_module_aliases(
	__name__,
	{
		"ai_comment_analyzer": "codeflow_engine.actions.ai_comment_analyzer",
		"analyze_console_logs": "codeflow_engine.actions.analyze_console_logs",
		"extract_pr_comment_data": "codeflow_engine.actions.extract_pr_comment_data",
		"find_dead_code": "codeflow_engine.actions.find_dead_code",
		"pr_review_analyzer": "codeflow_engine.actions.pr_review_analyzer",
	},
)

__all__ = ["AICommentAnalyzer", "PRReviewAnalyzer"]
