# ADR-0003: Failure and retry strategy

## Decision
Use explicit timeout budgets, bounded exponential backoff, idempotency-aware retries, bounded concurrency, token-bucket rate limiting where applicable, and circuit breaking for repeated dependency failures.

The inference router enforces bounded concurrency and a fixed backend execution timeout. The dependency-free resilience.py module provides reusable bounded retry, timeout, circuit-breaker, rate-limit, fallback, and idempotency primitives. Blind retries are not part of the router.

## Why
Hidden or unlimited retries amplify outages and can duplicate non-idempotent side effects. Explicit budgets make failure behavior observable and keep latency bounded.

## Alternatives considered
Unlimited retries, fixed-delay retries, and blind retries for every request were rejected.

## Trade-offs
Predictable failure and bounded latency are preferred over exhausting every dependency attempt. Thresholds and budgets must be tuned from measured traffic.

## Consequences
Provider adapters must classify retryable exceptions and only enable retries for safe/idempotent operations. Distributed cancellation and durable idempotency state belong to the deployment/provider layer.

## Implementation evidence
inference_platform/router.py, resilience.py, tests/test_resilience.py, tests/test_api.py, docs/FAILURE-MATRIX.md, and docs/OPERATIONS.md.
