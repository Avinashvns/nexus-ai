from typing import Any


class MemoryStore:
    def __init__(self):
        self._sessions: dict[
            str,
            list[dict[str, Any]],
        ] = {}

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

        if session_id not in self._sessions:
            self._sessions[session_id] = []

        self._sessions[session_id].append(
            {
                "role": role,
                "content": content,
            }
        )

    def get(
        self,
        session_id: str,
    ) -> list[dict[str, Any]]:
        return self._sessions.get(
            session_id,
            [],
        ).copy()

    def clear(
        self,
        session_id: str,
    ) -> None:
        self._sessions.pop(
            session_id,
            None,
        )


memory_store = MemoryStore()