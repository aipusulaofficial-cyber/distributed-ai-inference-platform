from fastapi.testclient import TestClient
from inference_platform.api import app

client = TestClient(app)


def test_live():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_inference_contract():
    response = client.post("/v1/inference", json={"prompt": "hello", "max_tokens": 5})
    assert response.status_code == 200
    assert response.json()["output"] == "hello"
    assert response.headers["x-request-id"]
