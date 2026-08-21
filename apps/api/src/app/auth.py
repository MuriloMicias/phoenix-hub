from fastapi import Header, HTTPException, status
from typing import Optional
import secrets

from app.core.settings import get_settings

settings = get_settings()


def get_token(authorization: Optional[str] = Header(default=None, alias="Authorization")) -> str:
    """Dependency that validates the Authorization header and returns the token.

    Expects header: "Authorization: Bearer <token>".
    Raises HTTPException(401) if missing/invalid. Raises RuntimeError if dev_token is not configured.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = authorization.split(" ", 1)[1]
    expected = getattr(settings, "dev_token", None)
    if expected is None:
        # Fail fast so CI/dev environments must explicitly set the dev token
        raise RuntimeError("dev_token not configured in settings (set via .env in dev)")

    # Timing-safe compare
    if not secrets.compare_digest(token, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return token
