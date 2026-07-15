from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=100,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    @field_validator("username")
    @classmethod
    def validate_username(
        cls,
        value: str,
    ) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Username cannot be empty"
            )

        return value


class LoginRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=100,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )