import os
import uuid
from copy import deepcopy
from datetime import date
from typing import Optional, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.exceptions_type import BadRequestException
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.core.utils.image_utils import ImageUtils
from src.modules.domain.anthropometric_data.dto.anthropometric_data_dto import AnthropometricDataDto
from src.modules.domain.anthropometric_data.dto.create_anthropometric_data_dto import (
    CreateAnthropometricDataDto,
)
from src.modules.domain.anthropometric_data.dto.update_anthropometric_data_dto import (
    UpdateAnthropometricDataDto,
    UserUpdateAnthropometricDataDto,
)
from src.modules.domain.anthropometric_data.entities.anthropometric_data_entity import (
    AnthropometricData,
)
from src.modules.domain.anthropometric_data.repositories.anthropometric_data_repository import (
    AnthropometricDataRepository,
)


class AnthropometricDataService:
    def __init__(self):
        self.anthropometric_data_repository = AnthropometricDataRepository()
        self.image_utils = ImageUtils("/src/static/images/body_photo")

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_anthropometric_data(
        self, anthropometric_data_dto: CreateAnthropometricDataDto, db: Session
    ) -> Optional[AnthropometricDataDto]:
        anthropometric_data_dto = self.__verify_date_and_values(anthropometric_data_dto)

        filename = None
        try:
            db.begin_nested()

            image = self.image_utils.valid_image64(anthropometric_data_dto.body_photo)
            delattr(anthropometric_data_dto, "body_photo")

            new_anthropometric_data = AnthropometricData(
                **anthropometric_data_dto.dict(exclude_unset=True)
            )
            new_anthropometric_data.id = uuid.uuid4()

            filename = new_anthropometric_data.body_photo = self.image_utils.save_image(
                str(new_anthropometric_data.id), image
            )

            new_anthropometric_data = await self.anthropometric_data_repository.create(
                new_anthropometric_data, db
            )
            new_anthropometric_data = await self.anthropometric_data_repository.save(
                new_anthropometric_data, db
            )

            new_anthropometric_data_dto = deepcopy(new_anthropometric_data)
            new_anthropometric_data_dto.body_photo = self.image_utils.get_image(
                new_anthropometric_data.body_photo
            )
            response = AnthropometricDataDto(**new_anthropometric_data_dto.__dict__)

            db.commit()
            return response
        except Exception as e:
            self.image_utils.delete_image(filename)
            db.rollback()
            raise e

    async def get_user_newest_anthropometric_data(
        self, user_id: str, db: Session
    ) -> Optional[AnthropometricDataDto]:
        newest_anthropometric_data = await self.anthropometric_data_repository.find(
            {
                "where": AnthropometricData.user_id == user_id,
                "order_by": desc(AnthropometricData.date),
                "relations": ["user"],
            },
            db,
        )
        if len(newest_anthropometric_data) == 0:
            raise BadRequestException("User has no anthropometric data")

        return AnthropometricDataDto(**newest_anthropometric_data[0].__dict__)

    async def get_all_user_anthropometric_data(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[AnthropometricDataDto]]:
        [
            all_user_anthropometric_data,
            total,
        ] = await self.anthropometric_data_repository.find_and_count(
            pagination,
            db,
        )

        all_anthropometric_data_dto = []
        for anthropometric_data in all_user_anthropometric_data:
            if "body_photo" in pagination["select"]:
                anthropometric_data.body_photo = self.image_utils.get_image(
                    anthropometric_data.body_photo
                )
            all_anthropometric_data_dto.append(
                AnthropometricDataDto(**anthropometric_data.__dict__)
            )

        return create_pagination_response_dto(
            all_anthropometric_data_dto,
            total,
            pagination["skip"],
            pagination["take"],
        )

    async def get_anthropometric_data_by_id(
        self, anthropometric_data_id: str, db: Session
    ) -> Optional[AnthropometricDataDto]:
        anthropometric_data = await self.anthropometric_data_repository.find_one_or_fail(
            {
                "where": AnthropometricData.id == anthropometric_data_id,
                "relations": ["user"],
            },
            db,
        )

        anthropometric_data.body_photo = self.image_utils.get_image(anthropometric_data.body_photo)
        return AnthropometricDataDto(**anthropometric_data.__dict__)

    async def user_update_anthropometric_data(
        self,
        user_id: str,
        update_anthropometric_data_dto: Union[
            UpdateAnthropometricDataDto, UserUpdateAnthropometricDataDto
        ],
        db: Session,
    ) -> Optional[UpdateResult]:
        last_data = await self.get_user_newest_anthropometric_data(user_id, db)
        return await self.update_anthropometric_data(
            str(last_data.id), update_anthropometric_data_dto, db
        )

    async def update_anthropometric_data(
        self,
        anthropometric_data_id: str,
        update_anthropometric_data_dto: Union[
            UpdateAnthropometricDataDto, UserUpdateAnthropometricDataDto
        ],
        db: Session,
    ) -> Optional[UpdateResult]:
        update_anthropometric_data_dto = self.__verify_values(update_anthropometric_data_dto)

        try:
            db.begin_nested()

            if isinstance(update_anthropometric_data_dto, UpdateAnthropometricDataDto):
                if "body_photo" in update_anthropometric_data_dto.dict(exclude_unset=True):
                    image = self.image_utils.valid_image64(
                        update_anthropometric_data_dto.body_photo
                    )
                delattr(update_anthropometric_data_dto, "body_photo")

                anthropometric_data = await self.anthropometric_data_repository.find_one_or_fail(
                    anthropometric_data_id, db
                )
                if "image" in locals():
                    if image:
                        anthropometric_data.body_photo = self.image_utils.save_image(
                            str(anthropometric_data.id), image
                        )
                        update_anthropometric_data_dto.body_photo = (
                            f"{anthropometric_data.id}.{image['format']}"
                        )
                    else:
                        self.image_utils.delete_image(str(anthropometric_data.body_photo))
                        update_anthropometric_data_dto.body_photo = None

            response = await self.anthropometric_data_repository.update(
                anthropometric_data_id, update_anthropometric_data_dto, db
            )
            db.commit()
            return response
        except Exception as e:
            db.rollback()
            raise e

    async def delete_anthropometric_data(
        self, anthropometric_data_id: str, db: Session
    ) -> Optional[UpdateResult]:
        return await self.anthropometric_data_repository.soft_delete(anthropometric_data_id, db)

    # ---------------------- PRIVATE METHODS ----------------------
    def __verify_date_and_values(
        self,
        anthropometric_data_dto: Union[CreateAnthropometricDataDto, UpdateAnthropometricDataDto],
    ) -> Union[CreateAnthropometricDataDto, UpdateAnthropometricDataDto]:
        if anthropometric_data_dto.date is None:
            anthropometric_data_dto.date = date.today()

        return self.__verify_values(anthropometric_data_dto)

    @staticmethod
    def __verify_values(
        anthropometric_data_dto: Union[CreateAnthropometricDataDto, UpdateAnthropometricDataDto],
    ) -> Union[CreateAnthropometricDataDto, UpdateAnthropometricDataDto]:
        for key in [
            "weight",
            "height",
            "waist_circumference",
            "fat_mass",
            "muscle_mass",
            "bone_mass",
            "body_water",
            "basal_metabolism",
            "visceral_fat",
        ]:
            if (
                key in anthropometric_data_dto.__dict__
                and anthropometric_data_dto.__dict__[key] is not None
                and anthropometric_data_dto.__dict__[key] < 0
            ):
                raise BadRequestException(f"{key} must be greater than or equal to 0")

        if (
            "date" in anthropometric_data_dto.__dict__
            and anthropometric_data_dto.date is not None
            and anthropometric_data_dto.date > date.today()
        ):
            raise BadRequestException("Date must be less than or equal to today")

        return anthropometric_data_dto
