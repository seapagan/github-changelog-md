"""Define the Changelog class.

This will encapsulate the logic for generating the changelog.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import typer  # pylint: disable=redefined-builtin
from github import Auth, Github, GithubException
from rich import print

from github_changelog_md.config import settings
from github_changelog_md.constants import ExitErrors
from github_changelog_md.helpers import header

if TYPE_CHECKING:
    from github.PaginatedList import PaginatedList
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

    def __init__(self, repo_name: str, user_name: Optional[str] = None) -> None:
        """Initialize the class."""
        self.auth = Auth.Token(settings.github_pat)
        self.git = Github(auth=self.auth)

        self.repo_name = repo_name
        self.user = user_name

        self.repo_data: Repository
        self.repo_releases: PaginatedList
        self.repo_prs: PaginatedList

    def run(self) -> None:
        """Run the changelog.

        Each individual step is a method that will be called in order, and
        contains it's own error handling.
        """
        header()
        # read the repository data
        self.get_repo_data()
        # get all the releases
        self.get_repo_releases()
        # get all closed PRs
        self.get_closed_prs()

        for pr in self.repo_prs:
            if pr.merged_at:
                print(pr.title, [label.name for label in pr.labels])

    def get_closed_prs(self):
        """Get info on all the closed PRs from GitHub."""
        print("  [green]->[/green] Getting Closed PRs ... ", end="")
        try:
            self.repo_prs = self.repo_data.get_pulls(
                state="closed", sort="created"
            )
        except GithubException as exc:
            git_error(exc)
        else:
            print(f"[green]{self.repo_prs.totalCount} Found[/green]")

    def get_repo_releases(self):
        """Get info on all the releases from GitHub."""
        print("  [green]->[/green] Getting Releases ... ", end="")
        try:
            self.repo_releases = self.repo_data.get_releases()
        except GithubException as exc:
            git_error(exc)
        else:
            print(f"[green]{self.repo_releases.totalCount} Found[/green]")

    def get_repo_data(self):
        """Read the repository data from GitHub."""
        print("  [green]->[/green] Getting Repository data ... ", end="")
        try:
            repo_user = self.user if self.user else self.git.get_user().login

            self.repo_data = self.git.get_user(repo_user).get_repo(
                self.repo_name
            )
        except GithubException as exc:
            git_error(exc)
        else:
            print("[green]Done[/green]")
            print(
                "  [green]->[/green] Repository : "
                f"[bold]{self.repo_data.full_name}[/bold]"
            )
