import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).parent
DB_PATH = ROOT / "menu.db"
MENU_JSON_PATH = ROOT / "menu.json"

SCHEMA = """
CREATE TABLE IF NOT EXISTS menu_items (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL CHECK (category IN ('entree','salad','side','dessert','drink')),
  price REAL NOT NULL,
  calories INTEGER NOT NULL,
  vegetarian INTEGER NOT NULL,   -- 0/1, SQLite has no bool
  vegan INTEGER NOT NULL,
  gluten_free INTEGER NOT NULL,
  spice_level INTEGER NOT NULL CHECK (spice_level BETWEEN 0 AND 3),
  description TEXT NOT NULL
);
"""

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)
        menu_items = json.loads(MENU_JSON_PATH.read_text())
        for item in menu_items:
            conn.execute(
                """
                INSERT OR REPLACE INTO menu_items (id, name, category, price, calories, vegetarian, vegan, gluten_free, spice_level, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item["id"],
                    item["name"],
                    item["category"],
                    item["price"],
                    item["calories"],
                    int(item["vegetarian"]),
                    int(item["vegan"]),
                    int(item["gluten_free"]),
                    item["spice_level"],
                    item["description"]
                )
            )