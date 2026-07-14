from abc import ABC, abstractmethod

from models.tool import ToolRequest, ToolResponse


class BaseTool(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, request: ToolRequest) -> ToolResponse:
        pass