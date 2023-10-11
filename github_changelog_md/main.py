"""Entry point for the main application loop."""
from typing import Optional

import typer
from github import Auth, Github
from rich import print  # pylint: disable=redefined-builtin

from github_changelog_md.helpers import get_app_version

from .config.settings import settings

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
    )
) -> None:
    """Entry point for the application."""
    if version:
        print(
            "\n[green]Github Changelog Markdown - "
            "Generate your CHANGELOG automatically."
            f"\n[/green]Version: {get_app_version()}; "
            "\u00a9 Grant Ramsay 2023\n"
        )
        raise typer.Exit()
    print("Welcome to Github Changelog Md!")
    auth = Auth.Token(settings.github_pat)
    git = Github(auth=auth)

    for repo in git.get_user().get_repos():
        print(repo.name)


if __name__ == "__main__":
    app()
