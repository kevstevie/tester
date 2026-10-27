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


def test_reverse_words_returns_single_word_unchanged():
    assert reverse_words("hello") == "hello"


def test_reverse_words_strips_whitespace_around_single_word():
    assert reverse_words("  hello\n") == "hello"


def test_reverse_words_result_has_no_leading_or_trailing_whitespace():
    result = reverse_words("\n  alpha beta \t")
    assert result == result.strip()
    assert result == "beta alpha"


def test_reverse_words_keeps_non_ascii_words_intact():
    assert reverse_words("héllo wörld ✓") == "✓ wörld héllo"


def test_reverse_words_twice_normalizes_whitespace_and_restores_order():
    assert reverse_words(reverse_words("  one   two three ")) == "one two three"
