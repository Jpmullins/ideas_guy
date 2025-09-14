from fastapi.testclient import TestClient


def test_list_characters():
    from src.adapters.api.main import app

    client = TestClient(app)
    r = client.get("/api/characters")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(c.get("id") == "ideas_guy" for c in data)

