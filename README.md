# Distributed AI Inference Platform

Production-oriented reference architecture for reliable, observable, horizontally scalable model serving.

## Engineering goals

- Replaceable model-runtime adapters behind a stable interface
- Health-aware backend routing and bounded concurrency
- Contract-first HTTP API with correlation IDs
- Deterministic tests without external model services
- CI, containerization, architecture documentation, and ADRs

## Architecture

```text
Client -> FastAPI API -> Inference Router -> Backend Registry -> Model Runtime
                         |                     |
                         +-> admission         +-> health state
                         +-> observability
```

## Quickstart

Requires Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn inference_platform.api:app --reload
```

Then call `GET /health/live`, `GET /health/ready`, or `POST /v1/inference`.

See [ARCHITECTURE.md](ARCHITECTURE.md) and [ADRs/0001-serving-boundaries.md](ADRs/0001-serving-boundaries.md).
