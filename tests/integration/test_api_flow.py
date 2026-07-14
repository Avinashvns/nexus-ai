from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from models import AgentResponse


client = TestClient(app)


def main():
    print("Starting Full API Integration Test")

    with open(
        "tests/data/sample.pdf",
        "rb",
    ) as file:
        upload_response = client.post(
            "/documents/upload",
            files={
                "file": (
                    "sample.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    assert upload_response.status_code == 200

    upload_data = upload_response.json()

    assert upload_data["success"] is True
    assert upload_data["chunk_count"] > 0

    print("\nDocument Upload:")
    print(upload_data)

    workflow_response = AgentResponse(
        success=True,
        output="Nexus AI is a multi-agent AI platform.",
        metadata={
            "workflow_completed": True,
        },
    )

    with patch(
        "api.routes.chat.workflow_engine.run",
        return_value=workflow_response,
    ):
        chat_response = client.post(
            "/chat",
            json={
                "message": (
                    "Explain what Nexus AI does."
                ),
                "session_id": "api-flow-test",
            },
        )

    assert chat_response.status_code == 200

    chat_data = chat_response.json()

    assert chat_data["success"] is True
    assert chat_data["response"]

    print("\nChat Response:")
    print(chat_data)

    print("\nFull API Integration Test Passed")


if __name__ == "__main__":
    main()