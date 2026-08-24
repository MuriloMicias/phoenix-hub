import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api" / "src"))

from app.core.settings import Settings


def test_settings_accepts_uppercase_env_aliases(monkeypatch):
    monkeypatch.setenv("APP_NAME", "Phoenix Hub Prod")
    monkeypatch.setenv("APP_VERSION", "9.9.9")
    monkeypatch.setenv("SERVICE_NAME", "phoenix-hub-prod")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("DEV_USER", "admin")
    monkeypatch.setenv("DEV_PASSWORD", "secret")
    monkeypatch.setenv("DEV_TOKEN", "token-123")

    settings = Settings()

    assert settings.app_name == "Phoenix Hub Prod"
    assert settings.app_version == "9.9.9"
    assert settings.service_name == "phoenix-hub-prod"
    assert settings.environment == "production"
    assert settings.debug is True
    assert settings.dev_user == "admin"
    assert settings.dev_password == "secret"
    assert settings.dev_token == "token-123"


def test_settings_requires_runtime_credentials_in_production(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.delenv("DEV_USER", raising=False)
    monkeypatch.delenv("DEV_PASSWORD", raising=False)
    monkeypatch.delenv("DEV_TOKEN", raising=False)

    with pytest.raises(ValidationError, match="DEV_USER|DEV_PASSWORD|DEV_TOKEN"):
        Settings()
