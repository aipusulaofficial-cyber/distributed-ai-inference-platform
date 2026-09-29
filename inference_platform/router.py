import asyncio
import math
from dataclasses import dataclass

from .backends import BackendError, InferenceBackend


@dataclass
class BackendState:
    backend: InferenceBackend
    healthy: bool = True


class NoHealthyBackend(BackendError):
    pass


class InferenceRouter:
    def __init__(
        self,
        backends: list[InferenceBackend],
        max_concurrency: int = 32,
        timeout_seconds: float = 2.0,
    ) -> None:
        if not backends:
            raise ValueError("at least one backend is required")
        if (
            isinstance(max_concurrency, bool)
            or not isinstance(max_concurrency, int)
            or max_concurrency < 1
        ):
            raise ValueError("max_concurrency must be a positive integer")
        if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be finite and positive")
        self._timeout_seconds = timeout_seconds
        self._states = [BackendState(b) for b in backends]
        self._cursor = 0
        self._lock = asyncio.Lock()
        self._semaphore = asyncio.Semaphore(max_concurrency)

    async def _next_healthy(self) -> BackendState:
        async with self._lock:
            for _ in range(len(self._states)):
                state = self._states[self._cursor % len(self._states)]
                self._cursor += 1
                if state.healthy:
                    return state
        raise NoHealthyBackend("no healthy inference backend is available")

    async def infer(self, prompt: str, max_tokens: int) -> tuple[str, str]:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be non-empty")
        if isinstance(max_tokens, bool) or not isinstance(max_tokens, int) or max_tokens < 1:
            raise ValueError("max_tokens must be a positive integer")
        async with self._semaphore:
            # Select an available backend only after obtaining an execution slot.
            state = await self._next_healthy()
            try:
                output = await asyncio.wait_for(
                    state.backend.infer(prompt, max_tokens),
                    timeout=self._timeout_seconds,
                )
                return output, state.backend.name
            except Exception as exc:
                state.healthy = False
                raise BackendError(f"backend {state.backend.name!r} failed") from exc

    def set_health(self, backend_name: str, healthy: bool) -> None:
        for state in self._states:
            if state.backend.name == backend_name:
                state.healthy = healthy
                return
        raise KeyError(backend_name)
