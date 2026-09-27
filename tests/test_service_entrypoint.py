from fastapi.testclient import TestClient

from service import app


def test_root_service_uses_real_inference_path():
    client = TestClient(app)
    response = client.post(
        "/v1/inference",
        headers={"x-request-id": "req-entrypoint-001"},
        json={"model": "echo", "prompt": "principal-platform", "max_tokens": 9},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["request_id"] == "req-entrypoint-001"
    assert body["model"] == "echo"
    assert body["output"] == "principal"
    assert body["backend"] == "echo"
