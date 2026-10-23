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
        ("1h30m", 5400),
        ("2d", 172800),
        ("45s", 45),
        ("1d2h3m4s", 93784),
        ("1m", 60),
        ("  1h30m  ", 5400),
        ("\t45s\n", 45),
        ("1H", 3600),
        ("1H30M", 5400),
        ("2D", 172800),
        ("05m", 300),
        ("0005m", 300),
        ("365d", 365 * 86400),
        ("8760h", 365 * 86400),
        ("0" * 50 + "1s", 1),
    ],
)
def test_parse_duration_accepts_valid_input(text, seconds):
    assert parse_duration(text) == seconds


@pytest.mark.parametrize(
    "bad",
    [
        "30m1h",
        "1h1h",
        "1s1m",
        "1m1d",
        "1h 30m",
        "1 h",
        "1h\t30m",
        "",
        "   ",
        "90",
        "-5m",
        "-1h",
        "h",
        "1hm",
        "5x",
        "5w",
        "1.5h",
        "+5m",
        "366d",
        "365d1s",
        "31536001s",
        "9" * 5000 + "s",
    ],
)
def test_parse_duration_rejects_invalid_input(bad):
    with pytest.raises(ValueError, match=re.escape(repr(bad))):
        parse_duration(bad)


@pytest.mark.parametrize("bad", ["30m1h", " 1h 30m ", "366d", ""])
def test_parse_duration_error_message_contains_original_input(bad):
    with pytest.raises(ValueError, match=re.escape(repr(bad))):
        parse_duration(bad)


def test_parse_duration_huge_digit_string_gets_our_message():
    with pytest.raises(ValueError, match="duration"):
        parse_duration("9" * 5000 + "s")


@pytest.mark.parametrize(
    ("text", "seconds"),
    [
        ("0s", 0),
        ("00d00h00m00s", 0),
        ("1D2H3M4S", 93784),
        ("1d2H3m4S", 93784),
        ("364d24h", 365 * 86400),
        ("364d23h59m60s", 365 * 86400),
        (" 5m ", 300),
        ("\n1d\n", 86400),
    ],
)
def test_parse_duration_boundaries_whitespace_and_case(text, seconds):
    assert parse_duration(text) == seconds


@pytest.mark.parametrize(
    "bad",
    [
        "364d25h",
        "365d0h1m",
        "1h30",
        "1h30m1",
        "1h\n30m",
        "1\x00s",
        "1h,30m",
        "1h30m,",
        "٣s",  # Arabic-indic digit
        "３s",  # full-width digit
        "1K",  # Kelvin sign must not case-fold to a unit
        "1ſ",  # long s must not case-fold to "s"
        "9" * 5000 + "d",
        "9" * 5000 + "h",
        "9" * 5000 + "m",
        "1d" + "9" * 5000 + "s",
    ],
)
def test_parse_duration_rejects_edge_inputs_with_input_in_message(bad):
    with pytest.raises(ValueError, match=re.escape(repr(bad))):
        parse_duration(bad)


def test_parse_duration_error_message_uses_unstripped_input():
    text = "  30m1h\n"
    with pytest.raises(ValueError) as excinfo:
        parse_duration(text)
    assert repr(text) in str(excinfo.value)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "bug: int() on >4300 leading zeros raises Python's own 'Exceeds the "
        "limit (4300 digits)' ValueError, which omits the offending input "
        "(rule 8) and rejects an input that rule 6 says is allowed"
    ),
)
@pytest.mark.parametrize(
    ("text", "seconds"),
    [("0" * 5000 + "1s", 1), ("0" * 5000 + "s", 0), ("0" * 5000 + "1m", 60)],
)
def test_parse_duration_very_long_leading_zeros(text, seconds):
    # Either parsing succeeds (leading zeros are allowed) or, if rejected,
    # the error must still carry the offending input.
    try:
        result = parse_duration(text)
    except ValueError as exc:
        assert repr(text) in str(exc)
    else:
        assert result == seconds
