# Contracts

Inference routing and controlled backend execution are the core domain boundary.

- **API contract:** versioned request/response schema with bounded prompt/model/token fields.
- **Domain contract:** deterministic backend selection, health state, bounded concurrency, and explicit failure classes.
- **Provider contract:** InferenceBackend interface; provider-specific failures are normalized to the domain BackendError taxonomy.
- **Timeout contract:** backend execution is bounded by a 2-second timeout at the router boundary.
- **Correlation contract:** caller-supplied request/correlation IDs are preserved and generated when absent.
- **Configuration contract:** deployment and runtime dependencies are declared in pyproject.toml and requirements-prod.txt.

Compatibility changes require tests before merge. The executable code and tests are authoritative; documentation must not claim capabilities that are not implemented.
