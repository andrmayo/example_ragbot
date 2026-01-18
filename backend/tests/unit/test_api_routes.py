from fastapi.testclient import TestClient

from resume_ragbot.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_unsupported_file():
    response = client.post(
        "/upload", files={"file": ("test.xyz", b"content", "application/octet-stream")}
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_ask_without_upload():
    response = client.post("/ask", json={"question": "What skills?"})
    assert response.status_code == 200
    assert "No resume content" in response.json()["answer"]
