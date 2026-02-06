"""Test the ChangeLog class."""

import datetime
from pathlib import Path
from typing import Any, cast
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

    def test_flatten_ignores_with_extend_and_allowlist(self, mocker) -> None:
        """Test flatten_ignores combines defaults and removes allowed labels."""
        changelog = _build_changelog(mocker)
        changelog.settings.ignored_labels = None
        changelog.settings.extend_ignored = ["bot-only"]
        changelog.settings.allowed_labels = ["question"]

        result = changelog.flatten_ignores()

        assert "bot-only" in result
        assert "question" not in result

    def test_flatten_ignores_uses_explicit_list(self, mocker) -> None:
        """Test flatten_ignores returns explicit ignored_labels unchanged."""
        changelog = _build_changelog(mocker)
        changelog.settings.ignored_labels = ["foo", "bar"]

        assert changelog.flatten_ignores() == ["foo", "bar"]

    def test_rename_sections_success(self, mocker) -> None:
        """Test rename_sections updates matching headings."""
        changelog = _build_changelog(mocker)
        changelog.settings.rename_sections = [
            {"old": "Bug Fixes", "new": "Fixes"}
        ]
        sections = cast(
            "list[tuple[str, str | None]]",
            [("Bug Fixes", "bug"), ("Merged Pull Requests", None)],
        )

        renamed = changelog.rename_sections(sections)

        assert ("Fixes", "bug") in renamed

    def test_rename_sections_invalid_raises_exit(self, mocker) -> None:
        """Test rename_sections exits when old heading does not exist."""
        changelog = _build_changelog(mocker)
        changelog.settings.rename_sections = [{"old": "Nope", "new": "New"}]
        sections = cast(
            "list[tuple[str, str | None]]",
            [("Bug Fixes", "bug")],
        )

        with pytest.raises(typer.Exit) as exc:
            changelog.rename_sections(sections)

        assert exc.value.args[0] == ExitErrors.INVALID_ACTION

    def test_extend_sections_with_insert_index(self, mocker) -> None:
        """Test extend_sections inserts custom sections at configured index."""
        changelog = _build_changelog(mocker)
        changelog.settings.extend_sections = [
            {"title": "Security", "label": "security"}
        ]
        changelog.settings.extend_sections_index = 1

        sections = changelog.extend_sections()

        assert sections[1] == ("Security", "security")

    def test_get_contributors_deduplicates_and_sorts(self, mocker) -> None:
        """Test get_contributors removes duplicates and sorts by name/login."""
        changelog = _build_changelog(mocker)
        user_b = MagicMock(login="b-user")
        user_b.name = "B User"
        user_a = MagicMock(login="a-user")
        user_a.name = "A User"
        changelog.repo_prs = cast(
            "Any",
            [
                MagicMock(user=user_b),
                MagicMock(user=user_a),
                MagicMock(user=user_b),
            ],
        )

        contributors = changelog.get_contributors()

        assert [u.login for u in contributors] == ["a-user", "b-user"]

    def test_ignore_items_and_get_sorted_items(self, mocker) -> None:
        """Test ignore_items filtering and get_sorted_items ordering."""
        changelog = _build_changelog(mocker)
        changelog.options["ignore_items"] = [2]
        items = [
            MagicMock(number=1, title="One"),
            MagicMock(number=2, title="Two"),
            MagicMock(number=3, title="[no changelog] hidden"),
        ]

        filtered = changelog.ignore_items(cast("Any", items))
        assert [item.number for item in filtered] == [1]

        changelog.options["item_order"] = "oldest-first"
        sorted_items = changelog.get_sorted_items(
            [MagicMock(number=3), MagicMock(number=1)]
        )
        assert [item.number for item in sorted_items] == [1, 3]

    def test_get_release_sections_respects_ignored_labels(self, mocker) -> None:
        """Test get_release_sections excludes PRs with ignored labels."""
        changelog = _build_changelog(mocker)
        changelog.sections = [("Bug Fixes", "bug")]
        changelog.ignored_labels = ["wontfix"]

        bug = MagicMock()
        bug_label = MagicMock()
        bug_label.name = "bug"
        bug.labels = [bug_label]
        ignored = MagicMock()
        ignored_label_1 = MagicMock()
        ignored_label_1.name = "bug"
        ignored_label_2 = MagicMock()
        ignored_label_2.name = "wontfix"
        ignored.labels = [ignored_label_1, ignored_label_2]

        grouped = changelog.get_release_sections([bug, ignored])

        assert grouped["Bug Fixes"] == [bug]

    def test_link_pull_requests_and_issues_assign_and_track_unreleased(
        self,
        mocker,
    ) -> None:
        """Test linking assigns items by release date and tracks unreleased."""
        changelog = _build_changelog(mocker)
        cast("Any", changelog.settings).ignored_users = ["ignored-bot"]

        rel_old = MagicMock(
            id=1,
            created_at=datetime.datetime(
                2021, 1, 1, tzinfo=datetime.timezone.utc
            ),
        )
        rel_new = MagicMock(
            id=2,
            created_at=datetime.datetime(
                2021, 1, 10, tzinfo=datetime.timezone.utc
            ),
        )
        changelog.repo_releases = [rel_new, rel_old]
        changelog.get_latest_release_date = MagicMock(
            return_value=datetime.datetime(
                2021, 1, 10, tzinfo=datetime.timezone.utc
            )
        )

        pr_old = MagicMock(
            id=101,
            merged_at=datetime.datetime(
                2021, 1, 1, tzinfo=datetime.timezone.utc
            ),
            user=MagicMock(login="dev1"),
        )
        pr_new = MagicMock(
            id=102,
            merged_at=datetime.datetime(
                2021, 1, 5, tzinfo=datetime.timezone.utc
            ),
            user=MagicMock(login="dev2"),
        )
        pr_unreleased = MagicMock(
            id=103,
            merged_at=datetime.datetime(
                2021, 1, 11, tzinfo=datetime.timezone.utc
            ),
            user=MagicMock(login="dev3"),
        )
        pr_ignored = MagicMock(
            id=104,
            merged_at=datetime.datetime(
                2021, 1, 2, tzinfo=datetime.timezone.utc
            ),
            user=MagicMock(login="ignored-bot"),
        )
        changelog.repo_prs = cast(
            "Any", [pr_old, pr_new, pr_unreleased, pr_ignored]
        )

        issue_old = MagicMock(
            id=201,
            closed_at=datetime.datetime(
                2021, 1, 1, tzinfo=datetime.timezone.utc
            ),
            user=MagicMock(login="dev1"),
        )
        issue_new = MagicMock(
            id=202,
            closed_at=datetime.datetime(
                2021, 1, 7, tzinfo=datetime.timezone.utc
            ),
            user=MagicMock(login="dev2"),
        )
        issue_unreleased = MagicMock(
            id=203,
            closed_at=datetime.datetime(
                2021, 1, 12, tzinfo=datetime.timezone.utc
            ),
            user=MagicMock(login="dev3"),
        )
        issue_ignored = MagicMock(
            id=204,
            closed_at=datetime.datetime(
                2021, 1, 2, tzinfo=datetime.timezone.utc
            ),
            user=MagicMock(login="ignored-bot"),
        )
        changelog.filtered_repo_issues = [
            issue_old,
            issue_new,
            issue_unreleased,
            issue_ignored,
        ]

        pr_by_release = changelog.link_pull_requests()
        issue_by_release = changelog.link_issues()

        assert pr_old in pr_by_release[1]
        assert pr_new in pr_by_release[2]
        assert changelog.unreleased == [pr_unreleased]
        assert issue_old in issue_by_release[1]
        assert issue_new in issue_by_release[2]
        assert changelog.unreleased_issues == [issue_unreleased]

    def test_run_quiet_and_contributors_path(self, mocker) -> None:
        """Test run covers quiet stdout redirect and contributors update."""
        changelog = _build_changelog(mocker)
        changelog.options["quiet"] = True
        changelog.options["contributors"] = True

        mocker.patch("github_changelog_md.changelog.changelog.header")
        changelog.rename_sections = MagicMock(return_value=[("Merged", None)])
        changelog.extend_sections = MagicMock(return_value=[("Merged", None)])
        changelog.flatten_ignores = MagicMock(return_value=[])
        changelog.get_repo_data = MagicMock(return_value=MagicMock())
        changelog.get_repo_releases = MagicMock(return_value=[])
        changelog.get_closed_prs = MagicMock(return_value=[])
        changelog.get_closed_issues = MagicMock(return_value=[])
        changelog.filter_issues = MagicMock(return_value=[])
        changelog.link_pull_requests = MagicMock(return_value={})
        changelog.link_issues = MagicMock(return_value={})
        changelog.generate_changelog = MagicMock()
        changelog.get_contributors = MagicMock(return_value=[])
        changelog.update_contributors = MagicMock()

        mock_path = mocker.patch("github_changelog_md.changelog.changelog.Path")
        devnull_handle = MagicMock()
        devnull_ctx = MagicMock()
        devnull_ctx.__enter__.return_value = devnull_handle
        devnull_ctx.__exit__.return_value = None
        mock_path.return_value.open.return_value = devnull_ctx

        changelog.run()

        changelog.get_contributors.assert_called_once()
        changelog.update_contributors.assert_called_once()

    def test_update_contributors_ignores_known_bots(self, mocker) -> None:
        """Test update_contributors skips IGNORED_CONTRIBUTORS logins."""
        changelog = _build_changelog(mocker)
        changelog.repo_data = MagicMock(name="repo_data")
        changelog.repo_data.name = "repo"

        ignored = MagicMock()
        ignored.login = "dependabot[bot]"
        ignored.name = "Dependabot"
        ignored.html_url = "https://github.com/apps/dependabot"
        normal = MagicMock()
        normal.login = "dev-user"
        normal.name = "Dev User"
        normal.html_url = "https://github.com/dev-user"
        changelog.contributors = [ignored, normal]

        mock_path = mocker.patch("github_changelog_md.changelog.changelog.Path")
        mock_path.cwd.return_value = Path("test_cwd")
        file_handle = MagicMock()
        mock_path.return_value.open.return_value.__enter__.return_value = (
            file_handle
        )

        changelog.update_contributors()
        rendered = "".join(
            call.args[0] for call in file_handle.write.call_args_list
        )
        assert "dependabot[bot]" not in rendered
        assert "dev-user" in rendered

    def test_generate_changelog_with_skip_and_no_depends(self, mocker) -> None:
        """Test generate_changelog skip message and depends warning block."""
        changelog = _build_changelog(mocker)
        changelog.repo_data = MagicMock(html_url="https://github.com/user/repo")
        changelog.repo_releases = [MagicMock(tag_name="v1.0.0")]
        changelog.options["skip_releases"] = ["v0.9.0"]
        changelog.options["show_depends"] = False
        changelog.options["show_unreleased"] = True
        changelog.process_unreleased = MagicMock()
        changelog.process_release = MagicMock()

        mock_path = mocker.patch("github_changelog_md.changelog.changelog.Path")
        mock_path.cwd.return_value = Path("test_cwd")
        file_handle = MagicMock()
        mock_path.return_value.open.return_value.__enter__.return_value = (
            file_handle
        )

        changelog.generate_changelog()
        rendered = "".join(
            call.args[0] for call in file_handle.write.call_args_list
        )
        assert "Dependency updates are excluded" in rendered
        changelog.process_unreleased.assert_called_once()
        changelog.process_release.assert_called_once()
        assert changelog.prev_release == changelog.repo_releases[0]

    def test_process_release_skip_prev_release_and_title(
        self,
        mocker,
    ) -> None:
        """Test process_release skip branch and title/diff rendering branch."""
        changelog = _build_changelog(mocker)
        changelog.options["skip_releases"] = ["v1.0.0"]
        release = MagicMock(
            id=1,
            tag_name="v1.0.0",
            created_at=datetime.datetime(
                2021, 1, 1, tzinfo=datetime.timezone.utc
            ),
            html_url="https://github.com/user/repo/releases/tag/v1.0.0",
            title="Release Title",
        )
        out = MagicMock()
        changelog.process_release(out, release)
        out.write.assert_not_called()

        changelog.options["skip_releases"] = None
        changelog.prev_release = "HEAD"
        changelog.generate_diff_url = MagicMock()
        changelog.show_before_text = MagicMock()
        changelog.check_yanked = MagicMock()
        changelog.show_release_text = MagicMock()
        changelog.rprint_issues = MagicMock()
        changelog.rprint_prs = MagicMock()
        changelog.pr_by_release = {1: [MagicMock()]}
        changelog.issue_by_release = {1: [MagicMock()]}
        mocker.patch(
            "github_changelog_md.changelog.changelog.title_unique",
            return_value=True,
        )
        out = MagicMock()
        changelog.process_release(out, release)
        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "**_Release Title_**" in rendered
        changelog.generate_diff_url.assert_called_once()

    def test_show_release_text_accepts_release_instance(self, mocker) -> None:
        """Test show_release_text branch when given a release instance."""
        changelog = _build_changelog(mocker)
        changelog.release_text_cache.release_text_by_release = {
            "v1.0.0": "Text"
        }

        class FakeRelease:
            def __init__(self) -> None:
                self.tag_name = "v1.0.0"

        mocker.patch(
            "github_changelog_md.changelog.changelog.GitRelease",
            FakeRelease,
        )
        out = MagicMock()
        changelog.show_release_text(out, cast("Any", FakeRelease()))
        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert rendered == "Text\n\n"

    def test_rprint_issues_skips_ignored_labels(self, mocker) -> None:
        """Test rprint_issues drops issues with ignored labels."""
        changelog = _build_changelog(mocker)
        changelog.options["show_issues"] = True
        changelog.ignored_labels = ["wontfix"]
        issue = MagicMock()
        issue.number = 7
        issue.title = "Ignored issue"
        issue.html_url = "https://github.com/user/repo/issues/7"
        label = MagicMock()
        label.name = "wontfix"
        issue.labels = [label]
        issue.closed_by = MagicMock(
            login="dev",
            html_url="https://github.com/dev",
        )
        out = MagicMock()
        changelog.rprint_issues(out, [issue])
        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "[#7]" not in rendered

    def test_generate_diff_url_with_release_prev(self, mocker) -> None:
        """Test generate_diff_url branch when prev_release is release object."""
        changelog = _build_changelog(mocker)
        changelog.repo_data = MagicMock(html_url="https://github.com/user/repo")
        changelog.options["show_diff"] = False
        changelog.options["show_patch"] = False

        class FakeRelease:
            def __init__(self, tag_name: str) -> None:
                self.tag_name = tag_name

        mocker.patch(
            "github_changelog_md.changelog.changelog.GitRelease",
            FakeRelease,
        )
        out = MagicMock()
        changelog.generate_diff_url(
            out,
            cast("Any", FakeRelease("v0.9.0")),
            cast("Any", FakeRelease("v1.0.0")),
        )
        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "v1.0.0...v0.9.0" in rendered
        assert "[`Diff`]" not in rendered
        assert "[`Patch`]" not in rendered

    def test_rprint_prs_skips_dependencies_when_disabled(self, mocker) -> None:
        """Test rprint_prs skips dependency section when show_depends=False."""
        changelog = _build_changelog(mocker)
        changelog.options["show_depends"] = False
        changelog.sections = [("Dependency Updates", "dependencies")]
        changelog.ignored_labels = []

        dep_pr = MagicMock()
        dep_pr.labels = [MagicMock(name="dependencies")]
        dep_pr.number = 1
        dep_pr.title = "dep"
        dep_pr.html_url = "https://github.com/user/repo/pull/1"
        dep_pr.user = MagicMock(login="bot", html_url="https://github.com/bot")

        changelog.get_release_sections = MagicMock(
            return_value={"Dependency Updates": [dep_pr]}
        )
        out = MagicMock()
        changelog.rprint_prs(out, [dep_pr])
        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "Dependency Updates" not in rendered

    def test_get_sorted_items_unknown_order_returns_input(self, mocker) -> None:
        """Test get_sorted_items returns input for unknown ordering value."""
        changelog = _build_changelog(mocker)
        changelog.options["item_order"] = "keep"
        items = [MagicMock(number=2), MagicMock(number=1)]
        assert changelog.get_sorted_items(items) is items

    def test_get_latest_release_date_uses_first_commit_when_no_releases(
        self,
        mocker,
    ) -> None:
        """Test get_latest_release_date falls back to first commit date."""
        changelog = _build_changelog(mocker)
        changelog.repo_releases = []
        first_date = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
        first_commit = MagicMock()
        first_commit.commit.committer.date = first_date
        changelog.repo_data = MagicMock()
        changelog.repo_data.get_commits.return_value.reversed = [first_commit]

        assert changelog.get_latest_release_date() == first_date

    def test_filter_issues_drops_pull_requests(self, mocker) -> None:
        """Test filter_issues keeps only issues without pull_request marker."""
        changelog = _build_changelog(mocker)
        issue = MagicMock(pull_request=None)
        pr_issue = MagicMock(pull_request=MagicMock())
        changelog.repo_issues = cast("Any", [issue, pr_issue])

        filtered = changelog.filter_issues()
        assert filtered == [issue]

    def test_api_wrapper_methods_success_and_error_paths(self, mocker) -> None:
        """Test API wrapper methods success/error branches."""
        changelog = _build_changelog(mocker)
        changelog.repo_data = MagicMock()

        issues = MagicMock(totalCount=2)
        pulls = MagicMock(totalCount=3)
        releases = MagicMock(totalCount=1)
        releases.__iter__.return_value = iter([MagicMock(tag_name="v1.0.0")])
        changelog.repo_data.get_issues.return_value = issues
        changelog.repo_data.get_pulls.return_value = pulls
        changelog.repo_data.get_releases.return_value = releases

        assert changelog.get_closed_issues() == issues
        assert changelog.get_closed_prs() == pulls
        assert len(changelog.get_repo_releases()) == 1

        git_error_mock = mocker.patch(
            "github_changelog_md.changelog.changelog.git_error",
            side_effect=typer.Exit(ExitErrors.GIT_ERROR),
        )
        changelog.repo_data.get_issues.side_effect = GithubException(
            status=500,
            data={"message": "boom"},
        )
        with pytest.raises(typer.Exit):
            changelog.get_closed_issues()
        assert git_error_mock.called

        changelog.repo_data.get_pulls.side_effect = GithubException(
            status=500,
            data={"message": "boom"},
        )
        with pytest.raises(typer.Exit):
            changelog.get_closed_prs()

        changelog.repo_data.get_releases.side_effect = GithubException(
            status=500,
            data={"message": "boom"},
        )
        with pytest.raises(typer.Exit):
            changelog.get_repo_releases()

    def test_get_repo_data_success_and_error(self, mocker) -> None:
        """Test get_repo_data success and exception handling."""
        changelog = _build_changelog(mocker)
        changelog.repo_name = "repo"
        changelog.user = None
        user_obj = MagicMock(login="owner")
        repo_obj = MagicMock(full_name="owner/repo")
        changelog.git = MagicMock()
        changelog.git.get_user.return_value = user_obj
        changelog.git.get_user.return_value.get_repo.return_value = repo_obj

        assert changelog.get_repo_data() == repo_obj

        git_error_mock = mocker.patch(
            "github_changelog_md.changelog.changelog.git_error",
            side_effect=typer.Exit(ExitErrors.GIT_ERROR),
        )
        changelog.git.get_user.side_effect = GithubException(
            status=404,
            data={"message": "no repo"},
        )
        with pytest.raises(typer.Exit):
            changelog.get_repo_data()
        assert git_error_mock.called
