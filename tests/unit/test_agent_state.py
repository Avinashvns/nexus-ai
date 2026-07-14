from models import AgentState


def main():
    state = AgentState(
        current_agent="Planner",
        task="Research Agentic AI"
    )

    print(state.model_dump())


if __name__ == "__main__":
    main()