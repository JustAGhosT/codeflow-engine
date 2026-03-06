"""CodeFlow Engine - Generation Actions."""

from codeflow_engine.actions.generate_barrel_file import GenerateBarrelFile
from codeflow_engine.actions.generate_prop_table import GeneratePropTable
from codeflow_engine.actions.generate_release_notes import GenerateReleaseNotes
from codeflow_engine.actions._module_aliases import register_module_aliases
from codeflow_engine.actions.scaffold_api_route import (
    ScaffoldApiRoute as ScaffoldAPIRoute,
)
from codeflow_engine.actions.scaffold_component import ScaffoldComponent
from codeflow_engine.actions.scaffold_shared_hook import ScaffoldSharedHook
from codeflow_engine.actions.svg_to_component import SvgToComponent as SVGToComponent

register_module_aliases(
    __name__,
    {
        "generate_barrel_file": "codeflow_engine.actions.generate_barrel_file",
        "generate_prop_table": "codeflow_engine.actions.generate_prop_table",
        "generate_release_notes": "codeflow_engine.actions.generate_release_notes",
        "scaffold_api_route": "codeflow_engine.actions.scaffold_api_route",
        "scaffold_component": "codeflow_engine.actions.scaffold_component",
        "scaffold_shared_hook": "codeflow_engine.actions.scaffold_shared_hook",
        "svg_to_component": "codeflow_engine.actions.svg_to_component",
    },
)

__all__ = [
    "GenerateBarrelFile",
    "GeneratePropTable",
    "GenerateReleaseNotes",
    "ScaffoldAPIRoute",
    "ScaffoldComponent",
    "ScaffoldSharedHook",
    "SVGToComponent",
]
