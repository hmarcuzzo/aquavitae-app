from datetime import date
from typing import List, Optional, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.exceptions_type import BadRequestException
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
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

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_anthropometric_data(
        self, anthropometric_data_dto: CreateAnthropometricDataDto, db: Session
    ) -> Optional[AnthropometricDataDto]:
        anthropometric_data_dto = self.__verify_date_and_values(anthropometric_data_dto)

        new_anthropometric_data = await self.anthropometric_data_repository.create(
            anthropometric_data_dto, db
        )

        new_anthropometric_data = await self.anthropometric_data_repository.save(
            new_anthropometric_data, db
        )
        return AnthropometricDataDto(**new_anthropometric_data.__dict__)

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
        pagination["relations"] = ["user"]

        [
            all_user_anthropometric_data,
            total,
        ] = await self.anthropometric_data_repository.find_and_count(
            pagination,
            db,
        )

        return create_pagination_response_dto(
            [
                AnthropometricDataDto(**anthropometric_data.__dict__)
                for anthropometric_data in all_user_anthropometric_data
            ],
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
        return await self.anthropometric_data_repository.update(
            {"where": AnthropometricData.id == anthropometric_data_id},
            update_anthropometric_data_dto,
            db,
        )

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
