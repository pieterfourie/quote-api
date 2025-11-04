# Repo: quote-api

A lightweight FastAPI project that serves a **Quote of the Day** based on your computer’s local date. It cycles through 365 quotes and repeats yearly.

---

## 🚀 Features
- Returns a different quote each day (`/today`)
- Fetch a random quote (`/random`)
- Access a quote by index (`/quotes/{id}`)
- Reload the quotes file dynamically (`/refresh`, optional token)
- File-based storage (`data/quotes.txt`) — no database required
- Automatically loops after day 365

---

## 🧱 Project Structure
```
quote-api/
│
├── app/
│   ├── main.py          # FastAPI app & routes
│   ├── loader.py        # File loader for quotes
│   └── models.py        # Pydantic models
│
├── data/
│   └── quotes.txt       # 365 quotes
│
├── scripts/
│   └── seed_365.py      # Optional helper to generate 365-line file
│
├── tests/
│   └── test_today.py    # Pytest for /today endpoint
│
├── requirements.txt     # Dependencies list
├── .gitignore
├── pyproject.toml
├── Dockerfile
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repo
```bash
git clone https://github.com/pieterfourie/quote-api.git
cd quote-api
```

### 2️⃣ (Optional) Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate   # PowerShell
# or
source .venv/Scripts/activate   # Git Bash
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Run locally
```bash
uvicorn app.main:app --reload
```
Then visit:
👉 http://127.0.0.1:8000/today

---

## 🌱 Environment Variables
- `QUOTES_PATH` – path to quotes file (default `data/quotes.txt`)
- `ADMIN_TOKEN` – optional secret for `/refresh`

Example (PowerShell):
```powershell
$env:ADMIN_TOKEN="supersecret"
```
Then call:
```bash
curl -X POST http://127.0.0.1:8000/refresh -H "X-Token: supersecret"
```

---

## 🧪 Test
```bash
pytest -q
```

---

## 🐳 Docker
```bash
docker build -t quote-api .
docker run -p 8000:8000 quote-api
```
Open http://127.0.0.1:8000/today

---

## 🧠 Notes
- The app uses the **local system date** (no timezone logic)
- On leap years, Feb 29 reuses March 1’s quote index
- Missing lines in `quotes.txt` are auto-padded to 365

---

## 💡 Future Ideas
- `/week` endpoint (7 upcoming quotes)
- `/healthz` endpoint for uptime checks
- Add CI workflow with `pytest` + `ruff`

---

## 📜 License
MIT — free to use and modify.
