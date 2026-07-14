from typing import Any

from pydantic import BaseModel, Field


class AgentState(BaseModel):
    current_agent: str = ""
    task: str = ""

    completed: bool = False

    context: dict[str, Any] = Field(default_factory=dict)

    metadata: dict[str, Any] = Field(default_factory=dict)