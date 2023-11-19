"""Define the Changelog class.

This will encapsulate the logic for generating the changelog.
"""
# mypy: disable-error-code="no-untyped-def"
from __future__ import annotations

import datetime
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

import typer
from github import Auth, Github, GithubException
from github.GitRelease import GitRelease
from rich import print  # pylint: disable=redefined-builtin

from github_changelog_md.config import get_settings
from github_changelog_md.constants import (
    CONTRIBUTORS_FILE,
    IGNORED_CONTRIBUTORS,
    IGNORED_LABELS,
    SECTIONS,
    ExitErrors,
    SectionHeadings,
)
from github_changelog_md.helpers import (
    cap_first_letter,
    get_index_of_tuple,
    get_section_name,
    header,
)

if TYPE_CHECKING:
    from io import TextIOWrapper

    from github.Commit import Commit
    from github.Issue import Issue
    from github.NamedUser import NamedUser
    from github.PaginatedList import PaginatedList
    from github.PullRequest import PullRequest
    from github.Repository import Repository


def git_error(exc: GithubException) -> None:
    """Handle a Git Exception."""
    print(
        f"\n[red]  X  Error {exc.status} while getting the "
        f"Repo : {exc.data.get('message')}\n",
        file=sys.stderr,
    )
    raise typer.Exit(ExitErrors.GIT_ERROR)


class ChangeLog:
    """Define the Changelog class."""

    done_str = "[green]Done[/green]"

    def __init__(
        self,
        repo_name: str,
        options: dict[str, Any],
    ) -> None:
        """Initialize the class."""
        try:
            self.auth = Auth.Token(get_settings().github_pat)
            self.git = Github(auth=self.auth)
        except AttributeError as exc:
            print(
                "\n[red]  X  Error: No GitHub PAT found in settings file\n",
                file=sys.stderr,
            )
            raise typer.Exit(ExitErrors.NO_PAT) from exc

        self.repo_name: str = repo_name
        self.user: str | None = options["user_name"]
        self.options = options
        self.settings = get_settings()

        self.sections: list[SectionHeadings]
        self.ignored_labels: list[str]

        self.repo_data: Repository
        self.repo_releases: list[GitRelease]
        self.repo_prs: PaginatedList[PullRequest]
        self.repo_issues: PaginatedList[Issue]
        self.pr_by_release: dict[int, list[PullRequest]]
        self.issue_by_release: dict[int, list[Issue]]
        self.filtered_repo_issues: list[Issue]
        self.unreleased: list[PullRequest]
        self.unreleased_issues: list[Issue]
        self.contributors: list[NamedUser]

    def run(self) -> None:
        """Run the changelog.

        Each individual step is a method that will be called in order, and
        contains it's own error handling.
        """
        if self.options["quiet"]:
            orig_stdout = sys.stdout
            out = open(os.devnull, "w")  # noqa: SIM115, PTH123
            sys.stdout = out

        header()

        self.sections = self.rename_sections(self.extend_sections())
        self.ignored_labels = self.flatten_ignores()

        self.repo_data = self.get_repo_data()
        self.repo_releases = self.get_repo_releases()
        self.repo_prs = self.get_closed_prs()
        self.repo_issues = self.get_closed_issues()
        # filter out PRs from actual issues (PR's are issues too but
        # we don't want them in the list).
        self.filtered_repo_issues = self.filter_issues()

        self.pr_by_release = self.link_pull_requests()
        self.issue_by_release = self.link_issues()

        # actually generate the changelog file from all the data we have
        # collected.
        self.generate_changelog()

        # update the CONTRIBUTORS.md file if requested
        if self.options["contributors"]:
            self.contributors = self.get_contributors()
            self.update_contributors()

        if self.options["quiet"]:
            sys.stdout = orig_stdout
            out.close()

    def flatten_ignores(self) -> list[str]:
        """Process the ignored labels.

        Takes into account the assorted ways the user can define the ignored
        labels.
        """
        if not self.settings.ignored_labels:
            ignored_labels = IGNORED_LABELS
            if self.settings.extend_ignored:
                ignored_labels = IGNORED_LABELS + self.settings.extend_ignored
            if self.settings.allowed_labels:
                ignored_labels = [
                    label
                    for label in ignored_labels
                    if label not in self.settings.allowed_labels
                ]
        else:
            ignored_labels = self.settings.ignored_labels

        return ignored_labels

    def rename_sections(
        self, sections: list[SectionHeadings]
    ) -> list[SectionHeadings]:
        """Rename the default sections with any user defined ones."""
        if not self.settings.rename_sections:
            return sections

        rename_sections = [
            (section["old"], section["new"])
            for section in self.settings.rename_sections
        ]

        try:
            for rename in rename_sections:
                index = get_index_of_tuple(sections, 0, rename[0])
                sections[index] = (rename[1], sections[index][1])
        except ValueError:
            print(
                f"[red]  X  Error: Section '[bold]{rename[0]}[/bold]' not "
                "found \\[[reverse]rename_sections[/reverse]]\n",
                file=sys.stderr,
            )
            sys.exit(ExitErrors.INVALID_ACTION)

        return sections

    def extend_sections(self) -> list[SectionHeadings]:
        """Extend the default sections with any user defined ones."""
        if not self.settings.extend_sections:
            return SECTIONS

        extend_sections = [
            (section["title"], section["label"])
            for section in self.settings.extend_sections
        ]

        insert_index = (
            self.settings.extend_sections_index
            if self.settings.extend_sections_index
            else get_index_of_tuple(SECTIONS, 1, "dependencies")
        )

        return (
            SECTIONS[:insert_index] + extend_sections + SECTIONS[insert_index:]
        )

    def get_contributors(self) -> list[NamedUser]:
        """This will get all the contributors to the repo.

        It will return a list of NamedUser objects, getting these from the list
        of PRs and Issues, removing any duplicates
        """
        user_list: list[NamedUser] = []
        print("  [green]->[/green] Getting Contributors ... ", end="")
        for pr in self.repo_prs:
            if pr.user not in user_list:
                user_list.append(pr.user)
        print(self.done_str)

        print("  [green]->[/green] Sorting Contributors ... ", end="")
        user_list.sort(key=lambda x: x.name if x.name else x.login)
        print(self.done_str)

        return user_list

    def update_contributors(self) -> None:
        """Update the CONTRIBUTORS.md file."""
        print("  [green]->[/green] Updating CONTRIBUTORS.md ... ", end="")
        with Path(Path.cwd() / CONTRIBUTORS_FILE).open(
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write("# Contributors\n\n")
            f.write(
                "The following people have contributed to the development "
                f"of {self.repo_data.name}:\n\n"
            )
            for contributor in self.contributors:
                if contributor.login in IGNORED_CONTRIBUTORS:
                    continue
                name = (
                    contributor.name if contributor.name else contributor.login
                ).capitalize()
                f.write(
                    f"- {name} "
                    f"([@{contributor.login}]({contributor.html_url}))\n",
                )
        print(self.done_str, "\n")

    def generate_changelog(self) -> None:
        """Generate a markdown changelog using the data we have gererated."""
        if self.options["skip_releases"]:
            print(
                "\n  [green]->[/green] Skipping releases: "
                f"{', '.join(self.options['skip_releases'])}",
            )

        print("  [green]->[/green] Generating Changelog ... ", end="")

        with Path(Path.cwd() / self.options["output_file"]).open(
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write("# Changelog\n\n")

            if self.settings.intro_text:
                f.write(f"{self.settings.intro_text}\n\n")

            if not self.options["show_depends"]:
                f.write(
                    "*Dependency updates are excluded from this changelog, "
                    "check each `Full Changelog` for details.*\n\n "
                )

            self.prev_release: GitRelease | (Literal["HEAD"] | None) = None

            if self.options["show_unreleased"]:
                self.process_unreleased(f)

            for release in self.repo_releases:
                self.process_release(f, release)
                self.prev_release = release

            # add a link to this generator at the bottom of the changelog
            f.write(
                "---\n"
                "*This changelog was generated using "
                "[github-changelog-md](http://changelog.seapagan.net/) "
                "by [Seapagan](https://github.com/seapagan)*\n",
            )

        print(self.done_str)
        print(
            f"  [green]->[/green] Changelog generated to "
            f"[bold]{Path.cwd() / self.options['output_file']}[/bold]\n",
        )

    def process_unreleased(
        self,
        f: TextIOWrapper,
    ) -> None:
        """Process the unreleased PRs and Issues into the changelog."""
        if len(self.unreleased) > 0 or len(self.unreleased_issues) > 0:
            heading = (
                self.options["next_release"]
                if self.options["next_release"]
                else "Unreleased"
            )
            text_date = (
                datetime.datetime.now(tz=datetime.timezone.utc)
                .date()
                .strftime(self.settings.date_format)
            )
            release_date = (
                f" ({text_date})" if self.options["next_release"] else ""
            )
            release_link = (
                "tree/HEAD"
                if not self.options["next_release"]
                else f'releases/tag/{self.options["next_release"]}'
            )
            f.write(
                f"## [{heading}]({self.repo_data.html_url}/{release_link})"
                f"{release_date}\n\n",
            )

            if (
                self.settings.release_text
                and not self.options["next_release"]
                and "unreleased"
                in [
                    release_text["release"].strip()
                    for release_text in self.settings.release_text
                ]
            ):
                f.write("\n")
                f.write(
                    next(
                        (
                            release_text["text"]
                            for release_text in self.settings.release_text
                            if release_text["release"].strip() == "unreleased"
                        ),
                        "",
                    )
                )
                f.write("\n\n")

            self.print_issues(f, self.unreleased_issues)
            self.print_prs(f, self.unreleased)

            self.prev_release = "HEAD"

    def process_release(
        self,
        f: TextIOWrapper,
        release: GitRelease,
    ) -> None:
        """Process a single release."""
        if (
            self.options["skip_releases"]
            and release.tag_name.strip() in self.options["skip_releases"]
        ):
            return
        if self.prev_release:
            self.generate_diff_url(f, self.prev_release, release)

        if self.settings.release_text_before and release.tag_name in [
            release_text["release"].strip()
            for release_text in self.settings.release_text_before
        ]:
            f.write("---\n\n")
            f.write(
                next(
                    (
                        release_text["text"]
                        for release_text in self.settings.release_text_before
                        if release_text["release"].strip() == release.tag_name
                    ),
                    "",
                )
            )
            f.write("\n---\n\n")

        text_date = release.created_at.date().strftime(
            self.settings.date_format
        )
        f.write(
            f"## [{release.tag_name}]({release.html_url}) ({text_date})",
        )
        if self.settings.yanked and release.tag_name in [
            yanked["release"].strip() for yanked in self.settings.yanked
        ]:
            f.write(" **[`YANKED`]**\n\n")
            reason = next(
                (
                    yanked["reason"]
                    for yanked in self.settings.yanked
                    if yanked["release"].strip() == release.tag_name
                ),
                "",
            )
            f.write(
                "**This release has been removed for the following reason and "
                "should not be used:**\n\n"
                f"- {reason}"
            )

        f.write("\n\n")
        if release.title != release.tag_name and release.title:
            f.write(f"**_'{cap_first_letter(release.title.strip())}'_**\n\n")
        pr_list: list[PullRequest] = self.pr_by_release.get(release.id, [])
        issue_list: list[Issue] = self.issue_by_release.get(release.id, [])

        if self.settings.release_text and release.tag_name in [
            release_text["release"].strip()
            for release_text in self.settings.release_text
        ]:
            f.write("\n")
            f.write(
                next(
                    (
                        release_text["text"]
                        for release_text in self.settings.release_text
                        if release_text["release"].strip() == release.tag_name
                    ),
                    "",
                )
            )
            f.write("\n\n")

        if self.settings.release_overrides and release.tag_name in [
            release_override["release"].strip()
            for release_override in self.settings.release_overrides
        ]:
            f.write(
                next(
                    (
                        release_override["text"]
                        for release_override in self.settings.release_overrides
                        if release_override["release"].strip()
                        == release.tag_name
                    ),
                    "",
                )
            )
            f.write("\n")
            return

        self.print_issues(f, issue_list)
        self.print_prs(f, pr_list)

        # if no closed releases or PR's then get the release body instead
        if len(issue_list) == 0 and len(pr_list) == 0:
            self.get_release_body(f, release)

    def get_release_body(
        self,
        f: TextIOWrapper,
        release: GitRelease,
    ) -> None:
        """Read the GitHub release body.

        first remove any existing diff links so we can add our
        own. The auto-generated release notes on GitHub will
        add a diff link to the release notes. We don't want that.
        """
        if release.body:
            body_lines = release.body.split("\n")
            for i, line in enumerate(body_lines):
                if f"{self.repo_data.html_url}/compare/" in line:
                    body_lines.pop(i)
                    break
            body = "\n".join(body_lines)
            if body.strip() and body[-2] != "\n":
                body += "\n"
            f.write(body)
        else:
            f.write(
                "There were no merged pull requests or closed issues "
                "for this release.\n\n"
                "See the Full Changelog below for details.\n\n"
            )

    def print_issues(
        self,
        f: TextIOWrapper,
        issue_list: list[Issue],
    ) -> None:
        """Print all the closed issues for a given release."""
        visible_issues = self.ignore_items(list(issue_list))
        if len(visible_issues) == 0 or not self.options["show_issues"]:
            return

        f.write("**Closed Issues**\n\n")
        for issue in self.get_sorted_items(visible_issues):
            if (
                any(
                    label.name.lower() in self.ignored_labels
                    for label in issue.labels
                )
                or "[no changelog]" in issue.title.lower()
            ):
                continue
            escaped_title = cap_first_letter(
                issue.title.replace("__", "\\_\\_").strip(),
            )
            f.write(
                f"- {escaped_title} "
                f"([#{issue.number}]({issue.html_url})) "
                f"by [{issue.user.login}]({issue.user.html_url})\n",
            )
        f.write("\n")

    def generate_diff_url(
        self,
        f: TextIOWrapper,
        prev_release: GitRelease | str,
        release_tag: GitRelease,
    ) -> None:
        """Generate a GitHub 3-dots link to the diff between two releases."""
        if isinstance(prev_release, GitRelease):
            prev_release = prev_release.tag_name
        elif self.options["next_release"]:
            prev_release = self.options["next_release"]
        f.write(
            f"[`Full Changelog`]"
            f"({self.repo_data.html_url}/compare/"
            f"{release_tag.tag_name}...{prev_release})",
        )
        if self.options["show_diff"]:
            f.write(
                f" | [`Diff`]({self.repo_data.html_url}/compare/"
                f"{release_tag.tag_name}...{prev_release}.diff)",
            )
        if self.options["show_patch"]:
            f.write(
                f" | [`Patch`]({self.repo_data.html_url}/compare/"
                f"{release_tag.tag_name}...{prev_release}.patch)",
            )
        f.write("\n\n")

    def print_prs(
        self,
        f: TextIOWrapper,
        pr_list: list[PullRequest],
    ) -> None:
        """Print all the PRs for a given release.

        They are sorted into sections depending on the labels they have.
        """
        if len(pr_list) == 0:
            return

        release_sections = self.get_release_sections(pr_list)

        # default section for PRs that don't have any of the specific labels we
        # have defined for section headings. This may be able to be merged with
        # the above dict comprehension?

        # find the new section title

        merged_section_title = next(
            (section[0] for section in self.sections if section[1] is None),
            "Merged Pull Requests",
        )
        release_sections[merged_section_title] = [
            pr
            for pr in pr_list
            if not any(
                label in [label.name.lower() for label in pr.labels]
                for _, label in self.sections
            )
            and not any(
                label in self.ignored_labels
                for label in [label.name.lower() for label in pr.labels]
            )
        ]

        for heading, prs in release_sections.items():
            is_dependencies = heading == get_section_name("dependencies")
            if is_dependencies and not self.options["show_depends"]:
                continue

            visible_prs = self.ignore_items(list(prs))

            if len(visible_prs) > 0:
                f.write(f"**{heading}**\n\n")
                sorted_prs = self.get_sorted_items(visible_prs)
                if is_dependencies:
                    # only show the max_depends number of PRs
                    visible_prs = sorted_prs[: self.options["max_depends"]]
                for pr in self.get_sorted_items(visible_prs):
                    escaped_title = cap_first_letter(
                        pr.title.replace("__", "\\_\\_").strip(),
                    )
                    f.write(
                        f"- {escaped_title} "
                        f"([#{pr.number}]({pr.html_url})) "
                        f"by [{pr.user.login}]({pr.user.html_url})\n",
                    )
                if (
                    is_dependencies
                    and len(sorted_prs) > self.options["max_depends"]
                ):
                    hidden_updates = (
                        len(sorted_prs) - self.options["max_depends"]
                    )
                    f.write(
                        f"- *and {hidden_updates} more dependency updates*\n",
                    )
                f.write("\n")

    def ignore_items(
        self, items: list[PullRequest | Issue]
    ) -> list[PullRequest | Issue]:
        """Ignore any PRs or Issues that have been marked as hidden."""
        if not self.options["ignore_items"]:
            return items
        return [
            item
            for item in items
            if item.number not in self.options["ignore_items"]
            and "[no changelog]" not in item.title.lower()
        ]

    def get_sorted_items(self, items: list[Any]) -> list[Any]:
        """Sort the PRs or Issues into the required order."""
        if self.options["item_order"] == "newest-first":
            return sorted(items, key=lambda x: x.number, reverse=True)
        if self.options["item_order"] == "oldest-first":
            return sorted(items, key=lambda x: x.number)
        # any other value will be ignored and the default order will be used
        return items

    def get_release_sections(
        self, pr_list: list[PullRequest]
    ) -> dict[str, list[PullRequest]]:
        """Return a dictionary of PRs sorted into sections.

        This handles the PRs that have a label, we handle the PRs that don't
        have a label separately.
        """
        return {
            heading: [
                pr
                for pr in pr_list
                if label in [label.name.lower() for label in pr.labels]
                and not any(
                    label in self.ignored_labels
                    for label in [label.name.lower() for label in pr.labels]
                )
            ]
            for heading, label in self.sections
        }

    def link_issues(self) -> dict[int, list[Issue]]:
        """Link Issues to their respective Release.

        This will create a dictionary with the key on the release id and
        the value a list of issues.
        """
        print(
            "  [green]->[/green] Linking Closed Issues to their respective "
            "Release ... ",
            end="",
        )
        issue_by_release: dict[int, list[Issue]] = {}
        for release in self.repo_releases[::-1]:
            issue_by_release[release.id] = []
            for issue in self.filtered_repo_issues:
                if (
                    issue.closed_at
                    and issue.closed_at <= release.created_at
                    and not any(
                        issue in issue_list
                        for issue_list in issue_by_release.values()
                    )
                    and issue.user.login not in self.settings.ignored_users
                ):
                    issue_by_release[release.id].append(issue)

        # Add any issue more recent than the last release to a specific
        # list. We need some special handling if there are no releases yet.
        last_release_date = self.get_latest_release_date()

        self.unreleased_issues = [
            issue
            for issue in self.filtered_repo_issues
            if issue.closed_at
            and issue.closed_at > last_release_date
            and not any(
                issue in pr_list for pr_list in issue_by_release.values()
            )
            and issue.user.login not in self.settings.ignored_users
        ]

        print(self.done_str)
        return issue_by_release

    def get_latest_release_date(self) -> datetime.date:
        """Return the date of the latest release."""
        try:
            last_release_date = self.repo_releases[-1].created_at
        except IndexError:
            # there have been no releases yet, so we need to get the date of
            # the first commit.
            first_commit: Commit = self.repo_data.get_commits().reversed[0]
            last_release_date = first_commit.commit.committer.date
        return last_release_date

    def link_pull_requests(self) -> dict[int, list[PullRequest]]:
        """Link Pull Requests to their respective Release.

        This will create a dictionary with the key on the release id and
        the value a list of pull requests.
        """
        print(
            "\n  [green]->[/green] Linking Pull Requests to their respective "
            "Release ... ",
            end="",
        )
        pr_by_release: dict[int, list[PullRequest]] = {}
        for release in self.repo_releases[::-1]:
            pr_by_release[release.id] = []
            for pr in self.repo_prs:
                if (
                    pr.merged_at
                    and pr.merged_at <= release.created_at
                    and not any(
                        pr in pr_list for pr_list in pr_by_release.values()
                    )
                    and pr.user.login not in self.settings.ignored_users
                ):
                    pr_by_release[release.id].append(pr)
        # Add any pull request more recent than the last release to a specific
        # list. We need some special handling if there are no releases yet.
        last_release_date = self.get_latest_release_date()

        self.unreleased = [
            pr
            for pr in self.repo_prs
            if pr.merged_at
            and pr.merged_at > last_release_date
            and not any(pr in pr_list for pr_list in pr_by_release.values())
            and pr.user.login not in self.settings.ignored_users
        ]
        print(self.done_str)
        return pr_by_release

    def filter_issues(self) -> list[Issue]:
        """Filter out non-merged PRs and actual issues."""
        print("\n  [green]->[/green] Filtering Issues from PRs... ", end="")
        filtered_repo_issues = [
            issue for issue in self.repo_issues if not issue.pull_request
        ]
        print(self.done_str)

        print(
            f"  [green]->[/green] Found [green]"
            f"{len(filtered_repo_issues)}"
            "[/green] Actual Closed Issues",
        )
        return filtered_repo_issues

    def get_closed_issues(self) -> PaginatedList[Issue]:  # type: ignore[return]
        """Get info on all the closed issues from GitHub."""
        print("  [green]->[/green] Getting Closed Issues ... ", end="")
        try:
            repo_issues = self.repo_data.get_issues(
                state="closed",
                sort="created",
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
            repo_prs = self.repo_data.get_pulls(
                state="closed", sort="created", direction="desc"
            )
        except GithubException as exc:
            git_error(exc)
        else:
            print(f"[green]{repo_prs.totalCount} Found[/green]")
            return repo_prs

    def get_repo_releases(self) -> list[GitRelease]:  # type: ignore[return]
        """Get info on all the releases from GitHub."""
        print("  [green]->[/green] Getting Releases ... ", end="")
        try:
            repo_releases = self.repo_data.get_releases()
        except GithubException as exc:
            git_error(exc)
        else:
            print(f"[green]{repo_releases.totalCount} Found[/green]")
            return list(repo_releases)

    def get_repo_data(self) -> Repository:  # type: ignore[return]
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
                f"[bold]{repo_data.full_name}[/bold]",
            )
            return repo_data
