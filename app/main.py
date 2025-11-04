# app/main.py
from fastapi import FastAPI, HTTPException, Depends, Header
from datetime import datetime
import os
import random

from .loader import load_quotes
from .models import Quote

DATA_PATH = os.environ.get("QUOTES_PATH", "data/quotes.txt")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")

# >>> THIS must be at module level, not inside a function <<<
app = FastAPI(title="quote-api (Quote of the Day)", version="1.0.0")

# Load quotes at import time (safe even if file is missing)
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

def parse_quote(text: str):
    """Split 'Quote — Author' into parts."""
    if "—" in text:
        parts = text.split("—", 1)
        quote, author = parts[0].strip(), parts[1].strip()
    elif "-" in text:
        parts = text.split("-", 1)
        quote, author = parts[0].strip(), parts[1].strip()
    else:
        quote, author = text.strip(), "Unknown"
    return quote, author


@app.get("/today", response_model=Quote)
def get_today():
    idx = today_index()
    text = QUOTES[idx]
    quote, author = parse_quote(text)
    return Quote(id=idx, quote=quote, author=author, day_of_year=idx + 1)


@app.get("/random", response_model=Quote)
def get_random():
    idx = random.randint(0, 364)
    text = QUOTES[idx]
    quote, author = parse_quote(text)
    return Quote(id=idx, quote=quote, author=author, day_of_year=idx + 1)


@app.get("/quotes/{qid}", response_model=Quote)
def get_quote(qid: int):
    if not 0 <= qid < 365:
        raise HTTPException(status_code=404, detail="Quote index out of range 0..364")
    text = QUOTES[qid]
    quote, author = parse_quote(text)
    return Quote(id=qid, quote=quote, author=author, day_of_year=qid + 1)
