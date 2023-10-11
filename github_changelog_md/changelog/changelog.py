"""Define the Changelog class.

This will encapsulate the logic for generating the changelog.
"""

import typer  # pylint: disable=redefined-builtin
from github import Auth, Github, GithubException
from rich import print

from github_changelog_md.config import settings
from github_changelog_md.constants import ExitErrors
from github_changelog_md.helpers import header


def git_error(exc: GithubException) -> None:
    """Handle a Git Exception."""
    print(
        f"\n[red]  X  Error {exc.status} while getting the "
        f"Repo : {exc.data.get('message')}\n"
    )
    raise typer.Exit(ExitErrors.GIT_ERROR)


class ChangeLog:
    """Define the Changelog class."""

    def __init__(self, repo) -> None:
        """Initialize the class."""
        self.auth = Auth.Token(settings.github_pat)
        self.git = Github(auth=self.auth)

        self.repo = repo

    def run(self) -> None:
        """Run the changelog."""
        header()
        print("  [green]->[/green] Getting Repository data ... ", end="")

        try:
            repo = self.git.get_user().get_repo(self.repo)
        except GithubException as exc:
            git_error(exc)
        else:
            print("[green]Done[/green]")
            print(
                "  [green]->[/green] Repository : "
                f"[bold]{repo.full_name}[/bold]"
            )
