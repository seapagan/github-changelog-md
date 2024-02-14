"""Test our manipulations of the TOMLSettings library."""
# mypy: disable-error-code="no-untyped-def"

import pytest
import pytest_mock
from simple_toml_settings.exceptions import SettingsNotFoundError

from github_changelog_md.config.settings import (
    Settings,
    get_pat_input,
    get_settings,
    get_settings_object,
)
from github_changelog_md.constants import CONFIG_FILE, ExitErrors

MOCK_PROMPT_ASK = "rich.prompt.Prompt.ask"


class TestSettings:
    """Test our settings module."""

    def test_get_settings_object_fails_no_file(
        self,
        fs,  # noqa: ARG002
    ) -> None:
        """Test we can't get a settings object without file existing."""
        with pytest.raises(SettingsNotFoundError) as exc:
            get_settings_object()

        assert (
            exc.value.args[0] == "Cant find a Config File, please create one."
        )

    def test_get_settings_object_suceeds(self, fs) -> None:
        """Create a fake settings file and test we can get a settings object."""
        fs.create_file(
            CONFIG_FILE,
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
        monkeypatch.setattr(MOCK_PROMPT_ASK, lambda _: "1234")
        pat = get_pat_input()

        assert pat == "1234"

    def test_get_pat_input_blank(
        self,
        fs,  # noqa: ARG002
        monkeypatch,
    ) -> None:
        """Test when we get an invalid PAT from the user."""
        monkeypatch.setattr(MOCK_PROMPT_ASK, lambda _: "")
        with pytest.raises(SystemExit) as exc:
            get_pat_input()

        assert exc.value.args[0] == ExitErrors.INVALID_ACTION

    def test_get_settings_with_config_file(
        self,
        config_file,  # noqa: ARG002
    ) -> None:
        """Test we can get a settings object."""
        settings = get_settings()

        assert settings.github_pat == "1234"
        assert settings.settings_file_name == CONFIG_FILE
        assert isinstance(settings, Settings)

    def test_get_settings_with_bad_schema(
        self,
        bad_schema,  # noqa: ARG002
    ) -> None:
        """Test we can get a settings object."""
        with pytest.raises(SystemExit) as exc:
            get_settings()

        assert exc.value.args[0] == ExitErrors.BAD_SCHEMA

    def test_settings_with_no_config_file(
        self,
        fs,
        monkeypatch,
    ) -> None:
        """Test we can get a settings object."""
        monkeypatch.setattr(MOCK_PROMPT_ASK, lambda _: "1234")
        settings = get_settings()

        assert settings.github_pat == "1234"
        assert settings.settings_file_name == CONFIG_FILE
        assert isinstance(settings, Settings)
        assert fs.exists(CONFIG_FILE)

    def test_settings_with_no_config_file_and_keyboard_interrupt(
        self,
        fs,
        mocker: pytest_mock.MockFixture,
    ) -> None:
        """Test we can get a settings object."""
        mocker.patch(
            MOCK_PROMPT_ASK,
            side_effect=KeyboardInterrupt,
        )
        with pytest.raises(SystemExit) as exc:
            get_settings()

        assert exc.value.args[0] == ExitErrors.USER_ABORT
        assert not fs.exists(CONFIG_FILE)

    def test_settings_with_no_write_permission_for_current_folder(
        self,
        fs,  # noqa: ARG002
        monkeypatch,
        mocker: pytest_mock.MockFixture,
    ) -> None:
        """Test settings error if we dont have write permission."""
        monkeypatch.setattr(MOCK_PROMPT_ASK, lambda _: "1234")
        mocker.patch(
            "pathlib.Path.open",
            side_effect=PermissionError,
        )
        with pytest.raises(SystemExit) as exc:
            get_settings()

        assert exc.value.args[0] == ExitErrors.PERMISSION_DENIED
