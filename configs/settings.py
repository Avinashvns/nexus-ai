from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings
    Loaded automatically from .env
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    app_name: str = Field(..., alias="APP_NAME")
    app_version: str = Field(..., alias="APP_VERSION")

    debug: bool = Field(..., alias="DEBUG")

    host: str = Field(..., alias="HOST")
    port: int = Field(..., alias="PORT")

    ollama_host: str = Field(..., alias="OLLAMA_HOST")
    default_model: str = Field(..., alias="DEFAULT_MODEL")    
    
    database_url: str = "sqlite:///./nexus_ai.db"

    log_level: str = Field(..., alias="LOG_LEVEL")


@lru_cache
def get_settings() -> Settings:
    """
    Returns cached settings instance.
    """
    return Settings()