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
from src.modules.domain.food.dto.food_category.create_food_category_dto import (
    CreateFoodCategoryDto,
)
from src.modules.domain.food.dto.food_category.food_category_dto import FoodCategoryDto
from src.modules.domain.food.dto.food_category.food_category_query_dto import (
    FindAllFoodCategoryQueryDto,
    OrderByFoodCategoryQueryDto,
)
from src.modules.domain.food.dto.food_category.update_food_category_dto import (
    UpdateFoodCategoryDto,
)
from src.modules.domain.food.entities.food_category_entity import FoodCategory
from src.modules.domain.food.services.food_category_service import FoodCategoryService
from src.modules.infrastructure.database import get_db

food_category_router = APIRouter(tags=["Food Category"], prefix="/food-category")

food_category_service = FoodCategoryService()


@food_category_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=FoodCategoryDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_food_categy(
    request: CreateFoodCategoryDto, database: Session = Depends(get_db)
) -> Optional[FoodCategoryDto]:
    return await food_category_service.create_food_category(request, database)


@food_category_router.get(
    "/get",
    response_model=PaginationResponseDto[FoodCategoryDto],
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_food_category_paginated(
    pagination: FindManyOptions = Depends(
        GetPagination(FoodCategory, FindAllFoodCategoryQueryDto, OrderByFoodCategoryQueryDto)
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[FoodCategoryDto]]:
    return await food_category_service.get_all_food_category_paginated(pagination, database)


@food_category_router.get(
    "/get/{id}",
    response_model=FoodCategoryDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_food_category_by_id(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[FoodCategoryDto]:
    return await food_category_service.find_one_food_category(str(id), database)


@food_category_router.patch(
    "/update/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_food_category(
    request: UpdateFoodCategoryDto, id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await food_category_service.update_food_category(str(id), request, database)


@food_category_router.delete(
    "/delete/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_food_category(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await food_category_service.delete_food_category(str(id), database)
