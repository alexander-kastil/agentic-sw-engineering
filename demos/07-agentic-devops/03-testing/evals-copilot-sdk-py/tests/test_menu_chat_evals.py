import re

import pytest

from judge import PASS_THRESHOLD, GroundednessJudge
from menu_assistant import MenuAssistant
from menu_catalog import build_grounding_context

GROUNDING_CONTEXT = build_grounding_context()

NON_MENU_DISH_KEYWORDS = ["sushi", "ramen", "burger", "taco", "sashimi", "dumpling", "curry", "kebab"]

DECLINE = re.compile(r"\b(not|no|don't|do not|doesn't|does not|sorry)\b", re.IGNORECASE)


@pytest.fixture(scope="module")
def assistant() -> MenuAssistant:
    return MenuAssistant()


@pytest.fixture(scope="module")
def judge() -> GroundednessJudge:
    return GroundednessJudge()


def assert_contains_price(answer: str, price: int) -> None:
    assert re.search(rf"(?<![\d.,]){price}(?:[.,]\d{{1,2}})?(?!\d|[.,]\d)", answer), f"Expected price {price} in answer: {answer}"


def assert_no_price_below(answer: str, minimum: int) -> None:
    for match in re.finditer(r"(?<![\d.,])(\d{1,3})(?:[.,]\d{1,2})?\s*(?:EUR|€)", answer, re.IGNORECASE):
        assert int(match.group(1)) >= minimum, f"Unexpected price below {minimum} EUR in answer: {answer}"


def assert_no_non_menu_dish(answer: str, asked_about: str | None = None) -> None:
    for keyword in NON_MENU_DISH_KEYWORDS:
        if keyword != asked_about:
            assert keyword not in answer.lower(), f"Unexpected non-menu dish '{keyword}' in answer: {answer}"


async def assert_grounded(judge: GroundednessJudge, question: str, answer: str) -> None:
    score, output = await judge.score(question, answer, GROUNDING_CONTEXT)
    assert score >= PASS_THRESHOLD, f"Groundedness score too low ({score}) for question '{question}': {answer}\nJudge: {output}"


async def test_cheapest_dish_mentions_falafel_and_price(assistant, judge):
    question = "What is the cheapest dish on the menu?"
    answer = await assistant.ask(question)

    assert "falafel" in answer.lower()
    assert_contains_price(answer, 12)
    assert_no_price_below(answer, 12)
    assert_no_non_menu_dish(answer)

    await assert_grounded(judge, question, answer)


async def test_vegetarian_option_mentions_falafel(assistant, judge):
    question = "What vegetarian option do you have?"
    answer = await assistant.ask(question)

    assert "falafel" in answer.lower()
    assert "schnitzel" not in answer.lower()
    assert "pad kra pao" not in answer.lower()
    assert "noodles" not in answer.lower()
    assert_no_non_menu_dish(answer)

    await assert_grounded(judge, question, answer)


async def test_sushi_question_declines_without_inventing_dish(assistant, judge):
    question = "Do you have sushi?"
    answer = await assistant.ask(question)

    assert "sushi is on the menu" not in answer.lower()
    assert DECLINE.search(answer), f"Expected a decline for a non-menu dish, got: {answer}"
    assert_no_non_menu_dish(answer, "sushi")

    await assert_grounded(judge, question, answer)


async def test_wiener_schnitzel_price_is_18(assistant, judge):
    question = "How much does the Wiener Schnitzel cost?"
    answer = await assistant.ask(question)

    assert "schnitzel" in answer.lower()
    assert_contains_price(answer, 18)
    assert_no_non_menu_dish(answer)

    await assert_grounded(judge, question, answer)


async def test_most_expensive_dish_mentions_pizza_tartufo_and_price(assistant, judge):
    question = "What is the most expensive dish on the menu?"
    answer = await assistant.ask(question)

    assert "pizza tartufo" in answer.lower()
    assert_contains_price(answer, 24)
    assert_no_non_menu_dish(answer)

    await assert_grounded(judge, question, answer)
