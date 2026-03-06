"""CodeFlow Engine - Git Actions."""

from codeflow_engine.actions.apply_git_patch import ApplyGitPatch
from codeflow_engine.actions._module_aliases import register_module_aliases
from codeflow_engine.actions.create_github_release import (
    CreateGithubRelease as CreateGitHubRelease,
)
from codeflow_engine.actions.delete_branch import DeleteBranch
from codeflow_engine.actions.find_merged_branches import FindMergedBranches

register_module_aliases(
    __name__,
    {
        "apply_git_patch": "codeflow_engine.actions.apply_git_patch",
        "create_github_release": "codeflow_engine.actions.create_github_release",
        "delete_branch": "codeflow_engine.actions.delete_branch",
        "find_merged_branches": "codeflow_engine.actions.find_merged_branches",
    },
)

__all__ = ["ApplyGitPatch", "CreateGitHubRelease", "DeleteBranch", "FindMergedBranches"]
