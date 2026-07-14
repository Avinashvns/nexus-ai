from memory.manager import memory_manager


def main():
    session_id = "test-session"

    memory_manager.add_user_message(
        session_id=session_id,
        content="My name is Avinash.",
    )

    memory_manager.add_assistant_message(
        session_id=session_id,
        content="Hello Avinash.",
    )

    memory_manager.add_user_message(
        session_id=session_id,
        content="What is my name?",
    )

    context = memory_manager.build_context(
        session_id=session_id,
    )

    print(context)

    assert "My name is Avinash." in context
    assert "Hello Avinash." in context
    assert "What is my name?" in context

    memory_manager.clear(session_id)

    print("\nMemory Manager Test Passed")


if __name__ == "__main__":
    main()