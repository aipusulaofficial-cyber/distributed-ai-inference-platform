# Principal Engineering Contract

## Scope
This repository is a production-oriented reference implementation for distributed AI inference. The evidence boundary is explicit: executable routing, validation, bounded concurrency, backend health, timeout handling, resilience primitives, observability, deployment controls, and CI are implemented; external GPU/model providers and durable distributed state remain adapter/deployment concerns.

## Core boundary
**Primary concern:** inference request routing and controlled backend execution.

The HTTP/API boundary validates untrusted input. The router selects only healthy backends, enforces bounded concurrency, applies a fixed backend timeout, normalizes backend failures, and propagates request/correlation identifiers. Resilience primitives provide bounded retries, idempotency protection, circuit breaking, rate limiting, fallback, and timeout helpers without coupling the core to a provider.

## Non-functional requirements
- **Determinism:** core behavior is reproducible in tests without live external model services.
- **Failure semantics:** invalid input, no healthy backend, backend failure, timeout, overload, and retry exhaustion have explicit behavior.
- **Security:** CI performs filesystem/dependency/secret scanning and emits an SBOM; containers run as non-root.
- **Operability:** liveness/readiness, structured logs, tracing, request/correlation IDs, latency signals, and operational runbooks are present.
- **Change safety:** CI gates formatting, linting, type checking, tests, coverage, container build, production smoke tests, and supply-chain checks.

## Review checklist
- [x] Public contracts are validated.
- [x] Domain policy is independent from infrastructure adapters.
- [x] Failure and retry behavior is explicit.
- [x] Resource limits are bounded where work can grow.
- [x] Tests cover happy path, invalid input, and representative failure paths.
- [x] Security-sensitive decisions are auditable.
- [x] CI validates the repository before merge.
- [x] Architecture trade-offs are documented rather than implied.

## Evidence boundary
The repository is not claiming production certification. Production rollout still requires environment-specific SLO validation, capacity/load testing, durable distributed state where required, real model-provider integration, secrets management, deployment verification, and operational ownership.
