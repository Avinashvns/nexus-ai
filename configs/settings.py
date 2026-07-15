from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """
    Application Settings.
    Loaded automatically from .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    app_name: str = Field(
        ...,
        alias="APP_NAME",
    )

    app_version: str = Field(
        ...,
        alias="APP_VERSION",
    )

    debug: bool = Field(
        ...,
        alias="DEBUG",
    )

    host: str = Field(
        ...,
        alias="HOST",
    )

    port: int = Field(
        ...,
        alias="PORT",
    )

    ollama_host: str = Field(
        ...,
        alias="OLLAMA_HOST",
    )

    default_model: str = Field(
        ...,
        alias="DEFAULT_MODEL",
    )

    database_url: str = Field(
        default="sqlite:///./nexus_ai.db",
        alias="DATABASE_URL",
    )

    log_level: str = Field(
        ...,
        alias="LOG_LEVEL",
    )

    @field_validator(
        "app_name",
        "app_version",
        "host",
        "default_model",
        "log_level",
    )
    @classmethod
    def validate_non_empty(
        cls,
        value: str,
    ) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Configuration value cannot be empty")

        return value

    @field_validator("ollama_host")
    @classmethod
    def validate_ollama_host(
        cls,
        value: str,
    ) -> str:
        value = value.strip()

        if not value.startswith(("http://", "https://")):
            raise ValueError("ollama_host must use HTTP or HTTPS")

        return value.rstrip("/")

    @field_validator("database_url")
    @classmethod
    def validate_database_url(
        cls,
        value: str,
    ) -> str:
        value = value.strip()

        if "://" not in value:
            raise ValueError("Invalid database URL")

        return value


@lru_cache
def get_settings() -> Settings:
    """
    Returns cached settings instance.
    """

    return Settings()
