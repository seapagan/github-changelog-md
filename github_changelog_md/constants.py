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


SECTIONS: list[SectionHeadings] = [
    ("Merged Pull Requests", None),
    ("Enhancements", "enhancement"),
    ("Bug Fixes", "bug"),
    ("Refactoring", "refactor"),
    ("Documentation", "documentation"),
    ("Dependency Updates", "dependencies"),
]

CONFIG_FILE = ".changelog_generator.toml"
