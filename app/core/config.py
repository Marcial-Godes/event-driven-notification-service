from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):

    # Entorno local por defecto
    app_env: str = "development"

    # Conexión a PostgreSQL
    database_url: str

    # Broker y backend para Celery
    celery_broker_url: str
    celery_result_backend: str

    # Reservado para futuras capas de autenticación
    secret_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()