"""Create a 365-line quotes file from a short seed list.
Usage:
uv run python scripts/seed_365.py data/quotes.txt
or
python scripts/seed_365.py data/quotes.txt
"""
from pathlib import Path
import sys


DEFAULTS = [
    "The only way out is through. — Robert Frost",
    "Do what you can, with what you have, where you are. — T. Roosevelt",
    "It always seems impossible until it's done. — Nelson Mandela",
]


def main(out_path: str):
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    base = DEFAULTS
    lines: list[str] = []
    while len(lines) < 365:
        for q in base:
            if len(lines) >= 365:
                break
            lines.append(q)

    p.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(lines)} quotes to {p}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "data/quotes.txt"
    main(target)
