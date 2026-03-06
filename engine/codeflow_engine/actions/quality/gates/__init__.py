"""Compatibility wrapper for grouped quality gates imports."""

from codeflow_engine.actions.quality_gates.evaluator import QualityGateEvaluator
from codeflow_engine.actions.quality_gates.models import QualityGate, QualityGateResult

__all__ = ["QualityGate", "QualityGateEvaluator", "QualityGateResult"]