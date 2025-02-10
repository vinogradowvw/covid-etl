from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from models.User import User
from core.exceptions.DuplicateUserError import DuplicateUserError
from services import UserService
from core.dependencies import get_user_service


router = APIRouter(prefix="/users",
                   tags=["Users"])


@router.post("/register")
async def register(user: User,
                   service: UserService = Depends(get_user_service)
                   ):
    try:
        user = await service.create_user(user)
        return user
    except DuplicateUserError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(error))


@router.post("/recreate-api-key")
async def recreate_api_key(user: User,
                           service: UserService = Depends(get_user_service)
                           ):
    return await service.recreate_api_key(user)
