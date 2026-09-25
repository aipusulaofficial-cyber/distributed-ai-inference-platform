from dataclasses import dataclass


@dataclass(frozen=True)
class InferenceRequest:
    model: str
    prompt: str
    max_tokens: int = 256

    def validate(self) -> None:
        if not self.model.strip() or not self.prompt.strip():
            raise ValueError("model and prompt are required")
        if not 1 <= self.max_tokens <= 8192:
            raise ValueError("max_tokens out of range")


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay: float = 0.1
    max_delay: float = 2.0

    def delay(self, attempt: int) -> float:
        if attempt < 0 or attempt >= self.max_attempts:
            raise ValueError("invalid attempt")
        return min(self.max_delay, self.base_delay * (2**attempt))


def classify_backend_error(exc: Exception) -> str:
    return "timeout" if isinstance(exc, TimeoutError) else "backend_error"
