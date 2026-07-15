from core.logger import app_logger
from database.base import Base, engine

import database.models


def init_database() -> None:
    app_logger.info(
        "Initializing database"
    )

    Base.metadata.create_all(
        bind=engine
    )

    app_logger.success(
        "Database initialized successfully"
    )