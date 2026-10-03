from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis import strategies as st

from service import app


@given(st.text(min_size=1, max_size=64))
def test_request_key_never_crashes(value):
    response = TestClient(app).post("/v1/inference", json={"prompt": value})
    assert response.status_code == 200
