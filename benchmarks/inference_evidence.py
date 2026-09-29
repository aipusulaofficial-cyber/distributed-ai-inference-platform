"""Small deterministic inference-path benchmark used for CI evidence."""

from __future__ import annotations

import json
import time
from pathlib import Path

from inference_domain import InferenceRequest


def run(iterations: int) -> dict[str, object]:
    samples: list[float] = []
    errors = 0
    for _ in range(iterations):
        started = time.perf_counter()
        try:
            request = InferenceRequest(model="evidence-model", prompt="hello")
            request.validate()
        except Exception:
            errors += 1
        samples.append((time.perf_counter() - started) * 1000)

    ordered = sorted(samples)

    def pct(q: float) -> float:
        return ordered[min(len(ordered) - 1, int(len(ordered) * q))]

    return {
        "iterations": iterations,
        "errors": errors,
        "error_rate": errors / iterations,
        "latency_ms": {
            "p50": round(pct(0.50), 3),
            "p95": round(pct(0.95), 3),
            "p99": round(pct(0.99), 3),
        },
        "contract": "InferenceRequest validation path",
        "measurement": "CI reference-path benchmark; not a production performance claim",
    }


def write_report(iterations: int, path: str) -> dict[str, object]:
    report = run(iterations)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    write_report(1000, "artifacts/inference-evidence.json")
