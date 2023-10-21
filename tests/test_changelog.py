"""Test the ChangeLog class."""
# mypy: disable-error-code="no-untyped-def"

import pytest
import typer
from github import GithubException

from github_changelog_md.changelog.changelog import git_error
from github_changelog_md.constants import ExitErrors


class TestChangelog:
    """Class with all tests for the ChangeLog class."""

    def test_git_error(self) -> None:
        """Test the git_error method."""
        git_exception = GithubException(
            status=404,
            data={"message": "Not Found"},
        )

        with pytest.raises(typer.Exit) as exc:
            git_error(git_exception)

        assert exc.value.args[0] == ExitErrors.GIT_ERROR
