from agents.executor import agent_executor
from models import AgentRequest


def main():
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

    response = agent_executor.execute(
        agent_name="ReasoningAgent",
        request=request,
    )

    print(response.model_dump())


if __name__ == "__main__":
    main()