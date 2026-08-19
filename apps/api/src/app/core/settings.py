from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Phoenix Hub API"
    app_version: str = "0.1.0"
    project_name: str = "phoenix-hub"
    service_name: str = "phoenix-hub-api"
    environment: str = "development"
    debug: bool = True

    # development auth helpers (defaults for local/dev only)
    dev_user: str = "admin"
    dev_password: str = "admin123"
    dev_token: str = "demo-token"

    # declare minimum python runtime for contributors/CI
    min_python_version: str = "3.10"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings() -> Settings:
    return Settings()
