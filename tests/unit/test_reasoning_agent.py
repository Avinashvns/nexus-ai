from agents.reasoning import reasoning_agent
from models import AgentRequest


def main():
    request = AgentRequest(
        task="Explain what Nexus AI does.",
        context={
            "retrieved_context": [
                {
                    "content": (
                        "Nexus AI is a multi-agent AI platform."
                    ),
                    "score": 0.91,
                },
                {
                    "content": (
                        "The system includes RAG and tool calling."
                    ),
                    "score": 0.85,
                },
            ]
        },
    )

    response = reasoning_agent.run(request)

    print(response.model_dump())


if __name__ == "__main__":
    main()