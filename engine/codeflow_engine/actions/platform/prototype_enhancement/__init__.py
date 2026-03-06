"""Compatibility wrapper for grouped prototype enhancement imports."""

from codeflow_engine.actions._module_aliases import register_module_aliases

register_module_aliases(
	__name__,
	{
		"config_loader": "codeflow_engine.actions.prototype_enhancement.config_loader",
		"enhancement_strategies": "codeflow_engine.actions.prototype_enhancement.enhancement_strategies",
		"enhancer": "codeflow_engine.actions.prototype_enhancement.enhancer",
		"file_generators": "codeflow_engine.actions.prototype_enhancement.file_generators",
		"generators": "codeflow_engine.actions.prototype_enhancement.generators",
		"platform_configs": "codeflow_engine.actions.prototype_enhancement.platform_configs",
		"template_metadata": "codeflow_engine.actions.prototype_enhancement.template_metadata",
	},
)

from codeflow_engine.actions.prototype_enhancement import *  # noqa: F403
