"""
CodeFlow Engine - Git Actions

Actions for Git operations like patches, branches, and releases.
"""

from typing import Any

# Import with error handling for optional dependencies
ApplyGitPatch: type[Any] | None = None
try:
    from codeflow_engine.actions.git.apply_git_patch import ApplyGitPatch
except ImportError:
    pass

DeleteBranch: type[Any] | None = None
try:
    from codeflow_engine.actions.git.delete_branch import DeleteBranch
except ImportError:
    pass

CreateGitHubRelease: type[Any] | None = None
try:
    from codeflow_engine.actions.git.create_github_release import CreateGitHubRelease
except ImportError:
    pass

__all__ = [
    "ApplyGitPatch",
    "CreateGitHubRelease",
    "DeleteBranch",
]
