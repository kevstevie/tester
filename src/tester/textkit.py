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


_DURATION = re.compile(
    r"(?:(?P<d>[0-9]+)d)?(?:(?P<h>[0-9]+)h)?(?:(?P<m>[0-9]+)m)?(?:(?P<s>[0-9]+)s)?",
    re.IGNORECASE | re.ASCII,
)
_UNIT_SECONDS = {"d": 86_400, "h": 3_600, "m": 60, "s": 1}
_MAX_SECONDS = 365 * 86_400  # 31_536_000
_MAX_SIGNIFICANT_DIGITS = len(str(_MAX_SECONDS))  # 8


def _duration_error(text: str, reason: str) -> ValueError:
    return ValueError(f"{reason}: {text!r}")


def parse_duration(text: str) -> int:
    """Parse a duration such as "1h30m" into a number of seconds.

    Rules:
    - one or more <integer><unit> parts, units d, h, m, s (case-insensitive)
    - units must appear in decreasing order and at most once
    - surrounding whitespace is ignored; inner whitespace is rejected
    - leading zeros are allowed
    - the total must not exceed 365 days
    """
    match = _DURATION.fullmatch(text.strip())
    if match is None or all(value is None for value in match.groupdict().values()):
        raise _duration_error(text, "invalid duration")

    total = 0
    for unit, digits in match.groupdict().items():
        if digits is None:
            continue
        # Strip leading zeros first so that int() never sees an over-long string.
        significant = digits.lstrip("0") or "0"
        if len(significant) > _MAX_SIGNIFICANT_DIGITS:
            raise _duration_error(text, "duration component too large")
        total += int(significant) * _UNIT_SECONDS[unit]

    if total > _MAX_SECONDS:
        raise _duration_error(text, "duration exceeds 365 days")
    return total
