# app/loader.py
from pathlib import Path

DEFAULT_PAD = "(empty)"

def load_quotes(path: str) -> list[str]:
    p = Path(path)
    if not p.exists():
        # return a default list instead of crashing
        lines = ["The only way out is through. — Robert Frost"]
    else:
        lines = [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines()]
    if len(lines) < 365:
        lines += [DEFAULT_PAD] * (365 - len(lines))
    return lines[:365]
