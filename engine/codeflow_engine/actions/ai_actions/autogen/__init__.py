"""Compatibility wrapper for grouped AutoGen imports."""

from codeflow_engine.actions._module_aliases import register_module_aliases

from codeflow_engine.actions.autogen.agents import AutoGenAgentFactory
from codeflow_engine.actions.autogen.models import AutoGenInputs, AutoGenOutputs
from codeflow_engine.actions.autogen.system import AutoGenAgentSystem

register_module_aliases(
    __name__,
    {
        "agents": "codeflow_engine.actions.autogen.agents",
        "models": "codeflow_engine.actions.autogen.models",
        "system": "codeflow_engine.actions.autogen.system",
    },
)

__all__ = [
    "AutoGenAgentFactory",
    "AutoGenAgentSystem",
    "AutoGenInputs",
    "AutoGenOutputs",
]
