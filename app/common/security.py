from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

from app.common.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def validate_api_key(api_key: str | None = Security(api_key_header)) -> str:
    if api_key is None or api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "API-Key"},
        )
    return api_key
