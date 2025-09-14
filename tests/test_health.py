import os
from fastapi.testclient import TestClient


def test_health_endpoint():
    # Ensure we use stub if any import triggers model creation elsewhere
    os.environ.setdefault("MODEL_PROVIDER", "stub")
    from src.adapters.api.main import app

    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

