import pytest

from tester.textkit import slugify, truncate, word_count


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


def test_word_count_counts_words():
    assert word_count("hello world") == 2


def test_word_count_ignores_extra_whitespace():
    assert word_count("  spaced   out  ") == 2


def test_word_count_empty_string_is_zero():
    assert word_count("") == 0
