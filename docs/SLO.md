# SLO / SLI

SLIs: p50/p95/p99 latency, throughput, error rate by error_type, concurrency/saturation, dependency latency/error rate, and resource saturation.

Baseline target: p95 request latency < 500 ms; error rate < 1%; admission rejects are tracked separately; backend dependency timeout budget 250 ms.

These are reference targets and must be recalibrated against production traffic.