from agents.writer import writer_agent
from models import AgentRequest


def main():
    request = AgentRequest(
        task="Explain Nexus AI.",
        context={
            "critic_output": (
                "Nexus AI is a multi-agent AI platform "
                "that combines RAG and tool calling."
            )
        },
    )

    response = writer_agent.run(request)

    print(response.model_dump())


if __name__ == "__main__":
    main()