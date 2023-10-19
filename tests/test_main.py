from unittest.mock import Mock

import pytest
from typer.testing import CliRunner

from github_changelog_md.main import app


@pytest.fixture()
def mock_changelog(mocker):
    return mocker.patch("github_changelog_md.main.ChangeLog")


def test_main_with_versio():
    runner = CliRunner()
    result = runner.invoke(app, ["--version"])
    assert "Github Changelog Markdown" in result.output


def test_main_with_repo(mock_changelog):
    mock_changelog_instance = Mock()
    mock_changelog.return_value = mock_changelog_instance

    runner = CliRunner()
    runner.invoke(app, ["--repo", "test_repo"])
    mock_changelog.assert_called_once_with("test_repo", None, None)
    mock_changelog_instance.run.assert_called_once()


def test_main_with_repo_and_user(mock_changelog):
    mock_changelog_instance = Mock()
    mock_changelog.return_value = mock_changelog_instance

    runner = CliRunner()
    runner.invoke(app, ["--repo", "test_repo", "--user", "test_user"])
    mock_changelog.assert_called_once_with("test_repo", "test_user", None)
    mock_changelog_instance.run.assert_called_once()


def test_main_with_repo_and_user_and_next_release(mock_changelog):
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
    mock_changelog.assert_called_once_with("test_repo", "test_user", "v1.0")
    mock_changelog_instance.run.assert_called_once()
