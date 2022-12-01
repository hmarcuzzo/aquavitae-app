import uuid
from copy import deepcopy
from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.exceptions_type import BadRequestException
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.find_one_options_type import FindOneOptions
from src.core.types.update_result_type import UpdateResult
from src.core.utils.image_utils import ImageUtils
from .dto.create_user_dto import CreateUserDto, CreateUserWithRoleDto
from .dto.update_user_dto import UpdateUserDto
from .dto.user_dto import UserDto
from .entities.user_entity import User
from .user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.image_utils = ImageUtils("/src/static/images/profile_photo")

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_user(
        self, user_dto: Union[CreateUserDto, CreateUserWithRoleDto], db_session: Session
    ) -> Optional[UserDto]:
        user = await self.__verify_email_exist(user_dto.email, db_session)

        if user:
            raise BadRequestException(f"Email already in use.", ["User", "email"])

        filename = None
        try:
            db_session.begin_nested()

            image = self.image_utils.valid_image64(user_dto.profile_photo)
            delattr(user_dto, "profile_photo")

            new_user = User(**user_dto.dict(exclude_unset=True))
            new_user.id = uuid.uuid4()

            filename = new_user.profile_photo = self.image_utils.save_image(str(new_user.id), image)

            new_user = await self.user_repository.create(new_user, db_session)
            new_user = await self.user_repository.save(new_user, db_session)

            new_user_dto = deepcopy(new_user)
            new_user_dto.profile_photo = self.image_utils.get_image(new_user.profile_photo)
            response = UserDto(**new_user_dto.__dict__)

            db_session.commit()
            return response
        except Exception as e:
            self.image_utils.delete_image(filename)
            db_session.rollback()
            raise e

    async def get_all_users(
        self, pagination: FindManyOptions, db_session: Session
    ) -> Optional[PaginationResponseDto[UserDto]]:
        [all_users, total] = await self.user_repository.find_and_count(
            pagination,
            db_session,
        )

        users_dto = []
        for user in all_users:
            if "profile_photo" in pagination["select"]:
                user.profile_photo = self.image_utils.get_image(user.profile_photo)
            users_dto.append(UserDto(**user.__dict__))

        return create_pagination_response_dto(
            users_dto,
            total,
            pagination["skip"],
            pagination["take"],
        )

    async def find_one_user(
        self, find_data: Union[FindOneOptions, str], db_session: Session
    ) -> Optional[UserDto]:
        user = await self.user_repository.find_one_or_fail(find_data, db_session)

        user.profile_photo = self.image_utils.get_image(user.profile_photo)
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

        try:
            db_session.begin_nested()

            if "profile_photo" in update_user_dto.dict(exclude_unset=True):
                image = self.image_utils.valid_image64(update_user_dto.profile_photo)
            delattr(update_user_dto, "profile_photo")

            user = await self.user_repository.find_one_or_fail(user_id, db_session)
            if "image" in locals():
                if image:
                    user.profile_photo = self.image_utils.save_image(str(user.id), image)
                    update_user_dto.profile_photo = f"{user.id}.{image[1]}"
                else:
                    self.image_utils.delete_image(str(user.profile_photo))
                    update_user_dto.profile_photo = None

            response = await self.user_repository.update(user_id, update_user_dto, db_session)
            db_session.commit()
            return response
        except Exception as e:
            db_session.rollback()
            raise e

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
