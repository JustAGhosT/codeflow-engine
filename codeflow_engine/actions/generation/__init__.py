"""
CodeFlow Engine - Generation Actions

Actions for generating code, documentation, and scaffolding.
"""

from typing import Any

# Import with error handling for optional dependencies
GenerateBarrelFile: type[Any] | None = None
try:
    from codeflow_engine.actions.generation.generate_barrel_file import GenerateBarrelFile
except ImportError:
    pass

GeneratePropTable: type[Any] | None = None
try:
    from codeflow_engine.actions.generation.generate_prop_table import GeneratePropTable
except ImportError:
    pass

GenerateReleaseNotes: type[Any] | None = None
try:
    from codeflow_engine.actions.generation.generate_release_notes import GenerateReleaseNotes
except ImportError:
    pass

__all__ = [
    "GenerateBarrelFile",
    "GeneratePropTable",
    "GenerateReleaseNotes",
]
