import agents

from agents.registry import agent_registry
from models import AgentRequest


def main():
    print(agent_registry.list_agents())

    agent = agent_registry.get(
        "ReasoningAgent"
    )

    request = AgentRequest(
        task="Explain Nexus AI.",
        context={
            "retrieved_context": [
                {
                    "content": (
                        "Nexus AI is a multi-agent AI platform."
                    ),
                    "score": 0.91,
                }
            ]
        },
    )

    response = agent.run(request)

    print(response.model_dump())


if __name__ == "__main__":
    main()