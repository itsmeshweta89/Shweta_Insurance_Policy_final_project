import os
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app import main as main_module


def test_chat_endpoint_returns_response(monkeypatch):
    monkeypatch.setattr(main_module, "chat", lambda session_id, message: ("ok", False))

    client = TestClient(main_module.app)
    response = client.post(
        "/chat",
        json={"message": "hello", "session_id": "abc"},
    )

    assert response.status_code == 200
    assert response.json() == {"response": "ok", "session_id": "abc", "cached": False}
