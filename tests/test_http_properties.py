from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis import strategies as st

from inference_platform.api import app

c = TestClient(app)


def test_contract():
    assert c.get("/health/live").status_code == 200


@given(st.text(max_size=32))
def test_property(prompt):
    response = c.post(
        "/v1/inference",
        json={"model": "echo", "prompt": prompt, "max_tokens": 1},
    )
    expected_status = 200 if prompt.strip() else 422
    assert response.status_code == expected_status
