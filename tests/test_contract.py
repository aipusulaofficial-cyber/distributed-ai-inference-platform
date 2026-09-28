from fastapi.testclient import TestClient
from service import app

def test_http_contract():
    c=TestClient(app)
    assert c.get("/health/live").status_code == 200
    r=c.post("/v1/inference",json={"prompt":"contract"})
    assert r.status_code == 200
    assert r.json()["request_id"]
    assert r.json()["evidence"]["decision"] == "ALLOW"

def test_readiness_contract():
    assert TestClient(app).get("/health/ready").json()["status"] == "ready"
