"""
File I/O Operations.

Provides safe file reading and writing operations with consistent error handling.
"""

from datetime import datetime, UTC
from pathlib import Path
import shutil
from typing import Any

import structlog


logger = structlog.get_logger(__name__)


class FileIO:
    """
    Handles basic file I/O operations with consistent error handling.

    Provides safe methods for reading, writing, copying, and moving files.
    Does NOT handle backups - use BackupService for that.
    """

    @staticmethod
    def read(file_path: str, encoding: str = "utf-8") -> tuple[bool, str]:
        """
        Read a file safely.

        Args:
            file_path: Path to the file
            encoding: File encoding (default: utf-8)

        Returns:
            Tuple of (success, content)
        """
        try:
            with Path(file_path).open(encoding=encoding) as f:
                content = f.read()
            return True, content
        except Exception as e:
            logger.warning("file_read_failed", file_path=file_path, error=str(e))
            return False, ""

    @staticmethod
    def read_or_none(file_path: str, encoding: str = "utf-8") -> str | None:
        """
        Read a file, returning None on failure.

        Args:
            file_path: Path to the file
            encoding: File encoding (default: utf-8)

        Returns:
            File content or None
        """
        success, content = FileIO.read(file_path, encoding)
        return content if success else None

    @staticmethod
    def write(
        file_path: str,
        content: str,
        encoding: str = "utf-8",
        create_dirs: bool = False,
    ) -> bool:
        """
        Write content to a file safely.

        Args:
            file_path: Path to the file
            content: Content to write
            encoding: File encoding (default: utf-8)
            create_dirs: Whether to create parent directories

        Returns:
            True if successful, False otherwise
        """
        try:
            path = Path(file_path)
            if create_dirs:
                path.parent.mkdir(parents=True, exist_ok=True)

            with path.open("w", encoding=encoding) as f:
                f.write(content)

            logger.debug("file_written", file_path=file_path, size=len(content))
            return True
        except Exception as e:
            logger.error("file_write_failed", file_path=file_path, error=str(e))
            return False

    @staticmethod
    def exists(file_path: str) -> bool:
        """
        Check if a file exists.

        Args:
            file_path: Path to check

        Returns:
            True if file exists
        """
        return Path(file_path).exists()

    @staticmethod
    def is_file(file_path: str) -> bool:
        """
        Check if path is a file.

        Args:
            file_path: Path to check

        Returns:
            True if path is a file
        """
        return Path(file_path).is_file()

    @staticmethod
    def is_dir(file_path: str) -> bool:
        """
        Check if path is a directory.

        Args:
            file_path: Path to check

        Returns:
            True if path is a directory
        """
        return Path(file_path).is_dir()

    @staticmethod
    def get_size(file_path: str) -> int:
        """
        Get file size in bytes.

        Args:
            file_path: Path to the file

        Returns:
            File size in bytes, 0 if file doesn't exist
        """
        try:
            return Path(file_path).stat().st_size
        except Exception:
            return 0

    @staticmethod
    def get_info(file_path: str) -> dict[str, Any]:
        """
        Get comprehensive file information.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with file information
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return {"exists": False}

            stat = path.stat()
            return {
                "exists": True,
                "size_bytes": stat.st_size,
                "size_mb": stat.st_size / (1024 * 1024),
                "modified_time": datetime.fromtimestamp(stat.st_mtime, tz=UTC).isoformat(),
                "created_time": datetime.fromtimestamp(stat.st_ctime, tz=UTC).isoformat(),
                "is_file": path.is_file(),
                "is_directory": path.is_dir(),
                "extension": path.suffix,
                "name": path.name,
                "stem": path.stem,
                "parent": str(path.parent),
            }
        except Exception as e:
            logger.debug("file_info_failed", file_path=file_path, error=str(e))
            return {"exists": False, "error": str(e)}

    @staticmethod
    def copy(source_path: str, destination_path: str) -> bool:
        """
        Copy a file safely.

        Args:
            source_path: Source file path
            destination_path: Destination file path

        Returns:
            True if successful
        """
        try:
            shutil.copy2(source_path, destination_path)
            logger.debug("file_copied", source=source_path, destination=destination_path)
            return True
        except Exception as e:
            logger.error(
                "file_copy_failed",
                source=source_path,
                destination=destination_path,
                error=str(e),
            )
            return False

    @staticmethod
    def move(source_path: str, destination_path: str) -> bool:
        """
        Move a file safely.

        Args:
            source_path: Source file path
            destination_path: Destination file path

        Returns:
            True if successful
        """
        try:
            shutil.move(source_path, destination_path)
            logger.debug("file_moved", source=source_path, destination=destination_path)
            return True
        except Exception as e:
            logger.error(
                "file_move_failed",
                source=source_path,
                destination=destination_path,
                error=str(e),
            )
            return False

    @staticmethod
    def delete(file_path: str) -> bool:
        """
        Delete a file safely.

        Args:
            file_path: Path to delete

        Returns:
            True if successful or file doesn't exist
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return True

            path.unlink()
            logger.debug("file_deleted", file_path=file_path)
            return True
        except Exception as e:
            logger.error("file_delete_failed", file_path=file_path, error=str(e))
            return False

    @staticmethod
    def mkdir(directory_path: str, parents: bool = True) -> bool:
        """
        Create a directory safely.

        Args:
            directory_path: Directory path to create
            parents: Whether to create parent directories

        Returns:
            True if successful
        """
        try:
            Path(directory_path).mkdir(parents=parents, exist_ok=True)
            return True
        except Exception as e:
            logger.error("mkdir_failed", directory_path=directory_path, error=str(e))
            return False
