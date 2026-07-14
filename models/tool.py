from typing import Any

from pydantic import BaseModel, Field


class ToolRequest(BaseModel):
    input: Any
    context: dict[str, Any] = Field(default_factory=dict)


class ToolResponse(BaseModel):
    success: bool
    output: Any
    metadata: dict[str, Any] = Field(default_factory=dict)