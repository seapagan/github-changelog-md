"""Test module for the 'main' module."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast
from unittest.mock import ANY, Mock

import pytest
from typer.testing import CliRunner

from github_changelog_md.constants import ExitErrors
from github_changelog_md.helpers import GitHubRemote
from github_changelog_md.main import app

if TYPE_CHECKING:
    from pytest_mock import MockerFixture
    from pytest_mock.plugin import MockType

    from github_changelog_md.constants import ChangelogOptions


@pytest.fixture
def mock_changelog(mocker: MockerFixture) -> MockType:
    """Return a mocked ChangeLog class."""
    return mocker.patch("github_changelog_md.main.ChangeLog")


default_options: ChangelogOptions = {
    "user_name": None,
    "next_release": None,
    "show_unreleased": True,
    "show_depends": True,
    "output_file": "CHANGELOG.md",
    "contributors": False,
    "quiet": False,
    "skip_releases": None,
    "show_issues": True,
    "item_order": "newest-first",
    "ignore_items": None,
    "max_depends": 10,
    "show_diff": True,
    "show_patch": True,
}


def _settings_mock(**overrides: object) -> Mock:
    """Return a settings-like mock with valid defaults."""
    settings = Mock()
    settings.github_pat = "1234"
    settings.unreleased = True
    settings.depends = True
    settings.output_file = "CHANGELOG.md"
    settings.contrib = False
    settings.quiet = False
    settings.skip_releases = None
    settings.show_issues = True
    settings.item_order = "newest-first"
    settings.ignore_items = None
    settings.max_depends = 10
    settings.show_diff = True
    settings.show_patch = True
    settings.yanked = None
    settings.release_text_before = None
    settings.release_text = None
    settings.release_overrides = None
    for key, value in overrides.items():
        setattr(settings, key, value)
    return settings


def _assert_changelog_called(
    mock_changelog: MockType, repo: str, options: ChangelogOptions
) -> None:
    """Assert the CLI created the changelog with orchestration dependencies."""
    mock_changelog.assert_called_once_with(repo, options, ANY, ANY)


@pytest.mark.usefixtures("config_file")
class TestCLI:
    """Test class for the CLI functionality."""

    def test_cli_with_version(self, mocker) -> None:
        """Test the main function with the version flag."""
        runner = CliRunner()
        mock_version = mocker.patch(
            "github_changelog_md.main.get_app_version", return_value="1.0.0"
        )
        # with pytest.raises(typer.Exit, match="0"):
        result = runner.invoke(app, ["--version"])
        mock_version.assert_called_once()
        assert "Github Changelog Markdown" in result.output
        assert "Version: 1.0.0;" in result.output

    def test_cli_with_repo(self, mock_changelog: MockType) -> None:
        """Test the main function with the repo flag."""
        mock_changelog_instance = Mock()
        mock_changelog.return_value = mock_changelog_instance

        runner = CliRunner()
        runner.invoke(app, ["--repo", "test_repo"])
        _assert_changelog_called(mock_changelog, "test_repo", default_options)
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
            (["--contrib"], {"contributors": True}),
            (["--no-contrib"], {"contributors": False}),
            (["--quiet"], {"quiet": True}),
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

        expected_options = cast(
            "ChangelogOptions", {**default_options, **cli_options[1]}
        )
        _assert_changelog_called(mock_changelog, "test_repo", expected_options)
        mock_changelog_instance.run.assert_called_once()

    def test_cli_with_repo_and_user(self, mock_changelog: MockType) -> None:
        """Test the main function with the repo and user flags."""
        mock_changelog_instance = Mock()
        mock_changelog.return_value = mock_changelog_instance

        runner = CliRunner()
        runner.invoke(app, ["--repo", "test_repo", "--user", "test_user"])

        expected_options = cast(
            "ChangelogOptions",
            {**default_options, "user_name": "test_user"},
        )
        _assert_changelog_called(mock_changelog, "test_repo", expected_options)
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

        expected_options = cast(
            "ChangelogOptions",
            {
                **default_options,
                "user_name": "test_user",
                "next_release": "v1.0",
            },
        )
        _assert_changelog_called(mock_changelog, "test_repo", expected_options)
        mock_changelog_instance.run.assert_called_once()

    def test_no_repo_specified_get_from_local_github_repo(
        self,
        mocker: MockerFixture,
        mock_changelog: MockType,
    ) -> None:
        """Test the main function with no repo specified.

        It should read the owner and repo from the local repo.
        """
        mock_changelog_instance = Mock()
        mock_changelog.return_value = mock_changelog_instance

        mocker.patch(
            "github_changelog_md.main.get_repo_remote",
            return_value=GitHubRemote(owner="test_owner", repo="test_repo"),
        )

        runner = CliRunner()
        runner.invoke(app)

        expected_options = cast(
            "ChangelogOptions",
            {**default_options, "user_name": "test_owner"},
        )
        _assert_changelog_called(
            mock_changelog,
            "test_repo",
            expected_options,
        )
        mock_changelog_instance.run.assert_called_once()

    def test_explicit_repo_ignores_local_repo_owner(
        self,
        mocker: MockerFixture,
        mock_changelog: MockType,
    ) -> None:
        """Test explicit repo keeps authenticated-user owner fallback."""
        mock_changelog_instance = Mock()
        mock_changelog.return_value = mock_changelog_instance

        get_repo_remote = mocker.patch(
            "github_changelog_md.main.get_repo_remote",
            return_value=GitHubRemote(owner="local_owner", repo="local_repo"),
        )

        runner = CliRunner()
        runner.invoke(app, ["--repo", "explicit_repo"])

        _assert_changelog_called(
            mock_changelog,
            "explicit_repo",
            default_options,
        )
        get_repo_remote.assert_not_called()
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
            "github_changelog_md.main.get_repo_remote",
            return_value=None,
        )

        runner = CliRunner()
        result = runner.invoke(app)
        assert "Could not find a local repository" in result.output
        mock_changelog.assert_not_called()
        mock_changelog_instance.run.assert_not_called()

    def test_no_pat_given(self, mocker, mock_changelog: MockType) -> None:
        """Test missing PAT exits before constructing ChangeLog."""
        settings = _settings_mock()
        del settings.github_pat
        mocker.patch(
            "github_changelog_md.main.get_settings", return_value=settings
        )

        runner = CliRunner()
        result = runner.invoke(app, ["--repo", "test_repo"])

        assert result.exit_code == ExitErrors.NO_PAT
        assert "No GitHub PAT found in settings file" in result.output
        mock_changelog.assert_not_called()

    def test_cli_rejects_invalid_item_order(
        self,
        mock_changelog: MockType,
    ) -> None:
        """Test invalid item ordering exits before constructing ChangeLog."""
        runner = CliRunner()
        result = runner.invoke(
            app,
            ["--repo", "test_repo", "--item-order", "sideways"],
        )

        assert result.exit_code == ExitErrors.INVALID_ACTION
        assert "item_order must be one of" in result.output
        mock_changelog.assert_not_called()

    def test_cli_rejects_negative_max_depends(
        self,
        mock_changelog: MockType,
    ) -> None:
        """Test negative dependency limits exit before generation."""
        runner = CliRunner()
        result = runner.invoke(
            app,
            ["--repo", "test_repo", "--max-depends=-1"],
        )

        assert result.exit_code == ExitErrors.INVALID_ACTION
        assert "max_depends must be greater than or equal to 0" in result.output
        mock_changelog.assert_not_called()

    def test_cli_accepts_zero_max_depends(
        self,
        mock_changelog: MockType,
    ) -> None:
        """Test zero is a valid dependency display limit."""
        mock_changelog_instance = Mock()
        mock_changelog.return_value = mock_changelog_instance

        runner = CliRunner()
        result = runner.invoke(
            app,
            ["--repo", "test_repo", "--max-depends=0"],
        )

        expected_options = cast(
            "ChangelogOptions",
            {**default_options, "max_depends": 0},
        )
        assert result.exit_code == 0
        _assert_changelog_called(mock_changelog, "test_repo", expected_options)
        mock_changelog_instance.run.assert_called_once()

    def test_cli_rejects_invalid_release_text_config(
        self,
        mocker: MockerFixture,
        mock_changelog: MockType,
    ) -> None:
        """Test malformed release text settings exit before generation."""
        settings = _settings_mock(release_text=[{"release": "v1.0.0"}])
        mocker.patch(
            "github_changelog_md.main.get_settings", return_value=settings
        )

        runner = CliRunner()
        result = runner.invoke(app, ["--repo", "test_repo"])

        assert result.exit_code == ExitErrors.INVALID_ACTION
        assert "release entry 1 is missing 'text'" in result.output
        mock_changelog.assert_not_called()
