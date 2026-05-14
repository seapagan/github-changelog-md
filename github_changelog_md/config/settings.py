"""Handle the settings for the project."""

from pathlib import Path
from typing import ClassVar

import typer
from rich import print as rprint
from rich.prompt import Prompt
from simple_toml_settings import TOMLSettings
from simple_toml_settings.exceptions import (
    SettingsNotFoundError,
    SettingsSchemaError,
)

from github_changelog_md.constants import (
    CONFIG_FILE,
    OUTPUT_FILE,
    ExitErrors,
)


class Settings(TOMLSettings):
    """Define the settings for the project."""

    github_pat: str
    output_file: str = OUTPUT_FILE
    unreleased: bool = True
    depends: bool = True
    contrib: bool = False
    quiet: bool = False
    skip_releases: list[str] | None = None
    extend_sections: list[dict[str, str]] | None = None
    extend_sections_index: int | None = None
    rename_sections: list[dict[str, str]] | None = None
    date_format: str = "%Y-%m-%d"
    show_issues: bool = True
    item_order: str = "newest-first"
    ignore_items: list[int] | None = None
    extend_ignored: list[str] | None = None
    ignored_labels: list[str] | None = None
    allowed_labels: list[str] | None = None
    ignore_strings: list[str] | None = None
    ignored_users: ClassVar[list[str]] = []
    max_depends: int = 10
    show_diff: bool = True
    show_patch: bool = True
    intro_text: str = ""
    yanked: list[dict[str, str]] | None = None
    release_text: list[dict[str, str]] | None = None
    release_text_before: list[dict[str, str]] | None = None
    release_overrides: list[dict[str, str]] | None = None


def get_settings_object() -> Settings:
    """Return a settings object for this app."""
    return Settings.get_instance(
        "changelog_generator",
        local_file=True,
        settings_file_name=CONFIG_FILE,
        auto_create=False,
        schema_version="1",
    )


def get_pat_input() -> str:
    """Return the GitHub PAT."""
    user_pat = Prompt.ask("[green]\nPlease enter your GitHub PAT[/green] ")
    if not user_pat:
        rprint("[red]No PAT entered, exiting.[/red]")
        raise typer.Exit(ExitErrors.INVALID_ACTION)
    return user_pat


# Missing config files are created manually so the prompted PAT can be written
# before loading Settings. A cleaner future version would seed that PAT through
# the Settings constructor and re-enable library-managed auto-creation.
def get_settings() -> Settings:
    """Actually return a settings object.

    This is the function that should be called from the main script.
    It will look for a config file and if it doesn't find one, it will prompt
    the user for a PAT and create a config file.
    """
    try:
        settings = get_settings_object()
    except SettingsNotFoundError:
        try:
            get_pat = get_pat_input()
        except KeyboardInterrupt:
            rprint("\n[red]Exiting[/red]")
            raise typer.Exit(ExitErrors.USER_ABORT) from None

        try:
            with Path(CONFIG_FILE).open("w") as f:
                f.write(f"[changelog_generator]\ngithub_pat = '{get_pat}'\n")
                f.flush()
                settings = get_settings_object()
                f.write(f"schema_version = '{settings.schema_version}'\n")
        except PermissionError:
            rprint(
                "\n[red]Permission denied. Please run the command in a folder "
                "you have write-access to.[/red]",
            )
            raise typer.Exit(ExitErrors.PERMISSION_DENIED) from None
    except SettingsSchemaError as e:
        rprint(f"\n[red]Error in the settings file: [bold]{e}[/bold][/red]")
        rprint(
            "\n[purple]Please fix the settings file and try again.\nYou can "
            "check the website at [bold]http://changelog.seapagan.net/[/bold] "
            "for more information.[/purple]\n"
        )
        raise typer.Exit(ExitErrors.BAD_SCHEMA) from e

    return settings
