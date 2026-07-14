from memory.store import MemoryStore


def main():
    memory = MemoryStore()

    session_id = "test-session"

    memory.add(
        session_id=session_id,
        role="user",
        content="My name is Avinash.",
    )

    memory.add(
        session_id=session_id,
        role="assistant",
        content="Hello Avinash.",
    )

    messages = memory.get(session_id)

    assert len(messages) == 2

    assert messages[0]["role"] == "user"

    assert messages[1]["role"] == "assistant"

    print(messages)

    memory.clear(session_id)

    assert memory.get(session_id) == []

    print("Memory Store Test Passed")


if __name__ == "__main__":
    main()