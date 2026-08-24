import os
from typing import Optional

from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(
        default="Phoenix Hub",
        validation_alias=AliasChoices("APP_NAME", "PROJECT_NAME", "app_name"),
    )
    app_version: str = Field(
        default="0.1.0",
        validation_alias=AliasChoices("APP_VERSION", "VERSION", "app_version"),
    )
    service_name: str = Field(
        default="phoenix-hub-api",
        validation_alias=AliasChoices("SERVICE_NAME", "service_name"),
    )
    environment: str = Field(
        default="development",
        validation_alias=AliasChoices("ENVIRONMENT", "environment"),
    )
    debug: bool = Field(
        default=False,
        validation_alias=AliasChoices("DEBUG", "debug"),
    )

    # development auth helpers — set via environment/.env in dev only
    dev_user: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("DEV_USER", "dev_user"),
    )
    dev_password: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("DEV_PASSWORD", "dev_password"),
    )
    dev_token: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("DEV_TOKEN", "dev_token"),
    )

    # declare minimum python runtime for contributors/CI
    min_python_version: str = "3.10"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_runtime_requirements(self) -> "Settings":
        env_name = (os.getenv("ENVIRONMENT", self.environment or "")).lower()

        if env_name == "production":
            missing = []
            for key in ("DEV_USER", "DEV_PASSWORD", "DEV_TOKEN"):
                if not os.getenv(key):
                    missing.append(key)
            if missing:
                raise ValueError(
                    "Production environment requires: " + ", ".join(missing)
                )

        return self

    @property
    def project_name(self) -> str:
        """
        Compatibility property: some code expects `settings.project_name`.
        Map it to app_name to avoid AttributeError.
        """
        return self.app_name


def get_settings() -> Settings:
    return Settings()
