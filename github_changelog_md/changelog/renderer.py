"""Markdown rendering for changelog generation."""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from io import StringIO
from typing import TYPE_CHECKING, Any, Literal

from github_changelog_md.changelog.models import (
    ChangelogIssue,
    ChangelogPullRequest,
    ChangelogRelease,
    ChangelogRepository,
)
from github_changelog_md.helpers import (
    cap_first_letter,
    get_section_name,
    title_unique,
)

if TYPE_CHECKING:  # pragma: no cover
    from io import TextIOWrapper

    from github_changelog_md.changelog.changelog import ReleaseTextCache
    from github_changelog_md.config.settings import Settings
    from github_changelog_md.constants import ChangelogOptions, SectionHeadings

Release = ChangelogRelease
PullRequestItem = ChangelogPullRequest
IssueItem = ChangelogIssue


@dataclass(slots=True)
class ChangelogRenderer:
    """Render changelog data to Markdown."""

    repo_data: ChangelogRepository
    repo_releases: list[Release]
    pr_by_release: dict[int, list[PullRequestItem]]
    issue_by_release: dict[int, list[IssueItem]]
    unreleased: list[PullRequestItem]
    unreleased_issues: list[IssueItem]
    release_text_cache: ReleaseTextCache
    options: ChangelogOptions
    settings: Settings
    sections: list[SectionHeadings]
    ignored_labels: list[str]
    prev_release: Release | Literal["HEAD"] | None = None

    def render(self) -> str:
        """Render the complete changelog Markdown."""
        output = StringIO()
        output.write("# Changelog\n\n")

        if self.settings.intro_text:
            output.write(f"{self.settings.intro_text}\n\n")

        if not self.options["show_depends"]:
            output.write(
                "*Dependency updates are excluded from this changelog, "
                "check each `Full Changelog` for details.*\n\n "
            )

        self.prev_release = None

        if self.options["show_unreleased"]:
            self.process_unreleased(output)

        for release in self.repo_releases:
            self.process_release(output, release)
            self.prev_release = release

        output.write(
            "---\n"
            "*This changelog was generated using "
            "[github-changelog-md](http://changelog.seapagan.net/) "
            "by [Seapagan](https://github.com/seapagan)*\n",
        )
        return output.getvalue()

    def process_unreleased(self, output: TextIOWrapper | StringIO) -> None:
        """Process the unreleased PRs and Issues into the changelog."""
        if self.unreleased or self.unreleased_issues:
            heading = self.options["next_release"] or "Unreleased"
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
                else f"releases/tag/{self.options['next_release']}"
            )
            output.write(
                f"## [{heading}]({self.repo_data.html_url}/{release_link})"
                f"{release_date}\n\n",
            )

            self.show_release_text(
                output,
                self.options["next_release"] or "unreleased",
            )

            self.rprint_issues(output, self.unreleased_issues)
            self.rprint_prs(output, self.unreleased)

            self.prev_release = "HEAD"

    def process_release(
        self,
        output: TextIOWrapper | StringIO,
        release: Release,
    ) -> None:
        """Process a single release."""
        if (
            self.options["skip_releases"]
            and release.tag_name.strip() in self.options["skip_releases"]
        ):
            return
        if self.prev_release:
            self.generate_diff_url(output, self.prev_release, release)

        self.show_before_text(output, release)

        text_date = release.created_at.date().strftime(
            self.settings.date_format
        )
        output.write(
            f"## [{release.tag_name}]({release.html_url}) ({text_date})",
        )
        self.check_yanked(output, release)

        output.write("\n\n")

        if title_unique(release):
            output.write(f"**_{cap_first_letter(release.title.strip())}_**\n\n")

        pr_list: list[PullRequestItem] = self.pr_by_release.get(release.id, [])
        issue_list: list[IssueItem] = self.issue_by_release.get(release.id, [])

        self.show_release_text(output, release)

        if (
            release.tag_name
            in self.release_text_cache.release_overrides_by_release
        ):
            output.write(
                self.release_text_cache.release_overrides_by_release[
                    release.tag_name
                ]
            )
            output.write("\n")
            return

        self.rprint_issues(output, issue_list)
        self.rprint_prs(output, pr_list)

        if not issue_list and not pr_list:
            self.get_release_body(output, release)

    def check_yanked(
        self, output: TextIOWrapper | StringIO, release: Release
    ) -> None:
        """Note if this release has been yanked, and the reason why."""
        if release.tag_name in self.release_text_cache.yanked_by_release:
            output.write(" **[`YANKED`]**\n\n")
            output.write(
                "**This release has been removed for the following reason and "
                "should not be used:**\n\n"
                f"- "
                f"{self.release_text_cache.yanked_by_release[release.tag_name]}"
            )

    def show_before_text(
        self, output: TextIOWrapper | StringIO, release: Release
    ) -> None:
        """Shows text before this release if it exists."""
        if (
            release.tag_name
            in self.release_text_cache.release_text_before_by_release
        ):
            output.write("---\n\n")
            output.write(
                self.release_text_cache.release_text_before_by_release[
                    release.tag_name
                ]
            )
            output.write("\n\n---\n\n")

    def show_release_text(
        self,
        output: TextIOWrapper | StringIO,
        release: str | Release,
    ) -> None:
        """Print the release_text if it exists."""
        tag_name = release if isinstance(release, str) else release.tag_name

        if tag_name in self.release_text_cache.release_text_by_release:
            output.write(
                self.release_text_cache.release_text_by_release[tag_name]
            )
            output.write("\n\n")

    def get_release_body(
        self,
        output: TextIOWrapper | StringIO,
        release: Release,
    ) -> None:
        """Render fallback release body text."""
        if release.body:
            body_lines = release.body.split("\n")
            for i, line in enumerate(body_lines):
                if f"{self.repo_data.html_url}/compare/" in line:
                    body_lines.pop(i)
                    break
            body = "\n".join(body_lines)
            if body.strip() and not body.endswith("\n"):
                body += "\n"
            output.write(body)
        else:
            output.write(
                "There were no merged pull requests or closed issues "
                "for this release.\n\n"
                "See the Full Changelog below for details.\n\n"
            )

    def rprint_issues(
        self,
        output: TextIOWrapper | StringIO,
        issue_list: list[IssueItem],
    ) -> None:
        """Print all the closed issues for a given release."""
        visible_issues = self.ignore_items(list(issue_list))
        if not visible_issues or not self.options["show_issues"]:
            return

        output.write("**Closed Issues**\n\n")
        for issue in self.get_sorted_items(visible_issues):
            if any(
                label.name.lower() in self.ignored_labels
                for label in issue.labels
            ):
                continue
            escaped_title = cap_first_letter(
                issue.title.replace("__", "\\_\\_").strip(),
            )
            try:
                output.write(
                    f"- {escaped_title} "
                    f"([#{issue.number}]({issue.html_url})) "
                    f"by [{issue.closed_by.login}]"
                    f"({issue.closed_by.html_url})\n",
                )
            except AttributeError:
                output.write(
                    f"- {escaped_title} ([#{issue.number}]({issue.html_url}))\n"
                )
        output.write("\n")

    def generate_diff_url(
        self,
        output: TextIOWrapper | StringIO,
        prev_release: Release | str,
        release_tag: Release,
    ) -> None:
        """Generate a GitHub 3-dots link to the diff between two releases."""
        if not isinstance(prev_release, str):
            prev_release = prev_release.tag_name
        elif self.options["next_release"]:
            prev_release = self.options["next_release"]
        output.write(
            f"[`Full Changelog`]"
            f"({self.repo_data.html_url}/compare/"
            f"{release_tag.tag_name}...{prev_release})",
        )
        if self.options["show_diff"]:
            output.write(
                f" | [`Diff`]({self.repo_data.html_url}/compare/"
                f"{release_tag.tag_name}...{prev_release}.diff)",
            )
        if self.options["show_patch"]:
            output.write(
                f" | [`Patch`]({self.repo_data.html_url}/compare/"
                f"{release_tag.tag_name}...{prev_release}.patch)",
            )
        output.write("\n\n")

    def rprint_prs(
        self,
        output: TextIOWrapper | StringIO,
        pr_list: list[PullRequestItem],
    ) -> None:
        """Print all the PRs for a given release."""
        if not pr_list:
            return

        release_sections = self.get_release_sections(pr_list)
        merged_section_title = next(
            (section[0] for section in self.sections if section[1] is None),
            "Merged Pull Requests",
        )
        release_sections[merged_section_title] = [
            pr
            for pr in pr_list
            if not any(
                section_label
                in [pr_label.name.lower() for pr_label in pr.labels]
                for _, section_label in self.sections
            )
            and not any(
                pr_label.name.lower() in self.ignored_labels
                for pr_label in pr.labels
            )
        ]

        for heading, prs in release_sections.items():
            is_dependencies = heading == get_section_name("dependencies")
            if is_dependencies and not self.options["show_depends"]:
                continue

            visible_prs = self.ignore_items(list(prs))

            if visible_prs:
                output.write(f"**{heading}**\n\n")
                sorted_prs = self.get_sorted_items(visible_prs)
                display_prs = (
                    sorted_prs[: self.options["max_depends"]]
                    if is_dependencies
                    else sorted_prs
                )
                for pr in display_prs:
                    escaped_title = cap_first_letter(
                        pr.title.replace("__", "\\_\\_").strip(),
                    )
                    output.write(
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
                    output.write(
                        f"- *and {hidden_updates} more dependency updates*\n",
                    )
                output.write("\n")

    def ignore_items(
        self, items: list[PullRequestItem | IssueItem]
    ) -> list[PullRequestItem | IssueItem]:
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
        return items

    def get_release_sections(
        self, pr_list: list[PullRequestItem]
    ) -> dict[str, list[PullRequestItem]]:
        """Return a dictionary of PRs sorted into sections."""
        return {
            heading: [
                pr
                for pr in pr_list
                if section_label
                in [pr_label.name.lower() for pr_label in pr.labels]
                and not any(
                    pr_label.name.lower() in self.ignored_labels
                    for pr_label in pr.labels
                )
            ]
            for heading, section_label in self.sections
        }
