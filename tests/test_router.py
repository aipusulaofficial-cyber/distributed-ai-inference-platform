import pytest

from inference_platform.backends import EchoBackend
from inference_platform.router import InferenceRouter, NoHealthyBackend


@pytest.mark.asyncio
async def test_routes_to_healthy_backend():
    router = InferenceRouter([EchoBackend(name="a")])
    output, backend = await router.infer("hello", 10)
    assert output == "hello"
    assert backend == "a"


@pytest.mark.asyncio
async def test_rejects_when_all_backends_are_unhealthy():
    router = InferenceRouter([EchoBackend(name="a")])
    router.set_health("a", False)
    with pytest.raises(NoHealthyBackend):
        await router.infer("hello", 10)


def test_requires_backend():
    with pytest.raises(ValueError):
        InferenceRouter([])
