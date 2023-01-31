from typing import Optional

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.personal_data.dto.activity_level.activity_level_dto import ActivityLevelDto
from src.modules.domain.personal_data.dto.activity_level.create_activity_level_dto import (
    CreateActivityLevelDto,
)
from src.modules.domain.personal_data.dto.activity_level.update_activity_level_dto import (
    UpdateActivityLevelDto,
)
from src.modules.domain.personal_data.entities.activity_level_entity import ActivityLevel
from src.modules.domain.personal_data.repositories.activity_level_repository import (
    ActivityLevelRepository,
)


class ActivityLevelService:
    def __init__(self):
        self.activity_level_repository = ActivityLevelRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_activity_level(
        self, activity_level_dto: CreateActivityLevelDto, db: Session
    ) -> Optional[ActivityLevelDto]:
        new_activity_level = await self.activity_level_repository.create(activity_level_dto, db)

        new_activity_level = self.activity_level_repository.save(new_activity_level, db)
        return ActivityLevelDto(**new_activity_level.__dict__)

    async def get_all_activity_level_paginated(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[ActivityLevelDto]]:
        [
            all_activity_levels,
            total,
        ] = await self.activity_level_repository.find_and_count(pagination, db)

        return create_pagination_response_dto(
            [ActivityLevelDto(**activity_level.__dict__) for activity_level in all_activity_levels],
            total,
            pagination["skip"],
            pagination["take"],
        )

    async def find_one_activity_level(
        self, activity_level_id: str, db: Session
    ) -> Optional[ActivityLevelDto]:
        activity_level = await self.activity_level_repository.find_one_or_fail(
            {
                "where": ActivityLevel.id == activity_level_id,
            },
            db,
        )

        return ActivityLevelDto(**activity_level.__dict__)

    async def update_activity_level(
        self, id: str, update_activity_level_dto: UpdateActivityLevelDto, db: Session
    ) -> Optional[UpdateResult]:
        return await self.activity_level_repository.update(id, update_activity_level_dto, db)

    async def delete_activity_level(
        self, activity_level_id: str, db: Session
    ) -> Optional[UpdateResult]:
        return await self.activity_level_repository.soft_delete(activity_level_id, db)
