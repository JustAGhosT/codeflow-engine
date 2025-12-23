"""
Centralized Security Patterns.

This module consolidates all security threat detection patterns in one place
to eliminate duplication across validators (DRY principle).
"""

import re
from dataclasses import dataclass, field
from typing import Pattern


@dataclass
class SecurityPatterns:
    """
    Centralized repository of security threat patterns.

    All validators should use these patterns instead of defining their own.
    This ensures consistency and makes updates easier.

    Attributes:
        sql_injection: Patterns to detect SQL injection attempts
        xss: Patterns to detect Cross-Site Scripting attempts
        command_injection: Patterns to detect command injection attempts
        path_traversal: Patterns to detect path traversal attempts
    """

    # SQL Injection patterns
    sql_injection: list[str] = field(default_factory=lambda: [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|UNION|SCRIPT)\b)",
        r"(\b(OR|AND)\b\s+\d+\s*=\s*\d+)",
        r"(\b(OR|AND)\b\s+['\"]\w+['\"]\s*=\s*['\"]\w+['\"])",
        r"(--|\b(COMMENT|REM)\b)",
        r"(\b(WAITFOR|DELAY)\b)",
        r"(\b(BENCHMARK|SLEEP)\b)",
        r"(\bUNION\s+SELECT\b)",
    ])

    # XSS patterns
    xss: list[str] = field(default_factory=lambda: [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe[^>]*>",
        r"<object[^>]*>",
        r"<embed[^>]*>",
        r"<form[^>]*>",
        r"<input[^>]*>",
        r"<textarea[^>]*>",
        r"<select[^>]*>",
    ])

    # Command injection patterns
    command_injection: list[str] = field(default_factory=lambda: [
        r"[;&|`$(){}[\]]",
        r"\b(cat|ls|pwd|whoami|id|uname|ps|top|kill|rm|cp|mv|chmod|chown)\b",
        r"\b(netcat|nc|telnet|ssh|scp|wget|curl|ftp|sftp)\b",
        r"\b(bash|sh|zsh|fish|powershell|cmd|command)\b",
        r"(>|>>|<|\|)",
    ])

    # Path traversal patterns
    path_traversal: list[str] = field(default_factory=lambda: [
        r"\.\./",
        r"\.\.\\",
        r"%2e%2e/",
        r"%2e%2e\\",
    ])

    _compiled_patterns: dict[str, list[Pattern[str]]] = field(
        default_factory=dict, init=False, repr=False
    )

    def __post_init__(self) -> None:
        """Compile patterns for better performance."""
        self._compile_patterns()

    def _compile_patterns(self) -> None:
        """Pre-compile regex patterns for performance."""
        self._compiled_patterns = {
            "sql_injection": [re.compile(p, re.IGNORECASE) for p in self.sql_injection],
            "xss": [re.compile(p, re.IGNORECASE) for p in self.xss],
            "command_injection": [re.compile(p) for p in self.command_injection],
            "path_traversal": [re.compile(p, re.IGNORECASE) for p in self.path_traversal],
        }

    def check_sql_injection(self, value: str) -> bool:
        """Check if value contains SQL injection patterns."""
        return self._check_patterns("sql_injection", value)

    def check_xss(self, value: str) -> bool:
        """Check if value contains XSS patterns."""
        return self._check_patterns("xss", value)

    def check_command_injection(self, value: str) -> bool:
        """Check if value contains command injection patterns."""
        return self._check_patterns("command_injection", value)

    def check_path_traversal(self, value: str) -> bool:
        """Check if value contains path traversal patterns."""
        return self._check_patterns("path_traversal", value)

    def _check_patterns(self, pattern_type: str, value: str) -> bool:
        """Check if value matches any pattern of the given type."""
        patterns = self._compiled_patterns.get(pattern_type, [])
        return any(pattern.search(value) for pattern in patterns)

    def check_all_threats(self, value: str) -> tuple[bool, str | None]:
        """
        Check for all security threats.

        Args:
            value: The string to check

        Returns:
            Tuple of (has_threat, threat_type) where threat_type is None if no threat
        """
        if self.check_sql_injection(value):
            return True, "SQL injection"
        if self.check_xss(value):
            return True, "XSS"
        if self.check_command_injection(value):
            return True, "command injection"
        if self.check_path_traversal(value):
            return True, "path traversal"
        return False, None


# Global default instance for common use
DEFAULT_SECURITY_PATTERNS = SecurityPatterns()
