from __future__ import annotations

from importlib import metadata
from pathlib import Path
from typing import TYPE_CHECKING

from github_changelog_md.constants import ExitErrors
from github_changelog_md.helpers import get_app_version, get_repo_name, header

if TYPE_CHECKING:
    import pytest
    from pyfakefs.fake_filesystem import FakeFileSystem
    from pytest_mock import MockerFixture


class TestHelpers:
    """Test class for the 'helpers' module."""

    patch_get_toml = "github_changelog_md.helpers.get_toml_path"
    test_toml_path = "tests/data/pyproject.toml"

    def test_get_repo_name_with_git_config(self, mocker: MockerFixture) -> None:
        """Test get_repo_name function with a valid git config file."""
        mocker.patch(
            "pathlib.Path.open",
            mocker.mock_open(
                read_data=(
                    '[remote "origin"]\n'
                    "url = https://github.com/user/repo.git\n"
                )
            ),
        )
        assert get_repo_name() == "repo"

    def test_get_repo_name_without_git_config(
        self, mocker: MockerFixture
    ) -> None:
        """Test get_repo_name function without a git config file."""
        mocker.patch("pathlib.Path.exists", return_value=False)
        assert get_repo_name() is None

    def test_header(self, capsys: pytest.CaptureFixture[str]) -> None:
        header()
        captured = capsys.readouterr()
        assert "GitHub Changelog Generator" in captured.out

    def test_get_app_version_with_toml_file(
        self, fs: FakeFileSystem, mocker: MockerFixture
    ) -> None:
        """Test get_app_version function with a valid pyproject.toml file."""

        fs.create_file(
            self.test_toml_path,
            contents=(
                "[tool.poetry]\n"
                'name = "github_changelog_md"\n'
                'version = "0.5.0"\n'
            ),
        )
        mocker.patch(
            self.patch_get_toml,
            return_value=Path(self.test_toml_path),
        )
        assert get_app_version() == "0.5.0"

    def test_get_app_version_bad_toml_file(
        self, fs: FakeFileSystem, mocker: MockerFixture
    ) -> None:
        """Test get_app_version function with a bad pyproject.toml file."""

        fs.create_file(
            self.test_toml_path,
            contents=("[tool.poetry]\n" 'name = "github_changelog_md"\n'),
        )
        mocker.patch(
            self.patch_get_toml,
            return_value=Path(self.test_toml_path),
        )
        mocked_exit = mocker.patch("github_changelog_md.helpers.sys.exit")

        assert get_app_version() is None
        assert mocked_exit.call_args[0][0] == ExitErrors.OS_ERROR

    def test_get_app_version_from_metadata(self, mocker: MockerFixture) -> None:
        """Test get_app_version function without a pyproject.toml file."""

        mocker.patch(
            self.patch_get_toml,
            return_value=Path(self.test_toml_path),
        )
        mocker.patch(
            "github_changelog_md.helpers.metadata.version",
            return_value="0.5.0",
        )
        assert get_app_version() == "0.5.0"

    def test_get_app_version_not_found(self, mocker: MockerFixture) -> None:
        """Test get_app_version function without a pyproject.toml file."""

        mocker.patch(
            self.patch_get_toml,
            return_value=Path(self.test_toml_path),
        )
        mocker.patch(
            "github_changelog_md.helpers.metadata.version",
            side_effect=metadata.PackageNotFoundError("Error message"),
        )
        mocked_exit = mocker.patch("github_changelog_md.helpers.sys.exit")

        assert get_app_version() is None
        assert mocked_exit.call_args[0][0] == ExitErrors.OS_ERROR
