from pathlib import Path
from typing import List

DEFAULT_PAD = "(empty)"

def load_qoutes(path: str) -> List[str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"The file at {path} does not exist.")
    
    lines = [ln.strip for ln in p.read_text(encoding="utf-8").splitlines()]

    #Enforcce exactly 365 items for a stable yearly loop
    if len(lines) < 365:
        lines += [DEFAULT_PAD] * (365 - len(lines))
    return lines[:365]
