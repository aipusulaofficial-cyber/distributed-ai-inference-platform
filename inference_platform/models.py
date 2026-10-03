from pydantic import BaseModel, Field, field_validator


class InferenceRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=32_000)
    model: str = Field(default="default", min_length=1, max_length=200)
    max_tokens: int = Field(default=256, ge=1, le=8192)

    @field_validator("prompt")
    @classmethod
    def prompt_must_contain_non_whitespace(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("prompt must be non-empty")
        return value


class InferenceResponse(BaseModel):
    request_id: str
    model: str
    output: str
    backend: str
    evidence: dict[str, object]
