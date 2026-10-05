import math

import pytest

from overload_policy import OverloadPolicy, OverloadSnapshot


@pytest.mark.parametrize(
    "snapshot,reason",
    [
        (OverloadSnapshot(active=32, queued=0, p95_latency_ms=100), "active-capacity-exhausted"),
        (OverloadSnapshot(active=1, queued=64, p95_latency_ms=100), "queue-capacity-exhausted"),
        (OverloadSnapshot(active=1, queued=1, p95_latency_ms=751), "tail-latency-budget-exhausted"),
    ],
)
def test_overload_is_shed_deterministically(snapshot, reason):
    decision = OverloadPolicy().evaluate(snapshot)
    assert decision.allowed is False
    assert decision.reason == reason


def test_healthy_capacity_is_admitted():
    decision = OverloadPolicy().evaluate(
        OverloadSnapshot(active=8, queued=4, p95_latency_ms=120)
    )
    assert decision.allowed is True
    assert decision.reason == "within-overload-budget"


@pytest.mark.parametrize(
    "snapshot",
    [
        OverloadSnapshot(active=-1, queued=0, p95_latency_ms=1),
        OverloadSnapshot(active=0, queued=-1, p95_latency_ms=1),
        OverloadSnapshot(active=0, queued=0, p95_latency_ms=math.nan),
        OverloadSnapshot(active=0, queued=0, p95_latency_ms=math.inf),
    ],
)
def test_invalid_telemetry_fails_closed(snapshot):
    with pytest.raises(ValueError):
        OverloadPolicy().evaluate(snapshot)
