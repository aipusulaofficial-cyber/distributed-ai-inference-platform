"""Compatibility entrypoint for the real inference service.

The canonical FastAPI application lives in inference_platform.api.
This module re-exports it so `uvicorn service:app` executes the same
router/backend path used by the package API and tests.
"""

from inference_platform.api import app

__all__ = ["app"]
