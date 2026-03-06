"""CodeFlow Engine - Maintenance Actions."""

from codeflow_engine.actions.enforce_import_order import EnforceImportOrder
from codeflow_engine.actions.find_large_assets import FindLargeAssets
from codeflow_engine.actions.generate_todo_report import GenerateTodoReport
from codeflow_engine.actions._module_aliases import register_module_aliases
from codeflow_engine.actions.update_dependency import UpdateDependency
from codeflow_engine.actions.update_docs_file import UpdateDocsFile
from codeflow_engine.actions.update_migration_plan import UpdateMigrationPlan

register_module_aliases(
    __name__,
    {
        "enforce_import_order": "codeflow_engine.actions.enforce_import_order",
        "find_large_assets": "codeflow_engine.actions.find_large_assets",
        "generate_todo_report": "codeflow_engine.actions.generate_todo_report",
        "update_dependency": "codeflow_engine.actions.update_dependency",
        "update_docs_file": "codeflow_engine.actions.update_docs_file",
        "update_migration_plan": "codeflow_engine.actions.update_migration_plan",
    },
)

__all__ = [
    "EnforceImportOrder",
    "FindLargeAssets",
    "GenerateTodoReport",
    "UpdateDependency",
    "UpdateDocsFile",
    "UpdateMigrationPlan",
]
