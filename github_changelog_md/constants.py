"""Define constants used throughout the application."""
from enum import IntEnum
from typing import Union

SectionHeadings = tuple[str, Union[str, None]]


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
