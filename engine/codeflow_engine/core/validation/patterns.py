"""Centralized Security Patterns."""

import re
from dataclasses import dataclass, field
from typing import Pattern


@dataclass
class SecurityPatterns:
    sql_injection: list[str] = field(
        default_factory=lambda: [
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|UNION|SCRIPT)\b)",
            r"(\b(OR|AND)\b\s+\d+\s*=\s*\d+)",
            r"(\b(OR|AND)\b\s+['\"]\w+['\"]\s*=\s*['\"]\w+['\"])",
            r"(--|\b(COMMENT|REM)\b)",
            r"(\b(WAITFOR|DELAY)\b)",
            r"(\b(BENCHMARK|SLEEP)\b)",
            r"(\bUNION\s+SELECT\b)",
        ]
    )
    xss: list[str] = field(
        default_factory=lambda: [
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
        ]
    )
    command_injection: list[str] = field(
        default_factory=lambda: [
            r"[;&|`$(){}[\]]",
            r"\b(cat|ls|pwd|whoami|id|uname|ps|top|kill|rm|cp|mv|chmod|chown)\b",
            r"\b(netcat|nc|telnet|ssh|scp|wget|curl|ftp|sftp)\b",
            r"\b(bash|sh|zsh|fish|powershell|cmd|command)\b",
            r"(>|>>|<|\|)",
        ]
    )
    path_traversal: list[str] = field(
        default_factory=lambda: [
            r"\.\./",
            r"\.\.\\",
            r"%2e%2e/",
            r"%2e%2e\\",
        ]
    )
    _compiled_patterns: dict[str, list[Pattern[str]]] = field(
        default_factory=dict, init=False, repr=False
    )

    def __post_init__(self) -> None:
        self._compiled_patterns = {
            "sql_injection": [re.compile(p, re.IGNORECASE) for p in self.sql_injection],
            "xss": [re.compile(p, re.IGNORECASE) for p in self.xss],
            "command_injection": [re.compile(p) for p in self.command_injection],
            "path_traversal": [
                re.compile(p, re.IGNORECASE) for p in self.path_traversal
            ],
        }

    def _check_patterns(self, pattern_type: str, value: str) -> bool:
        patterns = self._compiled_patterns.get(pattern_type, [])
        return any(pattern.search(value) for pattern in patterns)

    def check_sql_injection(self, value: str) -> bool:
        return self._check_patterns("sql_injection", value)

    def check_xss(self, value: str) -> bool:
        return self._check_patterns("xss", value)

    def check_command_injection(self, value: str) -> bool:
        return self._check_patterns("command_injection", value)

    def check_path_traversal(self, value: str) -> bool:
        return self._check_patterns("path_traversal", value)

    def check_all_threats(self, value: str) -> tuple[bool, str | None]:
        if self.check_sql_injection(value):
            return True, "SQL injection"
        if self.check_xss(value):
            return True, "XSS"
        if self.check_command_injection(value):
            return True, "command injection"
        if self.check_path_traversal(value):
            return True, "path traversal"
        return False, None


DEFAULT_SECURITY_PATTERNS = SecurityPatterns()
