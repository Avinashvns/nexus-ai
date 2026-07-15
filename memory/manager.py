from typing import Any

from memory.store import memory_store


class MemoryManager:
    def add_user_message(
        self,
        session_id: str,
        content: str,
        user_id: int | None = None,
    ) -> None:
        memory_store.add(
            session_id=session_id,
            role="user",
            content=content,
            user_id=user_id,
        )

    def add_assistant_message(
        self,
        session_id: str,
        content: str,
        user_id: int | None = None,
    ) -> None:
        memory_store.add(
            session_id=session_id,
            role="assistant",
            content=content,
            user_id=user_id,
        )

    def get_messages(
        self,
        session_id: str,
        user_id: int | None = None,
    ) -> list[dict[str, Any]]:
        return memory_store.get(
            session_id=session_id,
            user_id=user_id,
        )

    def build_context(
        self,
        session_id: str,
        limit: int = 10,
    ) -> str:
        messages = self.get_messages(session_id)

        recent_messages = messages[-limit:]

        context_lines: list[str] = []

        for message in recent_messages:
            role = message["role"].capitalize()
            content = message["content"]

            context_lines.append(f"{role}: {content}")

        return "\n".join(context_lines)

    def clear(
        self,
        session_id: str,
    ) -> None:
        memory_store.clear(session_id)


memory_manager = MemoryManager()
