from fastapi.testclient import TestClient

from database.init_db import init_database
from main import app


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def main() -> None:
    print("Starting Nexus AI v1 Regression Test")

    init_database()

    # -----------------------------------------
    # Health API
    # -----------------------------------------

    health_response = client.get("/health")

    assert health_response.status_code == 200

    print("Health API: PASS")

    # -----------------------------------------
    # Root API
    # -----------------------------------------

    root_response = client.get("/")

    assert root_response.status_code == 200

    print("Root API: PASS")

    # -----------------------------------------
    # Authentication Protection
    # -----------------------------------------

    chat_response = client.post(
        "/chat",
        json={
            "message": "Explain Nexus AI",
            "session_id": "v1-regression",
        },
    )

    assert chat_response.status_code == 401

    print("Protected Chat API: PASS")

    # -----------------------------------------
    # Workflow Protection
    # -----------------------------------------

    workflow_response = client.get(
        "/workflows/non-existent-workflow"
    )

    assert workflow_response.status_code == 401

    print("Protected Workflow API: PASS")

    # -----------------------------------------
    # Document Upload Safety
    # -----------------------------------------

    upload_response = client.post(
        "/documents/upload",
        files={
            "file": (
                "invalid.txt",
                b"invalid document",
                "text/plain",
            ),
        },
    )

    assert upload_response.status_code == 415

    print("Document Upload Safety: PASS")

    # -----------------------------------------
    # Security Headers
    # -----------------------------------------

    assert (
        health_response.headers.get(
            "x-content-type-options"
        )
        == "nosniff"
    )

    assert (
        health_response.headers.get(
            "x-frame-options"
        )
        == "DENY"
    )

    print("Security Headers: PASS")

    print()
    print("Nexus AI v1 Regression Test Passed")


if __name__ == "__main__":
    main()