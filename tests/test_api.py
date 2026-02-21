from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_invalid_file():
    response = client.post(
        "/predict",
        files={"file": ("test.txt", b"abc", "text/plain")}
    )
    assert response.status_code == 400