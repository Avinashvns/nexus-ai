from configs.settings import Settings
from core.logger import app_logger


def validate_configuration(
    settings: Settings,
) -> None:
    app_logger.info(
        "Validating application configuration"
    )

    if settings.database_url.startswith(
        "sqlite"
    ):
        app_logger.warning(
            "SQLite database configured"
        )

    if settings.default_model.endswith(
        ":8b"
    ):
        app_logger.warning(
            "Large LLM model configured"
        )

    app_logger.success(
        "Application configuration validated"
    )