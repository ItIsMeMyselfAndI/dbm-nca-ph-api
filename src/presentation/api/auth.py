from fastapi import Header, HTTPException, status

from src.infrastructure.config import settings


async def require_pipeline_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    if x_api_key is None or x_api_key != settings.PIPELINE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
