from uuid import uuid4
from fastapi import FastAPI, HTTPException, Request
from .backends import BackendError, EchoBackend
from .models import InferenceRequest, InferenceResponse
from .router import InferenceRouter, NoHealthyBackend

app = FastAPI(title="Distributed AI Inference Platform", version="0.1.0")
router = InferenceRouter([EchoBackend()])

@app.middleware("http")
async def correlation_id(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid4()))
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response

@app.get("/health/live")
async def live() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/health/ready")
async def ready() -> dict[str, str]:
    try:
        await router._next_healthy()
    except NoHealthyBackend as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"status": "ready"}

@app.post("/v1/inference", response_model=InferenceResponse)
async def inference(payload: InferenceRequest, request: Request) -> InferenceResponse:
    request_id = request.headers.get("x-request-id", str(uuid4()))
    try:
        output, backend = await router.infer(payload.prompt, payload.max_tokens)
    except NoHealthyBackend as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except BackendError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return InferenceResponse(request_id=request_id, model=payload.model, output=output, backend=backend)
