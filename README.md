# CECS 458 Group Project Phase 2: Menu Chatbot

Simple website chatbot. The backend uses the Gemini API (free tier) and gives the model a
tool, `search_menu`, that filters `menu.json` by category, price, calories, dietary flags,
spice level, and keyword.

## Layout

- `menu.json` the menu "database"
- `search.py` the search function Gemini calls as a tool
- `app.py` FastAPI server, `/api/chat` endpoint, keeps one Gemini chat per session
- `static/index.html` the chat UI

## Run it

1. Get a free key at https://aistudio.google.com/apikey
2. `cp .env.example .env` and paste your key in
3. `uv sync --locked`
4. `uv run uvicorn app:app --reload`
5. Open http://127.0.0.1:8000

No uv? `pip install fastapi uvicorn google-genai python-dotenv` then `uvicorn app:app --reload`.

## Menu item fields

id, name, category (entree, salad, side, dessert, drink), price, calories, vegetarian,
vegan, gluten_free, spice_level (0 to 3), description.

## Ideas for the team

- Add more menu items and fields (allergens, prep time, ingredients)
- Show matching items as cards in the UI, not just text
- Swap menu.json for SQLite
- Add tests for search_menu
