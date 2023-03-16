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
from src.modules.domain.meal.dto.type_of_meal.create_type_of_meal_dto import CreateTypeOfMealDto
from src.modules.domain.meal.dto.type_of_meal.type_of_meal_dto import TypeOfMealDto
from src.modules.domain.meal.dto.type_of_meal.type_of_meal_query_dto import (
    FindAllTypeOfMealQueryDto,
    OrderByTypeOfMealQueryDto,
)
from src.modules.domain.meal.dto.type_of_meal.update_type_of_meal_dto import UpdateTypeOfMealDto
from src.modules.domain.meal.entities.type_of_meal_entity import TypeOfMeal
from src.modules.domain.meal.services.type_of_meal_service import TypeOfMealService
from src.modules.infrastructure.database import get_db

type_of_meal_router = APIRouter(tags=["Type of Meal"], prefix="/type-of-meal")

type_of_meal_service = TypeOfMealService()


@type_of_meal_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=TypeOfMealDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_type_of_meal(
    request: CreateTypeOfMealDto, database: Session = Depends(get_db)
) -> Optional[TypeOfMealDto]:
    return await type_of_meal_service.create_type_of_meal(request, database)


@type_of_meal_router.get(
    "/get/{id}",
    response_model=TypeOfMealDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_type_of_meal_by_id(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[TypeOfMealDto]:
    return await type_of_meal_service.find_one_type_of_meal(str(id), database)


@type_of_meal_router.delete(
    "/delete/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_type_of_meal(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await type_of_meal_service.delete_type_of_meal(str(id), database)


@type_of_meal_router.patch(
    "/update/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_type_of_meal(
    request: UpdateTypeOfMealDto, id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await type_of_meal_service.update_type_of_meal(str(id), request, database)


@type_of_meal_router.get(
    "/get",
    response_model=PaginationResponseDto[TypeOfMealDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_type_of_meal_paginated(
    pagination: FindManyOptions = Depends(
        GetPagination(
            TypeOfMeal, TypeOfMealDto, FindAllTypeOfMealQueryDto, OrderByTypeOfMealQueryDto
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[TypeOfMealDto]]:
    return await type_of_meal_service.get_all_type_of_meal_paginated(pagination, database)
