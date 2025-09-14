import os
from fastapi.testclient import TestClient


def test_chat_uses_stub_provider_and_replies():
    os.environ["MODEL_PROVIDER"] = "stub"
    from importlib import reload
    import src.adapters.api.main as main

    reload(main)
    client = TestClient(main.app)

    r = client.post("/api/chat", json={"messages": [{"role": "user", "content": "Pitch a fridge app"}]})
    assert r.status_code == 200
    data = r.json()
    assert "reply" in data
    assert isinstance(data["reply"], str)

