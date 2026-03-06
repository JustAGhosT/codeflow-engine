"""Compatibility wrapper for grouped quality gates imports."""

from codeflow_engine.actions._module_aliases import register_module_aliases

register_module_aliases(
    __name__,
    {
        "evaluator": "codeflow_engine.actions.quality_gates.evaluator",
        "models": "codeflow_engine.actions.quality_gates.models",
    },
)

from codeflow_engine.actions.quality_gates.evaluator import (
    QualityGateValidator as QualityGateEvaluator,
)
from codeflow_engine.actions.quality_gates.models import (
    QualityGateInputs as QualityGate,
    QualityGateOutputs as QualityGateResult,
)

__all__ = ["QualityGate", "QualityGateEvaluator", "QualityGateResult"]
