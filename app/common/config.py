from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    APP_NAME: str = "Notification Service"
    APP_VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"
    API_KEY: str
    API_PREFIX: str = "/api"
    API_VERSION: str = "v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
