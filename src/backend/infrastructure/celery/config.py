from pydantic_settings import SettingsConfigDict, BaseSettings


class CelerySettings(BaseSettings):
    TASK_BROKER_URL: str
    PERIODIC_WORKER_QUEUE_NAME: str

    SENTRY_DSN: str = ""
    SENTRY_TRACES_SAMPLE_RATE: float
    SENTRY_ENVIRONMENT: str = "dev"

    model_config = SettingsConfigDict(
        env_file="../task_manager/src/backend/.env",
        env_file_encoding="utf-8",
        extra="allow",
    )


celery_settings = CelerySettings()
