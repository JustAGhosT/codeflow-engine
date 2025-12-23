"""
Event Models

This module contains data models for events and webhook payloads used in the CodeFlow system.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any


class EventType(StrEnum):
    """Types of events that can be processed."""

    PULL_REQUEST = "pull_request"
    PULL_REQUEST_REVIEW = "pull_request_review"
    PULL_REQUEST_REVIEW_COMMENT = "pull_request_review_comment"
    ISSUE = "issue"
    ISSUE_COMMENT = "issue_comment"
    PUSH = "push"
    COMMIT_COMMENT = "commit_comment"
    CHECK_RUN = "check_run"
    CHECK_SUITE = "check_suite"
    DEPLOYMENT = "deployment"
    RELEASE = "release"
    WORKFLOW_RUN = "workflow_run"
    CUSTOM = "custom"


class EventAction(StrEnum):
    """Common event actions."""

    OPENED = "opened"
    CLOSED = "closed"
    EDITED = "edited"
    DELETED = "deleted"
    CREATED = "created"
    UPDATED = "updated"
    MERGED = "merged"
    SYNCHRONIZE = "synchronize"
    REOPENED = "reopened"
    LABELED = "labeled"
    UNLABELED = "unlabeled"
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    REVIEW_REQUESTED = "review_requested"
    REVIEW_REQUEST_REMOVED = "review_request_removed"
    SUBMITTED = "submitted"
    DISMISSED = "dismissed"


@dataclass
class User:
    """User model for event actors."""

    id: int
    login: str
    type: str = "User"
    avatar_url: str | None = None
    html_url: str | None = None


@dataclass
class Repository:
    """Repository model for events."""

    id: int
    name: str
    full_name: str
    owner: User
    private: bool = False
    html_url: str | None = None
    default_branch: str = "main"


@dataclass
class PullRequest:
    """Pull request model for PR events."""

    id: int
    number: int
    title: str
    body: str | None
    state: str
    user: User
    base: dict[str, Any]
    head: dict[str, Any]
    html_url: str | None = None
    merged: bool = False
    mergeable: bool | None = None
    draft: bool = False
    labels: list[dict[str, Any]] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class Issue:
    """Issue model for issue events."""

    id: int
    number: int
    title: str
    body: str | None
    state: str
    user: User
    html_url: str | None = None
    labels: list[dict[str, Any]] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class Comment:
    """Comment model for comment events."""

    id: int
    body: str
    user: User
    html_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class WebhookEvent:
    """Base webhook event model."""

    event_type: EventType
    action: EventAction | str | None
    repository: Repository
    sender: User
    installation_id: int | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # Optional specific event data
    pull_request: PullRequest | None = None
    issue: Issue | None = None
    comment: Comment | None = None


@dataclass
class EventResult:
    """Result of processing an event."""

    success: bool
    event_type: EventType
    action: str | None = None
    message: str | None = None
    data: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    processing_time_ms: float | None = None


__all__ = [
    "Comment",
    "EventAction",
    "EventResult",
    "EventType",
    "Issue",
    "PullRequest",
    "Repository",
    "User",
    "WebhookEvent",
]
