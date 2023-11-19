"""Handle the settings for the project."""
import sys
from pathlib import Path
from typing import ClassVar, Optional

from rich import print  # pylint: disable=redefined-builtin
from rich.prompt import Prompt
from simple_toml_settings import TOMLSettings
from simple_toml_settings.exceptions import SettingsNotFoundError

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
    skip_releases: Optional[list[str]] = None
    extend_sections: Optional[list[dict[str, str]]] = None
    extend_sections_index: Optional[int] = None
    rename_sections: Optional[list[dict[str, str]]] = None
    date_format: str = "%Y-%m-%d"
    show_issues: bool = True
    item_order: str = "newest-first"
    ignore_items: Optional[list[int]] = None
    extend_ignored: Optional[list[str]] = None
    ignored_labels: Optional[list[str]] = None
    allowed_labels: Optional[list[str]] = None
    ignore_strings: Optional[list[str]] = None
    ignored_users: ClassVar[list[str]] = []
    max_depends: int = 10
    show_diff: bool = True
    show_patch: bool = True
    intro_text: str = ""
    yanked: Optional[list[dict[str, str]]] = None
    release_text: Optional[list[dict[str, str]]] = None
    release_text_before: Optional[list[dict[str, str]]] = None
    release_overrides: Optional[list[dict[str, str]]] = None


def get_settings_object() -> Settings:
    """Return a settings object for this app."""
    return Settings(
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
        print("[red]No PAT entered, exiting.[/red]")
        sys.exit(ExitErrors.INVALID_ACTION)
    return user_pat


# not too happy with this method of doing it. Ideally I need to modify the
# Settings class to allow for a default value of PAT to be set though the
# constructor, then enable autocreate again.
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
            print("\n[red]Exiting[/red]")
            sys.exit(ExitErrors.USER_ABORT)

        try:
            with Path(CONFIG_FILE).open("w") as f:
                f.write(f"[changelog_generator]\ngithub_pat = '{get_pat}'\n")
                f.flush()
                settings = get_settings_object()
                f.write(f"schema_version = '{settings.schema_version}'\n")
        except PermissionError:
            print(
                "\n[red]Permission denied. Please run the command in a folder "
                "you have write-access to.[/red]",
            )
            sys.exit(ExitErrors.PERMISSION_DENIED)

    return settings
