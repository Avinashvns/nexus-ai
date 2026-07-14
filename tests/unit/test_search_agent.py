from agents.search import search_agent
from models import AgentRequest


def main():
    request = AgentRequest(
        task="Agentic AI"
    )

    response = search_agent.run(request)

    assert response.success is True

    print(response.model_dump())


if __name__ == "__main__":
    main()