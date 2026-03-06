"""
CodeFlow Engine - Quality Actions

Actions for quality checks, security audits, and performance budgets.
"""

from typing import Any

# Import with error handling for optional dependencies
QualityGates: type[Any] | None = None
try:
    from codeflow_engine.actions.quality.quality_gates import QualityGates
except ImportError:
    pass

CheckPerformanceBudget: type[Any] | None = None
try:
    from codeflow_engine.actions.quality.check_performance_budget import CheckPerformanceBudget
except ImportError:
    pass

CheckLockfileDrift: type[Any] | None = None
try:
    from codeflow_engine.actions.quality.check_lockfile_drift import CheckLockfileDrift
except ImportError:
    pass

CheckDependencyLicenses: type[Any] | None = None
try:
    from codeflow_engine.actions.quality.check_dependency_licenses import CheckDependencyLicenses
except ImportError:
    pass

RunSecurityAudit: type[Any] | None = None
try:
    from codeflow_engine.actions.quality.run_security_audit import RunSecurityAudit
except ImportError:
    pass

RunAccessibilityAudit: type[Any] | None = None
try:
    from codeflow_engine.actions.quality.run_accessibility_audit import RunAccessibilityAudit
except ImportError:
    pass

VisualRegressionTest: type[Any] | None = None
try:
    from codeflow_engine.actions.quality.visual_regression_test import VisualRegressionTest
except ImportError:
    pass

__all__ = [
    "CheckDependencyLicenses",
    "CheckLockfileDrift",
    "CheckPerformanceBudget",
    "QualityGates",
    "RunAccessibilityAudit",
    "RunSecurityAudit",
    "VisualRegressionTest",
]
