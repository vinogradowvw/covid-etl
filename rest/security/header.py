from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException, status

from core.dependencies import get_user_service
from services import UserService

header_scheme = APIKeyHeader(name="x-key")


async def validate_api_key(x_key: str = Depends(header_scheme),
                           auth_service: UserService = Depends(get_user_service)):
    token_exists = await auth_service.token_exists(x_key)

    if not token_exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid API key")
