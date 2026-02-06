"""Define constants used throughout the application."""

from __future__ import annotations

from enum import IntEnum
from typing import Optional, TypedDict

SectionHeadings = tuple[str, Optional[str]]


class ChangelogOptions(TypedDict):
    """Type definition for the options passed to ChangeLog."""

    user_name: str | None
    next_release: str | None
    show_unreleased: bool
    show_depends: bool
    output_file: str
    contributors: bool
    quiet: bool
    skip_releases: list[str] | None
    show_issues: bool
    item_order: str
    ignore_items: list[int] | None
    max_depends: int
    show_diff: bool
    show_patch: bool


class ExitErrors(IntEnum):
    """Exit errors.

    Error codes for the application.
    """

    GIT_ERROR = 1
    PERMISSION_DENIED = 2
    USER_ABORT = 3
    OS_ERROR = 4
    INVALID_ACTION = 5
    NO_PAT = 6
    BAD_SCHEMA = 7


# label names should be lowercase
SECTIONS: list[SectionHeadings] = [
    ("Breaking Changes", "breaking"),
    ("Merged Pull Requests", None),
    ("Enhancements", "enhancement"),
    ("Bug Fixes", "bug"),
    ("Refactoring", "refactor"),
    ("Documentation", "documentation"),
    ("Dependency Updates", "dependencies"),
]

# label names should be lowercase
IGNORED_LABELS: list[str] = [
    "duplicate",
    "invalid",
    "question",
    "wontfix",
]

IGNORED_CONTRIBUTORS: list[str] = [
    "dependabot[bot]",
    "pre-commit-ci[bot]",
    "dependabot-preview[bot]",
]

CONFIG_FILE: str = ".changelog_generator.toml"
OUTPUT_FILE: str = "CHANGELOG.md"
CONTRIBUTORS_FILE: str = "CONTRIBUTORS.md"
