from dataclasses import dataclass
from typing import Protocol

class BackendError(RuntimeError):
    """Raised when an inference backend cannot complete a request."""

class InferenceBackend(Protocol):
    name: str
    weight: int
    async def infer(self, prompt: str, max_tokens: int) -> str: ...

@dataclass
class EchoBackend:
    """Deterministic backend for local development and tests."""
    name: str = "echo"
    weight: int = 1

    async def infer(self, prompt: str, max_tokens: int) -> str:
        return prompt[:max_tokens]
