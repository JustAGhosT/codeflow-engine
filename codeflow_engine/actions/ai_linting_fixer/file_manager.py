"""
File Manager Module - Facade for File Operations.

This module provides a high-level interface for file operations,
composing the core file components (FileIO, BackupService, ContentValidator).

For new code, prefer using the core components directly:
- codeflow_engine.core.files.FileIO
- codeflow_engine.core.files.BackupService
- codeflow_engine.core.files.ContentValidator
"""

import logging
from typing import Any

from codeflow_engine.core.files import (
    BackupService,
    ContentValidator,
    FileIO,
)


logger = logging.getLogger(__name__)


class FileManager:
    """
    Facade for file operations, backups, and validation.

    This class composes the core file components to provide
    backward-compatible high-level file management.

    For new code, consider using the core components directly.
    """

    def __init__(self, backup_directory: str | None = None) -> None:
        """
        Initialize the file manager.

        Args:
            backup_directory: Directory to store backups
        """
        self.backup_directory = backup_directory or "./backups"
        self._backup_service = BackupService(self.backup_directory)
        self._content_validator = ContentValidator()

    # ===================
    # Backup Operations
    # ===================

    def create_backup(self, file_path: str) -> str | None:
        """
        Create a backup of a file before modification.

        Args:
            file_path: Path to the file to backup

        Returns:
            Backup path or None if failed
        """
        backup = self._backup_service.create_backup(file_path)
        return backup.backup_path if backup else None

    def create_backups(self, file_paths: list) -> int:
        """
        Create backups for multiple files.

        Args:
            file_paths: List of file paths to backup

        Returns:
            Number of successful backups
        """
        return self._backup_service.create_backups(file_paths)

    def restore_from_backup(self, file_path: str, backup_path: str) -> bool:
        """
        Restore a file from its backup.

        Args:
            file_path: Target file path
            backup_path: Path to the backup

        Returns:
            True if successful
        """
        return self._backup_service.restore(file_path, backup_path)

    def list_backups(self, file_path: str | None = None) -> list:
        """
        List available backups.

        Args:
            file_path: Optional filter by original file

        Returns:
            List of backup info dictionaries
        """
        return self._backup_service.list_backups(file_path)

    def cleanup_old_backups(
        self,
        max_backups: int = 10,
        older_than_days: int | None = None,
    ) -> int:
        """
        Clean up old backup files.

        Args:
            max_backups: Maximum backups to keep
            older_than_days: Optional age limit

        Returns:
            Number of backups removed
        """
        return self._backup_service.cleanup_old_backups(max_backups, older_than_days)

    # ===================
    # File I/O Operations
    # ===================

    def read_file_safely(self, file_path: str) -> tuple[bool, str]:
        """
        Read a file safely.

        Args:
            file_path: Path to the file

        Returns:
            Tuple of (success, content)
        """
        return FileIO.read(file_path)

    def read_file(self, file_path: str) -> str | None:
        """
        Read a file and return its content.

        Args:
            file_path: Path to the file

        Returns:
            Content or None if failed
        """
        return FileIO.read_or_none(file_path)

    def write_file(self, file_path: str, content: str) -> bool:
        """
        Write content to a file.

        Args:
            file_path: Path to the file
            content: Content to write

        Returns:
            True if successful
        """
        return FileIO.write(file_path, content)

    def write_file_safely(
        self,
        file_path: str,
        content: str,
        backup: bool = True,
    ) -> bool:
        """
        Write content with optional backup.

        Args:
            file_path: Path to the file
            content: Content to write
            backup: Whether to create backup first

        Returns:
            True if successful
        """
        backup_path = None
        if backup and FileIO.exists(file_path):
            backup_result = self._backup_service.create_backup(file_path)
            backup_path = backup_result.backup_path if backup_result else None

        success = FileIO.write(file_path, content)

        if not success and backup_path:
            # Try to restore from backup
            self._backup_service.restore(file_path, backup_path)
            logger.info("Restored %s from backup after write failure", file_path)

        return success

    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists."""
        return FileIO.exists(file_path)

    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        return FileIO.get_size(file_path)

    def get_file_info(self, file_path: str) -> dict:
        """Get comprehensive file information."""
        return FileIO.get_info(file_path)

    def create_directory_safely(self, directory_path: str) -> bool:
        """Create a directory safely."""
        return FileIO.mkdir(directory_path)

    def copy_file_safely(self, source_path: str, destination_path: str) -> bool:
        """Copy a file safely."""
        return FileIO.copy(source_path, destination_path)

    def move_file_safely(self, source_path: str, destination_path: str) -> bool:
        """Move a file safely."""
        return FileIO.move(source_path, destination_path)

    def delete_file(self, file_path: str) -> bool:
        """Delete a file safely."""
        return FileIO.delete(file_path)

    # ===================
    # Content Validation
    # ===================

    def validate_file_content(self, content: str) -> dict[str, Any]:
        """
        Validate file content for common issues.

        Args:
            content: Content to validate

        Returns:
            Validation result dictionary
        """
        result = self._content_validator.validate(content)
        return {
            "valid": result.valid,
            "issues": result.issues,
            "warnings": result.warnings,
        }
