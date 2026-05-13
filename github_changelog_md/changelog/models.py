"""Internal changelog domain models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    import datetime

    from github.GitRelease import GitRelease
    from github.Issue import Issue as GithubIssue
    from github.Label import Label as GithubLabel
    from github.NamedUser import NamedUser
    from github.PullRequest import PullRequest as GithubPullRequest
    from github.Repository import Repository


@dataclass(frozen=True, slots=True)
class ChangelogUser:
    """User details needed while generating a changelog."""

    login: str
    html_url: str
    name: str | None = None


@dataclass(frozen=True, slots=True)
class ChangelogLabel:
    """Label details needed while generating a changelog."""

    name: str


@dataclass(frozen=True, slots=True)
class ChangelogRepository:
    """Repository details needed while generating a changelog."""

    name: str
    full_name: str
    html_url: str


@dataclass(frozen=True, slots=True)
class ChangelogRelease:
    """Release details needed while generating a changelog."""

    id: int
    tag_name: str
    title: str
    html_url: str
    created_at: datetime.datetime
    body: str | None = None


@dataclass(frozen=True, slots=True)
class ChangelogPullRequest:
    """Pull request details needed while generating a changelog."""

    id: int
    number: int
    title: str
    html_url: str
    user: ChangelogUser
    labels: list[ChangelogLabel]
    merged_at: datetime.datetime | None


@dataclass(frozen=True, slots=True)
class ChangelogIssue:
    """Issue details needed while generating a changelog."""

    id: int
    number: int
    title: str
    html_url: str
    user: ChangelogUser
    labels: list[ChangelogLabel]
    closed_at: datetime.datetime | None
    closed_by: ChangelogUser | None
    pull_request: object | None = None


def user_from_github(user: NamedUser | None) -> ChangelogUser | None:
    """Convert a PyGithub user to an internal changelog user."""
    if user is None:
        return None
    return ChangelogUser(
        login=user.login,
        html_url=user.html_url,
    )


def label_from_github(label: GithubLabel) -> ChangelogLabel:
    """Convert a PyGithub label to an internal changelog label."""
    return ChangelogLabel(name=label.name)


def repository_from_github(repository: Repository) -> ChangelogRepository:
    """Convert a PyGithub repository to an internal changelog repository."""
    return ChangelogRepository(
        name=repository.name,
        full_name=repository.full_name,
        html_url=repository.html_url,
    )


def release_from_github(release: GitRelease) -> ChangelogRelease:
    """Convert a PyGithub release to an internal changelog release."""
    return ChangelogRelease(
        id=release.id,
        tag_name=release.tag_name,
        title=release.title,
        html_url=release.html_url,
        created_at=release.created_at,
        body=release.body,
    )


def pull_request_from_github(
    pull_request: GithubPullRequest,
) -> ChangelogPullRequest:
    """Convert a PyGithub pull request to an internal changelog PR."""
    user = user_from_github(pull_request.user)
    if user is None:
        msg = "Pull request user cannot be None"
        raise ValueError(msg)

    return ChangelogPullRequest(
        id=pull_request.id,
        number=pull_request.number,
        title=pull_request.title,
        html_url=pull_request.html_url,
        user=user,
        labels=[label_from_github(label) for label in pull_request.labels],
        merged_at=pull_request.merged_at,
    )


def issue_from_github(issue: GithubIssue) -> ChangelogIssue:
    """Convert a PyGithub issue to an internal changelog issue."""
    user = user_from_github(issue.user)
    if user is None:
        msg = "Issue user cannot be None"
        raise ValueError(msg)

    return ChangelogIssue(
        id=issue.id,
        number=issue.number,
        title=issue.title,
        html_url=issue.html_url,
        user=user,
        labels=[label_from_github(label) for label in issue.labels],
        closed_at=issue.closed_at,
        closed_by=user_from_github(issue.closed_by),
        pull_request=issue.pull_request,
    )
