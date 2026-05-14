"""GitHub data access for changelog generation."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, NoReturn, TypeVar

import typer
from github import Auth, Github, GithubException
from rich import print as rprint
from rich.progress import (
    BarColumn,
    Progress,
    ProgressColumn,
    SpinnerColumn,
    Task,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from github_changelog_md.changelog.models import (
    ChangelogIssue,
    ChangelogPullRequest,
    ChangelogRelease,
    ChangelogRepository,
    issue_from_github,
    pull_request_from_github,
    release_from_github,
    repository_from_github,
)
from github_changelog_md.constants import ExitErrors

if TYPE_CHECKING:  # pragma: no cover
    import datetime
    from collections.abc import Callable, Iterable

    from github.Repository import Repository

GithubItem = TypeVar("GithubItem")
ChangelogItem = TypeVar("ChangelogItem")


class ItemCountColumn(ProgressColumn):
    """Render item counts for known and unknown totals."""

    def render(self, task: Task) -> str:
        """Render completed item count, with total when available."""
        completed = int(task.completed)
        if task.total is None:
            return str(completed)
        return f"{completed}/{int(task.total)}"


def git_error(exc: GithubException) -> NoReturn:
    """Handle a Git Exception."""
    rprint(
        f"\n[red]  X  Error {exc.status} while getting the "
        f"Repo : {exc.data.get('message')}\n",
        file=sys.stderr,
    )
    raise typer.Exit(ExitErrors.GIT_ERROR)


class GitHubDataSource:
    """Fetch and adapt GitHub repository data."""

    def __init__(self, git: Github) -> None:
        """Initialize the data source with a GitHub client."""
        self.git = git
        self.repo_data: Repository | None = None

    @classmethod
    def from_token(cls, github_pat: str) -> GitHubDataSource:
        """Create a data source from a GitHub personal access token."""
        auth = Auth.Token(github_pat)
        return cls(Github(auth=auth))

    def get_repo_data(
        self, repo_name: str, user: str | None
    ) -> ChangelogRepository:
        """Read the repository data from GitHub."""
        rprint("  [green]->[/green] Getting Repository data ... ", end="")
        try:
            repo_user = user or self.git.get_user().login
            self.repo_data = self.git.get_user(repo_user).get_repo(repo_name)
        except GithubException as exc:
            git_error(exc)
        else:
            rprint("[green]Done[/green]")
            repo = repository_from_github(self.repo_data)
            rprint(
                "  [green]->[/green] Repository : "
                f"[bold]{repo.full_name}[/bold]",
            )
            return repo

    def get_repo_releases(self) -> list[ChangelogRelease]:
        """Get release data from GitHub."""
        rprint("  [green]->[/green] Getting Releases ... ", end="")
        try:
            repo_releases = self._repo_data.get_releases()
        except GithubException as exc:
            git_error(exc)
        else:
            rprint(f"[green]{repo_releases.totalCount} Found[/green]")
            return self._adapt_items(
                "Loading release details",
                repo_releases,
                repo_releases.totalCount,
                release_from_github,
            )

    def get_closed_prs(self) -> list[ChangelogPullRequest]:
        """Get closed pull requests from GitHub."""
        rprint("  [green]->[/green] Getting Closed PRs ... ", end="")
        try:
            repo_prs = self._repo_data.get_pulls(
                state="closed", sort="created", direction="desc"
            )
        except GithubException as exc:
            git_error(exc)
        else:
            rprint(f"[green]{repo_prs.totalCount} Found[/green]")
            return self._adapt_items(
                "Loading PR details",
                repo_prs,
                repo_prs.totalCount,
                pull_request_from_github,
            )

    def get_closed_issues(self) -> list[ChangelogIssue]:
        """Get closed issues from GitHub."""
        rprint(
            "  [green]->[/green] Getting Closed Issue Candidates ... ",
        )
        try:
            repo_issues = self._repo_data.get_issues(
                state="closed",
                sort="created",
            )
        except GithubException as exc:
            git_error(exc)
        else:
            return self._adapt_items(
                "Loading issue candidates",
                repo_issues,
                0,
                issue_from_github,
            )

    def get_first_commit_date(self) -> datetime.datetime:
        """Return the first commit date for repositories without releases."""
        first_commit = self._repo_data.get_commits().reversed[0]
        return first_commit.commit.committer.date

    @property
    def _repo_data(self) -> Repository:
        if self.repo_data is None:
            msg = "Repository data has not been loaded"
            raise RuntimeError(msg)
        return self.repo_data

    def _adapt_items(
        self,
        description: str,
        items: Iterable[GithubItem],
        total: int,
        adapter: Callable[[GithubItem], ChangelogItem],
    ) -> list[ChangelogItem]:
        """Adapt GitHub items while showing visible progress."""
        adapted: list[ChangelogItem] = []
        progress_total = total if total > 0 else None
        columns: tuple[str | ProgressColumn, ...]
        if progress_total is None:
            columns = (
                SpinnerColumn(),
                TextColumn("  [green]->[/green] {task.description}"),
                ItemCountColumn(),
                TimeElapsedColumn(),
            )
        else:
            columns = (
                TextColumn("  [green]->[/green] {task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                ItemCountColumn(),
                TimeRemainingColumn(),
            )
        with Progress(
            *columns,
            redirect_stdout=False,
            redirect_stderr=False,
        ) as progress:
            task = progress.add_task(description, total=progress_total)
            for item in items:
                adapted.append(adapter(item))
                progress.advance(task)
        return adapted
