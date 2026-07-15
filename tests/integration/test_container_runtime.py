import json
import subprocess
import urllib.request


CONTAINER_NAME = "nexus-ai"
HEALTH_URL = "http://127.0.0.1:8000/health"


def main() -> None:
    print("Starting Container Runtime Regression Test")

    result = subprocess.run(
        [
            "docker",
            "inspect",
            CONTAINER_NAME,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    container_data = json.loads(result.stdout)[0]

    state = container_data["State"]

    assert state["Running"] is True

    print("Container Running: PASS")

    health = state.get("Health")

    assert health is not None
    assert health["Status"] == "healthy"

    print("Docker Healthcheck: PASS")

    with urllib.request.urlopen(
        HEALTH_URL,
        timeout=10,
    ) as response:
        assert response.status == 200

        payload = json.loads(
            response.read().decode("utf-8")
        )

    assert payload["status"] == "healthy"

    print("Health Endpoint: PASS")

    mounts = container_data["Mounts"]

    mount_destinations = {
        mount["Destination"]
        for mount in mounts
    }

    assert "/app/data" in mount_destinations
    assert "/app/logs" in mount_destinations

    print("Persistent Volumes: PASS")

    print()
    print("Container Runtime Regression Test Passed")


if __name__ == "__main__":
    main()