"""Define helper functions for the application."""

from __future__ import annotations

import sys
from importlib import metadata, resources
from pathlib import Path
from typing import TYPE_CHECKING

import rtoml
from rich import print as rprint

from github_changelog_md.constants import SECTIONS, ExitErrors, SectionHeadings

if TYPE_CHECKING:  # pragma: no cover
    from github.GitRelease import GitRelease


def get_toml_path() -> Path:
    """Return the full path of the pyproject.toml.

    This only works during development mode, since the pyproject.toml will not
    exist when the application is installed as a package.
    """
    return (
        Path(str(resources.files("github_changelog_md")))
        / ".."
        / "pyproject.toml"
    )


def get_app_version() -> str:
    """Return the API version from the pyproject.toml file.

    We cannot however just find the file on the local file system, as the
    application will be installed as a package, in which case we need to use
    metadata from the package. We still check for the local file first, and only
    if it does not exist, we use the metadata - this allows us to test the
    application locally without installing it.
    """
    toml_path = get_toml_path()

    if toml_path.exists():
        # we are locally developing the package
        try:
            config = rtoml.load(toml_path)
            version: str = config["project"]["version"]
        except (KeyError, OSError) as exc:
            rprint(f"Problem getting the Version : {exc}")
            sys.exit(ExitErrors.OS_ERROR)
        else:
            return version
    else:
        # if we are here then the package must be installed not local dev
        try:
            return metadata.version("github_changelog_md")
        except metadata.PackageNotFoundError as exc:
            rprint(f"Problem getting the Version : {exc}")
            sys.exit(ExitErrors.OS_ERROR)


def header() -> None:
    """Print the application header."""
    rprint(
        "\n[bold blue]GitHub Changelog Generator[/bold blue] "
        f"v{get_app_version()}\n",
    )


def get_repo_name() -> str | None:
    """Return the name of the repository from the current directory."""
    git_config_path = Path.cwd() / ".git" / "config"
    repo_name = None
    if git_config_path.exists():
        with Path(git_config_path).open("r", encoding="utf-8") as git_config:
            for line in git_config:
                if "url" in line:
                    repo_name = Path(line.split("=")[-1]).stem
    return repo_name


def cap_first_letter(string: str) -> str:
    """Capitalize the first letter of a string only.

    Using the build in string method capitalize() will actually change any other
    upper case letters to lower case, which is not what we want.
    """
    return string[:1].upper() + string[1:]


def get_section_name(label: str | None) -> str | None:
    """Gets a section title from a label."""
    for section in SECTIONS:
        if section[1] == label:
            return section[0]
    return None


def get_index_of_tuple(
    tuple_list: list[SectionHeadings], index: int, value: str | None
) -> int:
    """Return the index of a tuple in a list."""
    for pos, t in enumerate(tuple_list):
        if t[index] == value:
            return pos

    error_msg = f"'{value}' is not in the supplied list of Tuples"
    raise ValueError(error_msg)


def strip_first_alpha_char(version_string: str) -> str:
    """Strip the first character from a string if it is a letter."""
    if version_string and version_string[0].isalpha():
        return version_string[1:]
    return version_string


def title_unique(release: GitRelease) -> bool:
    """Ensures that the release title and tag name are not the same.

    It will remove the first alpha character from the title and tag (if it is a
    letter) and compare the two strings. Returns True if they are different,
    False otherwise.

    It will also return False if the title or tag name is empty.
    """
    if not release.title or not release.tag_name:
        return False
    return strip_first_alpha_char(release.title) != strip_first_alpha_char(
        release.tag_name
    )
