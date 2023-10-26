"""Entry point for the main application loop."""
from __future__ import annotations

from typing import Any, Optional

import typer
from rich import print  # pylint: disable=redefined-builtin

from github_changelog_md.changelog import ChangeLog
from github_changelog_md.constants import OUTPUT_FILE
from github_changelog_md.helpers import get_app_version, get_repo_name

app = typer.Typer(
    pretty_exceptions_show_locals=False,
    add_completion=False,
    no_args_is_help=True,
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
        default=True,
        help="Show unreleased changes in the Changelog.",
        show_default=True,
    ),
    depends: Optional[bool] = typer.Option(
        default=True,
        help="Show dependency updates in the Changelog.",
        show_default=True,
    ),
    output: Optional[str] = typer.Option(
        OUTPUT_FILE,
        "--output",
        "-o",
        help="Output file to write the Changelog to.",
        show_default=False,
    ),
) -> None:
    """Generate your CHANGELOG file Automatically.

    If you don't specify a repository name, the application will try to
    get the repository name from the current directory (assuming it is a git
    repository).
    """
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
            )
            raise typer.Exit

    options: dict[str, Any] = {
        "user_name": user,
        "next_release": next_release,
        "show_unreleased": unreleased,
        "show_depends": depends,
        "output_file": output,
    }

    cl = ChangeLog(repo, options)
    cl.run()
