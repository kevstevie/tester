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


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("/etc/passwd", "_etc_passwd"),
        ("../secret", "_secret"),
        ("a/../b", "a_.._b"),
        ("foo/..", "foo_.."),
        ("/..", "_.."),
        ("\\", "_"),
        ("a\\b/c", "a_b_c"),
    ],
)
def test_safe_filename_replaces_each_path_separator(name, expected):
    assert safe_filename(name) == expected


def test_safe_filename_keeps_inner_and_trailing_dots():
    assert safe_filename("a..b") == "a..b"
    assert safe_filename("archive.tar.gz") == "archive.tar.gz"
    assert safe_filename("name.") == "name."


def test_safe_filename_only_strips_dots_that_lead_the_sanitised_name():
    # A leading separator becomes "_", so the dots after it are no longer leading.
    assert safe_filename("/.hidden") == "_.hidden"
    # Characters replaced by "_" are not dots, so they shield the dots behind them.
    assert safe_filename(" .x") == "_.x"


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("naïve", "na_ve"),
        ("日本語.txt", "___.txt"),
        ("😀", "_"),
        ("a😀b", "a_b"),
        ("e\u0301", "e_"),  # "e" plus a combining accent
        ("\uff0e\uff0e\uff0f\uff0e\uff0e", "_____"),  # fullwidth "../.." lookalikes
        ("\u202etxt.exe", "_txt.exe"),  # right-to-left override
    ],
)
def test_safe_filename_replaces_each_unicode_code_point_with_one_underscore(name, expected):
    assert safe_filename(name) == expected


def test_safe_filename_unicode_only_input_stays_non_empty_and_ascii():
    result = safe_filename("日本語")
    assert result == "___"
    assert result.isascii()


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("a\x00b", "a_b"),
        ("a\nb", "a_b"),
        ("a\tb\r\n", "a_b__"),
        ("\x1b[31mred", "__31mred"),
        (" ", "_"),
        ("   ", "___"),
    ],
)
def test_safe_filename_replaces_control_and_whitespace_characters(name, expected):
    assert safe_filename(name) == expected


@pytest.mark.parametrize("name", ["...", ". . .", "..", ".", "...."])
def test_safe_filename_never_returns_dot_entries(name):
    assert safe_filename(name) not in {".", ".."}


def test_safe_filename_length_boundaries():
    assert safe_filename("a" * 99) == "a" * 99
    assert safe_filename("a" * 100) == "a" * 100
    assert safe_filename("a" * 101) == "a" * 100


def test_safe_filename_strips_leading_dots_before_limiting_length():
    assert safe_filename("." * 50 + "a" * 100) == "a" * 100
    assert safe_filename("." * 500) == "file"


def test_safe_filename_cuts_trailing_dots_beyond_the_limit():
    result = safe_filename("a" * 100 + "..")
    assert result == "a" * 100


def test_safe_filename_counts_replaced_characters_towards_the_limit():
    assert safe_filename("é" * 150) == "_" * 100


def test_safe_filename_is_idempotent():
    for name in ["../../etc/passwd", ".bashrc", "héllo wörld.txt", "", "a" * 150, "..", "ok.txt"]:
        once = safe_filename(name)
        assert safe_filename(once) == once


@pytest.mark.parametrize(
    "name",
    [
        "../../etc/passwd",
        "..\\..\\windows\\system32",
        "/absolute/path",
        "C:\\Users\\me\\file.txt",
        ".",
        "..",
        "",
        "日本語/../😀",
        "a\x00../b",
        "." * 300,
        "x/" * 200,
    ],
)
def test_safe_filename_result_uses_only_the_allowed_alphabet(name):
    result = safe_filename(name)
    assert result
    assert len(result) <= 100
    assert set(result) <= set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.")
    assert not result.startswith(".")


@pytest.mark.parametrize(
    "name",
    ["../../etc/passwd", "..\\..\\evil", "/tmp/evil", "..", ".", "", ".hidden", "a" * 300, "日本語"],
)
def test_safe_filename_creates_file_directly_inside_target_directory(tmp_path, name):
    target = tmp_path / "uploads"
    target.mkdir()

    created = target / safe_filename(name)
    created.write_text("data")

    assert created.parent == target
    assert created.resolve().parent == target.resolve()
    assert created.is_file()
    assert [p.name for p in tmp_path.iterdir()] == ["uploads"]
    assert not any(p.name.startswith(".") for p in target.iterdir())
