from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from models import AgentResponse


client = TestClient(app)


def main():
    success_response = AgentResponse(
        success=True,
        output="Nexus AI response",
        metadata={
            "workflow_completed": True,
        },
    )

    with patch(
        "api.routes.chat.workflow_engine.run",
        return_value=success_response,
    ):
        response = client.post(
            "/chat",
            json={
                "message": "Explain Nexus AI",
                "session_id": "api-test",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["response"] == "Nexus AI response"

    print(data)

    print("\nChat API Test Passed")


if __name__ == "__main__":
    main()