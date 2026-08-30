"""Tests for the documentation Markdown extensions."""

from pathlib import Path

import markdown
import pytest


def test_sourced_admonitions_are_converted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Convert alerts after the snippets extension expands a source file."""
    (tmp_path / "included.md").write_text(
        "> [!TIP]\n>\n> Linked content.\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    rendered = markdown.markdown(
        '--8<-- "included.md"',
        extensions=[
            "admonition",
            "pymdownx.snippets",
            "docs.hooks.google_style_notes:GoogleStyleNotesExtension",
        ],
    )

    assert '<div class="admonition tip">' in rendered
    assert '<p class="admonition-title">Tip</p>' in rendered
    assert "<p>Linked content.</p>" in rendered
    assert "--8<--" not in rendered
