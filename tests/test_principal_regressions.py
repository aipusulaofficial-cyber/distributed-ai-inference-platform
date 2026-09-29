import pytest

from inference_platform.router import InferenceRouter


class Backend:
    name = "echo"
    weight = 1

    async def infer(self, prompt, max_tokens):
        return prompt[:max_tokens]


@pytest.mark.asyncio
async def test_inference_returns_backend_identity():
    router = InferenceRouter([Backend()], max_concurrency=1)
    answer, backend = await router.infer("hello", 4)
    assert (answer, backend) == ("hell", "echo")
