"""
CodeFlow Engine - Maintenance Actions

Actions for maintenance tasks like updating dependencies, docs, and code quality.
"""

from typing import Any

# Import with error handling for optional dependencies
UpdateDependency: type[Any] | None = None
try:
    from codeflow_engine.actions.maintenance.update_dependency import UpdateDependency
except ImportError:
    pass

UpdateDocsFile: type[Any] | None = None
try:
    from codeflow_engine.actions.maintenance.update_docs_file import UpdateDocsFile
except ImportError:
    pass

UpdateMigrationPlan: type[Any] | None = None
try:
    from codeflow_engine.actions.maintenance.update_migration_plan import UpdateMigrationPlan
except ImportError:
    pass

FindLargeAssets: type[Any] | None = None
try:
    from codeflow_engine.actions.maintenance.find_large_assets import FindLargeAssets
except ImportError:
    pass

EnforceImportOrder: type[Any] | None = None
try:
    from codeflow_engine.actions.maintenance.enforce_import_order import EnforceImportOrder
except ImportError:
    pass

GenerateTodoReport: type[Any] | None = None
try:
    from codeflow_engine.actions.maintenance.generate_todo_report import GenerateTodoReport
except ImportError:
    pass

__all__ = [
    "EnforceImportOrder",
    "FindLargeAssets",
    "GenerateTodoReport",
    "UpdateDependency",
    "UpdateDocsFile",
    "UpdateMigrationPlan",
]
