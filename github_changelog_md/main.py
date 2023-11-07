"""Entry point for the main application loop."""
from __future__ import annotations

import sys
from typing import Any, Optional

import typer
from rich import print  # pylint: disable=redefined-builtin

from github_changelog_md.changelog import ChangeLog
from github_changelog_md.config import get_settings
from github_changelog_md.helpers import get_app_version, get_repo_name

app = typer.Typer(
    pretty_exceptions_show_locals=False,
    add_completion=False,
    no_args_is_help=False,
    rich_markup_mode="rich",
)


@app.command()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "-v",
        "--version",
        is_eager=True,
    ),
    repo: Optional[str] = typer.Option(
        None,
        "--repo",
        "-r",
        help="Name of the repository to generate the Changelog for.",
        show_default=False,
    ),
    user: Optional[str] = typer.Option(
        None,
        "--user",
        "-u",
        help="Name of the user or organisation that owns the repository.",
        show_default=False,
    ),
    next_release: Optional[str] = typer.Option(
        None,
        "--next-release",
        "-n",
        help="Name of the next release to generate the changelog for.",
        show_default=False,
    ),
    unreleased: Optional[bool] = typer.Option(
        default=None,
        help=(
            "Show unreleased changes in the Changelog, defaults to [bold]True"
            "[/bold]."
        ),
        show_default=False,
    ),
    contrib: Optional[bool] = typer.Option(
        default=None,
        help="Update the CONTRIBUTORS.md file, defaults to [bold]False[/bold].",
        show_default=False,
    ),
    depends: Optional[bool] = typer.Option(
        default=None,
        help=(
            "Show dependency updates in the Changelog, defaults to [bold]True"
            "[/bold]."
        ),
        show_default=False,
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file to write the Changelog to.",
        show_default=False,
    ),
    quiet: Optional[bool] = typer.Option(
        None,
        "--quiet",
        "-q",
        help="Suppress all output except errors.",
        show_default=False,
    ),
    skip: Optional[list[str]] = typer.Option(  # noqa: B008
        [],
        "--skip",
        "-s",
        help="Skip the suplied tag. Can be specified multiple times",
        show_default=False,
    ),
    issues: Optional[bool] = typer.Option(
        default=None,
        help=(
            "Show CLOSED issues in the Changelog, defaults to [bold]True"
            "[/bold]."
        ),
        show_default=False,
    ),
    item_order: Optional[str] = typer.Option(
        None,
        "--item-order",
        "-i",
        help=(
            "Order of PRs and Issues in a release section. "
            "Valid options are [bold]'newest-first'[/bold] or [bold]'oldest-"
            "first'[/bold]. Defaults to [bold]'newest-first'[/bold]."
        ),
        show_default=False,
    ),
    ignore: Optional[list[int]] = typer.Option(  # noqa: B008
        [],
        "--ignore",
        "-e",
        help=(
            "Ignore the supplied PR or Issue by its number. Can be specified "
            "multiple times."
        ),
        show_default=False,
    ),
    max_depends: Optional[int] = typer.Option(
        None,
        "--max-depends",
        "-m",
        help=(
            "Maximum number of dependency updates to show in the Changelog. "
            "Defaults to [bold]10[/bold]."
        ),
        show_default=False,
    ),
    show_diff: Optional[bool] = typer.Option(
        default=None,
        help=(
            "Show the diff of the PRs and Issues in the Changelog, defaults "
            "to [bold]True[/bold]."
        ),
        show_default=False,
    ),
    show_patch: Optional[bool] = typer.Option(
        default=None,
        help=(
            "Show the patch of the PRs and Issues in the Changelog, defaults "
            "to [bold]True[/bold]."
        ),
        show_default=False,
    ),
) -> None:
    """Generate your CHANGELOG file Automatically from GitHub."""
    if version:
        print(
            "\n[green]Github Changelog Markdown - "
            "Generate your CHANGELOG file automatically."
            f"\n[/green]Version: {get_app_version()}; "
            "\u00a9 Grant Ramsay 2023\n",
        )
        raise typer.Exit

    if not repo:
        # Try to get the repo from the current directory.
        repo = get_repo_name()

        if not repo:
            # cant find a local repo and none specified on the cmd line.
            print(
                "[red]  ->  Could not find a local repository, "
                "Please use the --repo option.\n",
                file=sys.stderr,
            )
            raise typer.Exit

    settings = get_settings()

    options: dict[str, Any] = {
        "user_name": user,
        "next_release": next_release,
        "show_unreleased": (
            settings.unreleased if unreleased is None else unreleased
        ),
        "show_depends": settings.depends if depends is None else depends,
        "output_file": settings.output_file if output is None else output,
        "contributors": settings.contrib if contrib is None else contrib,
        "quiet": settings.quiet if quiet is None else quiet,
        "skip_releases": settings.skip_releases if skip == [] else skip,
        "show_issues": settings.show_issues if issues is None else issues,
        "item_order": settings.item_order if item_order is None else item_order,
        "ignore_items": settings.ignore_items if ignore == [] else ignore,
        "max_depends": settings.max_depends
        if max_depends is None
        else max_depends,
        "show_diff": settings.show_diff if show_diff is None else show_diff,
        "show_patch": settings.show_patch if show_patch is None else show_patch,
    }

    changelog = ChangeLog(repo, options)
    changelog.run()
