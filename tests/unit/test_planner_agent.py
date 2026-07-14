from agents.planner import planner_agent
from models import AgentRequest


def test_valid_plan():
    plan = [
        {
            "id": 1,
            "task": "Search Agentic AI",
            "agent": "SearchAgent",
            "priority": 1,
            "status": "pending",
        }
    ]

    assert planner_agent.validate_plan(plan) is True


def test_invalid_agent():
    plan = [
        {
            "id": 1,
            "task": "Search Agentic AI",
            "agent": "UnknownAgent",
            "priority": 1,
            "status": "pending",
        }
    ]

    assert planner_agent.validate_plan(plan) is False


def test_invalid_status():
    plan = [
        {
            "id": 1,
            "task": "Search Agentic AI",
            "agent": "SearchAgent",
            "priority": 1,
            "status": "completed",
        }
    ]

    assert planner_agent.validate_plan(plan) is False


def main():
    test_valid_plan()
    test_invalid_agent()
    test_invalid_status()

    request = AgentRequest(
        task="Research Agentic AI and create a report."
    )

    response = planner_agent.run(request)

    print(response.model_dump())


if __name__ == "__main__":
    main()