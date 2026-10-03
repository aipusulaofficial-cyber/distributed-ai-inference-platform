import asyncio
import math

import pytest

from inference_platform.backends import EchoBackend
from inference_platform.router import InferenceRouter


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "prompt,tokens",
    [("", 1), ("  ", 1), ("hello", 0), ("hello", -1), ("hello", True)],
)
async def test_invalid_requests_rejected_before_backend(prompt, tokens):
    router = InferenceRouter([EchoBackend(name="echo")])
    with pytest.raises(ValueError):
        await router.infer(prompt, tokens)


@pytest.mark.parametrize("timeout", [math.nan, math.inf, -1.0, 0.0, True, "2"])
def test_invalid_timeout_configuration_fails_closed(timeout):
    with pytest.raises(ValueError, match="timeout"):
        InferenceRouter([EchoBackend(name="echo")], timeout_seconds=timeout)


@pytest.mark.asyncio
async def test_active_work_never_exceeds_admission_limit():
    class CountingBackend:
        name = "count"
        weight = 1

        def __init__(self):
            self.active = 0
            self.high_watermark = 0

        async def infer(self, prompt, max_tokens):
            self.active += 1
            self.high_watermark = max(self.high_watermark, self.active)
            await asyncio.sleep(0.001)
            self.active -= 1
            return prompt[:max_tokens]

    backend = CountingBackend()
    router = InferenceRouter([backend], max_concurrency=2)
    await asyncio.gather(*(router.infer("work", 4) for _ in range(10)))
    assert backend.high_watermark <= 2
