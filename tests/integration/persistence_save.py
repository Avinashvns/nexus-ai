from database.init_db import init_database
from memory.manager import memory_manager


SESSION_ID = "restart-persistence-test"


def main():
    init_database()

    memory_manager.clear(
        SESSION_ID
    )

    memory_manager.add_user_message(
        session_id=SESSION_ID,
        content="My project is Nexus AI.",
    )

    memory_manager.add_assistant_message(
        session_id=SESSION_ID,
        content=(
            "Nexus AI is your multi-agent "
            "AI platform."
        ),
    )

    print(
        "Memory saved successfully"
    )


if __name__ == "__main__":
    main()