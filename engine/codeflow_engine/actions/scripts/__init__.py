"""CodeFlow Engine - Script Actions."""

from codeflow_engine.actions.publish_package import PublishPackage
from codeflow_engine.actions._module_aliases import register_module_aliases
from codeflow_engine.actions.run_changed_tests import RunChangedTests
from codeflow_engine.actions.run_db_migrations import RunDBMigrations
from codeflow_engine.actions.run_script import RunScript
from codeflow_engine.actions.seed_database import SeedDatabase
from codeflow_engine.actions.take_screenshots import TakeScreenshots
from codeflow_engine.actions.trigger_deployment import TriggerDeployment

register_module_aliases(
    __name__,
    {
        "publish_package": "codeflow_engine.actions.publish_package",
        "run_changed_tests": "codeflow_engine.actions.run_changed_tests",
        "run_db_migrations": "codeflow_engine.actions.run_db_migrations",
        "run_script": "codeflow_engine.actions.run_script",
        "seed_database": "codeflow_engine.actions.seed_database",
        "take_screenshots": "codeflow_engine.actions.take_screenshots",
        "trigger_deployment": "codeflow_engine.actions.trigger_deployment",
    },
)

__all__ = [
    "PublishPackage",
    "RunChangedTests",
    "RunDBMigrations",
    "RunScript",
    "SeedDatabase",
    "TakeScreenshots",
    "TriggerDeployment",
]
