# Architecture

## Request path

1. Validate the inference contract.
2. Attach a correlation/request ID.
3. Select a healthy backend.
4. Enforce bounded local concurrency.
5. Execute through the backend protocol.
6. Return normalized output and backend metadata.

## Failure model

- Invalid request -> 4xx
- No healthy backend -> 503
- Backend execution failure -> 502
- Local overload -> 429 (reserved for an explicit admission-control layer)

The router intentionally does not blindly retry inference calls; retry semantics belong where idempotency, budgets, and user intent are known.

## Scaling boundary

The API is stateless. Production deployments can externalize health state and place multiple replicas behind a load balancer.

## Extension points

GPU/CPU runtime adapters, dynamic model loading, distributed health, OpenTelemetry, token/cost accounting, priority queues, and admission control.
