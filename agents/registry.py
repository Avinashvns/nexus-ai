from agents.base import BaseAgent


class AgentRegistry:
    def __init__(self):
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        if agent.name in self._agents:
            raise ValueError(
                f"Agent '{agent.name}' is already registered"
            )

        self._agents[agent.name] = agent

    def get(self, name: str) -> BaseAgent:
        agent = self._agents.get(name)

        if agent is None:
            raise KeyError(
                f"Agent '{name}' is not registered"
            )

        return agent

    def list_agents(self) -> list[str]:
        return list(self._agents.keys())


agent_registry = AgentRegistry()