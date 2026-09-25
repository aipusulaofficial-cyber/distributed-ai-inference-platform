from observability import PrincipalObservabilityMiddleware
"""Production HTTP surface for distributed-ai-inference-platform."""
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from otel_setup import tracer

app = FastAPI(title="distributed-ai-inference-platform", version="1.0.0")
app.add_middleware(PrincipalObservabilityMiddleware)


class InferenceRequest(BaseModel):
    request_id: str
    payload: dict[str, Any] = {}


@app.get("/health/live")
def live():
    return {"status": "ok"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}


@app.post("/v1/inference")
def handle(req: InferenceRequest):
    with tracer.start_as_current_span("inference") as span:
        span.set_attribute("request.key", req.request_id)
        return {"status": "accepted", "request_id": req.request_id}
