"""Test the ChangeLog class."""

# mypy: disable-error-code="no-untyped-def"
import datetime
from unittest.mock import MagicMock

import pytest
import typer
from github import GithubException

from github_changelog_md.changelog.changelog import ChangeLog, git_error
from github_changelog_md.constants import ExitErrors


@pytest.fixture
def mock_repo_data(mocker) -> MagicMock:
    """Mock out the repo data object."""
    mock_repo_data = MagicMock()
    mock_repo_data.html_url = "https://github.com/user/repo"
    mock_repo_data.get_commits.return_value.reversed = [
        MagicMock(
            commit=MagicMock(
                committer=mocker.MagicMock(
                    date=datetime.datetime(
                        2021,
                        1,
                        1,
                        tzinfo=datetime.timezone.utc,
                    ),
                ),
            ),
        ),
    ]
    return mock_repo_data


@pytest.fixture
def mock_repo() -> MagicMock:
    """Mock out the repo object."""
    mock_repo = MagicMock()
    mock_repo.get_commits.return_value.reversed = [
        MagicMock(
            commit=MagicMock(
                committer=MagicMock(
                    date=datetime.datetime(
                        2021,
                        1,
                        1,
                        tzinfo=datetime.timezone.utc,
                    ),
                ),
            ),
        ),
    ]
    mock_repo.get_releases.return_value = [
        MagicMock(
            id=1,
            tag_name="v1.0.0",
            html_url="https://github.com/user/repo/releases/tag/v1.0.0",
            created_at=datetime.datetime(
                2021,
                1,
                1,
                tzinfo=datetime.timezone.utc,
            ),
            title="Release 1.0.0",
            body="Release notes",
        ),
        MagicMock(
            id=2,
            tag_name="v0.1.0",
            html_url="https://github.com/user/repo/releases/tag/v0.1.0",
            created_at=datetime.datetime(
                2020,
                1,
                1,
                tzinfo=datetime.timezone.utc,
            ),
            title="Release 0.1.0",
            body="Release notes",
        ),
    ]
    mock_repo.get_pulls.return_value = [
        MagicMock(
            number=1,
            html_url="https://github.com/user/repo/pull/1",
            title="PR 1",
            user=MagicMock(
                login="user1",
                html_url="https://github.com/user1",
            ),
            labels=[MagicMock(name="bug")],
            merged_at=datetime.datetime(
                2021,
                1,
                1,
                tzinfo=datetime.timezone.utc,
            ),
        ),
        MagicMock(
            number=2,
            html_url="https://github.com/user/repo/pull/2",
            title="PR 2",
            user=MagicMock(
                login="user2",
                html_url="https://github.com/user2",
            ),
            labels=[MagicMock(name="enhancement")],
            merged_at=datetime.datetime(
                2021,
                1,
                1,
                tzinfo=datetime.timezone.utc,
            ),
        ),
    ]
    mock_repo.get_issues.return_value = [
        MagicMock(
            number=1,
            html_url="https://github.com/user/repo/issues/1",
            title="Issue 1",
            user=MagicMock(
                login="user1",
                html_url="https://github.com/user1",
            ),
            labels=[MagicMock(name="bug")],
            closed_at=datetime.datetime(
                2021,
                1,
                1,
                tzinfo=datetime.timezone.utc,
            ),
        ),
        MagicMock(
            number=2,
            html_url="https://github.com/user/repo/issues/2",
            title="Issue 2",
            user=MagicMock(
                login="user2",
                html_url="https://github.com/user2",
            ),
            labels=[MagicMock(name="enhancement")],
            closed_at=datetime.datetime(
                2021,
                1,
                1,
                tzinfo=datetime.timezone.utc,
            ),
        ),
    ]
    return mock_repo


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

    def test_no_pat_given(self, mocker, capsys) -> None:
        """Test the no_pat_given method."""
        mocker.patch(
            "github_changelog_md.changelog.changelog.get_settings",
            return_value="",
        )
        with pytest.raises(typer.Exit) as exc:
            ChangeLog("repo", {"user_name": None})

        output = capsys.readouterr()
        assert exc.value.args[0] == ExitErrors.NO_PAT
        assert "No GitHub PAT found in settings file" in output.err

    def test_run(
        self,
        mock_repo_data,
        mock_repo,
        mocker,
        config_file,  # noqa: ARG002
    ) -> None:
        """Test the overall run method."""
        mock_header = mocker.patch(
            "github_changelog_md.changelog.changelog.header",
            autospec=True,
        )
        mock_auth = MagicMock()
        mocker.patch(
            "github_changelog_md.changelog.changelog.Github",
            autospec=True,
            return_value=MagicMock(auth=mock_auth),
        )

        mock_path = mocker.patch(
            "github_changelog_md.changelog.changelog.Path",
            autospec=True,
        )
        mock_path.return_value.open.return_value.__enter__.return_value = (
            MagicMock()
        )
        changelog = ChangeLog(
            "repo",
            {
                "user_name": "user",
                "next_release": None,
                "show_unreleased": True,
                "contributors": False,
                "quiet": None,
            },
        )
        changelog.get_repo_data = MagicMock(return_value=mock_repo_data)
        changelog.get_closed_prs = MagicMock(
            return_value=mock_repo.get_pulls.return_value,
        )
        changelog.get_closed_issues = MagicMock(
            return_value=mock_repo.get_issues.return_value,
        )
        changelog.get_repo_releases = MagicMock(
            return_value=mock_repo.get_releases.return_value,
        )
        changelog.filter_issues = MagicMock(
            return_value=mock_repo.get_issues.return_value,
        )
        changelog.link_pull_requests = MagicMock(return_value={})
        changelog.link_issues = MagicMock(return_value={})
        changelog.generate_changelog = MagicMock()
        changelog.run()

        mock_header.assert_called_once()
        changelog.get_repo_data.assert_called_once()
        changelog.get_closed_prs.assert_called_once()
        changelog.get_closed_issues.assert_called_once()
        changelog.get_repo_releases.assert_called_once()
        changelog.filter_issues.assert_called_once()
        changelog.link_pull_requests.assert_called_once()
        changelog.link_issues.assert_called_once()
        changelog.generate_changelog.assert_called_once()
