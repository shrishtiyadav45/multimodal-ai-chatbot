"""API tests. Provider calls are mocked; no Gemini key is needed."""
from fastapi.testclient import TestClient
from backend.main import app
import backend.main as main

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_empty_text_rejected():
    response = client.post("/api/chat", data={"modality": "text", "message": "   "})
    assert response.status_code == 400


def test_text_success(monkeypatch):
    monkeypatch.setattr(main, "generate_reply", lambda *args: "A rainbow is caused by light interacting with water droplets.")
    response = client.post("/api/chat", data={"modality": "text", "message": "Explain a rainbow."})
    assert response.status_code == 200
    assert response.json()["modality"] == "text"
    assert "rainbow" in response.json()["text"].lower()


def test_image_requires_file():
    response = client.post("/api/chat", data={"modality": "image", "message": "What is shown?"})
    assert response.status_code == 400


def test_invalid_image_rejected_before_provider(monkeypatch):
    monkeypatch.setattr(main, "generate_reply", lambda *args: (_ for _ in ()).throw(AssertionError("must not call provider")))
    response = client.post("/api/chat", data={"modality": "image", "message": "Describe"},
                           files={"file": ("fake.jpg", b"not an image", "image/jpeg")})
    assert response.status_code == 415


def test_audio_requires_file():
    response = client.post("/api/chat", data={"modality": "audio", "message": "Summarize"})
    assert response.status_code == 400


def test_unsupported_modality_rejected():
    response = client.post("/api/chat", data={"modality": "video", "message": "Hi"})
    assert response.status_code == 422
