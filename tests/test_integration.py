import pytest
from fastapi.testclient import TestClient
from inference_platform.api import app
def test_http_contract_and_domain():
 c=TestClient(app);assert c.get("/health/live").status_code==200
 r=c.post("/v1/inference",json={"model":"echo","prompt":"hello","max_tokens":10});assert r.status_code==200,r.text
