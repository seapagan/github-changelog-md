"""Markdown rendering for changelog generation."""

from __future__ import annotations

import datetime
from dataclasses import dataclass
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

    def format_section_heading(self, heading: str) -> str:
        """Format a generated section heading."""
        if self.options["bold_sections"]:
            return f"**{heading}**\n\n"
        return f"### {heading}\n\n"

    def render(self) -> str:
        """Render the complete changelog Markdown."""
        output = ["# Changelog\n\n"]

        if self.settings.intro_text:
            intro_text = self.settings.intro_text.rstrip("\n")
            output.append(f"{intro_text}\n\n")

        if not self.options["show_depends"]:
            output.append(
                "*Dependency updates are excluded from this changelog, "
                "check each `Full Changelog` for details.*\n\n "
            )

        self.prev_release = None

        if self.options["show_unreleased"]:
            output.append(self.render_unreleased())

        for release in self.repo_releases:
            output.append(self.render_release(release))
            self.prev_release = release

        output.append(
            "---\n"
            "*This changelog was generated using "
            "[github-changelog-md](http://changelog.seapagan.net/) "
            "by [Seapagan](https://github.com/seapagan)*\n",
        )
        return "".join(output)

    def render_unreleased(self) -> str:
        """Process the unreleased PRs and Issues into the changelog."""
        if not self.unreleased and not self.unreleased_issues:
            return ""

        heading = self.options["next_release"] or "Unreleased"
        text_date = (
            datetime.datetime.now(tz=datetime.timezone.utc)
            .date()
            .strftime(self.settings.date_format)
        )
        release_date = f" ({text_date})" if self.options["next_release"] else ""
        release_link = (
            "tree/HEAD"
            if not self.options["next_release"]
            else f"releases/tag/{self.options['next_release']}"
        )
        self.prev_release = "HEAD"
        release_text = self.render_release_text(
            self.options["next_release"] or "unreleased"
        )
        return (
            f"## [{heading}]({self.repo_data.html_url}/{release_link})"
            f"{release_date}\n\n"
            f"{release_text}"
            f"{self.render_issues(self.unreleased_issues)}"
            f"{self.render_pull_requests(self.unreleased)}"
        )

    def render_release(
        self,
        release: Release,
    ) -> str:
        """Process a single release."""
        if (
            self.options["skip_releases"]
            and release.tag_name.strip() in self.options["skip_releases"]
        ):
            return ""

        output: list[str] = []
        if self.prev_release:
            output.append(self.render_diff_links(self.prev_release, release))

        output.append(self.render_before_text(release))

        text_date = release.created_at.date().strftime(
            self.settings.date_format
        )
        output.append(
            f"## [{release.tag_name}]({release.html_url}) ({text_date})",
        )
        output.append(self.render_yanked_notice(release))

        output.append("\n\n")

        if title_unique(release):
            output.append(
                f"**_{cap_first_letter(release.title.strip())}_**\n\n"
            )

        pr_list: list[PullRequestItem] = self.pr_by_release.get(release.id, [])
        issue_list: list[IssueItem] = self.issue_by_release.get(release.id, [])

        output.append(self.render_release_text(release))

        if (
            release.tag_name
            in self.release_text_cache.release_overrides_by_release
        ):
            override_text = (
                self.release_text_cache.release_overrides_by_release[
                    release.tag_name
                ]
            )
            output.append(f"{override_text}\n\n")
            return "".join(output)

        output.append(self.render_issues(issue_list))
        output.append(self.render_pull_requests(pr_list))

        if not issue_list and not pr_list:
            output.append(self.render_release_body(release))

        return "".join(output)

    def render_yanked_notice(self, release: Release) -> str:
        """Note if this release has been yanked, and the reason why."""
        if release.tag_name not in self.release_text_cache.yanked_by_release:
            return ""
        return (
            " **[`YANKED`]**\n\n"
            "**This release has been removed for the following reason and "
            "should not be used:**\n\n"
            f"- {self.release_text_cache.yanked_by_release[release.tag_name]}"
        )

    def render_before_text(self, release: Release) -> str:
        """Shows text before this release if it exists."""
        if (
            release.tag_name
            not in self.release_text_cache.release_text_before_by_release
        ):
            return ""
        return (
            "---\n\n"
            f"{self.release_text_cache.release_text_before_by_release[release.tag_name]}"
            "\n\n---\n\n"
        )

    def render_release_text(
        self,
        release: str | Release,
    ) -> str:
        """Print the release_text if it exists."""
        tag_name = release if isinstance(release, str) else release.tag_name

        if tag_name not in self.release_text_cache.release_text_by_release:
            return ""
        release_text = self.release_text_cache.release_text_by_release[tag_name]
        return f"{release_text}\n\n"

    def render_release_body(
        self,
        release: Release,
    ) -> str:
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
            return body
        return (
            "There were no merged pull requests or closed issues "
            "for this release.\n\n"
            "See the Full Changelog below for details.\n\n"
        )

    def render_issues(
        self,
        issue_list: list[IssueItem],
    ) -> str:
        """Print all the closed issues for a given release."""
        visible_issues = self.ignore_items(list(issue_list))
        if not visible_issues or not self.options["show_issues"]:
            return ""

        output = [self.format_section_heading("Closed Issues")]
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
                output.append(
                    f"- {escaped_title} "
                    f"([#{issue.number}]({issue.html_url})) "
                    f"by [{issue.closed_by.login}]"
                    f"({issue.closed_by.html_url})\n",
                )
            except AttributeError:
                output.append(
                    f"- {escaped_title} ([#{issue.number}]({issue.html_url}))\n"
                )
        output.append("\n")
        return "".join(output)

    def render_diff_links(
        self,
        prev_release: Release | str,
        release_tag: Release,
    ) -> str:
        """Generate a GitHub 3-dots link to the diff between two releases."""
        if not isinstance(prev_release, str):
            prev_release = prev_release.tag_name
        elif self.options["next_release"]:
            prev_release = self.options["next_release"]
        output = [
            f"[`Full Changelog`]"
            f"({self.repo_data.html_url}/compare/"
            f"{release_tag.tag_name}...{prev_release})"
        ]
        if self.options["show_diff"]:
            output.append(
                f" | [`Diff`]({self.repo_data.html_url}/compare/"
                f"{release_tag.tag_name}...{prev_release}.diff)",
            )
        if self.options["show_patch"]:
            output.append(
                f" | [`Patch`]({self.repo_data.html_url}/compare/"
                f"{release_tag.tag_name}...{prev_release}.patch)",
            )
        output.append("\n\n")
        return "".join(output)

    def render_pull_requests(
        self,
        pr_list: list[PullRequestItem],
    ) -> str:
        """Print all the PRs for a given release."""
        if not pr_list:
            return ""

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

        output: list[str] = []
        for heading, prs in release_sections.items():
            is_dependencies = heading == get_section_name("dependencies")
            if is_dependencies and not self.options["show_depends"]:
                continue

            visible_prs = self.ignore_items(list(prs))

            if visible_prs:
                output.append(self.format_section_heading(heading))
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
                    output.append(
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
                    output.append(
                        f"- *and {hidden_updates} more dependency updates*\n",
                    )
                output.append("\n")
        return "".join(output)

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
        msg = f"Unknown item order: {self.options['item_order']}"
        raise ValueError(msg)

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
