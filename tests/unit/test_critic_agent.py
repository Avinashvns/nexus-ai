from agents.critic import critic_agent
from models import AgentRequest


def main():
    request = AgentRequest(
        task="Explain Nexus AI.",
        context={
            "reasoning_output":
            "Nexus AI is a multi-agent AI platform with RAG."
        },
    )

    response = critic_agent.run(request)

    print(response.model_dump())


if __name__ == "__main__":
    main()