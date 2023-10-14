"""Define the Changelog class.

This will encapsulate the logic for generating the changelog.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional

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
        self.repo_releases: List[GitRelease]
        self.repo_prs: PaginatedList[PullRequest]
        self.repo_issues: PaginatedList[Issue]
        self.pr_by_release: Dict[int, List[PullRequest]]
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

        self.pr_by_release = self.link_pull_requests()

        # actually generate the changelog file from all the data we have
        # collected.
        self.generate_changelog()

    def generate_changelog(self) -> None:
        """Generate a markdown changelog using the data we have gererated."""
        print("\n  [green]->[/green] Generating Changelog ... ", end="")

        with Path(Path.cwd() / "CHANGELOG.md").open(
            mode="w", encoding="utf-8"
        ) as f:
            f.write("# Changelog\n\n")
            for release in self.repo_releases:
                f.write(
                    f"## [{release.tag_name}]({release.html_url}) "
                    f"({release.created_at.date()})\n\n"
                )
                pr_list: List[PullRequest] = self.pr_by_release.get(
                    release.id, []
                )
                for pr in pr_list[::-1]:
                    f.write(
                        f"- {pr.title}\n"
                        f"([#{pr.number}]({pr.html_url}))\n"
                        f"by **[{pr.user.login}]({pr.user.html_url})**\n"
                    )
                f.write("\n")

        print(self.done_str)

    def link_pull_requests(self) -> Dict[int, List[PullRequest]]:
        """Link Pull Requests to their respective Release.

        This will create a dictionary with the key on the release id and
        the value a list of pull requests.
        """
        print(
            "\n  [green]->[/green] Linking Pull Requests to their respective "
            "Release ... ",
            end="",
        )
        pr_by_release: Dict[int, List[PullRequest]] = {}
        for release in self.repo_releases[::-1]:
            pr_by_release[release.id] = []
            for pr in self.repo_prs:
                if (
                    pr.merged_at
                    and pr.merged_at <= release.created_at
                    and not any(
                        pr in pr_list for pr_list in pr_by_release.values()
                    )
                ):
                    pr_by_release[release.id].append(pr)
        print(self.done_str)
        return pr_by_release

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

    def get_repo_releases(self) -> List[GitRelease]:  # type: ignore
        """Get info on all the releases from GitHub."""
        print("  [green]->[/green] Getting Releases ... ", end="")
        try:
            repo_releases = self.repo_data.get_releases()
        except GithubException as exc:
            git_error(exc)
        else:
            print(f"[green]{repo_releases.totalCount} Found[/green]")
            return list(repo_releases)

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
