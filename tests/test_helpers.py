"""Test module to test the 'helpers' module."""

from __future__ import annotations

from importlib import metadata
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from github_changelog_md.constants import ExitErrors, SectionHeadings
from github_changelog_md.helpers import (
    cap_first_letter,
    get_app_version,
    get_index_of_tuple,
    get_repo_name,
    get_section_name,
    header,
    strip_first_alpha_char,
    title_unique,
)

if TYPE_CHECKING:
    from pyfakefs.fake_filesystem import FakeFileSystem
    from pytest_mock import MockerFixture


@pytest.fixture
def sample_section_headings() -> list[SectionHeadings]:
    """Fixture for providing a sample list of section headings."""
    return [
        ("Introduction", None),
        ("Methods", "1.0"),
        ("Results", "2.0"),
        ("Discussion", None),
    ]


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
                ),
            ),
        )
        assert get_repo_name() == "repo"

    def test_get_repo_name_without_git_config(
        self,
        mocker: MockerFixture,
    ) -> None:
        """Test get_repo_name function without a git config file."""
        mocker.patch("pathlib.Path.exists", return_value=False)
        assert get_repo_name() is None

    def test_header(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that the header function prints the correct output."""
        header()
        captured = capsys.readouterr()
        assert "GitHub Changelog Generator" in captured.out

    def test_get_app_version_with_toml_file(
        self,
        fs: FakeFileSystem,
        mocker: MockerFixture,
    ) -> None:
        """Test get_app_version function with a valid pyproject.toml file."""
        fs.create_file(
            self.test_toml_path,
            contents=(
                '[project]\nname = "github_changelog_md"\nversion = "0.5.0"\n'
            ),
        )
        mocker.patch(
            self.patch_get_toml,
            return_value=Path(self.test_toml_path),
        )
        assert get_app_version() == "0.5.0"

    def test_get_app_version_bad_toml_file(
        self,
        fs: FakeFileSystem,
        mocker: MockerFixture,
    ) -> None:
        """Test get_app_version function with a bad pyproject.toml file."""
        fs.create_file(
            self.test_toml_path,
            contents=('[project]\nname = "github_changelog_md"\n'),
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

    def test_cap_first_letter(self) -> None:
        """Test cap_first_letter function."""
        result = cap_first_letter("this IS a TeST strIng")
        assert result == "This IS a TeST strIng"

    def test_get_section_name(self) -> None:
        """The the get_section_name function.

        We just test a couple of the sections. This will break if we change any
        of the section names, but that's what tests are for!
        """
        assert get_section_name("bug") == "Bug Fixes"
        assert get_section_name("dependencies") == "Dependency Updates"
        assert get_section_name("not_a_label") is None
        assert get_section_name(None) == "Merged Pull Requests"

    def test_get_index_of_tuple_found(self, sample_section_headings) -> None:
        """Test get_index_of_tuple returns correct index when value is found."""
        index = get_index_of_tuple(sample_section_headings, 0, "Methods")
        assert index == 1, "Expected index of 1"

    def test_get_index_of_tuple_not_found(
        self, sample_section_headings
    ) -> None:
        """Test get_index_of_tuple raises ValueError when value is not found."""
        with pytest.raises(
            ValueError, match="not in the supplied list of Tuples"
        ) as exc_info:
            get_index_of_tuple(sample_section_headings, 0, "Conclusion")
        assert "'Conclusion' is not in the supplied list of Tuples" in str(
            exc_info.value
        ), "Expected a ValueError indicating 'Conclusion' was not found"

    def test_get_index_of_tuple_with_none_value(
        self, sample_section_headings
    ) -> None:
        """Test get_index_of_tuple when searching for None value."""
        index = get_index_of_tuple(sample_section_headings, 1, None)
        assert index == 0, (
            "Expected index of 0 for the first occurrence of None value"
        )

    def test_get_index_of_tuple_empty_list(self) -> None:
        """Test get_index_of_tuple with an empty list."""
        with pytest.raises(
            ValueError, match="not in the supplied list of Tuples"
        ) as exc_info:
            get_index_of_tuple([], 0, "Introduction")
        assert "'Introduction' is not in the supplied list of Tuples" in str(
            exc_info.value
        ), "Expected a ValueError, 'Introduction' was not found in empty list"

    def test_strip_first_alpha(self) -> None:
        """Test strip_first_alpha_char function."""
        assert strip_first_alpha_char("v1.0.0") == "1.0.0"
        assert strip_first_alpha_char("1.0.0") == "1.0.0"
        assert strip_first_alpha_char("a1.0.0") == "1.0.0"
        assert strip_first_alpha_char("a") == ""
        assert strip_first_alpha_char("") == ""

    @pytest.mark.parametrize(
        ("title", "tag_name", "expected"),
        [
            ("v1.0.0", "1.0.0", False),
            ("v1.0.0", "2.0.0", True),
            ("V1.0.0", "", False),
            ("", "1.0.0", False),
        ],
    )
    def test_title_unique(self, mocker, title, tag_name, expected) -> None:
        """Test the title_unique function."""
        release = mocker.Mock()
        release.title = title
        release.tag_name = tag_name

        assert title_unique(release) is expected
