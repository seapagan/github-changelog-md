"""Handle the settings for the project."""
from pathlib import Path

from rich import print  # pylint: disable=redefined-builtin
from rich.prompt import Prompt
from simple_toml_settings import TOMLSettings
from simple_toml_settings.exceptions import SettingsNotFound

from github_changelog_md.constants import ExitErrors


class Settings(TOMLSettings):
    """Define the settings for the project."""

    github_pat: str

    @staticmethod
    def get_settings():
        """Return a settings object for this app."""
        return Settings(
            "changelog_generator",
            local_file=True,
            settings_file_name=".changelog_generator.toml",
            auto_create=False,
        )


# not too happy with this method of doing it. Ideally I need to modify the
# Settings class to allow for a default value of PAT to be set though the
# constructor, then enable autosave again.
try:
    settings = Settings.get_settings()
except SettingsNotFound:
    try:
        get_pat = Prompt.ask("[green]\nPlease enter your GitHub PAT[/green] ")
    except KeyboardInterrupt:
        print("\n[red]Exiting[/red]")
        exit(ExitErrors.USER_ABORT)

    try:
        with Path(".changelog_generator.toml").open("w") as f:
            f.write(f"[changelog_generator]\ngithub_pat = '{get_pat}'\n")
        settings = Settings.get_settings()
        settings.save()
    except PermissionError:
        print(
            "\n[red]Permission denied. Please run the command in a folder "
            "you have write-access to.[/red]"
        )
        exit(ExitErrors.PERMISSION_DENIED)
