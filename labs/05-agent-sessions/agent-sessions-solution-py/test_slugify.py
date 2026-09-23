import pytest

from slugify import slugify


def test_slugifies_an_ordinary_title():
    assert slugify("Hello World") == "hello-world"


def test_collapses_runs_of_non_alphanumeric_characters_into_one_hyphen():
    assert slugify("Agent   Sessions --- Lab #5!") == "agent-sessions-lab-5"


def test_strips_leading_and_trailing_hyphens():
    assert slugify("  ...Trimmed Title...  ") == "trimmed-title"


def test_returns_an_empty_string_for_the_empty_string():
    assert slugify("") == ""


@pytest.mark.parametrize("value", [None, 42, {}, ["a"], b"bytes"])
def test_returns_an_empty_string_for_non_string_input(value):
    assert slugify(value) == ""


@pytest.mark.parametrize("value", ["---", "!!! ??? ..."])
def test_returns_an_empty_string_when_the_input_is_only_punctuation(value):
    assert slugify(value) == ""


def test_folds_accented_latin_characters_to_their_ascii_base():
    assert slugify("Café Über") == "cafe-uber"


def test_treats_a_letter_with_no_ascii_decomposition_as_a_separator():
    assert slugify("Straße Zwei") == "stra-e-zwei"


def test_returns_an_empty_string_for_scripts_with_no_ascii_equivalent():
    assert slugify("日本語") == ""
