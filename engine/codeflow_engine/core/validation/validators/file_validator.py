"""File Type Validator."""

import html
from pathlib import Path
from typing import Any

from codeflow_engine.core.validation.base import BaseTypeValidator
from codeflow_engine.core.validation.patterns import SecurityPatterns
from codeflow_engine.core.validation.result import ValidationResult, ValidationSeverity


class FileTypeValidator(BaseTypeValidator):
    DEFAULT_ALLOWED_EXTENSIONS = {".txt", ".json", ".yaml", ".yml", ".md"}
    TEXT_EXTENSIONS = {".txt", ".json", ".yaml", ".yml", ".md"}
    DEFAULT_MAX_SIZE = 10 * 1024 * 1024

    def __init__(self, allowed_extensions: set[str] | None = None, max_size: int | None = None, security_patterns: SecurityPatterns | None = None) -> None:
        super().__init__(security_patterns)
        self.allowed_extensions = allowed_extensions if allowed_extensions is not None else self.DEFAULT_ALLOWED_EXTENSIONS
        self.max_size = max_size if max_size is not None else self.DEFAULT_MAX_SIZE

    def can_validate(self, value: Any) -> bool:
        if isinstance(value, tuple) and len(value) == 2:
            filename, content = value
            return isinstance(filename, str) and isinstance(content, bytes)
        return False

    def validate(self, key: str, value: Any) -> ValidationResult:
        if not self.can_validate(value):
            return ValidationResult.failure(f"Expected file upload tuple (filename, content) for '{key}'", ValidationSeverity.MEDIUM)
        filename, content = value
        return self.validate_file_upload(filename, content)

    def validate_file_upload(self, filename: str, content: bytes, max_size: int | None = None) -> ValidationResult:
        effective_max_size = max_size if max_size is not None else self.max_size
        if len(content) > effective_max_size:
            return ValidationResult.failure(f"File too large: {len(content)} > {effective_max_size}", ValidationSeverity.MEDIUM)
        file_ext = Path(filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            return ValidationResult.failure(f"File extension not allowed: {file_ext}", ValidationSeverity.HIGH)
        if file_ext in self.TEXT_EXTENSIONS:
            content_result = self._validate_text_content(content)
            if not content_result.is_valid:
                return content_result
        return ValidationResult.success({
            "filename": html.escape(filename),
            "content": content,
            "size": len(content),
            "extension": file_ext,
        })

    def _validate_text_content(self, content: bytes) -> ValidationResult:
        try:
            content_str = content.decode("utf-8")
        except UnicodeDecodeError:
            return ValidationResult.failure("File contains invalid UTF-8 encoding", ValidationSeverity.HIGH)
        threat_result = self._check_security_threats("file_content", content_str)
        if not threat_result.is_valid:
            return threat_result
        return ValidationResult.success()