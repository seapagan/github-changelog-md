"""Entry point for the main application loop."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Annotated

import typer
from rich import print as rprint

from github_changelog_md.changelog import ChangeLog, build_release_text_cache
from github_changelog_md.changelog.github_data import GitHubDataSource
from github_changelog_md.config import get_settings
from github_changelog_md.config.validation import (
    ChangelogConfigError,
    validate_changelog_options,
    validate_settings,
)
from github_changelog_md.constants import ExitErrors
from github_changelog_md.helpers import get_app_version, get_repo_remote

if TYPE_CHECKING:
    from github_changelog_md.constants import ChangelogOptions

app = typer.Typer(
    pretty_exceptions_show_locals=False,
    add_completion=False,
    no_args_is_help=False,
    rich_markup_mode="rich",
)


@app.command()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "-v",
            "--version",
            is_eager=True,
        ),
    ] = None,
    repo: Annotated[
        str | None,
        typer.Option(
            "--repo",
            "-r",
            help="Name of the repository to generate the Changelog for.",
            show_default=False,
        ),
    ] = None,
    user: Annotated[
        str | None,
        typer.Option(
            "--user",
            "-u",
            help="Name of the user or organisation that owns the repository.",
            show_default=False,
        ),
    ] = None,
    next_release: Annotated[
        str | None,
        typer.Option(
            "--next-release",
            "-n",
            help="Name of the next release to generate the changelog for.",
            show_default=False,
        ),
    ] = None,
    unreleased: Annotated[
        bool | None,
        typer.Option(
            help=(
                "Show unreleased changes in the Changelog, defaults to "
                "[bold]True[/bold]."
            ),
            show_default=False,
        ),
    ] = None,
    contrib: Annotated[
        bool | None,
        typer.Option(
            help=(
                "Update the CONTRIBUTORS.md file, defaults to "
                "[bold]False[/bold]."
            ),
            show_default=False,
        ),
    ] = None,
    depends: Annotated[
        bool | None,
        typer.Option(
            help=(
                "Show dependency updates in the Changelog, defaults to "
                "[bold]True[/bold]."
            ),
            show_default=False,
        ),
    ] = None,
    output: Annotated[
        str | None,
        typer.Option(
            "--output",
            "-o",
            help="Output file to write the Changelog to.",
            show_default=False,
        ),
    ] = None,
    quiet: Annotated[
        bool | None,
        typer.Option(
            "--quiet",
            "-q",
            help="Suppress all output except errors.",
            show_default=False,
        ),
    ] = None,
    skip: Annotated[
        list[str] | None,
        typer.Option(
            "--skip",
            "-s",
            help="Skip the supplied tag. Can be specified multiple times",
            show_default=False,
        ),
    ] = None,
    issues: Annotated[
        bool | None,
        typer.Option(
            help=(
                "Show CLOSED issues in the Changelog, defaults to "
                "[bold]True[/bold]."
            ),
            show_default=False,
        ),
    ] = None,
    item_order: Annotated[
        str | None,
        typer.Option(
            "--item-order",
            "-i",
            help=(
                "Order of PRs and Issues in a release section. Valid options "
                "are [bold]'newest-first'[/bold] or "
                "[bold]'oldest-first'[/bold]."
                " Defaults to [bold]'newest-first'[/bold]."
            ),
            show_default=False,
        ),
    ] = None,
    ignore: Annotated[
        list[int] | None,
        typer.Option(
            "--ignore",
            "-e",
            help=(
                "Ignore the supplied PR or Issue by its number. Can be "
                "specified multiple times."
            ),
            show_default=False,
        ),
    ] = None,
    max_depends: Annotated[
        int | None,
        typer.Option(
            "--max-depends",
            "-m",
            help=(
                "Maximum number of dependency updates to show in the "
                "Changelog. Defaults to [bold]10[/bold]."
            ),
            show_default=False,
        ),
    ] = None,
    show_diff: Annotated[
        bool | None,
        typer.Option(
            help=(
                "Show the diff of the PRs and Issues in the Changelog, "
                "defaults to [bold]True[/bold]."
            ),
            show_default=False,
        ),
    ] = None,
    show_patch: Annotated[
        bool | None,
        typer.Option(
            help=(
                "Show the patch of the PRs and Issues in the Changelog, "
                "defaults to [bold]True[/bold]."
            ),
            show_default=False,
        ),
    ] = None,
    bold_sections: Annotated[
        bool | None,
        typer.Option(
            "--bold-sections/--no-bold-sections",
            "-b",
            help=(
                "Use legacy bold text for section headings instead of H3 "
                "Markdown headings, defaults to [bold]False[/bold]."
            ),
            show_default=False,
        ),
    ] = None,
) -> None:
    """Generate your CHANGELOG file Automatically from GitHub."""
    if version:
        rprint(
            "\n[green]Github Changelog Markdown - "
            "Generate your CHANGELOG file automatically."
            f"\n[/green]Version: {get_app_version()}; "
            "\u00a9 Grant Ramsay 2023\n",
        )
        raise typer.Exit

    if not repo:
        # Try to get the repo from the current directory.
        repo_remote = get_repo_remote()
        if repo_remote:
            repo = repo_remote.repo
            user = user or repo_remote.owner

        if not repo:
            rprint(
                "[red]  ->  Could not find a local repository, "
                "Please use the --repo option.\n",
                file=sys.stderr,
            )
            raise typer.Exit

    settings = get_settings()

    try:
        validate_settings(settings)
        options: ChangelogOptions = validate_changelog_options(
            {
                "user_name": user,
                "next_release": next_release,
                "show_unreleased": (
                    settings.unreleased if unreleased is None else unreleased
                ),
                "show_depends": (
                    settings.depends if depends is None else depends
                ),
                "output_file": (
                    settings.output_file if output is None else output
                ),
                "contributors": (
                    settings.contrib if contrib is None else contrib
                ),
                "quiet": settings.quiet if quiet is None else quiet,
                "skip_releases": settings.skip_releases
                if skip is None
                else skip,
                "show_issues": (
                    settings.show_issues if issues is None else issues
                ),
                "item_order": (
                    settings.item_order if item_order is None else item_order
                ),
                "ignore_items": (
                    settings.ignore_items if ignore is None else ignore
                ),
                "max_depends": (
                    settings.max_depends if max_depends is None else max_depends
                ),
                "show_diff": (
                    settings.show_diff if show_diff is None else show_diff
                ),
                "show_patch": (
                    settings.show_patch if show_patch is None else show_patch
                ),
                "bold_sections": (
                    settings.bold_sections
                    if bold_sections is None
                    else bold_sections
                ),
            }
        )
    except ChangelogConfigError as exc:
        rprint(f"\n[red]  X  Error: {exc}[/red]\n", file=sys.stderr)
        raise typer.Exit(ExitErrors.INVALID_ACTION) from exc

    try:
        data_source = GitHubDataSource.from_token(settings.github_pat)
    except AttributeError as exc:
        rprint(
            "\n[red]  X  Error: No GitHub PAT found in settings file\n",
            file=sys.stderr,
        )
        raise typer.Exit(ExitErrors.NO_PAT) from exc

    changelog = ChangeLog(
        repo,
        options,
        settings,
        data_source,
        build_release_text_cache(settings),
    )
    changelog.run()
