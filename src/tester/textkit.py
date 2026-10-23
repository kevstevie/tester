"""Small text helpers."""

import re

_NON_ALNUM = re.compile(r"[^a-z0-9]")
_UNSAFE_FILENAME_CHARS = re.compile(r"[^A-Za-z0-9._-]")
_MAX_FILENAME_LENGTH = 100


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


def safe_filename(name: str) -> str:
    """Turn arbitrary text into a file name that is safe to create in a directory.

    Guarantees for the returned string:
    - it is non-empty and at most 100 characters long;
    - it contains only ASCII letters, digits, ``.``, ``-`` and ``_``
      (any other character, including non-ASCII letters, becomes ``_``),
      so it never contains ``/``, ``\\`` or control characters;
    - it does not start with ``.``, so it is never ``.``, ``..`` or a hidden file;
    - an input that leaves nothing usable yields ``"file"``.
    """
    replaced = _UNSAFE_FILENAME_CHARS.sub("_", name)
    without_leading_dots = replaced.lstrip(".")
    limited = without_leading_dots[:_MAX_FILENAME_LENGTH]
    return limited or "file"
