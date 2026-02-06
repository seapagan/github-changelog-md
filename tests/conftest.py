"""Setup some fixtures for the tests."""

# mypy: disable-error-code="no-untyped-def"
from collections.abc import Generator

import pytest

from github_changelog_md.config.settings import Settings
from github_changelog_md.constants import CONFIG_FILE


@pytest.fixture(autouse=True)
def _reset_settings_singleton() -> Generator[None]:
    """Clear the Settings singleton between tests."""
    Settings._instances.pop(Settings, None)  # noqa: SLF001
    yield
    Settings._instances.pop(Settings, None)  # noqa: SLF001


@pytest.fixture
def config_file(fs) -> None:
    """Create a fake config file."""
    fs.create_file(
        CONFIG_FILE,
        contents="""
        [changelog_generator]
        github_pat = '1234'
        schema_version = '1'
        unreleased = true
        quiet = false
        depends = true
        contrib = false
        """,
    )


@pytest.fixture
def bad_schema(fs) -> None:
    """Create a fake config file with a bad schema."""
    fs.create_file(
        CONFIG_FILE,
        contents="""
        [changelog_generator]
        github_pat = '1234'
        schema_version = '2'
        unreleased = true
        quiet = false
        depends = true
        contrib = false
        """,
    )
