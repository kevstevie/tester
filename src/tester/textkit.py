"""Small text helpers."""

import re

_NON_ALNUM = re.compile(r"[^a-z0-9]")


def slugify(text: str) -> str:
    """Convert text into a URL-friendly slug."""
    lowered = text.strip().lower()
    return _NON_ALNUM.sub("-", lowered)


def truncate(text: str, limit: int) -> str:
    """Shorten text to at most limit characters, marking where it was cut.

    If the cut would fall inside a word, the text is cut at the last space
    before the limit instead, so whole words are kept when possible. If there
    is no such space, the text is cut hard at the limit.
    """
    if limit <= 0:
        raise ValueError("limit must be positive")
    if len(text) <= limit:
        return text
    kept = text[: limit - 1]
    inside_word = bool(kept) and not kept[-1].isspace() and not text[limit - 1].isspace()
    if inside_word:
        space = kept.rfind(" ")
        if space > 0:
            kept = kept[:space]
    return kept.rstrip() + "…"
