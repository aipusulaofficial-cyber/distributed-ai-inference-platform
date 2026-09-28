from fastapi.testclient import TestClient

from service import app


def test_http_contract():
    client = TestClient(app)
    assert client.get("/health/live").status_code == 200
    response = client.post("/v1/inference", json={"prompt": "contract"})
    assert response.status_code == 200
    assert response.json()["request_id"]
    assert response.json()["evidence"]["decision"] == "ALLOW"


def test_readiness_contract():
    assert TestClient(app).get("/health/ready").json()["status"] == "ready"
