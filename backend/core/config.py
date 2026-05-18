from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve the root-level .env regardless of the working directory:
# backend/core/config.py → backend/core/ → backend/ → project_root/
_ROOT_ENV = Path(__file__).resolve().parents[2] / ".env"


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
        env_file=str(_ROOT_ENV),
        env_file_encoding="utf-8",
    )


settings = Settings()
