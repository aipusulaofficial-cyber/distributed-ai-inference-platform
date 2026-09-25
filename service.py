"""Production HTTP surface for distributed-ai-inference-platform."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any
from otel_setup import tracer
app=FastAPI(title="distributed-ai-inference-platform",version="1.0.0")
class InferenceRequest(BaseModel):
 request_id: str
 payload: dict[str,Any]={}
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/inference")
def handle(req:InferenceRequest):
 with tracer.start_as_current_span("inference") as span:
  span.set_attribute("request.key",getattr(req,"request_id"))
  return {"status":"accepted","request_id":getattr(req,"request_id")}
