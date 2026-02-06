"""Test the ChangeLog class."""

# mypy: disable-error-code="no-untyped-def"
import datetime
from pathlib import Path
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

    def test_update_contributors_preserves_name_casing(self, mocker) -> None:
        """Test update_contributors does not alter contributor name casing."""
        changelog = _build_changelog(mocker)
        changelog.repo_data = MagicMock(name="repo_data")
        changelog.repo_data.name = "repo"
        contributor = MagicMock(name="contributor")
        contributor.login = "mcd"
        contributor.name = "McDonald"
        contributor.html_url = "https://github.com/mcd"
        changelog.contributors = [contributor]

        mock_path = mocker.patch(
            "github_changelog_md.changelog.changelog.Path",
        )
        mock_path.cwd.return_value = Path("test_cwd")
        file_handle = MagicMock()
        mock_path.return_value.open.return_value.__enter__.return_value = (
            file_handle
        )

        changelog.update_contributors()

        rendered = "".join(
            call.args[0] for call in file_handle.write.call_args_list
        )
        assert "- McDonald ([@mcd](https://github.com/mcd))" in rendered

    def test_process_unreleased_writes_unreleased_heading(self, mocker) -> None:
        """Test process_unreleased writes heading and links to HEAD."""
        changelog = _build_changelog(mocker)
        changelog.repo_data = MagicMock(html_url="https://github.com/user/repo")
        changelog.unreleased = [MagicMock()]
        changelog.unreleased_issues = []
        changelog.show_release_text = MagicMock()
        changelog.rprint_issues = MagicMock()
        changelog.rprint_prs = MagicMock()

        out = MagicMock()
        changelog.process_unreleased(out)

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "## [Unreleased]" in rendered
        assert "/tree/HEAD" in rendered
        assert changelog.prev_release == "HEAD"
        changelog.show_release_text.assert_called_once_with(
            out,
            "unreleased",
        )

    def test_process_unreleased_with_next_release_uses_tag_link(
        self,
        mocker,
    ) -> None:
        """Test process_unreleased link and heading for next_release option."""
        changelog = _build_changelog(mocker)
        changelog.options["next_release"] = "v2.0.0"
        changelog.repo_data = MagicMock(html_url="https://github.com/user/repo")
        changelog.unreleased = []
        changelog.unreleased_issues = [MagicMock()]
        changelog.show_release_text = MagicMock()
        changelog.rprint_issues = MagicMock()
        changelog.rprint_prs = MagicMock()

        out = MagicMock()
        changelog.process_unreleased(out)

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "## [v2.0.0]" in rendered
        assert "/releases/tag/v2.0.0" in rendered
        changelog.show_release_text.assert_called_once_with(
            out,
            "v2.0.0",
        )

    def test_generate_diff_url_with_diff_and_patch(self, mocker) -> None:
        """Test generate_diff_url renders changelog, diff, and patch links."""
        changelog = _build_changelog(mocker)
        changelog.repo_data = MagicMock(html_url="https://github.com/user/repo")
        release = MagicMock(tag_name="v1.0.0")
        out = MagicMock()

        changelog.generate_diff_url(out, "HEAD", release)

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "compare/v1.0.0...HEAD" in rendered
        assert "[`Diff`]" in rendered
        assert "[`Patch`]" in rendered

    def test_generate_diff_url_uses_next_release_option(self, mocker) -> None:
        """Test generate_diff_url prefers next_release override."""
        changelog = _build_changelog(mocker)
        changelog.options["next_release"] = "v2.0.0"
        changelog.repo_data = MagicMock(html_url="https://github.com/user/repo")
        release = MagicMock(tag_name="v1.0.0")
        out = MagicMock()

        changelog.generate_diff_url(out, "ignored", release)

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "compare/v1.0.0...v2.0.0" in rendered

    def test_rprint_prs_dependency_section_is_truncated(self, mocker) -> None:
        """Test dependency PRs are truncated with a summary line."""
        changelog = _build_changelog(mocker)
        changelog.options["max_depends"] = 1
        changelog.sections = [
            ("Merged Pull Requests", None),
            ("Dependency Updates", "dependencies"),
        ]
        changelog.ignored_labels = []

        dep_label_1 = MagicMock()
        dep_label_1.name = "dependencies"
        dep_label_2 = MagicMock()
        dep_label_2.name = "dependencies"

        pr_old = MagicMock()
        pr_old.number = 1
        pr_old.title = "bump dep old"
        pr_old.html_url = "https://github.com/user/repo/pull/1"
        pr_old.user = MagicMock(
            login="bot1", html_url="https://github.com/bot1"
        )
        pr_old.labels = [dep_label_1]

        pr_new = MagicMock()
        pr_new.number = 2
        pr_new.title = "bump dep new"
        pr_new.html_url = "https://github.com/user/repo/pull/2"
        pr_new.user = MagicMock(
            login="bot2", html_url="https://github.com/bot2"
        )
        pr_new.labels = [dep_label_2]

        changelog.get_release_sections = MagicMock(
            return_value={"Dependency Updates": [pr_old, pr_new]}
        )

        out = MagicMock()
        changelog.rprint_prs(out, [pr_old, pr_new])

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "Dependency Updates" in rendered
        assert "#2" in rendered
        assert "#1" not in rendered
        assert "and 1 more dependency updates" in rendered

    def test_process_release_falls_back_to_release_body(self, mocker) -> None:
        """Test process_release calls get_release_body when lists are empty."""
        changelog = _build_changelog(mocker)
        changelog.prev_release = None
        changelog.pr_by_release = {}
        changelog.issue_by_release = {}
        changelog.get_release_body = MagicMock()

        release = MagicMock()
        release.id = 1
        release.tag_name = "v1.0.0"
        release.title = "v1.0.0"
        release.html_url = "https://github.com/user/repo/releases/tag/v1.0.0"
        release.created_at = datetime.datetime(
            2021,
            1,
            1,
            tzinfo=datetime.timezone.utc,
        )

        out = MagicMock()
        changelog.process_release(out, release)

        changelog.get_release_body.assert_called_once_with(out, release)

    def test_get_release_body_strips_compare_link_and_adds_newline(
        self,
        mocker,
    ) -> None:
        """Test get_release_body removes compare line and appends newline."""
        changelog = _build_changelog(mocker)
        changelog.repo_data = MagicMock(html_url="https://github.com/user/repo")
        release = MagicMock()
        release.body = (
            "Highlights\n"
            "https://github.com/user/repo/compare/v0.9.0...v1.0.0\n"
            "More notes"
        )
        out = MagicMock()

        changelog.get_release_body(out, release)

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "compare/v0.9.0...v1.0.0" not in rendered
        assert "Highlights" in rendered
        assert "More notes\n" in rendered

    def test_get_release_body_without_notes_writes_fallback(
        self,
        mocker,
    ) -> None:
        """Test get_release_body writes fallback text when body is empty."""
        changelog = _build_changelog(mocker)
        release = MagicMock()
        release.body = ""
        out = MagicMock()

        changelog.get_release_body(out, release)

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "There were no merged pull requests or closed issues" in rendered
        assert "See the Full Changelog below for details." in rendered

    def test_rprint_issues_handles_missing_closed_by(self, mocker) -> None:
        """Test rprint_issues fallback when closed_by is unavailable."""
        changelog = _build_changelog(mocker)
        changelog.options["show_issues"] = True
        changelog.ignored_labels = []

        issue = MagicMock()
        issue.number = 42
        issue.title = "missing closer"
        issue.html_url = "https://github.com/user/repo/issues/42"
        issue.labels = []
        issue.closed_by = None

        out = MagicMock()
        changelog.rprint_issues(out, [issue])

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "**Closed Issues**" in rendered
        assert "[#42](https://github.com/user/repo/issues/42)" in rendered
        assert "by [" not in rendered

    def test_generate_changelog_writes_header_and_footer(self, mocker) -> None:
        """Test generate_changelog writes base structure and footer."""
        changelog = _build_changelog(mocker)
        changelog.repo_data = MagicMock(
            html_url="https://github.com/user/repo",
            name="repo",
        )
        changelog.repo_releases = []
        changelog.options["output_file"] = "CHANGELOG.md"
        changelog.options["show_unreleased"] = False
        changelog.options["show_depends"] = True
        changelog.settings.intro_text = "Intro line"
        changelog.process_unreleased = MagicMock()
        changelog.process_release = MagicMock()

        mock_path = mocker.patch(
            "github_changelog_md.changelog.changelog.Path",
        )
        mock_path.cwd.return_value = Path("test_cwd")
        file_handle = MagicMock()
        mock_path.return_value.open.return_value.__enter__.return_value = (
            file_handle
        )

        changelog.generate_changelog()

        rendered = "".join(
            call.args[0] for call in file_handle.write.call_args_list
        )
        assert rendered.startswith("# Changelog\n\n")
        assert "Intro line\n\n" in rendered
        assert "This changelog was generated using" in rendered
        changelog.process_unreleased.assert_not_called()
