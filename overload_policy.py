from dataclasses import dataclass
import math


@dataclass(frozen=True)
class OverloadSnapshot:
    active: int
    queued: int
    p95_latency_ms: float


@dataclass(frozen=True)
class AdmissionDecision:
    allowed: bool
    reason: str


@dataclass(frozen=True)
class OverloadPolicy:
    max_active: int = 32
    max_queue: int = 64
    max_p95_latency_ms: float = 750.0

    def __post_init__(self) -> None:
        for name, value in (("max_active", self.max_active), ("max_queue", self.max_queue)):
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(f"{name} must be a positive integer")
        if (
            isinstance(self.max_p95_latency_ms, bool)
            or not isinstance(self.max_p95_latency_ms, (int, float))
            or not math.isfinite(self.max_p95_latency_ms)
            or self.max_p95_latency_ms <= 0
        ):
            raise ValueError("max_p95_latency_ms must be finite and positive")

    def evaluate(self, snapshot: OverloadSnapshot) -> AdmissionDecision:
        if isinstance(snapshot.active, bool) or not isinstance(snapshot.active, int) or snapshot.active < 0:
            raise ValueError("active must be a non-negative integer")
        if isinstance(snapshot.queued, bool) or not isinstance(snapshot.queued, int) or snapshot.queued < 0:
            raise ValueError("queued must be a non-negative integer")
        if (
            isinstance(snapshot.p95_latency_ms, bool)
            or not isinstance(snapshot.p95_latency_ms, (int, float))
            or not math.isfinite(snapshot.p95_latency_ms)
            or snapshot.p95_latency_ms < 0
        ):
            raise ValueError("p95_latency_ms must be finite and non-negative")
        if snapshot.active >= self.max_active:
            return AdmissionDecision(False, "active-capacity-exhausted")
        if snapshot.queued >= self.max_queue:
            return AdmissionDecision(False, "queue-capacity-exhausted")
        if snapshot.p95_latency_ms > self.max_p95_latency_ms:
            return AdmissionDecision(False, "tail-latency-budget-exhausted")
        return AdmissionDecision(True, "within-overload-budget")
