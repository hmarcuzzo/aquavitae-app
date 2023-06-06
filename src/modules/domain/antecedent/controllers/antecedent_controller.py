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
from src.modules.domain.antecedent.dto.antecedent.antecedent_dto import AntecedentDto
from src.modules.domain.antecedent.dto.antecedent.antecedent_query_dto import (
    FindAllAntecedentQueryDto,
    OrderByAntecedentQueryDto,
)
from src.modules.domain.antecedent.dto.antecedent.create_antecedent import CreateAntecedentDto
from src.modules.domain.antecedent.dto.antecedent.update_antecedent_dto import UpdateAntecedentDto
from src.modules.domain.antecedent.entities.antecedent_entity import Antecedent
from src.modules.domain.antecedent.services.antecedent_service import AntecedentService
from src.modules.infrastructure.database import get_db

antecedent_router = APIRouter(tags=["Antecedent"], prefix="/antecedent")

antecedent_service = AntecedentService()


@antecedent_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=AntecedentDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_type_of_meal(
    request: CreateAntecedentDto, database: Session = Depends(get_db)
) -> Optional[AntecedentDto]:
    return await antecedent_service.create_antecedent(request, database)


@antecedent_router.get(
    "/get/{id}",
    response_model=AntecedentDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_type_of_meal_by_id(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[AntecedentDto]:
    return await antecedent_service.find_one_antecedent(str(id), database)


@antecedent_router.delete(
    "/delete/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_type_of_meal(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await antecedent_service.delete_antecedent(str(id), database)


@antecedent_router.patch(
    "/update/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_type_of_meal(
    request: UpdateAntecedentDto, id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await antecedent_service.update_antecedent(str(id), request, database)


@antecedent_router.get(
    "/get",
    response_model=PaginationResponseDto[AntecedentDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_type_of_meal_paginated(
    pagination: FindManyOptions = Depends(
        GetPagination(
            Antecedent,
            AntecedentDto,
            FindAllAntecedentQueryDto,
            OrderByAntecedentQueryDto,
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[AntecedentDto]]:
    return await antecedent_service.get_all_antecedent_paginated(pagination, database)
