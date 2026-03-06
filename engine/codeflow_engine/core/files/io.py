"""File I/O Operations."""

from datetime import UTC, datetime
from pathlib import Path
import shutil
from typing import Any

import structlog


logger = structlog.get_logger(__name__)


class FileIO:
    @staticmethod
    def read(file_path: str, encoding: str = "utf-8") -> tuple[bool, str]:
        try:
            with Path(file_path).open(encoding=encoding) as f:
                content = f.read()
            return True, content
        except Exception as e:
            logger.warning("file_read_failed", file_path=file_path, error=str(e))
            return False, ""

    @staticmethod
    def read_or_none(file_path: str, encoding: str = "utf-8") -> str | None:
        success, content = FileIO.read(file_path, encoding)
        return content if success else None

    @staticmethod
    def write(
        file_path: str, content: str, encoding: str = "utf-8", create_dirs: bool = False
    ) -> bool:
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
        return Path(file_path).exists()

    @staticmethod
    def is_file(file_path: str) -> bool:
        return Path(file_path).is_file()

    @staticmethod
    def is_dir(file_path: str) -> bool:
        return Path(file_path).is_dir()

    @staticmethod
    def get_size(file_path: str) -> int:
        try:
            return Path(file_path).stat().st_size
        except Exception:
            return 0

    @staticmethod
    def get_info(file_path: str) -> dict[str, Any]:
        try:
            path = Path(file_path)
            if not path.exists():
                return {"exists": False}
            stat = path.stat()
            return {
                "exists": True,
                "size_bytes": stat.st_size,
                "size_mb": stat.st_size / (1024 * 1024),
                "modified_time": datetime.fromtimestamp(
                    stat.st_mtime, tz=UTC
                ).isoformat(),
                "created_time": datetime.fromtimestamp(
                    stat.st_ctime, tz=UTC
                ).isoformat(),
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
        try:
            shutil.copy2(source_path, destination_path)
            logger.debug(
                "file_copied", source=source_path, destination=destination_path
            )
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
        try:
            Path(directory_path).mkdir(parents=parents, exist_ok=True)
            return True
        except Exception as e:
            logger.error("mkdir_failed", directory_path=directory_path, error=str(e))
            return False
