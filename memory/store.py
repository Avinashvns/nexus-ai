from typing import Any

from sqlalchemy import delete, select

from database.base import SessionLocal
from database.models import ConversationMessage


class MemoryStore:
    def add(
        self,
        session_id: str,
        role: str,
        content: Any,
    ) -> None:
        if not session_id.strip():
            raise ValueError(
                "session_id cannot be empty"
            )

        if role not in {
            "user",
            "assistant",
            "system",
        }:
            raise ValueError(
                f"Invalid memory role: {role}"
            )

        database = SessionLocal()

        try:
            message = ConversationMessage(
                session_id=session_id,
                role=role,
                content=str(content),
            )

            database.add(message)

            database.commit()

        except Exception:
            database.rollback()
            raise

        finally:
            database.close()

    def get(
        self,
        session_id: str,
    ) -> list[dict[str, Any]]:
        database = SessionLocal()

        try:
            statement = (
                select(ConversationMessage)
                .where(
                    ConversationMessage.session_id
                    == session_id
                )
                .order_by(
                    ConversationMessage.created_at.asc(),
                    ConversationMessage.id.asc(),
                )
            )

            messages = database.scalars(
                statement
            ).all()

            return [
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in messages
            ]

        finally:
            database.close()

    def clear(
        self,
        session_id: str,
    ) -> None:
        database = SessionLocal()

        try:
            statement = delete(
                ConversationMessage
            ).where(
                ConversationMessage.session_id
                == session_id
            )

            database.execute(statement)

            database.commit()

        except Exception:
            database.rollback()
            raise

        finally:
            database.close()


memory_store = MemoryStore()