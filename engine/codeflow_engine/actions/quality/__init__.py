"""CodeFlow Engine - Quality Actions."""

from codeflow_engine.actions.check_dependency_licenses import CheckDependencyLicenses
from codeflow_engine.actions.check_lockfile_drift import CheckLockfileDrift
from codeflow_engine.actions.check_performance_budget import CheckPerformanceBudget
from codeflow_engine.actions._module_aliases import register_module_aliases
from codeflow_engine.actions.quality_gates import QualityGateValidator as QualityGates
from codeflow_engine.actions.run_accessibility_audit import RunAccessibilityAudit
from codeflow_engine.actions.run_security_audit import RunSecurityAudit
from codeflow_engine.actions.visual_regression_test import VisualRegressionTest

register_module_aliases(
    __name__,
    {
        "check_dependency_licenses": "codeflow_engine.actions.check_dependency_licenses",
        "check_lockfile_drift": "codeflow_engine.actions.check_lockfile_drift",
        "check_performance_budget": "codeflow_engine.actions.check_performance_budget",
        "quality_gates": "codeflow_engine.actions.quality_gates",
        "run_accessibility_audit": "codeflow_engine.actions.run_accessibility_audit",
        "run_security_audit": "codeflow_engine.actions.run_security_audit",
        "visual_regression_test": "codeflow_engine.actions.visual_regression_test",
    },
)

__all__ = [
    "CheckDependencyLicenses",
    "CheckLockfileDrift",
    "CheckPerformanceBudget",
    "QualityGates",
    "RunAccessibilityAudit",
    "RunSecurityAudit",
    "VisualRegressionTest",
]
