from unittest.mock import patch

from database.init_db import init_database
from memory.manager import memory_manager
from models import AgentResponse
from workflow.engine import workflow_engine


SESSION_ID = "persistent-workflow-test"


def main():
    print(
        "Starting Persistent Workflow Memory Test"
    )

    init_database()

    memory_manager.clear(SESSION_ID)

    memory_manager.add_user_message(
        session_id=SESSION_ID,
        content="My project is Nexus AI.",
    )

    memory_manager.add_assistant_message(
        session_id=SESSION_ID,
        content="Nexus AI project noted.",
    )

    planner_response = AgentResponse(
        success=True,
        output=[
            {
                "id": 1,
                "task": "Answer using conversation memory",
                "agent": "ReasoningAgent",
                "priority": 1,
                "status": "pending",
            }
        ],
        metadata={
            "agent": "PlannerAgent",
        },
    )

    reasoning_response = AgentResponse(
        success=True,
        output="The user's project is Nexus AI.",
        metadata={
            "agent": "ReasoningAgent",
        },
    )

    captured_context = {}

    def mock_execute(
        agent_name,
        request,
    ):
        captured_context.update(
            request.context
        )

        return reasoning_response

    with patch(
        "workflow.engine.planner_agent.run",
        return_value=planner_response,
    ):
        with patch(
            "workflow.engine.agent_executor.execute",
            side_effect=mock_execute,
        ):
            response = workflow_engine.run(
                task="What is my project?",
                session_id=SESSION_ID,
            )

    assert response.success is True

    conversation_memory = (
        captured_context[
            "conversation_memory"
        ]
    )

    assert (
        "My project is Nexus AI."
        in conversation_memory
    )

    assert (
        "Nexus AI project noted."
        in conversation_memory
    )

    print("\nConversation Memory:")
    print(conversation_memory)

    print("\nWorkflow Response:")
    print(response.output)

    print(
        "\nPersistent Workflow Memory Test Passed"
    )


if __name__ == "__main__":
    main()