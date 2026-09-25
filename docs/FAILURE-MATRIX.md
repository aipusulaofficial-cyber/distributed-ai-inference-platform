# Failure matrix

| Failure | Detection | Action | Retry? | User impact |
|---|---|---|---|---|
| Invalid/untrusted input | contract validation | reject deterministically | No | 4xx |
| Dependency timeout | timeout budget | normalize + record dependency | Only if safe/idempotent | explicit dependency error/degradation |
| Dependency 5xx | provider adapter | bounded exponential backoff | Only if safe/idempotent | bounded latency |
| Repeated dependency failure | circuit breaker | open circuit | No while open | fast failure |
| Local overload | semaphore/token bucket | fail fast | No | 429/degraded path |
| Telemetry failure | exporter error | preserve domain result | bounded/exporter-local only | no domain corruption |

No healthy backend -> 503; overload -> 429; backend timeout -> bounded retry only for idempotent requests; repeated backend failure -> circuit open; overload/backpressure must fail fast.