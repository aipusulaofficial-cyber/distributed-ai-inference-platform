"""Concurrent HTTP inference-path evidence for CI.

Exercises the actual FastAPI inference boundary, router admission control, and backend path.
This is a repeatable CI acceptance benchmark, not a production hardware claim.
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import importlib

app = importlib.import_module("inference_platform.api").app


def run(requests: int = 200, workers: int = 16) -> dict[str, object]:
    if requests < 1 or workers < 1:
        raise ValueError("requests and workers must be positive")

    latencies: list[float] = []
    failures = 0

    def one(index: int) -> tuple[float, bool]:
        started = time.perf_counter()
        with TestClient(app) as client:
            response = client.post(
                "/v1/inference",
                headers={"x-request-id": f"benchmark-{index}"},
                json={
                    "model": "evidence-model",
                    "prompt": f"distinguished inference evidence {index}",
                    "max_tokens": 32,
                },
            )
        latency = (time.perf_counter() - started) * 1000
        if response.status_code != 200:
            return latency, False
        body = response.json()
        valid = (
            body.get("model") == "evidence-model"
            and bool(body.get("backend"))
            and body.get("evidence", {}).get("decision") == "ALLOW"
        )
        return latency, valid

    wall_started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(one, index) for index in range(requests)]
        for future in as_completed(futures):
            latency, ok = future.result()
            latencies.append(latency)
            failures += int(not ok)
    wall_s = time.perf_counter() - wall_started
    ordered = sorted(latencies)

    def pct(q: float) -> float:
        index = min(len(ordered) - 1, max(0, int((len(ordered) - 1) * q)))
        return ordered[index]

    return {
        "requests": requests,
        "workers": workers,
        "failures": failures,
        "error_rate": failures / requests,
        "throughput_rps": round(requests / wall_s, 2),
        "latency_ms": {
            "p50": round(statistics.median(ordered), 3),
            "p95": round(pct(0.95), 3),
            "p99": round(pct(0.99), 3),
        },
        "workload": "FastAPI TestClient -> /v1/inference -> router admission -> backend",
        "measurement": (
            "repeatable CI HTTP inference acceptance benchmark; not a production hardware claim"
        ),
    }


def write_report(path: str | Path) -> dict[str, object]:
    report = run()
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report


if __name__ == "__main__":
    write_report("artifacts/inference-evidence.json")
