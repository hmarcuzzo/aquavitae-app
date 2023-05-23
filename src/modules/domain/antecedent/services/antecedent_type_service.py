from typing import Optional

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.antecedent.dto.antecedent_type.antecedent_type_dto import AntecedentTypeDto
from src.modules.domain.antecedent.dto.antecedent_type.create_antecedent_type_dto import (
    CreateAntecedentTypeDto,
)
from src.modules.domain.antecedent.dto.antecedent_type.update_antecedent_type_dto import (
    UpdateAntecedentTypeDto,
)
from src.modules.domain.antecedent.entities.antecedent_type_entity import AntecedentType
from src.modules.domain.antecedent.repositories.antecedent_type_repository import (
    AntecedentTypeRepository,
)


class AntecedentTypeService:
    def __init__(self):
        self.antecedent_type_repository = AntecedentTypeRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_antecedent_type(
        self, antecedent_type_dto: CreateAntecedentTypeDto, db: Session
    ) -> Optional[AntecedentTypeDto]:
        new_antecedent_type = await self.antecedent_type_repository.create(antecedent_type_dto, db)

        new_antecedent_type = self.antecedent_type_repository.save(new_antecedent_type, db)
        return AntecedentTypeDto.from_orm(new_antecedent_type)

    async def find_one_antecedent_type(self, id: str, db: Session) -> Optional[AntecedentTypeDto]:
        antecedent_type = await self.antecedent_type_repository.find_one_or_fail(
            {"where": AntecedentType.id == id}, db
        )

        return AntecedentTypeDto.from_orm(antecedent_type)

    async def delete_antecedent_type(self, id: str, db: Session) -> Optional[UpdateResult]:
        return await self.antecedent_type_repository.soft_delete(id, db)

    async def update_antecedent_type(
        self, id: str, update_antecedent_type_dto: UpdateAntecedentTypeDto, db: Session
    ) -> Optional[UpdateResult]:
        return await self.antecedent_type_repository.update(id, update_antecedent_type_dto, db)

    async def get_all_antecedent_type_paginated(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[AntecedentTypeDto]]:
        [all_antecedent_type, total] = await self.antecedent_type_repository.find_and_count(
            pagination, db
        )

        return create_pagination_response_dto(
            [
                AntecedentTypeDto.from_orm(antecedent_type)
                for antecedent_type in all_antecedent_type
            ],
            total,
            pagination["skip"],
            pagination["take"],
        )
