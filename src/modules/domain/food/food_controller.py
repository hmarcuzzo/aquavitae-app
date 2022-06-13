from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import PaginationResponseDto
from src.core.constants.enum.user_role import UserRole
from src.core.decorators.http_decorator import Auth
from src.core.decorators.pagination_decorator import GetPagination
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.food.dto.create_food_dto import CreateFoodDto
from src.modules.domain.food.dto.food_dto import FoodDto
from src.modules.domain.food.dto.food_query_dto import (
    FindAllFoodQueryDto,
    OrderByFoodQueryDto,
)
from src.modules.domain.food.dto.update_food_dto import UpdateFoodDto
from src.modules.domain.food.entities.food_entity import Food
from src.modules.domain.food.food_service import FoodService
from src.modules.infrastructure.database import get_db

food_router = APIRouter(tags=["Food"], prefix="/food")

food_service = FoodService()


@food_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=FoodDto,
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def create_food(
    request: CreateFoodDto, database: Session = Depends(get_db)
) -> Optional[FoodDto]:
    return await food_service.create_food(request, database)


@food_router.get(
    "/get",
    response_model=PaginationResponseDto[FoodDto],
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def get_all_food_paginated(
    pagination: FindManyOptions = Depends(
        GetPagination(Food, FindAllFoodQueryDto, OrderByFoodQueryDto)
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[FoodDto]]:
    return await food_service.get_all_food_paginated(pagination, database)


@food_router.get(
    "/get/{id}", response_model=FoodDto, dependencies=[Depends(Auth([UserRole.ADMIN]))]
)
async def get_food_by_id(
    id: str, database: Session = Depends(get_db)
) -> Optional[FoodDto]:
    return await food_service.find_one_food(id, database)


@food_router.delete(
    "/delete/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def delete_food(
    id: str, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await food_service.delete_food(id, database)


@food_router.patch(
    "/update/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def update_food(
    request: UpdateFoodDto, id: str, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await food_service.update_food(id, request, database)
