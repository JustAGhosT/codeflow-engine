"""Development shim for the canonical monorepo package.

The only source-of-truth package lives at ``engine/codeflow_engine``.
This shim makes ``import codeflow_engine`` work from the repository root
without recreating or maintaining a duplicate source tree.
"""

from __future__ import annotations

from pathlib import Path

_CANONICAL_PACKAGE_DIR = (
    Path(__file__).resolve().parent.parent / "engine" / "codeflow_engine"
)
_CANONICAL_INIT = _CANONICAL_PACKAGE_DIR / "__init__.py"

if not _CANONICAL_INIT.exists():
    raise ImportError(
        "The canonical package was not found at engine/codeflow_engine. "
        "Check the monorepo layout."
    )

__path__ = [str(_CANONICAL_PACKAGE_DIR)]
__file__ = str(_CANONICAL_INIT)

if __spec__ is not None:
    __spec__.submodule_search_locations = __path__

exec(
    compile(_CANONICAL_INIT.read_text(encoding="utf-8"), __file__, "exec"),
    globals(),
    globals(),
)
