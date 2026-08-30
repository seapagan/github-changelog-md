"""Python-Markdown extension for Google-style admonitions."""

import re

from markdown import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

ADMONITION_TYPES: dict[str, str] = {
    "NOTE": "note",
    "TIP": "tip",
    "WARNING": "warning",
    "IMPORTANT": "info",
    "CAUTION": "danger",
}
ADMONITION_PATTERN = re.compile(
    r"^> \[!(NOTE|TIP|WARNING|IMPORTANT|CAUTION)\]\n>"
    r"([\s\S]*?)(?=\n(?!>)|\Z)",
    flags=re.MULTILINE,
)


def replace_admonition(match: re.Match[str]) -> str:
    """Convert a Google-style alert to a Material admonition."""
    original_type = match.group(1)
    content = match.group(2).strip()
    content_lines = [line.lstrip(">").strip() for line in content.split("\n")]

    while content_lines and not content_lines[0]:
        content_lines.pop(0)

    indented_content = "\n".join(
        f"    {line}" if line else "" for line in content_lines
    )
    return (
        f'!!! {ADMONITION_TYPES[original_type]} "{original_type.title()}"\n\n'
        f"{indented_content}\n"
    )


class GoogleStyleNotesPreprocessor(Preprocessor):
    """Convert alerts after snippets have expanded included Markdown."""

    def run(self, lines: list[str]) -> list[str]:
        """Convert all Google-style alerts in the expanded source."""
        converted = ADMONITION_PATTERN.sub(
            replace_admonition,
            "\n".join(lines),
        )
        return converted.split("\n")


class GoogleStyleNotesExtension(Extension):
    """Register Google-style alert conversion in the Markdown pipeline."""

    def extend_markdown(self, md: Markdown) -> None:
        """Run after the snippets preprocessor, which uses priority 32."""
        md.registerExtension(self)
        md.preprocessors.register(
            GoogleStyleNotesPreprocessor(md),
            "google_style_notes",
            31,
        )


setattr(
    GoogleStyleNotesExtension,
    Extension.extendMarkdown.__name__,
    GoogleStyleNotesExtension.extend_markdown,
)
