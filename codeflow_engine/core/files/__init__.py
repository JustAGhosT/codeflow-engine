"""
Core File Operations Module.

Provides focused file handling components following Single Responsibility Principle:
- FileIO: Basic file read/write operations
- BackupService: File backup and restore capabilities
- ContentValidator: File content validation
"""

from codeflow_engine.core.files.io import FileIO
from codeflow_engine.core.files.backup import BackupService, FileBackup
from codeflow_engine.core.files.validator import ContentValidator, ContentValidationResult

__all__ = [
    "FileIO",
    "BackupService",
    "FileBackup",
    "ContentValidator",
    "ContentValidationResult",
]
