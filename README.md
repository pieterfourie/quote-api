# Quote of the Day (FastAPI)


A tiny, file-backed FastAPI that returns a Quote of the Day based on the **host machine's local date**. The list loops across leap years using a fixed 365-item cycle.


## Endpoints
- `GET /today` → quote for today (fields: `id`, `text`, `day_of_year`)
- `GET /random` → a random quote
- `GET /quotes/{id}` → quote by index (0..364)
- `POST /refresh` → reloads the quotes file (require header `X-Token` if `ADMIN_TOKEN` is set)


## Run locally
```bash
# 1) Install deps
pip install -r <(python - <<'PY'\nprint('\n'.join(['fastapi>=0.115','uvicorn[standard]>=0.30','pydantic>=2.9']))\nPY)


# or use uv (recommended)
# curl -LsSf https://astral.sh/uv/install.sh | sh
# uv run uvicorn app.main:app --reload


# 2) Start dev server
uvicorn app.main:app --reload
# Visit: http://127.0.0.1:8000/today
```


> The app reads `data/quotes.txt`. Ensure it has **exactly 365 lines**. If fewer, it pads with `(empty)` entries on load.


## Environment Variables
- `QUOTES_PATH` (default `data/quotes.txt`)
- `ADMIN_TOKEN` (optional) — if set, `POST /refresh` requires header `X-Token: <token>`


## Leap Year Behavior
We compute the host's day-of-year and map it into a fixed 0..364 range using modulo 365. Feb 29 shares the same index as Mar 1 for consistency.


## Tests
```bash
python -m pytest -q
```


## Docker (optional)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir fastapi uvicorn[standard] pydantic
COPY app ./app
COPY data ./data
ENV QUOTES_PATH="data/quotes.txt"
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
```


### Run
```bash
docker build -t quote-api .
docker run -p 8000:8000 quote-api
```


## Why it’s a good portfolio piece
- Clean, deterministic logic (365-item cycle)
- File-backed configuration (no DB)
- Typed responses (Pydantic) & simple auth example
- Unit test + optional Docker
- Clear README and structure


Quickstart (copy/paste)
```bash
# create venv (optional)
python -m venv .venv && source .venv/bin/activate


# install
pip install fastapi==0.115.* uvicorn[standard]==0.30.* pydantic==2.9.*


# run
uvicorn app.main:app --reload


# try it
curl http://127.0.0.1:8000/today