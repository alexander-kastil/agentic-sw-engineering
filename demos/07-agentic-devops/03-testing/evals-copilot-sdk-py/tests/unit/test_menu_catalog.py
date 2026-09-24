import pytest

from menu_catalog import ITEMS, MenuItem, build_grounding_context, build_system_prompt, format_item

EXPECTED = {
    "Hand pulled Noodles": (17, 9, False),
    "Pad Kra Pao": (16, 12, False),
    "Wiener Schnitzel": (18, 13, False),
    "Falafel Plate": (12, 9, True),
    "Pizza Tartufo": (24, 4, True),
}

RULES = [
    "- Answer only from the menu items listed below. Never invent a dish that is not listed.",
    "- If the customer asks about a dish that is not on the menu, say clearly that it is not on the menu.",
    "- Always give prices in EUR.",
    "- Keep answers short, at most two sentences.",
]


def test_menu_has_five_items():
    assert len(ITEMS) == 5
    assert [item.name for item in ITEMS] == list(EXPECTED)


@pytest.mark.parametrize("item", ITEMS, ids=lambda item: item.name)
def test_item_price_stock_and_vegetarian_flag(item):
    assert (item.price_eur, item.stock, item.vegetarian) == EXPECTED[item.name]
    assert item.description


def test_falafel_is_cheapest_and_pizza_most_expensive():
    assert min(ITEMS, key=lambda item: item.price_eur).name == "Falafel Plate"
    assert max(ITEMS, key=lambda item: item.price_eur).name == "Pizza Tartufo"


def test_only_falafel_and_pizza_are_vegetarian():
    assert [item.name for item in ITEMS if item.vegetarian] == ["Falafel Plate", "Pizza Tartufo"]


def test_menu_item_is_frozen():
    with pytest.raises(AttributeError):
        ITEMS[0].price_eur = 1


def test_format_item_vegetarian():
    item = MenuItem("Soup", 5, 2, True, "Hot soup.")
    assert format_item(item) == "Soup: 5 EUR, 2 in stock, vegetarian. Hot soup."


def test_format_item_not_vegetarian():
    item = MenuItem("Steak", 30, 1, False, "Grilled.")
    assert format_item(item) == "Steak: 30 EUR, 1 in stock, not vegetarian. Grilled."


def test_system_prompt_header_and_rules():
    prompt = build_system_prompt()
    lines = prompt.splitlines()
    assert lines[:2] == ["You are the menu assistant for a small food shop.", "Rules:"]
    assert lines[2:6] == RULES
    assert lines[6:8] == ["", "Menu:"]


@pytest.mark.parametrize("item", ITEMS, ids=lambda item: item.name)
def test_system_prompt_lists_every_item(item):
    assert f"- {format_item(item)}" in build_system_prompt().splitlines()


def test_system_prompt_menu_section_order_and_trailing_newline():
    prompt = build_system_prompt()
    assert prompt.split("Menu:\n", 1)[1].splitlines() == [f"- {format_item(item)}" for item in ITEMS]
    assert prompt.endswith("\n")


def test_grounding_context_is_one_line_per_item():
    context = build_grounding_context()
    assert context == "".join(f"{format_item(item)}\n" for item in ITEMS)
    assert "Rules:" not in context
    assert len(context.splitlines()) == 5
