"""Define the Changelog class.

This will encapsulate the logic for generating the changelog.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Literal, Optional, Union

import typer  # pylint: disable=redefined-builtin
from github import Auth, Github, GithubException
from github.GitRelease import GitRelease
from rich import print

from github_changelog_md.config import settings
from github_changelog_md.constants import SECTIONS, ExitErrors
from github_changelog_md.helpers import header

if TYPE_CHECKING:
    from io import TextIOWrapper

    from github.Commit import Commit
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
        self.unreleased: List[PullRequest]

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
            prev_release: Union[GitRelease, Literal["HEAD"], None] = None

            if len(self.unreleased) > 0:
                f.write(
                    f"## [Unreleased]({self.repo_data.html_url}"
                    "/tree/HEAD)\n\n"
                )
                self.print_prs(f, self.unreleased)
                prev_release = "HEAD"

            for release in self.repo_releases:
                self.process_release(f, prev_release, release)
                prev_release = release

        print(self.done_str)
        print(
            f"\n  [green]->[/green] Changelog generated to "
            f"[bold]{Path.cwd() / 'CHANGELOG.md'}[/bold]\n"
        )

    def process_release(self, f, prev_release, release):
        """Process a single release."""
        if prev_release:
            self.generate_diff_url(f, prev_release, release)
        f.write(
            f"## [{release.tag_name}]({release.html_url}) "
            f"({release.created_at.date()})\n\n"
        )
        if release.title != release.tag_name and release.title:
            f.write(f"### {release.title}\n\n")
        pr_list: List[PullRequest] = self.pr_by_release.get(release.id, [])
        if len(pr_list) > 0:
            self.print_prs(f, pr_list)
        else:
            # first remove any existing diff links so we can add our
            # own. The auto-generated release notes on GitHub will
            # add a diff link to the release notes. We don't want that.
            body_lines = release.body.split("\n")
            for i, line in enumerate(body_lines):
                if f"{self.repo_data.html_url}/compare/" in line:
                    body_lines.pop(i)
                    break
            body = "\n".join(body_lines)
            if body[-2] != "\n":
                body += "\n"
            f.write(body)

    def generate_diff_url(
        self,
        f,
        prev_release: Union[GitRelease, str],
        release_tag: GitRelease,
    ) -> None:
        """Generate a GitHub 3-dots link to the diff between two releases."""
        if isinstance(prev_release, GitRelease):
            prev_release = prev_release.tag_name
        f.write(
            f"[`Full Changelog`]"
            f"({self.repo_data.html_url}/compare/"
            f"{release_tag.tag_name}...{prev_release})\n\n"
        )

    def print_prs(self, f: TextIOWrapper, pr_list: List[PullRequest]) -> None:
        """Print all the PRs for a given release.

        They are sorted into sections depending on the labels they have.
        """
        release_sections = {
            heading: [
                pr
                for pr in pr_list
                if label in [label.name for label in pr.labels]
            ]
            for heading, label in SECTIONS
        }

        # default section for PRs that don't have any of the specific labels we
        # have defined for section headings. This may be able to be merged with
        # the above dict comprehension?
        release_sections["Merged Pull Requests"] = [
            pr
            for pr in pr_list
            if not any(
                label in [label.name for label in pr.labels]
                for _, label in SECTIONS
            )
        ]

        for heading, prs in release_sections.items():
            if len(prs) > 0:
                f.write(f"### {heading}\n\n")
                for pr in prs[::-1]:
                    f.write(
                        f"- {pr.title}\n"
                        f"([#{pr.number}]({pr.html_url}))\n"
                        f"by [{pr.user.login}]({pr.user.html_url})\n"
                    )
                f.write("\n")

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
        # Add any pull request more recent than the last release to a specific
        # list. We need some special handling if there are no releases yet.
        try:
            last_release_date = self.repo_releases[-1].created_at
        except IndexError:
            # there have been no releases yet, so we need to get the date of
            # the first commit.
            first_commit: Commit = self.repo_data.get_commits().reversed[0]
            last_release_date = first_commit.commit.committer.date

        self.unreleased = [
            pr
            for pr in self.repo_prs
            if pr.merged_at
            and pr.merged_at > last_release_date
            and not any(pr in pr_list for pr_list in pr_by_release.values())
        ]
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
            return repo_data
