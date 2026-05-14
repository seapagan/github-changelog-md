"""Pure changelog item bucketing logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, Protocol, TypeVar

if TYPE_CHECKING:  # pragma: no cover
    import datetime
    from collections.abc import Callable

    from github_changelog_md.changelog.models import (
        ChangelogIssue,
        ChangelogPullRequest,
        ChangelogRelease,
        ChangelogUser,
    )


class BucketableItem(Protocol):
    """Item fields required for release bucketing."""

    @property
    def id(self) -> int:
        """Return the item id."""
        ...

    @property
    def user(self) -> ChangelogUser:
        """Return the item author."""
        ...


ChangelogItem = TypeVar("ChangelogItem", bound=BucketableItem)


@dataclass(frozen=True, slots=True)
class BucketedItems(Generic[ChangelogItem]):
    """Items assigned to releases plus items newer than the latest release."""

    by_release: dict[int, list[ChangelogItem]]
    unreleased: list[ChangelogItem]


def get_unreleased_cutoff(
    releases: list[ChangelogRelease],
    fallback_date: datetime.datetime,
) -> datetime.datetime:
    """Return the date after which items are considered unreleased."""
    if not releases:
        return fallback_date
    return max(releases, key=lambda release: release.created_at).created_at


def bucket_pull_requests(
    releases: list[ChangelogRelease],
    pull_requests: list[ChangelogPullRequest],
    unreleased_cutoff: datetime.datetime,
    ignored_users: list[str],
) -> BucketedItems[ChangelogPullRequest]:
    """Assign pull requests to releases by merge date."""
    return _bucket_items(
        releases=releases,
        items=pull_requests,
        unreleased_cutoff=unreleased_cutoff,
        ignored_users=ignored_users,
        item_date=lambda pull_request: pull_request.merged_at,
    )


def bucket_issues(
    releases: list[ChangelogRelease],
    issues: list[ChangelogIssue],
    unreleased_cutoff: datetime.datetime,
    ignored_users: list[str],
) -> BucketedItems[ChangelogIssue]:
    """Assign issues to releases by close date."""
    return _bucket_items(
        releases=releases,
        items=issues,
        unreleased_cutoff=unreleased_cutoff,
        ignored_users=ignored_users,
        item_date=lambda issue: issue.closed_at,
    )


def _bucket_items(
    releases: list[ChangelogRelease],
    items: list[ChangelogItem],
    unreleased_cutoff: datetime.datetime,
    ignored_users: list[str],
    item_date: Callable[[ChangelogItem], datetime.datetime | None],
) -> BucketedItems[ChangelogItem]:
    """Assign dated items to the first release after their date."""
    by_release: dict[int, list[ChangelogItem]] = {
        release.id: [] for release in releases
    }
    sorted_releases = sorted(releases, key=lambda release: release.created_at)
    sorted_items = sorted(
        items,
        key=lambda item: _date_or_cutoff(item, item_date, unreleased_cutoff),
    )
    ignored_user_set = set(ignored_users)
    seen: set[int] = set()

    for release in sorted_releases:
        for item in sorted_items:
            date = item_date(item)
            if (
                date
                and date <= release.created_at
                and item.id not in seen
                and item.user.login not in ignored_user_set
            ):
                by_release[release.id].append(item)
                seen.add(item.id)

    unreleased: list[ChangelogItem] = []
    for item in sorted_items:
        date = item_date(item)
        if (
            date
            and date > unreleased_cutoff
            and item.id not in seen
            and item.user.login not in ignored_user_set
        ):
            unreleased.append(item)
    return BucketedItems(by_release=by_release, unreleased=unreleased)


def _date_or_cutoff(
    item: ChangelogItem,
    item_date: Callable[[ChangelogItem], datetime.datetime | None],
    unreleased_cutoff: datetime.datetime,
) -> datetime.datetime:
    """Return an item's date or the cutoff for undated items."""
    date = item_date(item)
    if date is None:
        return unreleased_cutoff
    return date
