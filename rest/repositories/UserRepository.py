from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from core.exceptions import DuplicateUserError
from models import UserModel
from repositories.Repository import Repository


class UserRepository(Repository):

    async def save_user(self, user: UserModel):
        try:
            self.client.add(user)
            await self.client.commit()
            await self.client.refresh(user)
        except IntegrityError:
            await self.client.rollback()
            raise DuplicateUserError(f"User with username {user.username} already exists")
        else:
            await self.client.rollback()

    async def get_all_users(self) -> list[UserModel]:
        result = await self.client.execute(select(UserModel))
        return result.scalars().all()

    async def get_user_by_username(self, username: str) -> UserModel:
        return await self.client.get(UserModel, username)
