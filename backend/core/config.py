import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def resolve_env_file() -> Path:
    env_override = os.getenv("ENV_FILE")

    if env_override:
        return Path(env_override).expanduser().resolve()

    current = Path(__file__).resolve().parent

    for directory in [current, *current.parents]:
        candidate = directory / ".env"

        if candidate.is_file():
            return candidate

    return Path(".env")


_ROOT_ENV = resolve_env_file()


class Settings(BaseSettings):
    groq_api_key: str
    database_url: str
    checkpoint_database_url: str
    secret_key: str
    access_token_expire_minutes: int = 30
    postgres_user: str = "postgres"
    postgres_password: str = ""
    postgres_db: str = "skillbridge"

    model_config = SettingsConfigDict(
        env_file=_ROOT_ENV,
        extra="ignore",
    )


settings = Settings()

