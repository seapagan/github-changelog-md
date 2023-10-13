"""Define the Changelog class.

This will encapsulate the logic for generating the changelog.
"""
from __future__ import annotations

import time
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

import typer  # pylint: disable=redefined-builtin
from github import Auth, Github, GithubException
from rich import print

from github_changelog_md.config import settings
from github_changelog_md.constants import ExitErrors
from github_changelog_md.helpers import header

if TYPE_CHECKING:
    from github.GitRelease import GitRelease
    from github.Issue import Issue
    from github.PaginatedList import PaginatedList
    from github.PullRequest import PullRequest
    from github.Repository import Repository


def git_error(exc: GithubException) -> None:
    """Handle a Git Exception."""
    print(
        f"\n[red]  X  Error {exc.status} while getting the "
        f"Repo : {exc.data.get('message')}\n"
    )
    raise typer.Exit(ExitErrors.GIT_ERROR)


class ChangeLog:
    """Define the Changelog class."""

    done_str = "[green]Done[/green]"

    def __init__(self, repo_name: str, user_name: Optional[str] = None) -> None:
        """Initialize the class."""
        self.auth = Auth.Token(settings.github_pat)
        self.git = Github(auth=self.auth)

        self.repo_name: str = repo_name
        self.user: Optional[str] = user_name

        self.repo_data: Repository
        self.repo_releases: PaginatedList[GitRelease]
        self.repo_prs: PaginatedList[PullRequest]
        self.repo_issues: PaginatedList[Issue]
        self.release_data: List[Tuple[int, float, str, str]]
        self.pr_by_date: Dict[float, PullRequest]
        self.filtered_repo_issues: List[Issue]

    def run(self) -> None:
        """Run the changelog.

        Each individual step is a method that will be called in order, and
        contains it's own error handling.
        """
        header()
        self.repo_data = self.get_repo_data()
        self.repo_releases = self.get_repo_releases()
        self.repo_prs = self.get_closed_prs()
        self.repo_issues = self.get_closed_issues()
        # filter out PRs from actual issues (PR's are issues too but
        # we don't want them in the list).
        self.filtered_repo_issues = self.filter_issues()

        self.release_data = self.extract_release_data()
        self.pr_by_date = self.extract_pr_by_date()

        print(self.filtered_repo_issues)
        print(self.release_data)
        print(self.pr_by_date)

    def extract_pr_by_date(self) -> Dict[float, PullRequest]:
        """Extract PRs by date into a dictionary.

        This will enable much faster lookup of PRs by date
        """
        print("  [green]->[/green] Extracting PRs by date ... ", end="")
        pr_by_date = {
            time.mktime(pr.merged_at.timetuple()): pr
            for pr in self.repo_prs
            if pr.merged_at
        }
        print(self.done_str)
        return pr_by_date

    def extract_release_data(self) -> List[Tuple[int, float, str, str]]:
        """Extract creation dates and more for each Release.

        return a list of tuples
        """
        print("\n  [green]->[/green] Extracting Release data ... ", end="")
        release_data = []
        for release in self.repo_releases:
            release_data.append(
                (
                    release.id,
                    time.mktime(release.created_at.timetuple()),
                    release.title,
                    release.tag_name,
                )
            )
        print(self.done_str)
        return release_data

    def filter_issues(self) -> List[Issue]:
        """Filter out non-merged PRs and actual issues."""
        print("\n  [green]->[/green] Filtering Issues from PRs... ", end="")
        filtered_repo_issues = [
            issue for issue in self.repo_issues if not issue.pull_request
        ]
        print(self.done_str)

        print(
            f"  [green]->[/green] Found [green]"
            f"{len(filtered_repo_issues)}"
            "[/green] Actual Closed Issues"
        )
        return filtered_repo_issues

    def get_closed_issues(self) -> PaginatedList[Issue]:  # type: ignore
        """Get info on all the closed issues from GitHub."""
        print("  [green]->[/green] Getting Closed Issues ... ", end="")
        try:
            repo_issues = self.repo_data.get_issues(
                state="closed", sort="created"
            )
        except GithubException as exc:
            git_error(exc)
        else:
            print(f"[green]{repo_issues.totalCount} Found[/green]")
            return repo_issues

    def get_closed_prs(self) -> PaginatedList[PullRequest]:  # type: ignore
        """Get info on all the closed PRs from GitHub."""
        print("  [green]->[/green] Getting Closed PRs ... ", end="")
        try:
            repo_prs = self.repo_data.get_pulls(state="closed", sort="created")
        except GithubException as exc:
            git_error(exc)
        else:
            print(f"[green]{repo_prs.totalCount} Found[/green]")
            return repo_prs

    def get_repo_releases(self) -> PaginatedList[GitRelease]:  # type: ignore
        """Get info on all the releases from GitHub."""
        print("  [green]->[/green] Getting Releases ... ", end="")
        try:
            repo_releases = self.repo_data.get_releases()
        except GithubException as exc:
            git_error(exc)
        else:
            print(f"[green]{repo_releases.totalCount} Found[/green]")
            return repo_releases

    def get_repo_data(self) -> Repository:  # type: ignore
        """Read the repository data from GitHub."""
        print("  [green]->[/green] Getting Repository data ... ", end="")
        try:
            repo_user = self.user if self.user else self.git.get_user().login

            repo_data = self.git.get_user(repo_user).get_repo(self.repo_name)
        except GithubException as exc:
            git_error(exc)
        else:
            print(self.done_str)
            print(
                "  [green]->[/green] Repository : "
                f"[bold]{repo_data.full_name}[/bold]"
            )
            return repo_data
