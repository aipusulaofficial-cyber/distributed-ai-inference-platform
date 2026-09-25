from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=32_000)
    model: str = Field(default="default", min_length=1, max_length=200)
    max_tokens: int = Field(default=256, ge=1, le=8192)


class InferenceResponse(BaseModel):
    request_id: str
    model: str
    output: str
    backend: str
