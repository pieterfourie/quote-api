# app/models.py
from pydantic import BaseModel

class Quote(BaseModel):
    id: int
    quote: str
    author: str
    day_of_year: int | None = None
