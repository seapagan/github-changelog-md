"""Validate and normalize changelog configuration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:  # pragma: no cover
    from github_changelog_md.config.settings import Settings
    from github_changelog_md.constants import ChangelogOptions

ItemOrder = Literal["newest-first", "oldest-first"]

VALID_ITEM_ORDERS: tuple[ItemOrder, ...] = ("newest-first", "oldest-first")


class ChangelogConfigError(ValueError):
    """Raised when changelog configuration is invalid."""


@dataclass(frozen=True, slots=True)
class ReleaseConfigEntry:
    """Normalized release-specific text configuration."""

    release: str
    value: str


def validate_item_order(value: str) -> ItemOrder:
    """Return a valid item order or raise a config error."""
    if value in VALID_ITEM_ORDERS:
        return value
    valid_values = ", ".join(VALID_ITEM_ORDERS)
    msg = f"item_order must be one of: {valid_values}"
    raise ChangelogConfigError(msg)


def validate_max_depends(value: int) -> int:
    """Return a valid dependency display limit."""
    if value >= 0:
        return value
    msg = "max_depends must be greater than or equal to 0"
    raise ChangelogConfigError(msg)


def validate_changelog_options(
    options: ChangelogOptions,
) -> ChangelogOptions:
    """Validate resolved changelog options before running generation."""
    options["item_order"] = validate_item_order(options["item_order"])
    options["max_depends"] = validate_max_depends(options["max_depends"])
    return options


def validate_settings(settings: Settings) -> None:
    """Validate settings values that need stricter domain checks."""
    validate_item_order(settings.item_order)
    validate_max_depends(settings.max_depends)
    normalize_release_entries(settings.yanked, value_key="reason")
    normalize_release_entries(settings.release_text_before, value_key="text")
    normalize_release_entries(settings.release_text, value_key="text")
    normalize_release_entries(settings.release_overrides, value_key="text")


def normalize_release_entries(
    values: list[dict[str, str]] | None,
    value_key: str,
    *,
    strip_value: bool = False,
) -> dict[str, str]:
    """Build a release-tag keyed lookup table from config entries."""
    if not values:
        return {}

    lookup: dict[str, str] = {}
    for entry in _release_config_entries(
        values,
        value_key=value_key,
        strip_value=strip_value,
    ):
        lookup[entry.release] = entry.value
    return lookup


def _release_config_entries(
    values: list[dict[str, str]],
    value_key: str,
    *,
    strip_value: bool,
) -> list[ReleaseConfigEntry]:
    """Return normalized release config entries."""
    entries: list[ReleaseConfigEntry] = []
    for index, value in enumerate(values, start=1):
        release = _required_value(value, "release", index).strip()
        text = _required_value(value, value_key, index)
        if strip_value:
            text = text.strip()
        if not release:
            msg = f"release entry {index} has an empty release tag"
            raise ChangelogConfigError(msg)
        entries.append(ReleaseConfigEntry(release=release, value=text))
    return entries


def _required_value(
    value: dict[str, str],
    key: str,
    index: int,
) -> str:
    """Return a required release config value."""
    try:
        result = value[key]
    except KeyError as exc:
        msg = f"release entry {index} is missing '{key}'"
        raise ChangelogConfigError(msg) from exc
    if not isinstance(result, str):
        msg = f"release entry {index} value '{key}' must be a string"
        raise ChangelogConfigError(msg)
    return result
