import pytest

from tester.textkit import slugify, truncate


def test_slugify_lowercases_and_joins_words():
    assert slugify("Hello World") == "hello-world"


def test_slugify_ignores_surrounding_whitespace():
    assert slugify("  Hello World  ") == "hello-world"


def test_truncate_leaves_short_text_alone():
    assert truncate("abc", 5) == "abc"


def test_truncate_marks_where_it_cut():
    assert truncate("abcdef", 3) == "ab…"


def test_truncate_cuts_at_last_space_instead_of_splitting_word():
    result = truncate("hello wonderful world", 12)
    assert result == "hello…"
    assert len(result) <= 12


def test_truncate_hard_cuts_when_no_space_available():
    assert truncate("abcdefghijkl", 5) == "abcd…"


def test_truncate_keeps_whole_word_when_cut_lands_on_boundary():
    assert truncate("hello world again", 12) == "hello world…"


def test_truncate_rejects_non_positive_limit():
    with pytest.raises(ValueError):
        truncate("abc", 0)
