from pydantic import ValidationError

from api.schemas.chat import ChatRequest
from core.constants import MAX_TASK_LENGTH


def main():
    valid_request = ChatRequest(
        task="Explain Nexus AI",
        session_id="test-session",
    )

    assert (
        valid_request.task
        == "Explain Nexus AI"
    )

    try:
        ChatRequest(
            task="   ",
            session_id="test-session",
        )

        raise AssertionError(
            "Whitespace task was accepted"
        )

    except ValidationError:
        pass

    try:
        ChatRequest(
            task="A" * (MAX_TASK_LENGTH + 1),
            session_id="test-session",
        )

        raise AssertionError(
            "Oversized task was accepted"
        )

    except ValidationError:
        pass

    try:
        ChatRequest(
            task="Explain Nexus AI",
            session_id="   ",
        )

        raise AssertionError(
            "Whitespace session ID was accepted"
        )

    except ValidationError:
        pass

    print(
        "Request Validation Test Passed"
    )


if __name__ == "__main__":
    main()