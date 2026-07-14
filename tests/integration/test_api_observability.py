from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from models import AgentResponse


client = TestClient(app)


def main():
    print(
        "Starting API Observability Test"
    )

    workflow_response = AgentResponse(
        success=True,
        output="Nexus AI response",
        metadata={
            "workflow_id": (
                "test-workflow-123"
            ),
            "execution_history": [
                {
                    "step_id": 1,
                    "agent": "ReasoningAgent",
                    "success": True,
                    "attempts": 1,
                }
            ],
            "metrics": {
                "workflow_success": True,
                "workflow_duration_seconds": 1.25,
                "agent_count": 1,
                "agents": [
                    {
                        "agent": "ReasoningAgent",
                        "success": True,
                        "duration_seconds": 1.0,
                    }
                ],
            },
        },
    )

    with patch(
        "api.routes.chat.workflow_engine.run",
        return_value=workflow_response,
    ):
        response = client.post(
            "/chat",
            json={
                "message": "Explain Nexus AI",
                "session_id": (
                    "observability-test"
                ),
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    metadata = data["metadata"]

    assert (
        metadata["workflow_id"]
        == "test-workflow-123"
    )

    assert "execution_history" in metadata

    assert "metrics" in metadata

    metrics = metadata["metrics"]

    assert (
        metrics["workflow_success"]
        is True
    )

    assert metrics["agent_count"] == 1

    assert (
        metrics["agents"][0]["agent"]
        == "ReasoningAgent"
    )

    print("\nAPI Response:")
    print(data)

    print(
        "\nAPI Observability Test Passed"
    )


if __name__ == "__main__":
    main()