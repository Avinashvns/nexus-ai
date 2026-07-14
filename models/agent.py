from typing import Any

from pydantic import BaseModel, Field

class AgentRequest(BaseModel):
    task: str
    context: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    success: bool
    output: Any
    metadata: dict[str, Any] = Field(default_factory=dict)