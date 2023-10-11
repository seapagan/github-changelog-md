"""Define constants used throughout the application."""
from enum import IntEnum


class ExitErrors(IntEnum):
    """Exit errors.

    Error codes for the application.
    """

    GIT_ERROR = 1
    PERMISSION_DENIED = 2
    USER_ABORT = 3
    OS_ERROR = 4
    INVALID_ACTION = 5
