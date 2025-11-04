from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_today_endpoint():
    r = client.get("/today")
    assert r.status_code == 200
    body = r.json()
    assert set(["id", "text", "day_of_year"]).issubset(body.keys())
    assert isinstance(body["text"], str)
