# ADR-0001: Keep model runtimes behind an interface

**Status:** Accepted

## Context

Model runtimes evolve independently from HTTP and routing concerns. Tight coupling makes testing harder and migrations expensive.

## Decision

Define a small `InferenceBackend` protocol and adapt runtime-specific SDKs to it.

## Consequences

Positive: deterministic tests, replaceable runtimes, clear ownership boundaries.

Trade-off: adapters must normalize runtime-specific failures and metadata.
