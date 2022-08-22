from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.types.exceptions_type import BadRequestException
from src.core.types.find_one_options_type import FindOneOptions
from src.core.types.update_result_type import UpdateResult
from .dto.create_user_dto import CreateUserDto
from .dto.update_user_dto import UpdateUserDto
from .dto.user_dto import UserDto
from .entities.user_entity import User
from .user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_user(self, user_dto: CreateUserDto, db_session: Session) -> Optional[UserDto]:
        user = await self.__verify_email_exist(user_dto.email, db_session)

        if user:
            raise BadRequestException(f"Email already in use.", ["User", "email"])

        new_user = await self.user_repository.create(user_dto, db_session)

        new_user = await self.user_repository.save(new_user, db_session)
        return UserDto(**new_user.__dict__)

    async def get_all_users(self, db_session: Session) -> Optional[List[UserDto]]:
        all_users = await self.user_repository.find(db=db_session)

        return [UserDto(**user.__dict__) for user in all_users]

    async def find_one_user(
        self, find_data: Union[FindOneOptions, str], db_session: Session
    ) -> Optional[UserDto]:
        user = await self.user_repository.find_one_or_fail(find_data, db_session)

        return UserDto(**user.__dict__)

    async def delete_user(self, user_id: str, db_session: Session) -> Optional[UpdateResult]:
        return await self.user_repository.soft_delete(user_id, db_session)

    async def update_user(
        self, user_id: str, update_user_dto: UpdateUserDto, db_session: Session
    ) -> Optional[UpdateResult]:
        if update_user_dto.email:
            user = await self.__verify_email_exist(update_user_dto.email, db_session)

            if user:
                raise BadRequestException(f"Email already in use.", ["User", "email"])

        return await self.user_repository.update(user_id, update_user_dto, db_session)

    # ---------------------- INTERFACE METHODS ----------------------
    async def get_one_user(
        self, find_data: Union[FindOneOptions, str], db_session: Session
    ) -> Optional[UserDto]:
        user = await self.user_repository.find_one_or_fail(find_data, db_session)

        return user

    async def update_last_access(
        self, user_id: Union[str, UUID], db_session: Session
    ) -> Optional[UpdateResult]:
        return await self.user_repository.update(
            user_id, {"last_access": datetime.now()}, db_session
        )

    # ---------------------- PRIVATE METHODS ----------------------
    async def __verify_email_exist(self, email: str, db_session: Session) -> Optional[User]:
        return await self.user_repository.find_one({"where": User.email == email}, db_session)
