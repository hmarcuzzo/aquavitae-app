from typing import Optional

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.antecedent.dto.antecedent.antecedent_dto import AntecedentDto
from src.modules.domain.antecedent.dto.antecedent.create_antecedent import CreateAntecedentDto
from src.modules.domain.antecedent.dto.antecedent.update_antecedent_dto import UpdateAntecedentDto
from src.modules.domain.antecedent.entities.antecedent_entity import Antecedent
from src.modules.domain.antecedent.repositories.antecedent_repository import AntecedentRepository


class AntecedentService:
    def __init__(self):
        self.antecedent_repository = AntecedentRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_antecedent(
        self, antecedent_type_dto: CreateAntecedentDto, db: Session
    ) -> Optional[AntecedentDto]:
        new_antecedent = await self.antecedent_repository.create(antecedent_type_dto, db)

        new_antecedent = self.antecedent_repository.save(new_antecedent, db)
        return AntecedentDto.from_orm(new_antecedent)

    async def find_one_antecedent(self, id: str, db: Session) -> Optional[AntecedentDto]:
        antecedent = await self.antecedent_repository.find_one_or_fail(
            {"where": Antecedent.id == id}, db
        )

        return AntecedentDto.from_orm(antecedent)

    async def delete_antecedent(self, id: str, db: Session) -> Optional[UpdateResult]:
        return await self.antecedent_repository.soft_delete(id, db)

    async def update_antecedent(
        self, id: str, update_antecedent_dto: UpdateAntecedentDto, db: Session
    ) -> Optional[UpdateResult]:
        return await self.antecedent_repository.update(id, update_antecedent_dto, db)

    async def get_all_antecedent_paginated(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[AntecedentDto]]:
        [all_antecedent, total] = await self.antecedent_repository.find_and_count(pagination, db)

        return create_pagination_response_dto(
            [AntecedentDto.from_orm(antecedent) for antecedent in all_antecedent],
            total,
            pagination["skip"],
            pagination["take"],
        )
