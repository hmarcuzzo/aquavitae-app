from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.core.types.update_result_type import UpdateResult
from src.modules.domain.personal_data.dto.personal_data.create_personal_data_dto import (
    CreatePersonalDataDto,
)
from src.modules.domain.personal_data.dto.personal_data.personal_data_dto import PersonalDataDto
from src.modules.domain.personal_data.dto.personal_data.update_personal_data_dto import (
    UpdatePersonalDataDto,
)
from src.modules.domain.personal_data.entities.personal_data_entity import PersonalData
from src.modules.domain.personal_data.repositories.personal_data_repository import (
    PersonalDataRepository,
)


class PersonalDataService:
    def __init__(self):
        self.personal_data_repository = PersonalDataRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_personal_data(
        self, personal_data_dto: CreatePersonalDataDto, db: Session
    ) -> Optional[PersonalDataDto]:
        new_personal_data = await self.personal_data_repository.create(personal_data_dto, db)

        new_personal_data = await self.personal_data_repository.save(new_personal_data, db)
        return PersonalDataDto(**new_personal_data.__dict__)

    async def find_one_personal_data(self, user_id: str, db: Session) -> Optional[PersonalDataDto]:
        response = await self.find_several_personal_data_by_id([user_id], db)
        return response[0] if response else None

    async def find_several_personal_data_by_id(
        self, users_id: List[str], db: Session
    ) -> Optional[List[PersonalDataDto]]:
        users_personal_data = await self.personal_data_repository.find(
            {
                "where": or_(*[PersonalData.user_id == user_id for user_id in users_id]),
                "relations": ["activity_level", "user"],
            },
            db,
        )

        return [
            PersonalDataDto(**user_personal_data.__dict__)
            for user_personal_data in users_personal_data
        ]

    async def update_personal_data(
        self,
        user_id: str,
        update_personal_data_dto: UpdatePersonalDataDto,
        db: Session,
    ) -> Optional[UpdateResult]:
        return await self.personal_data_repository.update(
            {"where": PersonalData.user_id == user_id}, update_personal_data_dto, db
        )
