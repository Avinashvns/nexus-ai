from typing import Any

from pydantic import BaseModel, Field, field_validator

from core.constants import (
    MAX_SESSION_ID_LENGTH,
    MAX_TASK_LENGTH,
)


class ChatRequest(BaseModel):
    task: str = Field(
        ...,
        min_length=1,
        max_length=MAX_TASK_LENGTH,
    )

    session_id: str = Field(
        ...,
        min_length=1,
        max_length=MAX_SESSION_ID_LENGTH,
    )

    @field_validator(
        "task",
        "session_id",
    )
    @classmethod
    def validate_non_empty_text(
        cls,
        value: str,
    ) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Value cannot be empty"
            )

        return value


class ChatResponse(BaseModel):
    success: bool
    response: Any
    metadata: dict[str, Any]