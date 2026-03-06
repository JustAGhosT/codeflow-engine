"""Compatibility wrapper for grouped AutoGen imports."""

from codeflow_engine.actions.autogen.agents import AutoGenAgentFactory
from codeflow_engine.actions.autogen.models import AutoGenInputs, AutoGenOutputs
from codeflow_engine.actions.autogen.system import AutoGenAgentSystem

__all__ = [
    "AutoGenAgentFactory",
    "AutoGenAgentSystem",
    "AutoGenInputs",
    "AutoGenOutputs",
]
