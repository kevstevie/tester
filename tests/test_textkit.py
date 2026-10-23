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


def test_truncate_cuts_at_the_last_space_not_the_first():
    assert truncate("one two three four", 14) == "one two three…"


def test_truncate_does_not_leave_trailing_whitespace_before_ellipsis():
    assert truncate("hello   wonderful", 10) == "hello…"


def test_truncate_cuts_at_word_end_when_limit_just_reaches_the_next_word():
    # The ellipsis takes the slot of the first dropped character, so a word
    # that would only fit without the ellipsis must be dropped as well.
    assert truncate("hello wonderful world", 20) == "hello wonderful…"
    assert truncate("hello wonderful world", 7) == "hello…"


def test_truncate_returns_text_unchanged_when_exactly_at_limit():
    assert truncate("hello wonderful world", 21) == "hello wonderful world"


def test_truncate_with_limit_of_one_returns_only_the_ellipsis():
    assert truncate("abcdef", 1) == "…"


def test_truncate_hard_cuts_a_single_long_word_even_with_spaces_after_it():
    # The only space comes after the cut, so there is nothing earlier to use.
    assert truncate("abcdefghij klm", 5) == "abcd…"


@pytest.mark.parametrize(
    "text",
    [
        "hello wonderful world",
        "abcdefghijklmnop",
        "a b c d e f g h i j",
        "hello   wonderful   world",
        "one two three four five six",
    ],
)
def test_truncate_never_exceeds_limit(text):
    for limit in range(1, len(text) + 3):
        result = truncate(text, limit)
        assert len(result) <= limit, (text, limit, result)
        if len(text) > limit:
            assert result.endswith("…")


def test_truncate_rejects_non_positive_limit():
    with pytest.raises(ValueError):
        truncate("abc", 0)
