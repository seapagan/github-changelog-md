"""Entry point for the main application loop."""
from typing import Optional

import typer
from rich import print  # pylint: disable=redefined-builtin

from github_changelog_md.changelog import ChangeLog
from github_changelog_md.helpers import get_app_version

app = typer.Typer(
    pretty_exceptions_show_locals=False,
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def main(
    version: Optional[bool] = typer.Option(
        None, "-v", "--version", is_eager=True
    ),
    repo: str = typer.Option(
        ...,
        "-repo",
        "-r",
        help="Name of the repository to generate the changelog for.",
        show_default=False,
    ),
) -> None:
    """Generate your CHANGELOG file Automatically."""
    if version:
        print(
            "\n[green]Github Changelog Markdown - "
            "Generate your CHANGELOG file automatically."
            f"\n[/green]Version: {get_app_version()}; "
            "\u00a9 Grant Ramsay 2023\n"
        )
        raise typer.Exit()

    cl = ChangeLog(repo)
    cl.run()


if __name__ == "__main__":
    app()
