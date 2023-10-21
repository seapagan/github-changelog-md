"""Test our manipulations of the TOMLSettings library."""
# mypy: disable-error-code="no-untyped-def"
import pytest
from simple_toml_settings.exceptions import SettingsNotFound

from github_changelog_md.config.settings import (
    get_pat_input,
    get_settings_object,
)


class TestSettings:
    """Test our settings module."""

    def test_get_settings_object_fails_no_file(
        self,
        fs,  # noqa: ARG002
    ) -> None:
        """Test we can't get a settings object without file existing."""
        with pytest.raises(SettingsNotFound) as exc:
            get_settings_object()

        assert (
            exc.value.args[0] == "Cant find a Config File, please create one."
        )

    def test_get_settings_object_suceeds(self, fs) -> None:
        """Create a fake settings file and test we can get a settings object."""
        fs.create_file(
            ".changelog_generator.toml",
            contents="[changelog_generator]\ngithub_pat = '1234'\n",
        )
        settings = get_settings_object()
        assert settings.github_pat == "1234"

    def test_get_pat_input(
        self,
        fs,  # noqa: ARG002
        monkeypatch,
    ) -> None:
        """Test we can get a PAT from the user."""
        monkeypatch.setattr("rich.prompt.Prompt.ask", lambda _: "1234")
        pat = get_pat_input()
        assert pat == "1234"
