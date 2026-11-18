"""Menu search. search_menu is the function we hand to Gemini as a tool."""
import json
from pathlib import Path
from typing import Optional

MENU_PATH = Path(__file__).parent / "menu.json"


def load_menu() -> list[dict]:
    return json.loads(MENU_PATH.read_text())


def search_menu(
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    max_calories: Optional[int] = None,
    vegetarian: Optional[bool] = None,
    vegan: Optional[bool] = None,
    gluten_free: Optional[bool] = None,
    max_spice_level: Optional[int] = None,
    keyword: Optional[str] = None,
) -> list[dict]:
    """Search the restaurant menu. Every argument is optional and they are combined with AND.

    Args:
        category: One of entree, salad, side, dessert, drink.
        max_price: Highest price in dollars.
        max_calories: Highest calorie count.
        vegetarian: True to only return vegetarian items.
        vegan: True to only return vegan items.
        gluten_free: True to only return gluten free items.
        max_spice_level: Highest spice level, 0 (none) to 3 (hot).
        keyword: Text to look for in the item name or description.

    Returns:
        A list of matching menu items, each with name, category, price, calories,
        dietary flags, spice_level, and description.
    """
    results = []
    for item in load_menu():
        if category and item["category"] != category.lower():
            continue
        if max_price is not None and item["price"] > max_price:
            continue
        if max_calories is not None and item["calories"] > max_calories:
            continue
        if vegetarian and not item["vegetarian"]:
            continue
        if vegan and not item["vegan"]:
            continue
        if gluten_free and not item["gluten_free"]:
            continue
        if max_spice_level is not None and item["spice_level"] > max_spice_level:
            continue
        if keyword:
            text = (item["name"] + " " + item["description"]).lower()
            if keyword.lower() not in text:
                continue
        results.append(item)
    return results
