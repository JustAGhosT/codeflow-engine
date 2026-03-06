"""Compatibility wrapper for grouped platform analysis imports."""

from codeflow_engine.actions._module_aliases import register_module_aliases

register_module_aliases(
	__name__,
	{
		"base": "codeflow_engine.actions.platform_detection.analysis.base",
		"handlers": "codeflow_engine.actions.platform_detection.analysis.handlers",
		"patterns": "codeflow_engine.actions.platform_detection.analysis.patterns",
	},
)

from codeflow_engine.actions.platform_detection.analysis import *  # noqa: F403
