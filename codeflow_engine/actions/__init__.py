"""
CodeFlow Engine Actions.

Core automation actions for GitHub PR processing, organized by category:
- analysis: Code analysis actions (PR review, comment analysis)
- generation: Code/content generation (scaffolding, release notes)
- git: Git operations (patches, branches, releases)
- issues: Issue/PR management (labels, comments)
- quality: Quality checks (security, performance, accessibility)
- ai_actions: AI/LLM-powered features (AutoGen, memory systems)
- platform: Platform detection and integration
- scripts: Script/workflow execution
- maintenance: Maintenance tasks
"""

from typing import Any

from codeflow_engine.actions.registry import ActionRegistry

# Import category modules with error handling for optional dependencies
ai_actions = None
try:
    from codeflow_engine.actions import ai_actions
except (ImportError, OSError):
    pass

analysis = None
try:
    from codeflow_engine.actions import analysis
except (ImportError, OSError):
    pass

base = None
try:
    from codeflow_engine.actions import base
except (ImportError, OSError):
    pass

generation = None
try:
    from codeflow_engine.actions import generation
except (ImportError, OSError):
    pass

git = None
try:
    from codeflow_engine.actions import git
except (ImportError, OSError):
    pass

issues = None
try:
    from codeflow_engine.actions import issues
except (ImportError, OSError):
    pass

maintenance = None
try:
    from codeflow_engine.actions import maintenance
except (ImportError, OSError):
    pass

platform = None
try:
    from codeflow_engine.actions import platform
except (ImportError, OSError):
    pass

quality = None
try:
    from codeflow_engine.actions import quality
except (ImportError, OSError):
    pass

scripts = None
try:
    from codeflow_engine.actions import scripts
except (ImportError, OSError):
    pass

# Re-export commonly used actions for backward compatibility
# Analysis
AICommentAnalyzer: type[Any] | None = None
try:
    from codeflow_engine.actions.analysis import AICommentAnalyzer
except ImportError:
    pass

PRReviewAnalyzer: type[Any] | None = None
try:
    from codeflow_engine.actions.analysis import PRReviewAnalyzer
except ImportError:
    pass

# Issues
IssueCreator: type[Any] | None = None
try:
    from codeflow_engine.actions.issues import IssueCreator
except ImportError:
    pass

PRCommentHandler: type[Any] | None = None
try:
    from codeflow_engine.actions.issues import PRCommentHandler
except ImportError:
    pass

CreateOrUpdateIssue: type[Any] | None = None
try:
    from codeflow_engine.actions.issues import CreateOrUpdateIssue
except ImportError:
    pass

PostComment: type[Any] | None = None
try:
    from codeflow_engine.actions.issues import PostComment
except ImportError:
    pass

LabelPR: type[Any] | None = None
try:
    from codeflow_engine.actions.issues import LabelPR
except ImportError:
    pass

# Git
ApplyGitPatch: type[Any] | None = None
try:
    from codeflow_engine.actions.git import ApplyGitPatch
except ImportError:
    pass

# Quality
QualityGates: type[Any] | None = None
try:
    from codeflow_engine.actions.quality import QualityGates
except ImportError:
    pass

RunSecurityAudit: type[Any] | None = None
try:
    from codeflow_engine.actions.quality import RunSecurityAudit
except ImportError:
    pass

CheckPerformanceBudget: type[Any] | None = None
try:
    from codeflow_engine.actions.quality import CheckPerformanceBudget
except ImportError:
    pass

VisualRegressionTest: type[Any] | None = None
try:
    from codeflow_engine.actions.quality import VisualRegressionTest
except ImportError:
    pass

# AI Actions
AutoGenImplementation: type[Any] | None = None
try:
    from codeflow_engine.actions.ai_actions import AutoGenImplementation
except ImportError:
    pass

AutoGenAgentSystem: type[Any] | None = None
try:
    from codeflow_engine.actions.ai_actions import AutoGenAgentSystem
except ImportError:
    pass

Mem0MemoryManager: type[Any] | None = None
try:
    from codeflow_engine.actions.ai_actions import Mem0MemoryManager
except ImportError:
    pass

LearningMemorySystem: type[Any] | None = None
try:
    from codeflow_engine.actions.ai_actions import LearningMemorySystem
except ImportError:
    pass

LLMProviderManager: type[Any] | None = None
try:
    from codeflow_engine.actions.ai_actions.llm import LLMProviderManager
except ImportError:
    pass

# Platform
PlatformDetector: type[Any] | None = None
try:
    from codeflow_engine.actions.platform import PlatformDetector
except ImportError:
    pass

MultiPlatformIntegrator: type[Any] | None = None
try:
    from codeflow_engine.actions.platform import MultiPlatformIntegrator
except ImportError:
    pass

PrototypeEnhancer: type[Any] | None = None
try:
    from codeflow_engine.actions.platform import PrototypeEnhancer
except ImportError:
    pass

# Generation
GenerateReleaseNotes: type[Any] | None = None
try:
    from codeflow_engine.actions.generation import GenerateReleaseNotes
except ImportError:
    pass

# All available exports
__all__ = [
    # Registry
    "ActionRegistry",
    # Category modules
    "ai_actions",
    "analysis",
    "base",
    "generation",
    "git",
    "issues",
    "maintenance",
    "platform",
    "quality",
    "scripts",
    # Backward compatible action exports
    "AICommentAnalyzer",
    "ApplyGitPatch",
    "AutoGenAgentSystem",
    "AutoGenImplementation",
    "CheckPerformanceBudget",
    "CreateOrUpdateIssue",
    "GenerateReleaseNotes",
    "IssueCreator",
    "LLMProviderManager",
    "LabelPR",
    "LearningMemorySystem",
    "Mem0MemoryManager",
    "MultiPlatformIntegrator",
    "PRCommentHandler",
    "PRReviewAnalyzer",
    "PlatformDetector",
    "PostComment",
    "PrototypeEnhancer",
    "QualityGates",
    "RunSecurityAudit",
    "VisualRegressionTest",
]
