from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Phoenix Hub API"
    app_version: str = "0.1.0"
    project_name: str = "phoenix-hub"
    service_name: str = "phoenix-hub-api"
    environment: str = "development"
    debug: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings() -> Settings:
    return Settings()
