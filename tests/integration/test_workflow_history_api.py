from uuid import uuid4

from fastapi.testclient import TestClient

from database.init_db import init_database
from database.repositories import (
    workflow_repository,
)
from main import app


client = TestClient(app)


def main():
    print(
        "Starting Workflow History API Test"
    )

    init_database()

    workflow_id = str(uuid4())

    workflow_repository.create(
        workflow_id=workflow_id,
        session_id="history-api-test",
        task="Explain Nexus AI",
    )

    workflow_repository.mark_completed(
        workflow_id=workflow_id,
        metrics={
            "workflow_success": True,
            "workflow_duration_seconds": 2.5,
            "agent_count": 1,
            "agents": [
                {
                    "agent": "ReasoningAgent",
                    "success": True,
                    "duration_seconds": 2.0,
                }
            ],
        },
        execution_history=[
            {
                "step_id": 1,
                "agent": "ReasoningAgent",
                "success": True,
                "attempts": 1,
            }
        ],
    )

    response = client.get(
        f"/workflows/{workflow_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    workflow = data["workflow"]

    assert (
        workflow["workflow_id"]
        == workflow_id
    )

    assert workflow["status"] == "completed"

    assert workflow["metrics"] is not None

    assert (
        workflow["metrics"]["agent_count"]
        == 1
    )

    assert (
        workflow["execution_history"][0][
            "agent"
        ]
        == "ReasoningAgent"
    )

    print("\nWorkflow API Response:")
    print(data)

    missing_response = client.get(
        "/workflows/non-existent-workflow"
    )

    assert missing_response.status_code == 404

    print(
        "\nWorkflow History API Test Passed"
    )


if __name__ == "__main__":
    main()