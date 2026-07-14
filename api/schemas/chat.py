from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
    )

    session_id: str = Field(
        default="default",
        min_length=1,
    )


class ChatResponse(BaseModel):
    success: bool
    response: Any
    metadata: dict[str, Any]