from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Phoenix Hub"
    app_version: str = "0.0.0"
    service_name: str = "phoenix-hub"
    environment: str = "development"
    debug: bool = True

    # development auth helpers — set via environment/.env in dev only
    dev_user: Optional[str] = None
    dev_password: Optional[str] = None
    dev_token: Optional[str] = None

    # declare minimum python runtime for contributors/CI
    min_python_version: str = "3.10"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings() -> Settings:
    return Settings()
