from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class WebSettings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    APP_CORS_ALLOW_ORIGINS: List[str]

    SENTRY_DSN: str = ""
    SENTRY_TRACES_SAMPLE_RATE: float
    SENTRY_ENVIRONMENT: str = "dev"

    model_config = SettingsConfigDict(
        env_file="../task_manager/src/backend/.env",
        env_file_encoding="utf-8",
        extra="allow",
    )


web_settings = WebSettings()
