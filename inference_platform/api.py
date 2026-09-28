import time

from fastapi import FastAPI, HTTPException, Request

from observability import configure_observability, get_logger
from runtime_evidence import request_id_from_headers, runtime_evidence

from .backends import BackendError, EchoBackend
from .models import InferenceRequest, InferenceResponse
from .router import InferenceRouter, NoHealthyBackend


configure_observability()
logger = get_logger(__name__)
app = FastAPI(title="Distributed AI Inference Platform", version="0.1.0")
router = InferenceRouter([EchoBackend()])
