# app/main.py
from fastapi import FastAPI, HTTPException, Depends, Header
from datetime import datetime
import os
import random
import re

from .loader import load_quotes
from .models import Quote

# --- parsing: support em dash, en dash, or hyphen ---
_SPLIT_RE = re.compile(r"\s*[—–-]\s*")  # em, en, hyphen

def parse_quote(text: str) -> tuple[str, str]:
    """
    Accept lines like:
      'Quote — Author'  'Quote – Author'  'Quote - Author'  'Quote—Author'
    Fallback author = 'Unknown' if no separator is found.
    """
    parts = _SPLIT_RE.split(text, maxsplit=1)
    if len(parts) == 2:
        quote, author = parts[0].strip(), parts[1].strip()
    else:
        quote, author = text.strip(), "Unknown"
    return quote, author

DATA_PATH = os.environ.get("QUOTES_PATH", "data/quotes.txt")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")

app = FastAPI(title="quote-api (Quote of the Day)", version="1.0.0")

# Load quotes at import time (don’t crash if missing)
try:
    QUOTES = load_quotes(DATA_PATH)
except FileNotFoundError:
    QUOTES = ["(missing quotes.txt)"] * 365

def admin_auth(x_token: str | None = Header(default=None)):
    if ADMIN_TOKEN and x_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

def today_index() -> int:
    d = datetime.now().timetuple().tm_yday  # 1..365/366
    return (d - 1) % 365

@app.get("/today", response_model=Quote)
def get_today():
    idx = today_index()
    quote, author = parse_quote(QUOTES[idx])
    return Quote(id=idx, quote=quote, author=author, day_of_year=idx + 1)

@app.get("/random", response_model=Quote)
def get_random():
    idx = random.randint(0, 364)
    quote, author = parse_quote(QUOTES[idx])
    return Quote(id=idx, quote=quote, author=author, day_of_year=idx + 1)

@app.get("/quotes/{qid}", response_model=Quote)
def get_quote(qid: int):
    if not 0 <= qid < 365:
        raise HTTPException(status_code=404, detail="Quote index out of range 0..364")
    quote, author = parse_quote(QUOTES[qid])
    return Quote(id=qid, quote=quote, author=author, day_of_year=qid + 1)

@app.post("/refresh", dependencies=[Depends(admin_auth)])
def refresh():
    global QUOTES
    QUOTES = load_quotes(DATA_PATH)
    return {"ok": True, "count": len(QUOTES)}
