"""Handle the settings for the project."""
from simple_toml_settings import TOMLSettings


class Settings(TOMLSettings):
    """Define the settings for the project."""

    github_pat: str = ""


settings = Settings(
    "changelog_gen", local_file=True, settings_file_name=".changelog_gen.toml"
)
