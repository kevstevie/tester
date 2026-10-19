"""Small text helpers."""

import re

_NON_ALNUM = re.compile(r"[^a-z0-9]")


def slugify(text: str) -> str:
    """Convert text into a URL-friendly slug."""
    lowered = text.strip().lower()
    return _NON_ALNUM.sub("-", lowered)


def truncate(text: str, limit: int) -> str:
    """Shorten text to at most limit characters, marking where it was cut."""
    if limit <= 0:
        raise ValueError("limit must be positive")
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def word_count(text: str) -> int:
    """Return the number of whitespace-separated words in text."""
    return len(text.split())
