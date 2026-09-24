from dataclasses import dataclass


@dataclass(frozen=True)
class MenuItem:
    name: str
    price_eur: int
    stock: int
    vegetarian: bool
    description: str


ITEMS = [
    MenuItem(
        "Hand pulled Noodles",
        17,
        9,
        False,
        "Hand pulled noodles made with love by our experienced cooks from Sichuan. Served with your choice of meat, vegetables, and smashed cucumber salad.",
    ),
    MenuItem(
        "Pad Kra Pao",
        16,
        12,
        False,
        "Pad Kra Pao definitely one of the most popular spicy dishes in Thailand. Cooked with thai holy basil, long beans and chicken. Served with jasmine rice and fried egg.",
    ),
    MenuItem(
        "Wiener Schnitzel",
        18,
        13,
        False,
        "Wiener Schnitzel is a traditional Austrian dish consisting of a thin slice of veal coated in breadcrumbs and fried. Served with potato salad and lemon.",
    ),
    MenuItem(
        "Falafel Plate",
        12,
        9,
        True,
        "Falafel is a deep-fried ball, doughnut or patty made from ground chickpeas. Served with hummus, pita bread, and salad.",
    ),
    MenuItem(
        "Pizza Tartufo",
        24,
        4,
        True,
        "Pizza truffle is well tasting, exclusive joy for your taste bud. A delight of white pizza where the protagonist is our cheese with truffle flakes.",
    ),
]


def format_item(item: MenuItem) -> str:
    diet = "vegetarian" if item.vegetarian else "not vegetarian"
    return f"{item.name}: {item.price_eur} EUR, {item.stock} in stock, {diet}. {item.description}"


def build_system_prompt() -> str:
    lines = [
        "You are the menu assistant for a small food shop.",
        "Rules:",
        "- Answer only from the menu items listed below. Never invent a dish that is not listed.",
        "- If the customer asks about a dish that is not on the menu, say clearly that it is not on the menu.",
        "- Always give prices in EUR.",
        "- Keep answers short, at most two sentences.",
        "",
        "Menu:",
    ]
    lines.extend(f"- {format_item(item)}" for item in ITEMS)
    return "\n".join(lines) + "\n"


def build_grounding_context() -> str:
    return "\n".join(format_item(item) for item in ITEMS) + "\n"
