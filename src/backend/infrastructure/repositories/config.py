from pydantic_settings import SettingsConfigDict, BaseSettings


class DbSettings(BaseSettings):
    DATABASE_URL: str
    DB_SCHEMA: str = "public"

    model_config = SettingsConfigDict(
        env_file="../task_manager/src/backend/.env",
        env_file_encoding="utf-8",
        extra="allow",
    )


db_settings = DbSettings()
