from typing import List, Optional

from sqlalchemy.orm import Session

from src.core.types.exceptions_type import BadRequestException
from src.core.types.update_result_type import UpdateResult
from .dto.create_user_dto import CreateUserDto
from .dto.update_user_dto import UpdateUserDto
from .dto.user_dto import UserDto
from .entities.user_entity import User
from .user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    # PUBLIC METHODS
    async def create_user(self, user_dto: CreateUserDto, db_session: Session) -> Optional[UserDto]:
        user = await self.__verify_email_exist(user_dto.email, db_session)

        if user:
            raise BadRequestException(f'An "User" with email {user_dto.email} already exists.')

        new_user = User(name=user_dto.name, email=user_dto.email, password=user_dto.password)
        new_user = await self.user_repository.create(db_session, new_user)

        return UserDto(self.user_repository.save(db_session, new_user))

    async def get_all_users(self, db_session: Session) -> Optional[List[UserDto]]:
        all_users = await self.user_repository.find(db_session)

        return list(map(UserDto, all_users))

    async def get_user_by_id(self, user_id: str, db_session: Session) -> Optional[UserDto]:
        user = await self.user_repository.find_one_or_fail(db_session, user_id)

        return UserDto(user)

    async def delete_user(self, user_id: str, db_session: Session) -> Optional[UpdateResult]:
        return await self.user_repository.soft_delete(db_session, user_id)

    async def update_user(
            self, user_id: str, update_user_dto: UpdateUserDto, database: Session
    ) -> Optional[UpdateResult]:
        return await self.user_repository.update(database, user_id, update_user_dto)

    # PRIVATE METHODS
    async def __verify_email_exist(self, email: str, db_session: Session) -> Optional[User]:
        return await self.user_repository.find_one(db_session, {'where': User.email == email})

