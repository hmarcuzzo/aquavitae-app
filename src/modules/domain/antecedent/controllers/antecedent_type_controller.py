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
from src.modules.domain.antecedent.dto.antecedent_type.antecedent_type_dto import AntecedentTypeDto
from src.modules.domain.antecedent.dto.antecedent_type.antecedent_type_query_dto import (
    FindAllAntecedentTypeQueryDto,
    OrderByAntecedentTypeQueryDto,
)
from src.modules.domain.antecedent.dto.antecedent_type.create_antecedent_type_dto import (
    CreateAntecedentTypeDto,
)
from src.modules.domain.antecedent.dto.antecedent_type.update_antecedent_type_dto import (
    UpdateAntecedentTypeDto,
)
from src.modules.domain.antecedent.entities.antecedent_type_entity import AntecedentType
from src.modules.domain.antecedent.services.antecedent_type_service import AntecedentTypeService
from src.modules.infrastructure.database import get_db

antecedent_type_router = APIRouter(tags=["Antecedent Type"], prefix="/antecedent-type")

antecedent_type_service = AntecedentTypeService()


@antecedent_type_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=AntecedentTypeDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_type_of_meal(
    request: CreateAntecedentTypeDto, database: Session = Depends(get_db)
) -> Optional[AntecedentTypeDto]:
    return await antecedent_type_service.create_antecedent_type(request, database)


@antecedent_type_router.get(
    "/get/{id}",
    response_model=AntecedentTypeDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_type_of_meal_by_id(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[AntecedentTypeDto]:
    return await antecedent_type_service.find_one_antecedent_type(str(id), database)


@antecedent_type_router.delete(
    "/delete/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_type_of_meal(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await antecedent_type_service.delete_antecedent_type(str(id), database)


@antecedent_type_router.patch(
    "/update/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_type_of_meal(
    request: UpdateAntecedentTypeDto, id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await antecedent_type_service.update_antecedent_type(str(id), request, database)


@antecedent_type_router.get(
    "/get",
    response_model=PaginationResponseDto[AntecedentTypeDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_type_of_meal_paginated(
    pagination: FindManyOptions = Depends(
        GetPagination(
            AntecedentType,
            AntecedentTypeDto,
            FindAllAntecedentTypeQueryDto,
            OrderByAntecedentTypeQueryDto,
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[AntecedentTypeDto]]:
    return await antecedent_type_service.get_all_antecedent_type_paginated(pagination, database)
