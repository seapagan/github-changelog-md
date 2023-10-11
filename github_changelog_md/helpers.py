"""Define helper functions for the application."""
import sys
from importlib import metadata, resources
from pathlib import Path

import rtoml
from rich import print  # pylint: disable=redefined-builtin

from github_changelog_md.constants import ExitErrors


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
            version: str = config["tool"]["poetry"]["version"]
        except (KeyError, OSError) as exc:
            print(f"Problem getting the Version : {exc}")
            sys.exit(ExitErrors.OS_ERROR)
        else:
            return version
    else:
        # if we are here then the package must be installed not local dev
        try:
            return metadata.version("github_changelog_md")
        except metadata.PackageNotFoundError as exc:
            print(f"Problem getting the Version : {exc}")
            sys.exit(ExitErrors.OS_ERROR)
