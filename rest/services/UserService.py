from fastapi import HTTPException, status
from repositories import UserRepository
from models.User import User, UserModel
from passlib.context import CryptContext
from secrets import token_hex


class UserService():

    def __init__(self, repository: UserRepository) -> None:
        self.__repository = repository
        self.__hashing_context = CryptContext(["sha256_crypt"])

    def __hash(self, token: str) -> str:
        return self.__hashing_context.hash(token)

    async def create_user(self, user: User) -> User:
        user.token = await self.__generate_api_key()
        user_model = UserModel(**user.model_dump())
        user_model.token = self.__hash(user.token)
        user_model.password = self.__hash(user.password)
        await self.__repository.save_user(user_model)
        return user

    async def __generate_api_key(self) -> str:
        api_key = token_hex(16)
        return api_key

    async def recreate_api_key(self, user: User):

        user_model = await self.__repository.get_user_by_username(user.username)

        passowrd_correct = await self.__validate_password(user.password, user_model.password)
        if not passowrd_correct:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Incorrect password or username')

        user.token = await self.__generate_api_key()
        user_model.token = self.__hash(user.token)
        await self.__repository.client.commit()
        return user

    async def token_exists(self, token: str) -> bool:
        users = await self.__repository.get_all_users()
        return any([self.__hashing_context.verify(token, user.token) for user in users])

    async def __validate_password(self, plaintext_pwd: str, hashed_pwd: str) -> bool:
        return self.__hashing_context.verify(plaintext_pwd, hashed_pwd)
