from agents.base import BaseAgent
from models.agent import AgentRequest, AgentResponse


class DemoAgent(BaseAgent):
    def run(self, request: AgentRequest) -> AgentResponse:
        return AgentResponse(
            success=True,
            output={
                "message": f"{self.name} executed",
                "task": request.task,
            },
        )


def main():
    agent = DemoAgent("Demo Agent")

    request = AgentRequest(
        task="Hello Nexus"
    )

    response = agent.run(request)

    print(response.model_dump())


if __name__ == "__main__":
    main()