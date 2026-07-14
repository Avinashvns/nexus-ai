
from abc import ABC, abstractmethod

from models.agent import AgentRequest, AgentResponse

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def run(self, task: AgentRequest) -> AgentResponse:
        pass