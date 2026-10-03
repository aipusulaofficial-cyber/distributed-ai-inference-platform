# Distributed AI Inference Platform

[![CI](https://github.com/aipusulaofficial-cyber/distributed-ai-inference-platform/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/aipusulaofficial-cyber/distributed-ai-inference-platform/actions/workflows/ci.yml)
[![Production Tests](https://github.com/aipusulaofficial-cyber/distributed-ai-inference-platform/actions/workflows/production-tests.yml/badge.svg?branch=main)](https://github.com/aipusulaofficial-cyber/distributed-ai-inference-platform/actions/workflows/production-tests.yml)
[![Security / SBOM](https://github.com/aipusulaofficial-cyber/distributed-ai-inference-platform/actions/workflows/security-sbom.yml/badge.svg?branch=main)](https://github.com/aipusulaofficial-cyber/distributed-ai-inference-platform/actions/workflows/security-sbom.yml)


A model-serving platform for reliable inference with routing, bounded concurrency, health-aware backends and observable request contracts.

## Request path
```text
client -> inference API -> router -> healthy backend -> model execution -> response
                         |             |
                    concurrency    health state
                         |
                      metrics
```

## Core behavior
- Requests are routed only through explicit backend boundaries.
- Concurrency is bounded to protect runtime resources.
- Backend health participates in routing decisions.
- Inference failures remain distinguishable from successful responses.
- Operational context is correlated with requests.

## Runtime hardening
The Kubernetes deployment uses non-root execution, `RuntimeDefault` seccomp, disabled privilege escalation, a read-only root filesystem, dropped Linux capabilities, readiness/liveness probes and CPU/memory limits. Images use concrete versions rather than `latest`.

## Verification
CI, production tests, security/SBOM checks and dependency auditing form the delivery gates.

## Evidence
[deploy/kubernetes.yaml](deploy/kubernetes.yaml) · [ARCHITECTURE.md](ARCHITECTURE.md) · [docs/PRINCIPAL-ENGINEERING.md](docs/PRINCIPAL-ENGINEERING.md)

## Portfolio evidence
[Portfolio evidence map](docs/PORTFOLIO_EVIDENCE.md) — executable proof, architecture mapping and reviewable CI evidence.
