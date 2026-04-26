from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"

    database_url: str
    redis_url: str

    secret_key: str

    celery_broker_url: str
    celery_result_backend: str

    rate_limit_per_minute: int = 5
    max_retries: int = 5

    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()