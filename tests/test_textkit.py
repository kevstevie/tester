import re

import pytest

from tester.textkit import parse_duration, slugify, truncate


def test_slugify_lowercases_and_joins_words():
    assert slugify("Hello World") == "hello-world"


def test_slugify_ignores_surrounding_whitespace():
    assert slugify("  Hello World  ") == "hello-world"


def test_truncate_leaves_short_text_alone():
    assert truncate("abc", 5) == "abc"


def test_truncate_marks_where_it_cut():
    assert truncate("abcdef", 3) == "ab…"


def test_truncate_rejects_non_positive_limit():
    with pytest.raises(ValueError):
        truncate("abc", 0)


@pytest.mark.parametrize(
    ("text", "seconds"),
    [
        # rule 1: one or more <integer><unit> parts
        ("1h30m", 5400),
        ("2d", 172800),
        ("45s", 45),
        ("1d2h3m4s", 93784),
        ("1m", 60),
        # rule 2: strictly decreasing order, each unit at most once
        ("364d24h", 365 * 86400),
        ("364d23h59m60s", 365 * 86400),
        # rule 3: surrounding whitespace is ignored
        ("  1h30m  ", 5400),
        ("\t45s\n", 45),
        (" 5m ", 300),
        ("\n1d\n", 86400),
        # rule 4: uppercase units
        ("1H", 3600),
        ("1H30M", 5400),
        ("2D", 172800),
        ("1D2H3M4S", 93784),
        ("1d2H3m4S", 93784),
        # rule 6: leading zeros
        ("05m", 300),
        ("0005m", 300),
        ("0s", 0),
        ("00d00h00m00s", 0),
        ("0" * 50 + "1s", 1),
        ("0" * 5000 + "1s", 1),
        ("0" * 5000 + "s", 0),
        ("0" * 5000 + "1m", 60),
        # rule 7: exactly 365 days is allowed
        ("365d", 365 * 86400),
        ("8760h", 365 * 86400),
    ],
)
def test_parse_duration_accepts_valid_input(text, seconds):
    assert parse_duration(text) == seconds


@pytest.mark.parametrize(
    "bad",
    [
        # rule 2: wrong order or repeated units
        "30m1h",
        "1h1h",
        "1s1m",
        "1m1d",
        # rule 3: whitespace inside is rejected
        "1h 30m",
        " 1h 30m ",
        "  30m1h\n",
        "1 h",
        "1h\t30m",
        "1h\n30m",
        # rule 5: empty input, bare number, negative, zero-length part, unknown unit
        "",
        "   ",
        "90",
        "1h30",
        "1h30m1",
        "-5m",
        "-1h",
        "+5m",
        "h",
        "1hm",
        "5x",
        "5w",
        "1.5h",
        "1h,30m",
        "1h30m,",
        "1\x00s",
        # rule 4/5: only ASCII digits and the exact unit letters count
        "٣s",  # Arabic-indic digit
        "３s",  # full-width digit
        "1K",  # Kelvin sign must not case-fold to a unit
        "1ſ",  # long s must not case-fold to "s"
        # rule 7: more than 365 days, including huge digit strings
        "366d",
        "365d1s",
        "31536001s",
        "364d25h",
        "365d0h1m",
        "9" * 5000 + "s",
        "9" * 5000 + "d",
        "9" * 5000 + "h",
        "9" * 5000 + "m",
        "1d" + "9" * 5000 + "s",
    ],
)
def test_parse_duration_rejects_invalid_input(bad):
    # rule 8: the error message includes repr() of the original (unstripped) input
    with pytest.raises(ValueError, match=re.escape(repr(bad))):
        parse_duration(bad)


def test_parse_duration_huge_digit_string_gets_our_message():
    # Must be rejected by our own guard, not by Python's int() digit limit.
    with pytest.raises(ValueError, match="duration component too large"):
        parse_duration("9" * 5000 + "s")
