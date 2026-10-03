import asyncio

import pytest

from inference_platform.backends import BackendError
from inference_platform.router import InferenceRouter


class SlowBackend:
    name = "slow"

    async def infer(self, prompt, max_tokens):
        await asyncio.sleep(2.1)
        return "late"


@pytest.mark.asyncio
async def test_backend_timeout_marks_dependency_failure():
    r = InferenceRouter([SlowBackend()], max_concurrency=1)
    with pytest.raises(BackendError):
        await r.infer("x", 1)
