"""
Content Validator.

Validates file content for common issues and encoding problems.
"""

from dataclasses import dataclass, field
from typing import Any

import structlog


logger = structlog.get_logger(__name__)


@dataclass
class ContentValidationResult:
    """Result of content validation."""

    valid: bool = True
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class ContentValidator:
    """
    Validates file content for common issues.

    Checks for:
    - Empty content
    - Encoding issues
    - Long lines
    - Mixed line endings
    - Trailing whitespace
    """

    # Default thresholds
    MAX_LINE_LENGTH = 1000
    WARN_LINE_LENGTH = 500

    def __init__(
        self,
        max_line_length: int = MAX_LINE_LENGTH,
        warn_line_length: int = WARN_LINE_LENGTH,
        check_trailing_whitespace: bool = True,
        check_mixed_line_endings: bool = True,
    ) -> None:
        """
        Initialize the content validator.

        Args:
            max_line_length: Maximum allowed line length (issues if exceeded)
            warn_line_length: Line length that triggers a warning
            check_trailing_whitespace: Whether to check for trailing whitespace
            check_mixed_line_endings: Whether to check for mixed line endings
        """
        self.max_line_length = max_line_length
        self.warn_line_length = warn_line_length
        self.check_trailing_whitespace = check_trailing_whitespace
        self.check_mixed_line_endings = check_mixed_line_endings

    def validate(self, content: str) -> ContentValidationResult:
        """
        Validate file content.

        Args:
            content: The content to validate

        Returns:
            ContentValidationResult with validation outcome
        """
        result = ContentValidationResult()

        # Check for empty content
        if not content.strip():
            result.warnings.append("Content is empty")
            result.metadata["is_empty"] = True
            return result

        # Check encoding
        self._check_encoding(content, result)
        if not result.valid:
            return result

        lines = content.split("\n")
        result.metadata["line_count"] = len(lines)

        # Check line lengths
        self._check_line_lengths(lines, result)

        # Check line endings
        if self.check_mixed_line_endings:
            self._check_line_endings(content, result)

        # Check trailing whitespace
        if self.check_trailing_whitespace:
            self._check_trailing_whitespace(lines, result)

        return result

    def _check_encoding(self, content: str, result: ContentValidationResult) -> None:
        """Check for encoding issues."""
        try:
            content.encode("utf-8")
        except UnicodeEncodeError:
            result.issues.append("Content contains invalid UTF-8 characters")
            result.valid = False

    def _check_line_lengths(
        self,
        lines: list[str],
        result: ContentValidationResult,
    ) -> None:
        """Check for long lines."""
        long_lines = []
        very_long_lines = []

        for i, line in enumerate(lines, 1):
            line_len = len(line)
            if line_len > self.max_line_length:
                very_long_lines.append(i)
            elif line_len > self.warn_line_length:
                long_lines.append(i)

        if very_long_lines:
            result.warnings.append(
                f"Lines exceeding {self.max_line_length} chars: {very_long_lines[:5]}"
                + (f" (+{len(very_long_lines) - 5} more)" if len(very_long_lines) > 5 else "")
            )

        if long_lines:
            result.metadata["long_lines"] = long_lines[:10]

    def _check_line_endings(self, content: str, result: ContentValidationResult) -> None:
        """Check for mixed line endings."""
        has_crlf = "\r\n" in content
        # Check for standalone CR or LF after removing CRLF
        content_without_crlf = content.replace("\r\n", "")
        has_lf = "\n" in content_without_crlf
        has_cr = "\r" in content_without_crlf

        line_ending_types = sum([has_crlf, has_lf, has_cr])
        if line_ending_types > 1:
            result.warnings.append("Mixed line endings detected (CRLF/LF/CR)")
            result.metadata["mixed_line_endings"] = True

        # Record the detected line ending type
        if has_crlf and not has_lf and not has_cr:
            result.metadata["line_ending"] = "CRLF"
        elif has_lf and not has_crlf and not has_cr:
            result.metadata["line_ending"] = "LF"
        elif has_cr and not has_crlf and not has_lf:
            result.metadata["line_ending"] = "CR"
        else:
            result.metadata["line_ending"] = "mixed"

    def _check_trailing_whitespace(
        self,
        lines: list[str],
        result: ContentValidationResult,
    ) -> None:
        """Check for trailing whitespace."""
        lines_with_trailing = []

        for i, line in enumerate(lines, 1):
            if line and line != line.rstrip():
                lines_with_trailing.append(i)

        if lines_with_trailing:
            count = len(lines_with_trailing)
            result.metadata["trailing_whitespace_lines"] = count
            if count > 10:
                result.warnings.append(f"{count} lines have trailing whitespace")

    def validate_for_write(self, content: str, strict: bool = False) -> tuple[bool, str]:
        """
        Validate content before writing.

        Args:
            content: Content to validate
            strict: If True, warnings become blocking issues

        Returns:
            Tuple of (is_valid, message)
        """
        result = self.validate(content)

        if not result.valid:
            return False, "; ".join(result.issues)

        if strict and result.warnings:
            return False, "; ".join(result.warnings)

        return True, "Content is valid"
