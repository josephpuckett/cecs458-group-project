"""Menu search. search_menu is the function we hand to Gemini as a tool."""
import sqlite3
from typing import Optional
from init_db import DB_PATH


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

    # WHERE clause
    clauses, params = [], []
    if category:
        clauses.append("category = ?")
        params.append(category.lower())
    if max_price is not None:
        clauses.append("price <= ?")
        params.append(max_price)
    if vegan:
        clauses.append("vegan = 1")
    if max_calories is not None:
        clauses.append("calories <= ?")
        params.append(max_calories)
    if vegetarian:
        clauses.append("vegetarian = 1")
    if gluten_free:
        clauses.append("gluten_free = 1")
    if max_spice_level is not None:
        clauses.append("spice_level <= ?")
        params.append(max_spice_level)
    if keyword:
        clauses.append("(name || ' ' || description) LIKE ?")
        params.append(f"%{keyword}%")

        

    sql = "SELECT * FROM menu_items"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)

    # Run it
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row      # rows act like dicts
        rows = conn.execute(sql, params).fetchall()

    # Convert back to the same shape menu.json had
    results = []
    for row in rows:
        item = dict(row)
        for flag in ("vegetarian", "vegan", "gluten_free"):
            item[flag] = bool(item[flag])
        results.append(item)
    return results

