import time

from fastapi import FastAPI, HTTPException, Request

from observability import configure_observability, get_logger
from runtime_evidence import request_id_from_headers, runtime_evidence
from .backends import BackendError, EchoBackend
from .models import InferenceRequest, InferenceResponse
from .router import InferenceRouter, NoHealthyBackend


configure_observability()
logger = get_logger(__name__)
app = FastAPI(title="Distributed AI Inference Platform", version="0.1.0")
router = InferenceRouter([EchoBackend()])


@app.middleware("http")
async def correlation_id(request: Request, call_next):
    started = time.perf_counter()
    request_id = request_id_from_headers(request.headers)
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    response.headers["x-correlation-id"] = request.headers.get("x-correlation-id", request_id)
    response.headers["x-latency-ms"] = f"{(time.perf_counter() - started) * 1000:.3f}"
    return response


@app.get("/health/live")
async def live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
async def ready() -> dict[str, str]:
    try:
        if not any(state.healthy for state in router._states):
            raise NoHealthyBackend("no healthy backend")
    except NoHealthyBackend as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"status": "ready"}


@app.post("/v1/inference", response_model=InferenceResponse)
async def inference(payload: InferenceRequest, request: Request) -> InferenceResponse:
    started = time.perf_counter()
    request_id = request_id_from_headers(request.headers)
    try:
        output, backend = await router.infer(payload.prompt, payload.max_tokens)
    except NoHealthyBackend as exc:
        evidence = runtime_evidence(request_id=request_id, stage="inference.route", decision="FAIL", started=started, error=str(exc), circuit_state="OPEN")
        raise HTTPException(status_code=503, detail={"error": str(exc), "evidence": evidence}) from exc
    except BackendError as exc:
        evidence = runtime_evidence(request_id=request_id, stage="inference.backend", decision="FAIL", started=started, error=str(exc))
        raise HTTPException(status_code=502, detail={"error": str(exc), "evidence": evidence}) from exc
    return InferenceResponse(request_id=request_id, model=payload.model, output=output, backend=backend, evidence=runtime_evidence(request_id=request_id, stage="inference.backend", decision="ALLOW", started=started))
