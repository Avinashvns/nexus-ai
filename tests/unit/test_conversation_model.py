from sqlalchemy import select

from database.base import SessionLocal
from database.init_db import init_database
from database.models import ConversationMessage


def main():
    init_database()

    database = SessionLocal()

    session_id = "database-memory-test"

    try:
        database.query(
            ConversationMessage
        ).filter(
            ConversationMessage.session_id
            == session_id
        ).delete()

        database.commit()

        message = ConversationMessage(
            session_id=session_id,
            role="user",
            content="My project is Nexus AI.",
        )

        database.add(message)

        database.commit()

        database.refresh(message)

        assert message.id is not None

        statement = (
            select(ConversationMessage)
            .where(
                ConversationMessage.session_id
                == session_id
            )
        )

        stored_message = database.scalar(
            statement
        )

        assert stored_message is not None

        assert (
            stored_message.content
            == "My project is Nexus AI."
        )

        assert stored_message.role == "user"

        print(
            {
                "id": stored_message.id,
                "session_id": (
                    stored_message.session_id
                ),
                "role": stored_message.role,
                "content": stored_message.content,
                "created_at": str(
                    stored_message.created_at
                ),
            }
        )

    finally:
        database.close()

    print(
        "\nConversation Model Test Passed"
    )


if __name__ == "__main__":
    main()