from fastapi.testclient import TestClient


def test_models_endpoint_lists_options():
    from src.adapters.api.main import app

    client = TestClient(app)
    r = client.get("/api/models")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(m.get("provider") in ("vllm", "huggingface", "stub") for m in data)

