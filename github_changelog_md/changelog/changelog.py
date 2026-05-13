"""Define the Changelog class.

This will encapsulate the logic for generating the changelog.
"""

from __future__ import annotations

import contextlib
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, TypeAlias

import typer
from rich import print as rprint

from github_changelog_md.changelog.bucketing import (
    bucket_issues,
    bucket_pull_requests,
    get_unreleased_cutoff,
)
from github_changelog_md.changelog.models import (
    ChangelogIssue,
    ChangelogPullRequest,
    ChangelogRelease,
    ChangelogRepository,
    ChangelogUser,
)
from github_changelog_md.changelog.renderer import ChangelogRenderer
from github_changelog_md.constants import (
    CONTRIBUTORS_FILE,
    IGNORED_CONTRIBUTORS,
    IGNORED_LABELS,
    SECTIONS,
    ChangelogOptions,
    ExitErrors,
    SectionHeadings,
)
from github_changelog_md.helpers import (
    get_index_of_tuple,
    header,
)

if TYPE_CHECKING:  # pragma: no cover
    import datetime
    from io import TextIOWrapper

    from github_changelog_md.changelog.github_data import GitHubDataSource
    from github_changelog_md.config.settings import Settings

Release: TypeAlias = ChangelogRelease
PullRequestItem: TypeAlias = ChangelogPullRequest
IssueItem: TypeAlias = ChangelogIssue


@dataclass
class ReleaseTextCache:
    """Cache release-text settings keyed by release tag."""

    yanked_by_release: dict[str, str] = field(default_factory=dict)
    release_text_before_by_release: dict[str, str] = field(default_factory=dict)
    release_text_by_release: dict[str, str] = field(default_factory=dict)
    release_overrides_by_release: dict[str, str] = field(default_factory=dict)


class ChangeLog:
    """Define the Changelog class."""

    done_str = "[green]Done[/green]"

    def __init__(
        self,
        repo_name: str,
        options: ChangelogOptions,
        settings: Settings,
        data_source: GitHubDataSource,
    ) -> None:
        """Initialize the class."""
        self.settings = settings
        self.data_source = data_source
        self.repo_name: str = repo_name
        self.user: str | None = options["user_name"]
        self.options = options

        self.sections: list[SectionHeadings]
        self.ignored_labels: list[str]

        self.repo_data: ChangelogRepository
        self.repo_releases: list[Release]
        self.repo_prs: list[PullRequestItem]
        self.repo_issues: list[IssueItem]
        self.pr_by_release: dict[int, list[PullRequestItem]]
        self.issue_by_release: dict[int, list[IssueItem]]
        self.prev_release: Release | Literal["HEAD"] | None = None
        self.filtered_repo_issues: list[IssueItem]
        self.unreleased: list[PullRequestItem]
        self.unreleased_issues: list[IssueItem]
        self.contributors: list[ChangelogUser]
        self.release_text_cache = ReleaseTextCache(
            yanked_by_release=self.build_release_lookup(
                self.settings.yanked,
                value_key="reason",
            ),
            release_text_before_by_release=self.build_release_lookup(
                self.settings.release_text_before,
                value_key="text",
                strip_value=True,
            ),
            release_text_by_release=self.build_release_lookup(
                self.settings.release_text,
                value_key="text",
                strip_value=True,
            ),
            release_overrides_by_release=self.build_release_lookup(
                self.settings.release_overrides,
                value_key="text",
            ),
        )

    @staticmethod
    def build_release_lookup(
        values: list[dict[str, str]] | None,
        value_key: str,
        *,
        strip_value: bool = False,
    ) -> dict[str, str]:
        """Build a release-tag keyed lookup table for fast text lookups."""
        if not values:
            return {}

        lookup: dict[str, str] = {}
        for value in values:
            release = value["release"].strip()
            text = value[value_key].strip() if strip_value else value[value_key]
            lookup[release] = text

        return lookup

    def run(self) -> None:
        """Run the changelog.

        Each individual step is a method that will be called in order, and
        contains it's own error handling.
        """
        with contextlib.ExitStack() as stack:
            if self.options["quiet"]:
                devnull = stack.enter_context(Path(os.devnull).open("w"))
                stack.enter_context(contextlib.redirect_stdout(devnull))

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
            rprint(
                f"[red]  X  Error: Section '[bold]{rename[0]}[/bold]' not "
                "found \\[[reverse]rename_sections[/reverse]]\n",
                file=sys.stderr,
            )
            raise typer.Exit(ExitErrors.INVALID_ACTION) from None

        return sections

    def extend_sections(self) -> list[SectionHeadings]:
        """Extend the default sections with any user defined ones."""
        if not self.settings.extend_sections:
            return list(SECTIONS)

        extend_sections = [
            (section["title"], section["label"])
            for section in self.settings.extend_sections
        ]

        insert_index = (
            self.settings.extend_sections_index
            or get_index_of_tuple(SECTIONS, 1, "dependencies")
        )

        return (
            SECTIONS[:insert_index] + extend_sections + SECTIONS[insert_index:]
        )

    def get_contributors(self) -> list[ChangelogUser]:
        """This will get all the contributors to the repo.

        It will return a list of NamedUser objects, getting these from the list
        of PRs and Issues, removing any duplicates
        """
        user_list: list[ChangelogUser] = []
        rprint("  [green]->[/green] Getting Contributors ... ", end="")
        for pr in self.repo_prs:
            if pr.user not in user_list:
                user_list.append(pr.user)
        rprint(self.done_str)

        rprint("  [green]->[/green] Sorting Contributors ... ", end="")
        user_list.sort(key=lambda x: x.name or x.login)
        rprint(self.done_str)

        return user_list

    def update_contributors(self) -> None:
        """Update the CONTRIBUTORS.md file."""
        rprint("  [green]->[/green] Updating CONTRIBUTORS.md ... ", end="")
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
                name = contributor.name or contributor.login
                f.write(
                    f"- {name} "
                    f"([@{contributor.login}]({contributor.html_url}))\n",
                )
        rprint(self.done_str, "\n")

    def generate_changelog(self) -> None:
        """Generate a markdown changelog using the data we have gererated."""
        if self.options["skip_releases"]:
            rprint(
                "\n  [green]->[/green] Skipping releases: "
                f"{', '.join(self.options['skip_releases'])}",
            )

        rprint("  [green]->[/green] Generating Changelog ... ", end="")

        rendered_changelog = self._renderer().render()
        with Path(Path.cwd() / self.options["output_file"]).open(
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write(rendered_changelog)

        rprint(self.done_str)
        rprint(
            f"  [green]->[/green] Changelog generated to "
            f"[bold]{Path.cwd() / self.options['output_file']}[/bold]\n",
        )

    def _renderer(self) -> ChangelogRenderer:
        """Create the Markdown renderer for the current changelog data."""
        return ChangelogRenderer(
            repo_data=getattr(
                self,
                "repo_data",
                ChangelogRepository(
                    name=self.repo_name,
                    full_name=self.repo_name,
                    html_url="",
                ),
            ),
            repo_releases=getattr(self, "repo_releases", []),
            pr_by_release=getattr(self, "pr_by_release", {}),
            issue_by_release=getattr(self, "issue_by_release", {}),
            unreleased=getattr(self, "unreleased", []),
            unreleased_issues=getattr(self, "unreleased_issues", []),
            release_text_cache=self.release_text_cache,
            options=self.options,
            settings=self.settings,
            sections=getattr(self, "sections", SECTIONS),
            ignored_labels=getattr(self, "ignored_labels", []),
            prev_release=self.prev_release,
        )

    def process_unreleased(
        self,
        f: TextIOWrapper,
    ) -> None:
        """Process the unreleased PRs and Issues into the changelog."""
        renderer = self._renderer()
        renderer.process_unreleased(f)
        self.prev_release = renderer.prev_release

    def process_release(
        self,
        f: TextIOWrapper,
        release: Release,
    ) -> None:
        """Process a single release."""
        self._renderer().process_release(f, release)

    def check_yanked(self, f: TextIOWrapper, release: Release) -> None:
        """Note if this release has been yanked, and the reason why."""
        self._renderer().check_yanked(f, release)

    def show_before_text(self, f: TextIOWrapper, release: Release) -> None:
        """Shows text before this release if it exists."""
        self._renderer().show_before_text(f, release)

    def show_release_text(
        self,
        f: TextIOWrapper,
        release: str | Release,
    ) -> None:
        """Print the release_text if it exists."""
        self._renderer().show_release_text(f, release)

    def get_release_body(
        self,
        f: TextIOWrapper,
        release: Release,
    ) -> None:
        """Read the GitHub release body."""
        self._renderer().get_release_body(f, release)

    def rprint_issues(
        self,
        f: TextIOWrapper,
        issue_list: list[IssueItem],
    ) -> None:
        """Print all the closed issues for a given release."""
        self._renderer().rprint_issues(f, issue_list)

    def generate_diff_url(
        self,
        f: TextIOWrapper,
        prev_release: Release | str,
        release_tag: Release,
    ) -> None:
        """Generate a GitHub 3-dots link to the diff between two releases."""
        self._renderer().generate_diff_url(f, prev_release, release_tag)

    def rprint_prs(
        self,
        f: TextIOWrapper,
        pr_list: list[PullRequestItem],
    ) -> None:
        """Print all the PRs for a given release."""
        self._renderer().rprint_prs(f, pr_list)

    def ignore_items(
        self, items: list[PullRequestItem | IssueItem]
    ) -> list[PullRequestItem | IssueItem]:
        """Ignore any PRs or Issues that have been marked as hidden."""
        return self._renderer().ignore_items(items)

    def get_sorted_items(self, items: list[Any]) -> list[Any]:
        """Sort the PRs or Issues into the required order."""
        return self._renderer().get_sorted_items(items)

    def get_release_sections(
        self, pr_list: list[PullRequestItem]
    ) -> dict[str, list[PullRequestItem]]:
        """Return a dictionary of PRs sorted into sections.

        This handles the PRs that have a label, we handle the PRs that don't
        have a label separately.
        """
        return self._renderer().get_release_sections(pr_list)

    def link_issues(self) -> dict[int, list[IssueItem]]:
        """Link Issues to their respective Release.

        This will create a dictionary with the key on the release id and
        the value a list of issues.
        """
        rprint(
            "  [green]->[/green] Linking Closed Issues to their respective "
            "Release ... ",
            end="",
        )
        issue_by_release: dict[int, list[IssueItem]] = {}
        unreleased_cutoff = self.get_unreleased_cutoff()
        bucketed = bucket_issues(
            self.repo_releases,
            self.filtered_repo_issues,
            unreleased_cutoff,
            self.settings.ignored_users,
        )
        issue_by_release.update(bucketed.by_release)
        self.unreleased_issues = bucketed.unreleased

        rprint(self.done_str)
        return issue_by_release

    def get_unreleased_cutoff(self) -> datetime.datetime:
        """Return the date after which items are considered unreleased."""
        if self.repo_releases:
            return get_unreleased_cutoff(
                self.repo_releases,
                self.repo_releases[0].created_at,
            )
        return self.data_source.get_first_commit_date()

    def link_pull_requests(self) -> dict[int, list[PullRequestItem]]:
        """Link Pull Requests to their respective Release.

        This will create a dictionary with the key on the release id and
        the value a list of pull requests.
        """
        rprint(
            "\n  [green]->[/green] Linking Pull Requests to their respective "
            "Release ... ",
            end="",
        )
        pr_by_release: dict[int, list[PullRequestItem]] = {}
        unreleased_cutoff = self.get_unreleased_cutoff()
        bucketed = bucket_pull_requests(
            self.repo_releases,
            self.repo_prs,
            unreleased_cutoff,
            self.settings.ignored_users,
        )
        pr_by_release.update(bucketed.by_release)
        self.unreleased = bucketed.unreleased
        rprint(self.done_str)
        return pr_by_release

    def filter_issues(self) -> list[IssueItem]:
        """Filter out non-merged PRs and actual issues."""
        rprint("\n  [green]->[/green] Filtering Issues from PRs... ", end="")
        filtered_repo_issues: list[IssueItem] = [
            issue for issue in self.repo_issues if not issue.pull_request
        ]
        rprint(self.done_str)

        rprint(
            f"  [green]->[/green] Found [green]"
            f"{len(filtered_repo_issues)}"
            "[/green] Actual Closed Issues",
        )
        return filtered_repo_issues

    def get_closed_issues(self) -> list[IssueItem]:
        """Get info on all the closed issues from GitHub."""
        return self.data_source.get_closed_issues()

    def get_closed_prs(self) -> list[PullRequestItem]:
        """Get info on all the closed PRs from GitHub."""
        return self.data_source.get_closed_prs()

    def get_repo_releases(self) -> list[Release]:
        """Get info on all the releases from GitHub."""
        return self.data_source.get_repo_releases()

    def get_repo_data(self) -> ChangelogRepository:
        """Read the repository data from GitHub."""
        return self.data_source.get_repo_data(self.repo_name, self.user)
