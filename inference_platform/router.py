import asyncio
from dataclasses import dataclass

from .backends import BackendError, InferenceBackend

@dataclass
class BackendState:
    backend: InferenceBackend
    healthy: bool = True

class NoHealthyBackend(BackendError):
    pass

class InferenceRouter:
    def __init__(self, backends: list[InferenceBackend], max_concurrency: int = 32) -> None:
        if not backends:
            raise ValueError("at least one backend is required")
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be positive")
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
        state = await self._next_healthy()
        async with self._semaphore:
            try:
                return await state.backend.infer(prompt, max_tokens), state.backend.name
            except Exception as exc:
                state.healthy = False
                raise BackendError(f"backend {state.backend.name!r} failed") from exc

    def set_health(self, backend_name: str, healthy: bool) -> None:
        for state in self._states:
            if state.backend.name == backend_name:
                state.healthy = healthy
                return
        raise KeyError(backend_name)
