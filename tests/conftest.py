"""Setup some fixtures for the tests."""
# mypy: disable-error-code="no-untyped-def"
import pytest

from github_changelog_md.constants import CONFIG_FILE


@pytest.fixture()
def config_file(fs) -> None:  # noqa: PT004
    """Create a fake config file."""
    fs.create_file(
        CONFIG_FILE,
        contents="[changelog_generator]\ngithub_pat = '1234'\n",
    )
