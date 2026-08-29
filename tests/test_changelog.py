"""Test the ChangeLog class."""

import datetime
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, cast
from unittest.mock import MagicMock

import pytest
import typer
from github import GithubException
from github.GitRelease import GitRelease

from github_changelog_md.changelog.bucketing import (
    bucket_issues,
    bucket_pull_requests,
    get_unreleased_cutoff,
)
from github_changelog_md.changelog.changelog import (
    ChangeLog,
    build_release_text_cache,
)
from github_changelog_md.changelog.github_data import (
    GitHubDataSource,
    ItemCountColumn,
    git_error,
)
from github_changelog_md.changelog.models import (
    ChangelogIssue,
    ChangelogLabel,
    ChangelogPullRequest,
    ChangelogRelease,
    ChangelogRepository,
    ChangelogUser,
    issue_from_github,
    label_from_github,
    pull_request_from_github,
    release_from_github,
    user_from_github,
)
from github_changelog_md.config.validation import (
    ChangelogConfigError,
    validate_changelog_options,
)
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
        "bold_sections": False,
    }


class _MockChangeLog(ChangeLog):
    data_source: MagicMock


def _build_changelog(
    _mocker=None, settings_overrides: Mapping[str, object] | None = None
) -> _MockChangeLog:
    if settings_overrides is None and isinstance(_mocker, Mapping):
        settings_overrides = _mocker

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
    data_source = MagicMock(spec=GitHubDataSource)
    if settings_overrides:
        for key, value in settings_overrides.items():
            setattr(settings, key, value)

    return _MockChangeLog(
        "repo",
        _default_options(),
        settings,
        data_source,
        build_release_text_cache(settings),
    )


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


@dataclass
class _OutputScenario:
    releases: list[Any] = field(default_factory=list)
    prs_by_release: dict[int, list[ChangelogPullRequest]] = field(
        default_factory=dict
    )
    issues_by_release: dict[int, list[ChangelogIssue]] = field(
        default_factory=dict
    )
    unreleased_prs: list[ChangelogPullRequest] = field(default_factory=list)
    unreleased_issues: list[ChangelogIssue] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class _LazyGithubUser:
    login: str
    html_url: str

    @property
    def name(self) -> str:
        msg = "name should not be read during item adaptation"
        raise AssertionError(msg)


def _date(year: int, month: int, day: int) -> datetime.datetime:
    return datetime.datetime(year, month, day, tzinfo=datetime.timezone.utc)


def _user(login: str, name: str | None = None) -> ChangelogUser:
    return ChangelogUser(
        login=login,
        html_url=f"https://github.com/{login}",
        name=name,
    )


def _label(name: str) -> ChangelogLabel:
    return ChangelogLabel(name=name)


def _release(
    release_id: int,
    tag_name: str,
    title: str,
    created_at: datetime.datetime,
    body: str | None = "",
) -> ChangelogRelease:
    return ChangelogRelease(
        id=release_id,
        tag_name=tag_name,
        title=title,
        html_url=f"https://github.com/user/repo/releases/tag/{tag_name}",
        created_at=created_at,
        body=body,
    )


def _pr(
    number: int,
    title: str,
    user_login: str,
    labels: list[ChangelogLabel],
) -> ChangelogPullRequest:
    return ChangelogPullRequest(
        id=number,
        number=number,
        title=title,
        html_url=f"https://github.com/user/repo/pull/{number}",
        user=_user(user_login),
        labels=labels,
        merged_at=None,
    )


def _issue(
    number: int,
    title: str,
    user_login: str,
    labels: list[ChangelogLabel],
    *,
    closed_by_login: str | None = None,
) -> ChangelogIssue:
    return ChangelogIssue(
        id=number,
        number=number,
        title=title,
        html_url=f"https://github.com/user/repo/issues/{number}",
        user=_user(user_login),
        labels=labels,
        closed_at=None,
        closed_by=_user(closed_by_login) if closed_by_login else None,
        pull_request=None,
    )


def _github_release(
    release_id: int,
    tag_name: str,
    title: str,
    created_at: datetime.datetime,
    body: str = "",
) -> GitRelease:
    release = MagicMock(spec=GitRelease)
    release.id = release_id
    release.tag_name = tag_name
    release.title = title
    release.created_at = created_at
    release.body = body
    release.html_url = f"https://github.com/user/repo/releases/tag/{tag_name}"
    return cast("GitRelease", release)


def _render_changelog(
    changelog: ChangeLog, mocker, scenario: _OutputScenario
) -> str:
    changelog.options["output_file"] = "CHANGELOG.md"
    changelog.repo_data = MagicMock(
        html_url="https://github.com/user/repo",
        name="repo",
    )
    changelog.repo_releases = cast("Any", scenario.releases)
    changelog.pr_by_release = cast("Any", scenario.prs_by_release)
    changelog.issue_by_release = cast("Any", scenario.issues_by_release)
    changelog.unreleased = cast("Any", scenario.unreleased_prs)
    changelog.unreleased_issues = cast("Any", scenario.unreleased_issues)
    changelog.sections = [
        ("Breaking Changes", "breaking"),
        ("Merged Pull Requests", None),
        ("Enhancements", "enhancement"),
        ("Bug Fixes", "bug"),
        ("Refactoring", "refactor"),
        ("Documentation", "documentation"),
        ("Dependency Updates", "dependencies"),
    ]
    changelog.ignored_labels = ["duplicate", "invalid", "question", "wontfix"]

    mock_path = mocker.patch("github_changelog_md.changelog.changelog.Path")
    mock_path.cwd.return_value = Path("test_cwd")
    file_handle = MagicMock()
    mock_path.return_value.open.return_value.__enter__.return_value = (
        file_handle
    )

    changelog.generate_changelog()

    return "".join(call.args[0] for call in file_handle.write.call_args_list)


class TestChangelogModels:
    """Tests for changelog domain model adapters."""

    def test_github_user_and_label_adapters(self) -> None:
        """Test PyGithub user and label conversion."""
        user = MagicMock()
        user.login = "dev-user"
        user.html_url = "https://github.com/dev-user"
        user.name = "Dev User"
        label = MagicMock(name="bug")
        label.name = "bug"

        assert user_from_github(cast("Any", user)) == ChangelogUser(
            login="dev-user",
            html_url="https://github.com/dev-user",
        )
        assert user_from_github(None) is None
        assert label_from_github(label) == ChangelogLabel(name="bug")

    def test_github_user_adapter_avoids_lazy_name_fetch(self) -> None:
        """Test user conversion does not hydrate full profile data."""
        user = _LazyGithubUser(
            login="dev-user",
            html_url="https://github.com/dev-user",
        )

        assert user_from_github(cast("Any", user)) == ChangelogUser(
            login="dev-user",
            html_url="https://github.com/dev-user",
        )

    def test_github_release_adapter(self) -> None:
        """Test PyGithub release conversion."""
        release = _github_release(
            release_id=1,
            tag_name="v1.0.0",
            title="Version 1",
            created_at=_date(2021, 1, 1),
            body="Release notes",
        )

        assert release_from_github(release) == ChangelogRelease(
            id=1,
            tag_name="v1.0.0",
            title="Version 1",
            html_url="https://github.com/user/repo/releases/tag/v1.0.0",
            created_at=_date(2021, 1, 1),
            body="Release notes",
        )

    def test_github_pull_request_adapter(self) -> None:
        """Test PyGithub pull request conversion."""
        label = MagicMock()
        label.name = "enhancement"
        user = MagicMock()
        user.login = "dev-user"
        user.html_url = "https://github.com/dev-user"
        user.name = None
        pull_request = MagicMock()
        pull_request.id = 10
        pull_request.number = 5
        pull_request.title = "add feature"
        pull_request.html_url = "https://github.com/user/repo/pull/5"
        pull_request.user = user
        pull_request.labels = [label]
        pull_request.merged_at = _date(2021, 1, 2)

        assert pull_request_from_github(pull_request) == ChangelogPullRequest(
            id=10,
            number=5,
            title="add feature",
            html_url="https://github.com/user/repo/pull/5",
            user=ChangelogUser(
                login="dev-user",
                html_url="https://github.com/dev-user",
            ),
            labels=[ChangelogLabel(name="enhancement")],
            merged_at=_date(2021, 1, 2),
        )

    def test_github_issue_adapter(self) -> None:
        """Test PyGithub issue conversion."""
        label = MagicMock()
        label.name = "bug"
        user = MagicMock()
        user.login = "reporter"
        user.html_url = "https://github.com/reporter"
        user.name = None
        closed_by = MagicMock()
        closed_by.login = "maintainer"
        closed_by.html_url = "https://github.com/maintainer"
        closed_by.name = "Maintainer"
        issue = MagicMock()
        issue.id = 20
        issue.number = 7
        issue.title = "fix bug"
        issue.html_url = "https://github.com/user/repo/issues/7"
        issue.user = user
        issue.labels = [label]
        issue.closed_at = _date(2021, 1, 3)
        issue.closed_by = closed_by
        issue.pull_request = None

        assert issue_from_github(issue) == ChangelogIssue(
            id=20,
            number=7,
            title="fix bug",
            html_url="https://github.com/user/repo/issues/7",
            user=ChangelogUser(
                login="reporter",
                html_url="https://github.com/reporter",
            ),
            labels=[ChangelogLabel(name="bug")],
            closed_at=_date(2021, 1, 3),
            closed_by=ChangelogUser(
                login="maintainer",
                html_url="https://github.com/maintainer",
            ),
        )

    def test_github_item_adapters_require_users(self) -> None:
        """Test PR and issue conversion rejects missing users."""
        pull_request = MagicMock(user=None)
        issue = MagicMock(user=None)

        with pytest.raises(
            ValueError, match="Pull request user cannot be None"
        ):
            pull_request_from_github(pull_request)
        with pytest.raises(ValueError, match="Issue user cannot be None"):
            issue_from_github(issue)


class TestGitHubDataSource:
    """Tests for the GitHub data source boundary."""

    def test_from_token_builds_github_client(self, mocker) -> None:
        """Test token factory owns GitHub client construction."""
        auth = MagicMock()
        git = MagicMock()
        auth_token = mocker.patch(
            "github_changelog_md.changelog.github_data.Auth.Token",
            return_value=auth,
        )
        github = mocker.patch(
            "github_changelog_md.changelog.github_data.Github",
            return_value=git,
        )

        data_source = GitHubDataSource.from_token("token")

        auth_token.assert_called_once_with("token")
        github.assert_called_once_with(auth=auth)
        assert data_source.git is git

    def test_item_count_column_handles_unknown_total(self) -> None:
        """Test progress counts omit invalid totals."""
        expected_count = 7
        task = MagicMock(completed=expected_count, total=None)

        assert ItemCountColumn().render(task) == str(expected_count)

    def test_fetch_methods_report_progress(self, mocker) -> None:
        """Test GitHub item adaptation advances visible progress."""
        expected_total = 3
        progress = MagicMock()
        progress.__enter__.return_value = progress
        progress.add_task.return_value = "task-id"
        progress_cls = mocker.patch(
            "github_changelog_md.changelog.github_data.Progress",
            return_value=progress,
        )
        data_source = GitHubDataSource(MagicMock())
        user = MagicMock()
        user.login = "dev"
        user.html_url = "https://github.com/dev"
        user.name = None
        repo_prs = MagicMock(totalCount=expected_total)
        repo_prs.__iter__.return_value = iter(
            [
                MagicMock(
                    id=pr_id,
                    number=pr_id,
                    title=f"pr {pr_id}",
                    html_url=f"https://github.com/user/repo/pull/{pr_id}",
                    user=user,
                    labels=[],
                    merged_at=_date(2021, 1, pr_id),
                )
                for pr_id in range(1, expected_total + 1)
            ]
        )
        repo = MagicMock()
        repo.get_pulls.return_value = repo_prs
        data_source.repo_data = repo

        assert len(data_source.get_closed_prs()) == expected_total
        progress_cls.assert_called_once()
        progress.add_task.assert_called_once_with(
            "Loading PR details", total=expected_total
        )
        assert progress.advance.call_count == expected_total
        progress.advance.assert_called_with("task-id")

    def test_fetch_progress_handles_unknown_total(self, mocker) -> None:
        """Test progress uses an unknown total when GitHub count is invalid."""
        progress = MagicMock()
        progress.__enter__.return_value = progress
        progress.add_task.return_value = "task-id"
        mocker.patch(
            "github_changelog_md.changelog.github_data.Progress",
            return_value=progress,
        )
        data_source = GitHubDataSource(MagicMock())
        user = MagicMock()
        user.login = "reporter"
        user.html_url = "https://github.com/reporter"
        user.name = None
        issue = MagicMock()
        issue.id = 1
        issue.number = 1
        issue.title = "issue"
        issue.html_url = "https://github.com/user/repo/issues/1"
        issue.user = user
        issue.labels = []
        issue.closed_at = _date(2021, 1, 1)
        issue.closed_by = user
        issue.pull_request = None
        repo_issues = MagicMock(totalCount=0)
        repo_issues.__iter__.return_value = iter([issue])
        repo = MagicMock()
        repo.get_issues.return_value = repo_issues
        data_source.repo_data = repo

        assert len(data_source.get_closed_issues()) == 1
        progress.add_task.assert_called_once_with(
            "Loading issue candidates", total=None
        )

    def test_get_repo_data_returns_repository_model(self) -> None:
        """Test repository lookup converts PyGithub data."""
        git = MagicMock()
        current_user = MagicMock(login="owner")
        owner_user = MagicMock()
        repo = MagicMock()
        repo.name = "repo"
        repo.full_name = "owner/repo"
        repo.html_url = "https://github.com/owner/repo"
        owner_user.get_repo.return_value = repo
        git.get_user.side_effect = [current_user, owner_user]

        data_source = GitHubDataSource(git)

        assert data_source.get_repo_data("repo", None) == ChangelogRepository(
            name="repo",
            full_name="owner/repo",
            html_url="https://github.com/owner/repo",
        )
        owner_user.get_repo.assert_called_once_with("repo")

    def test_fetch_methods_return_domain_models(self) -> None:
        """Test release, PR, issue, and first commit fetch paths."""
        data_source = GitHubDataSource(MagicMock())

        label = MagicMock()
        label.name = "bug"
        user = MagicMock()
        user.login = "dev"
        user.html_url = "https://github.com/dev"
        user.name = None
        release = _github_release(
            release_id=1,
            tag_name="v1.0.0",
            title="Version 1",
            created_at=_date(2021, 1, 1),
            body="Body",
        )
        pr = MagicMock()
        pr.id = 2
        pr.number = 20
        pr.title = "fix pr"
        pr.html_url = "https://github.com/user/repo/pull/20"
        pr.user = user
        pr.labels = [label]
        pr.merged_at = _date(2021, 1, 2)
        issue = MagicMock()
        issue.id = 3
        issue.number = 30
        issue.title = "fix issue"
        issue.html_url = "https://github.com/user/repo/issues/30"
        issue.user = user
        issue.labels = [label]
        issue.closed_at = _date(2021, 1, 3)
        issue.closed_by = user
        issue.pull_request = None
        first_commit = MagicMock()
        first_commit.commit.committer.date = _date(2020, 1, 1)

        repo = MagicMock()
        repo.get_releases.return_value = MagicMock(totalCount=1)
        repo.get_releases.return_value.__iter__.return_value = iter([release])
        repo.get_pulls.return_value = MagicMock(totalCount=1)
        repo.get_pulls.return_value.__iter__.return_value = iter([pr])
        repo.get_issues.return_value = MagicMock(totalCount=1)
        repo.get_issues.return_value.__iter__.return_value = iter([issue])
        repo.get_commits.return_value.reversed = [first_commit]
        data_source.repo_data = repo

        assert data_source.get_repo_releases() == [
            ChangelogRelease(
                id=1,
                tag_name="v1.0.0",
                title="Version 1",
                html_url="https://github.com/user/repo/releases/tag/v1.0.0",
                created_at=_date(2021, 1, 1),
                body="Body",
            )
        ]
        assert data_source.get_closed_prs() == [
            ChangelogPullRequest(
                id=2,
                number=20,
                title="fix pr",
                html_url="https://github.com/user/repo/pull/20",
                user=_user("dev"),
                labels=[_label("bug")],
                merged_at=_date(2021, 1, 2),
            )
        ]
        assert data_source.get_closed_issues() == [
            ChangelogIssue(
                id=3,
                number=30,
                title="fix issue",
                html_url="https://github.com/user/repo/issues/30",
                user=_user("dev"),
                labels=[_label("bug")],
                closed_at=_date(2021, 1, 3),
                closed_by=_user("dev"),
            )
        ]
        assert data_source.get_first_commit_date() == _date(2020, 1, 1)

    def test_fetch_methods_route_github_errors(self, mocker) -> None:
        """Test GitHub exceptions use the shared exit path."""
        data_source = GitHubDataSource(MagicMock())
        data_source.repo_data = MagicMock()
        data_source.repo_data.get_issues.side_effect = GithubException(
            status=500,
            data={"message": "boom"},
        )
        git_error_mock = mocker.patch(
            "github_changelog_md.changelog.github_data.git_error",
            side_effect=typer.Exit(ExitErrors.GIT_ERROR),
        )

        with pytest.raises(typer.Exit):
            data_source.get_closed_issues()

        git_error_mock.assert_called_once()

    def test_other_github_errors_use_shared_exit_path(self, mocker) -> None:
        """Test repository, release, and PR errors use shared error handling."""
        expected_errors = ["repo error", "release error", "pull error"]
        git = MagicMock()
        git.get_user.side_effect = GithubException(
            status=404,
            data={"message": "missing"},
        )
        git_error_mock = mocker.patch(
            "github_changelog_md.changelog.github_data.git_error",
            side_effect=typer.Exit(ExitErrors.GIT_ERROR),
        )
        data_source = GitHubDataSource(git)

        with pytest.raises(typer.Exit):
            data_source.get_repo_data("repo", None)

        repo = MagicMock()
        data_source.repo_data = repo
        repo.get_releases.side_effect = GithubException(
            status=500,
            data={"message": "release boom"},
        )
        with pytest.raises(typer.Exit):
            data_source.get_repo_releases()

        repo.get_pulls.side_effect = GithubException(
            status=500,
            data={"message": "pull boom"},
        )
        with pytest.raises(typer.Exit):
            data_source.get_closed_prs()

        assert git_error_mock.call_count == len(expected_errors)

    def test_fetch_requires_repository_data(self) -> None:
        """Test fetch methods require repository lookup first."""
        data_source = GitHubDataSource(MagicMock())

        with pytest.raises(RuntimeError, match="Repository data"):
            data_source.get_first_commit_date()


class TestChangelogBucketing:
    """Tests for pure release bucketing logic."""

    def test_unreleased_cutoff_uses_latest_release_date(self) -> None:
        """Test cutoff is independent of release list order."""
        fallback_date = _date(2020, 1, 1)
        releases = [
            _release(1, "v1.0.0", "Old", _date(2021, 1, 1)),
            _release(2, "v2.0.0", "New", _date(2021, 1, 10)),
        ]

        assert get_unreleased_cutoff(releases[::-1], fallback_date) == _date(
            2021, 1, 10
        )

    def test_unreleased_cutoff_uses_fallback_without_releases(self) -> None:
        """Test cutoff uses first commit date when there are no releases."""
        fallback_date = _date(2020, 1, 1)

        assert get_unreleased_cutoff([], fallback_date) == fallback_date

    def test_bucket_pull_requests_sorts_releases_and_tracks_unreleased(
        self,
    ) -> None:
        """Test PRs are assigned by date regardless of release input order."""
        releases = [
            _release(2, "v2.0.0", "New", _date(2021, 1, 10)),
            _release(1, "v1.0.0", "Old", _date(2021, 1, 1)),
        ]
        pr_old = replace(_pr(1, "old", "dev", []), merged_at=_date(2021, 1, 1))
        pr_new = replace(_pr(2, "new", "dev", []), merged_at=_date(2021, 1, 5))
        pr_unreleased = replace(
            _pr(3, "unreleased", "dev", []),
            merged_at=_date(2021, 1, 11),
        )
        pr_undated = _pr(4, "undated", "dev", [])

        result = bucket_pull_requests(
            releases,
            [pr_unreleased, pr_undated, pr_new, pr_old],
            _date(2021, 1, 10),
            [],
        )

        assert result.by_release[1] == [pr_old]
        assert result.by_release[2] == [pr_new]
        assert result.unreleased == [pr_unreleased]

    def test_bucket_pull_requests_handles_exact_release_timestamp(self) -> None:
        """Test an item exactly on a release timestamp belongs to it."""
        release = _release(1, "v1.0.0", "Release", _date(2021, 1, 1))
        pull_request = replace(
            _pr(1, "exact", "dev", []),
            merged_at=release.created_at,
        )

        result = bucket_pull_requests(
            [release],
            [pull_request],
            release.created_at,
            [],
        )

        assert result.by_release[1] == [pull_request]
        assert result.unreleased == []

    def test_bucket_issues_ignores_users_and_no_release_unreleased(
        self,
    ) -> None:
        """Test issue bucketing ignores configured users and no-release path."""
        issue = replace(
            _issue(1, "issue", "dev", []),
            closed_at=_date(2021, 1, 2),
        )
        ignored = replace(
            _issue(2, "ignored", "bot", []),
            closed_at=_date(2021, 1, 3),
        )

        result = bucket_issues(
            [],
            [ignored, issue],
            _date(2021, 1, 1),
            ["bot"],
        )

        assert result.by_release == {}
        assert result.unreleased == [issue]


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
        mock_path = mocker.patch(
            "github_changelog_md.changelog.changelog.Path",
        )
        mock_path.return_value.open.return_value.__enter__.return_value = (
            MagicMock()
        )
        changelog = _build_changelog(mocker)
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

    def test_constructor_does_not_read_release_settings(self) -> None:
        """Test release text config is supplied instead of read on init."""
        settings = MagicMock(spec=[])
        data_source = MagicMock(spec=GitHubDataSource)

        changelog = ChangeLog(
            "repo",
            _default_options(),
            settings,
            data_source,
        )

        assert changelog.release_text_cache.yanked_by_release == {}
        assert changelog.release_text_cache.release_text_before_by_release == {}
        assert changelog.release_text_cache.release_text_by_release == {}
        assert changelog.release_text_cache.release_overrides_by_release == {}

    def test_build_release_cache_maps_are_created(self) -> None:
        """Test release lookup caches are built from settings."""
        settings = MagicMock()
        settings.yanked = [{"release": " v1.0.0 ", "reason": "bad build"}]
        settings.release_text_before = [
            {"release": " v1.0.0 ", "text": " before text "}
        ]
        settings.release_text = [
            {"release": " v1.0.0 ", "text": " release text "}
        ]
        settings.release_overrides = [
            {"release": " v1.0.0 ", "text": " override text\n"}
        ]

        cache = build_release_text_cache(settings)

        assert cache.yanked_by_release["v1.0.0"] == "bad build"
        assert cache.release_text_before_by_release["v1.0.0"] == "before text"
        assert cache.release_text_by_release["v1.0.0"] == "release text"
        assert cache.release_overrides_by_release["v1.0.0"] == "override text"

    def test_build_release_lookup_rejects_missing_value_key(self) -> None:
        """Test release lookup config requires the expected value key."""
        with pytest.raises(
            ChangelogConfigError,
            match="release entry 1 is missing 'text'",
        ):
            ChangeLog.build_release_lookup(
                [{"release": "v1.0.0"}],
                value_key="text",
            )

    def test_build_release_lookup_rejects_empty_release(self) -> None:
        """Test release lookup config requires a non-empty release tag."""
        with pytest.raises(
            ChangelogConfigError,
            match="release entry 1 has an empty release tag",
        ):
            ChangeLog.build_release_lookup(
                [{"release": "  ", "text": "Release note"}],
                value_key="text",
            )

    def test_build_release_lookup_rejects_non_string_value(self) -> None:
        """Test release lookup config values must be strings."""
        with pytest.raises(
            ChangelogConfigError,
            match="release entry 1 value 'text' must be a string",
        ):
            ChangeLog.build_release_lookup(
                cast("Any", [{"release": "v1.0.0", "text": 123}]),
                value_key="text",
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
        changelog.unreleased = [_pr(1, "pending change", "dev", [])]
        changelog.unreleased_issues = []

        out = MagicMock()
        changelog.process_unreleased(out)

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "## [Unreleased]" in rendered
        assert "/tree/HEAD" in rendered
        assert changelog.prev_release == "HEAD"
        assert "Pending change" in rendered

    def test_process_unreleased_with_next_release_uses_tag_link(
        self,
        mocker,
    ) -> None:
        """Test process_unreleased link and heading for next_release option."""
        changelog = _build_changelog(mocker)
        changelog.options["next_release"] = "v2.0.0"
        changelog.repo_data = MagicMock(html_url="https://github.com/user/repo")
        changelog.unreleased = [_pr(1, "pending change", "dev", [])]
        changelog.unreleased_issues = []

        out = MagicMock()
        changelog.process_unreleased(out)

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "## [v2.0.0]" in rendered
        assert "/releases/tag/v2.0.0" in rendered
        assert "Pending change" in rendered

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

    @pytest.mark.parametrize(
        ("bold_sections", "expected"),
        [
            (False, "### Security\n\n"),
            (True, "**Security**\n\n"),
        ],
    )
    def test_rprint_prs_formats_section_heading(
        self,
        mocker,
        bold_sections,
        expected: str,
    ) -> None:
        """Test generated section headings use the selected Markdown style."""
        changelog = _build_changelog(mocker)
        changelog.options["bold_sections"] = bold_sections
        changelog.sections = [("Security", "security")]
        changelog.ignored_labels = []
        out = MagicMock()

        changelog.rprint_prs(
            out,
            [_pr(1, "security change", "dev", [_label("security")])],
        )

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert expected in rendered

    def test_rprint_prs_formats_renamed_and_custom_sections(
        self, mocker
    ) -> None:
        """Test all configured PR section titles use H3 headings by default."""
        changelog = _build_changelog(mocker)
        changelog.sections = [
            ("Merged Pull Requests", None),
            ("Fixes", "bug"),
            ("Security", "security"),
        ]
        changelog.ignored_labels = []
        pull_requests = [
            _pr(1, "plain change", "dev", []),
            _pr(2, "fixed bug", "dev", [_label("bug")]),
            _pr(3, "security change", "dev", [_label("security")]),
        ]
        out = MagicMock()

        changelog.rprint_prs(out, pull_requests)

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "### Merged Pull Requests\n\n" in rendered
        assert "### Fixes\n\n" in rendered
        assert "### Security\n\n" in rendered

    def test_legacy_bold_style_applies_to_issues_and_prs(self, mocker) -> None:
        """Test legacy bold formatting covers both section renderer paths."""
        changelog = _build_changelog(mocker)
        changelog.options["bold_sections"] = True
        changelog.sections = [("Merged Pull Requests", None)]
        changelog.ignored_labels = []
        issue_out = MagicMock()
        pr_out = MagicMock()

        changelog.rprint_issues(
            issue_out,
            [_issue(1, "closed issue", "reporter", [])],
        )
        changelog.rprint_prs(
            pr_out,
            [_pr(2, "merged change", "dev", [])],
        )

        rendered_issues = "".join(
            call.args[0] for call in issue_out.write.call_args_list
        )
        rendered_prs = "".join(
            call.args[0] for call in pr_out.write.call_args_list
        )
        assert "**Closed Issues**\n\n" in rendered_issues
        assert "**Merged Pull Requests**\n\n" in rendered_prs
        assert "### " not in rendered_issues
        assert "### " not in rendered_prs

    def test_process_release_falls_back_to_release_body(self, mocker) -> None:
        """Test process_release renders release body when lists are empty."""
        changelog = _build_changelog(mocker)
        changelog.prev_release = None
        changelog.pr_by_release = {}
        changelog.issue_by_release = {}

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
        release.body = None

        out = MagicMock()
        changelog.process_release(out, release)
        rendered = "".join(call.args[0] for call in out.write.call_args_list)

        assert "There were no merged pull requests" in rendered

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

    def test_get_release_body_preserves_markdown_headings(self, mocker) -> None:
        """Test release-body headings are outside section-style formatting."""
        changelog = _build_changelog(mocker)
        release = MagicMock(body="# Highlights\n\n## Details")
        out = MagicMock()

        changelog.get_release_body(out, release)

        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert rendered == "# Highlights\n\n## Details\n"

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
        assert "### Closed Issues" in rendered
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

    def test_generate_changelog_normalizes_multiline_intro_spacing(
        self, mocker
    ) -> None:
        """Test multiline intro text does not add an extra blank line."""
        changelog = _build_changelog(mocker)
        changelog.repo_data = MagicMock(
            html_url="https://github.com/user/repo",
            name="repo",
        )
        changelog.repo_releases = [
            _release(
                release_id=1,
                tag_name="v1.0.0",
                title="v1.0.0",
                created_at=_date(2021, 1, 10),
            )
        ]
        changelog.options["output_file"] = "CHANGELOG.md"
        changelog.options["show_unreleased"] = False
        changelog.settings.intro_text = "First paragraph\n\nSecond paragraph\n"

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
        assert "Second paragraph\n\n## [v1.0.0]" in rendered
        assert "Second paragraph\n\n\n## [v1.0.0]" not in rendered

    def test_generate_changelog_renders_release_sections_golden(
        self, mocker
    ) -> None:
        """Test a release renders issues and PR sections as Markdown."""
        changelog = _build_changelog(mocker)
        changelog.options["show_unreleased"] = False
        changelog.options["ignore_items"] = [99]
        changelog.options["max_depends"] = 1

        release = _release(
            release_id=1,
            tag_name="v1.0.0",
            title="v1.0.0",
            created_at=_date(2021, 1, 10),
        )
        issue = _issue(
            number=7,
            title="fixed issue",
            user_login="reporter",
            labels=[_label("bug")],
            closed_by_login="maintainer",
        )
        ignored_issue = _issue(
            number=8,
            title="support request",
            user_login="reporter",
            labels=[_label("question")],
            closed_by_login="maintainer",
        )
        pr_plain = _pr(
            number=2,
            title="internal cleanup",
            user_login="dev-two",
            labels=[],
        )
        pr_feature = _pr(
            number=3,
            title="add feature",
            user_login="dev-three",
            labels=[_label("enhancement")],
        )
        pr_dep_old = _pr(
            number=4,
            title="bump dep old",
            user_login="dependabot[bot]",
            labels=[_label("dependencies")],
        )
        pr_dep_new = _pr(
            number=5,
            title="bump dep new",
            user_login="dependabot[bot]",
            labels=[_label("dependencies")],
        )
        pr_ignored = _pr(
            number=99,
            title="hidden change",
            user_login="dev-hidden",
            labels=[],
        )

        rendered = _render_changelog(
            changelog,
            mocker,
            _OutputScenario(
                releases=[release],
                prs_by_release={
                    release.id: [
                        pr_plain,
                        pr_feature,
                        pr_dep_old,
                        pr_dep_new,
                        pr_ignored,
                    ]
                },
                issues_by_release={release.id: [issue, ignored_issue]},
            ),
        )

        assert rendered == (
            "# Changelog\n\n"
            "## [v1.0.0](https://github.com/user/repo/releases/tag/v1.0.0) "
            "(2021-01-10)\n\n"
            "### Closed Issues\n\n"
            "- Fixed issue ([#7](https://github.com/user/repo/issues/7)) "
            "by [maintainer](https://github.com/maintainer)\n\n"
            "### Merged Pull Requests\n\n"
            "- Internal cleanup ([#2](https://github.com/user/repo/pull/2)) "
            "by [dev-two](https://github.com/dev-two)\n\n"
            "### Enhancements\n\n"
            "- Add feature ([#3](https://github.com/user/repo/pull/3)) "
            "by [dev-three](https://github.com/dev-three)\n\n"
            "### Dependency Updates\n\n"
            "- Bump dep new ([#5](https://github.com/user/repo/pull/5)) "
            "by [dependabot[bot]](https://github.com/dependabot[bot])\n"
            "- *and 1 more dependency updates*\n\n"
            "---\n"
            "*This changelog was generated using "
            "[github-changelog-md](http://changelog.seapagan.net/) "
            "by [Seapagan](https://github.com/seapagan)*\n"
        )

    def test_generate_changelog_renders_unreleased_golden(self, mocker) -> None:
        """Test unreleased changes render to the current HEAD link."""
        changelog = _build_changelog(
            mocker,
            {"release_text": [{"release": "unreleased", "text": "Preview"}]},
        )
        changelog.options["show_unreleased"] = True

        rendered = _render_changelog(
            changelog,
            mocker,
            _OutputScenario(
                unreleased_prs=[
                    _pr(
                        number=12,
                        title="prepare next work",
                        user_login="dev-next",
                        labels=[],
                    )
                ],
                unreleased_issues=[
                    _issue(
                        number=11,
                        title="closed next issue",
                        user_login="reporter",
                        labels=[],
                    )
                ],
            ),
        )

        assert rendered == (
            "# Changelog\n\n"
            "## [Unreleased](https://github.com/user/repo/tree/HEAD)\n\n"
            "Preview\n\n"
            "### Closed Issues\n\n"
            "- Closed next issue "
            "([#11](https://github.com/user/repo/issues/11))\n\n"
            "### Merged Pull Requests\n\n"
            "- Prepare next work "
            "([#12](https://github.com/user/repo/pull/12)) "
            "by [dev-next](https://github.com/dev-next)\n\n"
            "---\n"
            "*This changelog was generated using "
            "[github-changelog-md](http://changelog.seapagan.net/) "
            "by [Seapagan](https://github.com/seapagan)*\n"
        )

    def test_generate_changelog_renders_release_text_variants_golden(
        self, mocker
    ) -> None:
        """Test configured release text, yanked notes, and overrides render."""
        changelog = _build_changelog(
            mocker,
            {
                "release_text_before": [
                    {"release": "v1.0.0", "text": "Before release"}
                ],
                "release_text": [{"release": "v1.0.0", "text": "Release note"}],
                "release_overrides": [
                    {"release": "v2.0.0", "text": "Override body\n"}
                ],
                "yanked": [{"release": "v1.0.0", "reason": "bad artifact"}],
            },
        )
        changelog.options["show_unreleased"] = False
        release_two = _release(
            release_id=2,
            tag_name="v2.0.0",
            title="v2.0.0",
            created_at=_date(2021, 2, 1),
        )
        release_one = _release(
            release_id=1,
            tag_name="v1.0.0",
            title="Release One",
            created_at=_date(2021, 1, 1),
        )

        rendered = _render_changelog(
            changelog,
            mocker,
            _OutputScenario(releases=[release_two, release_one]),
        )

        assert rendered == (
            "# Changelog\n\n"
            "## [v2.0.0](https://github.com/user/repo/releases/tag/v2.0.0) "
            "(2021-02-01)\n\n"
            "Override body\n\n"
            "[`Full Changelog`](https://github.com/user/repo/compare/"
            "v1.0.0...v2.0.0) | [`Diff`](https://github.com/user/repo/"
            "compare/v1.0.0...v2.0.0.diff) | [`Patch`](https://github.com/"
            "user/repo/compare/v1.0.0...v2.0.0.patch)\n\n"
            "---\n\n"
            "Before release\n\n"
            "---\n\n"
            "## [v1.0.0](https://github.com/user/repo/releases/tag/v1.0.0) "
            "(2021-01-01) **[`YANKED`]**\n\n"
            "**This release has been removed for the following reason and "
            "should not be used:**\n\n"
            "- bad artifact\n\n"
            "**_Release One_**\n\n"
            "Release note\n\n"
            "There were no merged pull requests or closed issues "
            "for this release.\n\n"
            "See the Full Changelog below for details.\n\n"
            "---\n"
            "*This changelog was generated using "
            "[github-changelog-md](http://changelog.seapagan.net/) "
            "by [Seapagan](https://github.com/seapagan)*\n"
        )

    def test_generate_changelog_renders_skip_and_no_releases_golden(
        self, mocker
    ) -> None:
        """Test skipped releases and an otherwise empty changelog output."""
        changelog = _build_changelog(mocker)
        changelog.options["show_unreleased"] = False
        changelog.options["show_depends"] = False
        changelog.options["skip_releases"] = ["v1.0.0"]
        skipped = _release(
            release_id=1,
            tag_name="v1.0.0",
            title="v1.0.0",
            created_at=_date(2021, 1, 1),
        )

        rendered = _render_changelog(
            changelog,
            mocker,
            _OutputScenario(releases=[skipped]),
        )

        assert rendered == (
            "# Changelog\n\n"
            "*Dependency updates are excluded from this changelog, "
            "check each `Full Changelog` for details.*\n\n "
            "---\n"
            "*This changelog was generated using "
            "[github-changelog-md](http://changelog.seapagan.net/) "
            "by [Seapagan](https://github.com/seapagan)*\n"
        )

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
        changelog.get_unreleased_cutoff = MagicMock(
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
        assert "This changelog was generated using" in rendered

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
        changelog.pr_by_release = {}
        changelog.issue_by_release = {}
        release.body = None
        out = MagicMock()
        changelog.process_release(out, release)
        rendered = "".join(call.args[0] for call in out.write.call_args_list)
        assert "**_Release Title_**" in rendered
        assert "[`Full Changelog`]" in rendered

    def test_show_release_text_accepts_release_instance(self, mocker) -> None:
        """Test show_release_text branch when given a release instance."""
        changelog = _build_changelog(mocker)
        changelog.release_text_cache.release_text_by_release = {
            "v1.0.0": "Text"
        }

        class FakeRelease:
            def __init__(self) -> None:
                self.tag_name = "v1.0.0"

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

    def test_validate_changelog_options_rejects_unknown_order(self) -> None:
        """Test invalid ordering is rejected before changelog rendering."""
        options = _default_options()
        options["item_order"] = "keep"

        with pytest.raises(
            ChangelogConfigError,
            match="item_order must be one of",
        ):
            validate_changelog_options(options)

    def test_get_sorted_items_rejects_unknown_order(self, mocker) -> None:
        """Test renderer fails clearly if invalid ordering reaches it."""
        changelog = _build_changelog(mocker)
        changelog.options["item_order"] = "keep"

        with pytest.raises(ValueError, match="Unknown item order: keep"):
            changelog.get_sorted_items([MagicMock(number=1)])

    def test_get_unreleased_cutoff_uses_first_commit_when_no_releases(
        self,
        mocker,
    ) -> None:
        """Test get_unreleased_cutoff falls back to first commit date."""
        changelog = _build_changelog(mocker)
        changelog.repo_releases = []
        first_date = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
        changelog.data_source.get_first_commit_date.return_value = first_date

        assert changelog.get_unreleased_cutoff() == first_date

    def test_get_unreleased_cutoff_uses_latest_release(self, mocker) -> None:
        """Test get_unreleased_cutoff is independent of release list order."""
        changelog = _build_changelog(mocker)
        changelog.repo_releases = [
            _release(1, "v1.0.0", "Old", _date(2021, 1, 1)),
            _release(2, "v2.0.0", "New", _date(2021, 1, 10)),
        ]

        assert changelog.get_unreleased_cutoff() == _date(2021, 1, 10)

    def test_filter_issues_drops_pull_requests(self, mocker) -> None:
        """Test filter_issues keeps only issues without pull_request marker."""
        changelog = _build_changelog(mocker)
        issue = MagicMock(pull_request=None)
        pr_issue = MagicMock(pull_request=MagicMock())
        changelog.repo_issues = cast("Any", [issue, pr_issue])

        filtered = changelog.filter_issues()
        assert filtered == [issue]

    def test_api_wrapper_methods_success_and_error_paths(self, mocker) -> None:
        """Test API wrapper methods delegate to the data source."""
        changelog = _build_changelog(mocker)
        issues = [_issue(1, "issue", "dev", [])]
        pulls = [_pr(2, "pr", "dev", [])]
        releases = [_release(3, "v1.0.0", "v1.0.0", _date(2021, 1, 1))]
        changelog.data_source.get_closed_issues.return_value = issues
        changelog.data_source.get_closed_prs.return_value = pulls
        changelog.data_source.get_repo_releases.return_value = releases

        assert changelog.get_closed_issues() == issues
        assert changelog.get_closed_prs() == pulls
        assert changelog.get_repo_releases() == releases

    def test_get_repo_data_delegates_to_data_source(self, mocker) -> None:
        """Test get_repo_data uses the configured data source."""
        changelog = _build_changelog(mocker)
        changelog.repo_name = "repo"
        changelog.user = "owner"
        repo = ChangelogRepository(
            name="repo",
            full_name="owner/repo",
            html_url="https://github.com/owner/repo",
        )
        changelog.data_source.get_repo_data.return_value = repo

        assert changelog.get_repo_data() == repo
        changelog.data_source.get_repo_data.assert_called_once_with(
            "repo", "owner"
        )
