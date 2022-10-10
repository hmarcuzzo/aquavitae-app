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
from src.modules.domain.antecedent.services.antecedent_type_service import AntecedentTypeService
from src.modules.domain.food.dto.food.create_food_dto import CreateFoodDto
from src.modules.domain.food.dto.food.food_dto import FoodDto
from src.modules.domain.food.dto.food.food_query_dto import (
    FindAllFoodQueryDto,
    OrderByFoodQueryDto,
)
from src.modules.domain.food.dto.food.update_food_dto import UpdateFoodDto
from src.modules.domain.food.entities.food_entity import Food
from src.modules.domain.food.services.food_service import FoodService
from src.modules.infrastructure.database import get_db

antecedent_type_router = APIRouter(tags=["Antecedent Type"], prefix="/antecedent-type")

antecedent_type_service = AntecedentTypeService()
