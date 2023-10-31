"""Test module for the 'main' module."""
from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
from typer.testing import CliRunner

from github_changelog_md.main import app

if TYPE_CHECKING:
    from pytest_mock import MockerFixture
    from pytest_mock.plugin import MockType


@pytest.fixture()
def mock_changelog(mocker: MockerFixture) -> MockType:
    """Return a mocked ChangeLog class."""
    return mocker.patch("github_changelog_md.main.ChangeLog")


default_options = {
    "user_name": None,
    "next_release": None,
    "show_unreleased": True,
    "show_depends": True,
    "output_file": "CHANGELOG.md",
    "contributors": False,
}


class TestCLI:
    """Test class for the CLI functionality."""

    def test_cli_with_version(self) -> None:
        """Test the main function with the version flag."""
        runner = CliRunner()
        result = runner.invoke(app, ["--version"])
        assert "Github Changelog Markdown" in result.output

    def test_cli_with_repo(self, mock_changelog: MockType) -> None:
        """Test the main function with the repo flag."""
        mock_changelog_instance = Mock()
        mock_changelog.return_value = mock_changelog_instance

        runner = CliRunner()
        runner.invoke(app, ["--repo", "test_repo"])
        mock_changelog.assert_called_once_with(
            "test_repo",
            default_options,
        )
        mock_changelog_instance.run.assert_called_once()

    @pytest.mark.parametrize(
        "cli_options",
        [
            (["--output", "custom_file"], {"output_file": "custom_file"}),
            (["--next-release", "v1.0"], {"next_release": "v1.0"}),
            (["--unreleased"], {"show_unreleased": True}),
            (["--no-unreleased"], {"show_unreleased": False}),
            (["--depends"], {"show_depends": True}),
            (["--no-depends"], {"show_depends": False}),
        ],
    )
    def test_different_cli_options(
        self,
        mock_changelog: MockType,
        cli_options: tuple[list[str], dict[str, bool]],
    ) -> None:
        """Test that the CLI options are properly passed to ChangeLog().

        We only test the optional flags here.
        """
        mock_changelog_instance = Mock()
        mock_changelog.return_value = mock_changelog_instance

        runner = CliRunner()
        runner.invoke(app, ["--repo", "test_repo", *cli_options[0]])

        expected_options = {**default_options, **cli_options[1]}
        mock_changelog.assert_called_once_with(
            "test_repo",
            expected_options,
        )
        mock_changelog_instance.run.assert_called_once()

    def test_cli_with_repo_and_user(self, mock_changelog: MockType) -> None:
        """Test the main function with the repo and user flags."""
        mock_changelog_instance = Mock()
        mock_changelog.return_value = mock_changelog_instance

        runner = CliRunner()
        runner.invoke(app, ["--repo", "test_repo", "--user", "test_user"])

        expected_options = {**default_options, "user_name": "test_user"}
        mock_changelog.assert_called_once_with(
            "test_repo",
            expected_options,
        )
        mock_changelog_instance.run.assert_called_once()

    def test_cli_with_repo_and_user_and_next_release(
        self,
        mock_changelog: MockType,
    ) -> None:
        """Test the main function with the repo, user and next release flags."""
        mock_changelog_instance = Mock()
        mock_changelog.return_value = mock_changelog_instance

        runner = CliRunner()
        runner.invoke(
            app,
            [
                "--repo",
                "test_repo",
                "--user",
                "test_user",
                "--next-release",
                "v1.0",
            ],
        )

        expected_options = {
            **default_options,
            "user_name": "test_user",
            "next_release": "v1.0",
        }
        mock_changelog.assert_called_once_with(
            "test_repo",
            expected_options,
        )
        mock_changelog_instance.run.assert_called_once()

    def test_no_repo_specified_get_from_local_repo(
        self,
        mocker: MockerFixture,
        mock_changelog: MockType,
    ) -> None:
        """Test the main function with no repo specified.

        It should read the name from the local repo.
        """
        mock_changelog_instance = Mock()
        mock_changelog.return_value = mock_changelog_instance

        mocker.patch(
            "github_changelog_md.main.get_repo_name",
            return_value="test_local_repo",
        )

        runner = CliRunner()
        runner.invoke(app)

        mock_changelog.assert_called_once_with(
            "test_local_repo",
            default_options,
        )
        mock_changelog_instance.run.assert_called_once()

    def test_no_repo_specified_and_no_local_repo_found(
        self,
        mocker: MockerFixture,
        mock_changelog: MockType,
    ) -> None:
        """Test the main function with no repo specified.

        In this case there is also no local repo to read from.
        """
        mock_changelog_instance = Mock()
        mock_changelog.return_value = mock_changelog_instance

        mocker.patch(
            "github_changelog_md.main.get_repo_name",
            return_value=None,
        )

        runner = CliRunner()
        result = runner.invoke(app)
        assert "Could not find a local repository" in result.output
        mock_changelog.assert_not_called()
        mock_changelog_instance.run.assert_not_called()
