from database.init_db import init_database
from memory.manager import memory_manager


SESSION_ID = "restart-persistence-test"


def main():
    init_database()

    messages = memory_manager.get_messages(
        SESSION_ID
    )

    assert len(messages) == 2

    assert (
        messages[0]["content"]
        == "My project is Nexus AI."
    )

    assert (
        messages[1]["content"]
        == (
            "Nexus AI is your multi-agent "
            "AI platform."
        )
    )

    print("Persisted Memory:")

    for message in messages:
        print(message)

    print(
        "\nApplication Restart "
        "Persistence Test Passed"
    )


if __name__ == "__main__":
    main()