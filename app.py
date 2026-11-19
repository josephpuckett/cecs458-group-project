import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types
from pydantic import BaseModel

from init_db import init_db
init_db()

from search import search_menu

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
STATIC = Path(__file__).parent / "static"

SYSTEM_PROMPT = (
    "You are a friendly assistant for a restaurant. Help guests find things to eat "
    "and drink. Always use the search_menu tool to look up items instead of guessing, "
    "and only recommend items the tool returns. Mention price and any relevant "
    "dietary info. Keep replies short. If nothing matches, say so and suggest the "
    "closest option."
)

app = FastAPI()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools=[search_menu])

# one Gemini chat per browser session, kept in memory (fine for a demo)
sessions: dict = {}


class ChatIn(BaseModel):
    message: str
    session_id: str | None = None


@app.post("/api/chat")
def chat(body: ChatIn):
    sid = body.session_id or str(uuid.uuid4())
    if sid not in sessions:
        sessions[sid] = client.chats.create(model=MODEL, config=config)
    try:
        reply = sessions[sid].send_message(body.message)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gemini error: {e}")
    return {"reply": reply.text or "Sorry, I came up empty. Try asking another way.", "session_id": sid}


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


app.mount("/static", StaticFiles(directory=STATIC), name="static")
