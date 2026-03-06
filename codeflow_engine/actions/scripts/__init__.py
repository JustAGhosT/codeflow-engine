"""
CodeFlow Engine - Script Actions

Actions for running scripts, tests, deployments, and database operations.
"""

from typing import Any

# Import with error handling for optional dependencies
RunScript: type[Any] | None = None
try:
    from codeflow_engine.actions.scripts.run_script import RunScript
except ImportError:
    pass

RunChangedTests: type[Any] | None = None
try:
    from codeflow_engine.actions.scripts.run_changed_tests import RunChangedTests
except ImportError:
    pass

RunDBMigrations: type[Any] | None = None
try:
    from codeflow_engine.actions.scripts.run_db_migrations import RunDBMigrations
except ImportError:
    pass

SeedDatabase: type[Any] | None = None
try:
    from codeflow_engine.actions.scripts.seed_database import SeedDatabase
except ImportError:
    pass

TriggerDeployment: type[Any] | None = None
try:
    from codeflow_engine.actions.scripts.trigger_deployment import TriggerDeployment
except ImportError:
    pass

PublishPackage: type[Any] | None = None
try:
    from codeflow_engine.actions.scripts.publish_package import PublishPackage
except ImportError:
    pass

__all__ = [
    "PublishPackage",
    "RunChangedTests",
    "RunDBMigrations",
    "RunScript",
    "SeedDatabase",
    "TriggerDeployment",
]
