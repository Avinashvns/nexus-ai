from memory.manager import memory_manager


def main():
    session_a = "session-a"
    session_b = "session-b"

    memory_manager.clear(session_a)
    memory_manager.clear(session_b)

    memory_manager.add_user_message(
        session_id=session_a,
        content="My project is Nexus AI.",
    )

    memory_manager.add_assistant_message(
        session_id=session_a,
        content="Nexus AI project noted.",
    )

    memory_manager.add_user_message(
        session_id=session_b,
        content="I am learning Python.",
    )

    memory_a = memory_manager.build_context(
        session_id=session_a,
    )

    memory_b = memory_manager.build_context(
        session_id=session_b,
    )

    print("Session A Memory:")
    print(memory_a)

    print("\nSession B Memory:")
    print(memory_b)

    assert "Nexus AI" in memory_a
    assert "Python" not in memory_a

    assert "Python" in memory_b
    assert "Nexus AI" not in memory_b

    print("\nSession Isolation Test Passed")


if __name__ == "__main__":
    main()