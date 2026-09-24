import importlib
import re

import pytest

evals = importlib.import_module("tests.test_menu_chat_evals")



def test_eval_module_grounding_context_has_five_lines():
    assert evals.GROUNDING_CONTEXT.count("\n") == 5


@pytest.mark.parametrize(
    "answer",
    ["Falafel costs 12 EUR.", "Falafel costs 12.00 EUR.", "Falafel costs 12,00 €.", "Price: 12.5", "(12)", "12"],
)
def test_contains_price_accepts_variants(answer):
    evals.assert_contains_price(answer, 12)


@pytest.mark.parametrize(
    "answer",
    ["It costs 112 EUR.", "It costs 120 EUR.", "No price here.", "It costs 18 EUR.", "It costs 1.12 EUR.", "It costs 3,12 EUR.", "Order 12.345 ready."],
)
def test_contains_price_rejects_other_numbers(answer):
    with pytest.raises(AssertionError):
        evals.assert_contains_price(answer, 12)


@pytest.mark.parametrize(
    "answer",
    ["Falafel is 12 EUR.", "Falafel 12,00 € and Pizza 24 EUR.", "No prices at all.", "We have 3 dishes under 20.", "Pizza 24.00 eur"],
)
def test_no_price_below_passes(answer):
    evals.assert_no_price_below(answer, 12)


@pytest.mark.parametrize("answer", ["Soup is 5 EUR.", "Soup is 11,50 €.", "Falafel 12 EUR, water 2 EUR."])
def test_no_price_below_fails(answer):
    with pytest.raises(AssertionError):
        evals.assert_no_price_below(answer, 12)


def test_no_price_below_ignores_decimal_fraction_digits():
    evals.assert_no_price_below("Total 12.50 EUR", 12)


@pytest.mark.parametrize("keyword", evals.NON_MENU_DISH_KEYWORDS)
def test_non_menu_dish_detected_case_insensitive(keyword):
    with pytest.raises(AssertionError):
        evals.assert_no_non_menu_dish(f"We also serve {keyword.upper()} today.")


def test_non_menu_dish_clean_answer_passes():
    evals.assert_no_non_menu_dish("The Falafel Plate costs 12 EUR.")


def test_non_menu_dish_asked_about_is_excluded():
    evals.assert_no_non_menu_dish("Sorry, sushi is not on the menu.", "sushi")


def test_non_menu_dish_other_keyword_still_fails_when_one_excluded():
    with pytest.raises(AssertionError):
        evals.assert_no_non_menu_dish("No sushi, but we have ramen.", "sushi")






@pytest.mark.parametrize(
    "answer",
    ["Sushi is not on the menu.", "No, we don't have sushi.", "We do not serve that.", "Sorry!", "It doesn't exist.", "NOT available"],
)
def test_decline_regex_matches(answer):
    assert evals.DECLINE.search(answer)


@pytest.mark.parametrize("answer", ["Yes, sushi is on the menu.", "Nothing like it.", "Notable dish.", "Knot"])
def test_decline_regex_rejects(answer):
    assert not evals.DECLINE.search(answer)


class FixedJudge:
    def __init__(self, score):
        self.fixed = score
        self.calls = []

    async def score(self, query, response, context):
        self.calls.append((query, response, context))
        return self.fixed, "raw judge output"


async def test_assert_grounded_passes_at_threshold():
    fixed_judge = FixedJudge(evals.PASS_THRESHOLD)
    await evals.assert_grounded(fixed_judge, "q", "a")
    assert fixed_judge.calls == [("q", "a", evals.GROUNDING_CONTEXT)]


async def test_assert_grounded_fails_below_threshold():
    with pytest.raises(AssertionError, match="raw judge output"):
        await evals.assert_grounded(FixedJudge(evals.PASS_THRESHOLD - 1), "q", "a")
