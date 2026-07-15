from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    workflow_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        index=True,
        nullable=False,
    )

    session_id: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
    )

    task: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="running",
    )

    metrics: Mapped[
        dict[str, Any] | None
    ] = mapped_column(
        JSON,
        nullable=True,
    )

    execution_history: Mapped[
        list[dict[str, Any]] | None
    ] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(
            timezone.utc
        ),
        nullable=False,
    )

    completed_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True,
    )