from typing import Optional

from sqlalchemy.orm import Session

from src.core.types.update_result_type import UpdateResult
from src.modules.domain.personal_data.dto.personal_data.personal_data_dto import PersonalDataDto
from src.modules.domain.personal_data.dto.personal_data.update_personal_data_dto import (
    UpdatePersonalDataDto,
)
from src.modules.domain.personal_data.entities.personal_data import PersonalData
from src.modules.domain.personal_data.repositories.personal_data_repository import (
    PersonalDataRepository,
)


class PersonalDataService:
    def __init__(self):
        self.personal_data_repository = PersonalDataRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def find_one_personal_data(
        self, personal_data_user_id: str, db: Session
    ) -> Optional[PersonalDataDto]:
        personal_data = await self.personal_data_repository.find_one_or_fail(
            {
                "where": PersonalData.user_id == personal_data_user_id,
                "relations": ["activity_level", "user"],
            },
            db,
        )

        return PersonalDataDto(**personal_data.__dict__)

    async def update_personal_data(
        self,
        personal_data_user_id: str,
        update_personal_data_dto: UpdatePersonalDataDto,
        db: Session,
    ) -> Optional[UpdateResult]:
        return await self.personal_data_repository.update(
            {"where": PersonalData.user_id == personal_data_user_id}, update_personal_data_dto, db
        )
