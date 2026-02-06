"""Test the ChangeLog class."""

# mypy: disable-error-code="no-untyped-def"
import datetime
from unittest.mock import MagicMock

import pytest
import typer
from github import GithubException

from github_changelog_md.changelog.changelog import ChangeLog, git_error
from github_changelog_md.constants import ChangelogOptions, ExitErrors


def _default_options() -> ChangelogOptions:
    return {
        "user_name": "user",
        "next_release": None,
        "show_unreleased": True,
        "show_depends": True,
        "output_file": "CHANGELOG.md",
        "contributors": False,
        "quiet": False,
        "skip_releases": None,
        "show_issues": True,
        "item_order": "newest-first",
        "ignore_items": None,
        "max_depends": 10,
        "show_diff": True,
        "show_patch": True,
    }


def _build_changelog(mocker, settings_overrides=None) -> ChangeLog:
    settings = MagicMock()
    settings.github_pat = "1234"
    settings.yanked = None
    settings.release_text_before = None
    settings.release_text = None
    settings.release_overrides = None
    settings.date_format = "%Y-%m-%d"
    settings.ignored_users = []
    settings.intro_text = ""
    settings.extend_sections = None
    settings.extend_sections_index = None
    settings.rename_sections = None
    settings.ignored_labels = None
    settings.extend_ignored = None
    settings.allowed_labels = None
    if settings_overrides:
        for key, value in settings_overrides.items():
            setattr(settings, key, value)

    mocker.patch(
        "github_changelog_md.changelog.changelog.get_settings",
        return_value=settings,
    )
    mocker.patch(
        "github_changelog_md.changelog.changelog.Github",
        return_value=MagicMock(),
    )

    return ChangeLog("repo", _default_options())


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
            ChangeLog(
                "repo",
                {
                    "user_name": None,
                    "next_release": None,
                    "show_unreleased": True,
                    "show_depends": True,
                    "output_file": "CHANGELOG.md",
                    "contributors": False,
                    "quiet": False,
                    "skip_releases": None,
                    "show_issues": True,
                    "item_order": "newest-first",
                    "ignore_items": None,
                    "max_depends": 10,
                    "show_diff": True,
                    "show_patch": True,
                },
            )

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
                "show_depends": True,
                "output_file": "CHANGELOG.md",
                "contributors": False,
                "quiet": False,
                "skip_releases": None,
                "show_issues": True,
                "item_order": "newest-first",
                "ignore_items": None,
                "max_depends": 10,
                "show_diff": True,
                "show_patch": True,
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

    def test_build_release_cache_maps_are_created(self, mocker) -> None:
        """Test release lookup caches are built at initialization."""
        changelog = _build_changelog(
            mocker,
            {
                "yanked": [{"release": " v1.0.0 ", "reason": "bad build"}],
                "release_text_before": [
                    {"release": " v1.0.0 ", "text": " before text "}
                ],
                "release_text": [
                    {"release": " v1.0.0 ", "text": " release text "}
                ],
                "release_overrides": [
                    {"release": " v1.0.0 ", "text": "override text"}
                ],
            },
        )

        assert (
            changelog.release_text_cache.yanked_by_release["v1.0.0"]
            == "bad build"
        )
        assert (
            changelog.release_text_cache.release_text_before_by_release[
                "v1.0.0"
            ]
            == "before text"
        )
        assert (
            changelog.release_text_cache.release_text_by_release["v1.0.0"]
            == "release text"
        )
        assert (
            changelog.release_text_cache.release_overrides_by_release["v1.0.0"]
            == "override text"
        )

    def test_check_yanked_uses_cache(self, mocker) -> None:
        """Test check_yanked reads from release_text_cache."""
        changelog = _build_changelog(mocker)
        changelog.release_text_cache.yanked_by_release = {"v1.0.0": "bad build"}
        out = MagicMock()
        release = MagicMock(tag_name="v1.0.0")

        changelog.check_yanked(out, release)

        assert any(
            "`YANKED`" in call.args[0] for call in out.write.call_args_list
        )
        assert any(
            "bad build" in call.args[0] for call in out.write.call_args_list
        )

    def test_show_before_text_uses_cache(self, mocker) -> None:
        """Test show_before_text reads from release_text_cache."""
        changelog = _build_changelog(mocker)
        changelog.release_text_cache.release_text_before_by_release = {
            "v1.0.0": "Before text"
        }
        out = MagicMock()
        release = MagicMock(tag_name="v1.0.0")

        changelog.show_before_text(out, release)

        written = "".join(call.args[0] for call in out.write.call_args_list)
        assert written == "---\n\nBefore text\n\n---\n\n"

    def test_show_release_text_uses_cache(self, mocker) -> None:
        """Test show_release_text reads from release_text_cache."""
        changelog = _build_changelog(mocker)
        changelog.release_text_cache.release_text_by_release = {
            "v1.0.0": "Release text"
        }
        out = MagicMock()

        changelog.show_release_text(out, "v1.0.0")

        written = "".join(call.args[0] for call in out.write.call_args_list)
        assert written == "Release text\n\n"

    def test_process_release_uses_override_cache(self, mocker) -> None:
        """Test process_release returns early when override text exists."""
        changelog = _build_changelog(
            mocker,
            {"date_format": "%Y-%m-%d"},
        )
        changelog.prev_release = None
        changelog.release_text_cache.release_overrides_by_release = {
            "v1.0.0": "Override body"
        }
        changelog.pr_by_release = {}
        changelog.issue_by_release = {}
        changelog.rprint_issues = MagicMock()
        changelog.rprint_prs = MagicMock()

        release = MagicMock()
        release.tag_name = "v1.0.0"
        release.html_url = "https://github.com/user/repo/releases/tag/v1.0.0"
        release.created_at = datetime.datetime(
            2021,
            1,
            1,
            tzinfo=datetime.timezone.utc,
        )
        release.title = "v1.0.0"

        out = MagicMock()
        changelog.process_release(out, release)

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "Override body\n" in rendered
        changelog.rprint_issues.assert_not_called()
        changelog.rprint_prs.assert_not_called()
