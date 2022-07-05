from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.common.dto.pagination_response_dto import PaginationResponseDto
from src.core.constants.enum.user_role import UserRole
from src.core.decorators.http_decorator import Auth
from src.core.decorators.pagination_decorator import GetPagination
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.personal_data.dto.activity_level.activity_level_dto import ActivityLevelDto
from src.modules.domain.personal_data.dto.activity_level.activity_level_query_dto import (FindAllActivityLevelQueryDto,
                                                                                          OrderByActivityLevelQueryDto)
from src.modules.domain.personal_data.dto.activity_level.create_activity_level_dto import CreateActivityLevelDto
from src.modules.domain.personal_data.dto.activity_level.update_activity_level_dto import UpdateActivityLevelDto
from src.modules.domain.personal_data.entities.activity_level import ActivityLevel
from src.modules.domain.personal_data.services.activity_level_service import ActivityLevelService
from src.modules.infrastructure.database import get_db

activity_level_router = APIRouter(tags=["Activity Level"], prefix="/activity-level")

activity_level_service = ActivityLevelService()


@activity_level_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=ActivityLevelDto,
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def create_activity_level(
    request: CreateActivityLevelDto, database: Session = Depends(get_db)
) -> Optional[ActivityLevelDto]:
    return await activity_level_service.create_activity_level(request, database)


@activity_level_router.get(
    "/get",
    response_model=PaginationResponseDto[ActivityLevelDto],
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def get_all_activity_level_paginated(
    pagination: FindManyOptions = Depends(
        GetPagination(
            ActivityLevel, FindAllActivityLevelQueryDto, OrderByActivityLevelQueryDto
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[ActivityLevelDto]]:
    return await activity_level_service.get_all_activity_level_paginated(
        pagination, database
    )


@activity_level_router.get(
    "/get/{id}",
    response_model=ActivityLevelDto,
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def get_activity_level_by_id(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[ActivityLevelDto]:
    return await activity_level_service.find_one_activity_level(str(id), database)


@activity_level_router.patch(
    "/update/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def update_activity_level(
    request: UpdateActivityLevelDto, id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await activity_level_service.update_activity_level(str(id), request, database)


@activity_level_router.delete(
    "/delete/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def delete_activity_level(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await activity_level_service.delete_activity_level(str(id), database)
