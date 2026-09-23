import pytest

from tester.textkit import slugify, truncate


def test_slugify_lowercases_and_joins_words():
    assert slugify("Hello World") == "hello-world"


def test_slugify_ignores_surrounding_whitespace():
    assert slugify("  Hello World  ") == "hello-world"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello   World", "hello-world"),
        ("Hello, _ World", "hello-world"),
        ("Hello, World!", "hello-world"),
        ("...Hello World", "hello-world"),
    ],
)
def test_slugify_collapses_and_strips_separators(text, expected):
    assert slugify(text) == expected


def test_truncate_leaves_short_text_alone():
    assert truncate("abc", 5) == "abc"


def test_truncate_marks_where_it_cut():
    assert truncate("abcdef", 3) == "ab…"


def test_truncate_rejects_non_positive_limit():
    with pytest.raises(ValueError):
        truncate("abc", 0)
