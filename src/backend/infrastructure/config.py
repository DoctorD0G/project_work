from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "App name"

    model_config = SettingsConfigDict(
        env_file="../task_manager/src/backend/.env",
        env_file_encoding="utf-8",
        extra="allow",
    )


app_settings = AppSettings()
