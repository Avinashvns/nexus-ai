from pydantic import ValidationError

from configs.settings import Settings
from core.config_validation import (
    validate_configuration,
)


def main():
    valid_settings = Settings(
        app_name="Nexus AI",
        ollama_host="http://localhost:11434",
        default_model="qwen3:4b",
        database_url="sqlite:///./test.db",
    )

    validate_configuration(
        valid_settings
    )

    assert (
        valid_settings.ollama_host
        == "http://localhost:11434"
    )

    try:
        Settings(
            ollama_host="localhost:11434",
        )

        raise AssertionError(
            "Invalid Ollama host was accepted"
        )

    except ValidationError:
        pass

    try:
        Settings(
            database_url="invalid-database-url",
        )

        raise AssertionError(
            "Invalid database URL was accepted"
        )

    except ValidationError:
        pass

    try:
        Settings(
            default_model="   ",
        )

        raise AssertionError(
            "Empty model was accepted"
        )

    except ValidationError:
        pass

    print(
        "Configuration validation successful"
    )

    print(
        "\nConfig Validation Test Passed"
    )


if __name__ == "__main__":
    main()