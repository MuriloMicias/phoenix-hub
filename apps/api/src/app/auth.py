from fastapi import Depends, Header, HTTPException, status
from typing import Optional

from app.core.settings import get_settings

settings = get_settings()


def get_token(authorization: Optional[str] = Header(default=None, alias="Authorization")) -> str:
    """Dependency that validates the Authorization header and returns the token.

    It expects header in the shape: "Authorization: Bearer <token>".
    Raises HTTPException(401) if missing/invalid.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = authorization.split(" ", 1)[1]
    # compare with settings.dev_token; fallback to a default 'replace-me-in-env' if not provided
    expected = getattr(settings, "dev_token", "replace-me-in-env")
    if token != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return token
