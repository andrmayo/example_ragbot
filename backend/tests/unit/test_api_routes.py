import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from resume_ragbot.api.routes import retrievers
from resume_ragbot.main import app


@pytest.fixture
def client():
    """Fresh test client with cleared state."""
    retrievers.clear()
    yield TestClient(app)
    retrievers.clear()


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_unsupported_file(client: TestClient):
    response = client.post(
        "/upload", files={"file": ("test.xyz", b"content", "application/octet-stream")}
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_upload(client: TestClient, sample_pdf):
    with open(sample_pdf, "rb") as f:
        response = client.post("/upload", files={"file": ("resume.pdf", f)})

    assert response.status_code == 200
    assert "Indexed" in response.json()["message"]


def test_ask_without_upload(client: TestClient):
    response = client.post("/ask", json={"question": "What skills?"})
    assert response.status_code == 200
    assert "No resume content" in response.json()["answer"]


@patch("resume_ragbot.api.routes.get_client")
def test_ask_with_resume(mock_get_client: MagicMock, client: TestClient, sample_pdf):
    # Setup mock
    mock_llm = MagicMock()
    mock_llm.complete.return_value = MagicMock(
        content='{"answer": "Mocked answer", "sources_used": ["resume.pdf"]}'
    )
    mock_get_client.return_value = mock_llm

    # Upload
    with open(sample_pdf, "rb") as f:
        client.post("/upload", files={"file": ("resume.pdf", f)})

    # Ask
    response = client.post("/ask", json={"question": "What skills?"})

    assert response.status_code == 200
    assert response.json()["answer"] == "Mocked answer"
    mock_llm.complete.assert_called_once()
