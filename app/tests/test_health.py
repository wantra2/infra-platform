from fastapi.testclient import TestClient

from infra_api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_ready():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

def test_metrics():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "http_request" in response.text
