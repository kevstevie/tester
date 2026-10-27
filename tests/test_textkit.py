import pytest

from tester.textkit import reverse_words, slugify, truncate


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


def test_reverse_words_reverses_word_order():
    assert reverse_words("hello big world") == "world big hello"


def test_reverse_words_drops_extra_and_surrounding_whitespace():
    assert reverse_words("  one   two  ") == "two one"


def test_reverse_words_treats_tabs_and_newlines_as_separators():
    assert reverse_words("a\tb\n c") == "c b a"


def test_reverse_words_returns_empty_string_for_empty_input():
    assert reverse_words("") == ""


def test_reverse_words_returns_empty_string_for_whitespace_only_input():
    assert reverse_words("   \t ") == ""
