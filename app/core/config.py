from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "FieldData Weather Alerts"
    api_v1_prefix: str = "/api/v1"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    postgres_server: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "fielddata"
    postgres_password: str = "fielddata"
    postgres_db: str = "fielddata"
    database_url: str = (
        "postgresql+asyncpg://fielddata:fielddata@localhost:5432/fielddata"
    )
    alert_evaluation_interval_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

