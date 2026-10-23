import pytest

from tester.textkit import safe_filename, slugify, truncate


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


def test_safe_filename_neutralises_path_traversal():
    result = safe_filename("../../etc/passwd")
    assert result == "_.._etc_passwd"
    assert "/" not in result and "\\" not in result


def test_safe_filename_neutralises_windows_traversal():
    assert safe_filename("..\\..\\windows\\system32") == "_.._windows_system32"


@pytest.mark.parametrize("name", [".", "..", "..."])
def test_safe_filename_maps_dot_only_names_to_file(name):
    assert safe_filename(name) == "file"


def test_safe_filename_removes_leading_dots():
    assert safe_filename(".bashrc") == "bashrc"
    assert safe_filename("...hidden") == "hidden"


def test_safe_filename_keeps_allowed_characters():
    assert safe_filename("report-2024_v1.final.txt") == "report-2024_v1.final.txt"


def test_safe_filename_replaces_other_characters():
    assert safe_filename("my file?.txt") == "my_file_.txt"


def test_safe_filename_replaces_non_ascii_characters():
    result = safe_filename("héllo wörld.txt")
    assert result == "h_llo_w_rld.txt"
    assert result.isascii()


def test_safe_filename_empty_input_becomes_file():
    assert safe_filename("") == "file"


def test_safe_filename_caps_length_at_100():
    assert safe_filename("a" * 150) == "a" * 100
    assert len(safe_filename("." + "b" * 200)) == 100


@pytest.mark.parametrize(
    "name",
    ["../../etc/passwd", "..\\..\\windows\\system32", ".", "..", "...", ".bashrc", "...hidden", "my file?.txt", "héllo wörld.txt", "", "a" * 150],
)
def test_safe_filename_properties(name):
    result = safe_filename(name)
    assert 0 < len(result) <= 100
    assert "/" not in result and "\\" not in result
    assert not result.startswith(".")
    assert result not in {".", ".."}
