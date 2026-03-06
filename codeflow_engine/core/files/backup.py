"""
Backup Service.

Provides file backup, restore, and cleanup operations.
"""

from dataclasses import dataclass, field
from datetime import datetime, UTC
import operator
from pathlib import Path
import shutil
from typing import Any

import structlog

from codeflow_engine.core.files.io import FileIO


logger = structlog.get_logger(__name__)


@dataclass
class FileBackup:
    """Information about a file backup."""

    file_path: str
    backup_path: str
    backup_time: datetime
    original_size: int
    metadata: dict[str, Any] = field(default_factory=dict)


class BackupService:
    """
    Manages file backups and restore operations.

    Provides:
    - Creating timestamped backups
    - Listing available backups
    - Restoring from backups
    - Cleanup of old backups
    """

    def __init__(self, backup_directory: str = "./backups") -> None:
        """
        Initialize the backup service.

        Args:
            backup_directory: Directory to store backups
        """
        self.backup_directory = Path(backup_directory)
        self._ensure_backup_directory()

    def _ensure_backup_directory(self) -> None:
        """Ensure the backup directory exists."""
        try:
            self.backup_directory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.warning("backup_dir_create_failed", error=str(e))

    def create_backup(self, file_path: str, prefix: str = "") -> FileBackup | None:
        """
        Create a backup of a file.

        Args:
            file_path: Path to the file to backup
            prefix: Optional prefix for backup filename

        Returns:
            FileBackup info or None if failed
        """
        path = Path(file_path)
        if not path.exists():
            logger.warning("backup_source_not_found", file_path=file_path)
            return None

        try:
            timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            prefix_part = f"{prefix}_" if prefix else ""
            backup_filename = f"{path.stem}.{prefix_part}backup_{timestamp}{path.suffix}"
            backup_path = self.backup_directory / backup_filename

            shutil.copy2(file_path, backup_path)

            backup = FileBackup(
                file_path=str(path.resolve()),
                backup_path=str(backup_path),
                backup_time=datetime.now(UTC),
                original_size=FileIO.get_size(file_path),
            )

            logger.info("backup_created", file_path=file_path, backup_path=str(backup_path))
            return backup

        except Exception as e:
            logger.error("backup_failed", file_path=file_path, error=str(e))
            return None

    def create_backups(self, file_paths: list[str], prefix: str = "") -> int:
        """
        Create backups for multiple files.

        Args:
            file_paths: List of file paths to backup
            prefix: Optional prefix for backup filenames

        Returns:
            Number of successful backups
        """
        successful = 0
        for file_path in file_paths:
            if self.create_backup(file_path, prefix):
                successful += 1
        return successful

    def restore(self, file_path: str, backup_path: str) -> bool:
        """
        Restore a file from backup.

        Args:
            file_path: Original file path to restore to
            backup_path: Path to the backup file

        Returns:
            True if successful
        """
        if not Path(backup_path).exists():
            logger.error("backup_not_found", backup_path=backup_path)
            return False

        try:
            shutil.copy2(backup_path, file_path)
            logger.info("file_restored", file_path=file_path, backup_path=backup_path)
            return True
        except Exception as e:
            logger.error(
                "restore_failed",
                file_path=file_path,
                backup_path=backup_path,
                error=str(e),
            )
            return False

    def list_backups(self, file_path: str | None = None) -> list[dict[str, Any]]:
        """
        List available backups.

        Args:
            file_path: Optional filter by original file

        Returns:
            List of backup info dictionaries, sorted newest first
        """
        try:
            if not self.backup_directory.exists():
                return []

            backups = []
            for backup_file in self.backup_directory.glob("*.backup_*"):
                try:
                    stat = backup_file.stat()
                    backup_info = {
                        "backup_path": str(backup_file),
                        "backup_name": backup_file.name,
                        "size_bytes": stat.st_size,
                        "modified_time": datetime.fromtimestamp(
                            stat.st_mtime, tz=UTC
                        ).isoformat(),
                    }

                    # Extract original filename
                    name = backup_file.name
                    if ".backup_" in name:
                        original_stem = name.split(".backup_")[0]
                        # Remove any prefix (e.g., "session_")
                        parts = original_stem.rsplit(".", 1)
                        backup_info["original_stem"] = parts[0] if parts else original_stem

                        # Filter by file_path if specified
                        if file_path:
                            file_stem = Path(file_path).stem
                            if not backup_info["original_stem"].endswith(file_stem):
                                continue

                    backups.append(backup_info)
                except Exception:
                    continue

            # Sort by modification time (newest first)
            backups.sort(key=operator.itemgetter("modified_time"), reverse=True)
            return backups

        except Exception as e:
            logger.error("list_backups_failed", error=str(e))
            return []

    def get_latest_backup(self, file_path: str) -> str | None:
        """
        Get the path to the latest backup for a file.

        Args:
            file_path: Original file path

        Returns:
            Path to latest backup or None
        """
        backups = self.list_backups(file_path)
        return backups[0]["backup_path"] if backups else None

    def cleanup_old_backups(
        self,
        max_backups: int = 10,
        older_than_days: int | None = None,
    ) -> int:
        """
        Clean up old backup files.

        Args:
            max_backups: Maximum number of backups to keep
            older_than_days: Optional age limit in days

        Returns:
            Number of backups removed
        """
        try:
            backups = self.list_backups()
            if len(backups) <= max_backups:
                return 0

            # Identify backups to remove
            backups_to_remove = backups[max_backups:]

            # Filter by age if specified
            if older_than_days:
                cutoff_time = datetime.now(UTC).timestamp() - (older_than_days * 24 * 60 * 60)
                backups_to_remove = [
                    backup for backup in backups_to_remove
                    if datetime.fromisoformat(backup["modified_time"]).timestamp() < cutoff_time
                ]

            removed = 0
            for backup in backups_to_remove:
                try:
                    Path(backup["backup_path"]).unlink()
                    logger.debug("backup_removed", backup_path=backup["backup_path"])
                    removed += 1
                except Exception as e:
                    logger.warning(
                        "backup_remove_failed",
                        backup_path=backup["backup_path"],
                        error=str(e),
                    )

            logger.info("backups_cleaned", removed=removed)
            return removed

        except Exception as e:
            logger.error("cleanup_failed", error=str(e))
            return 0
