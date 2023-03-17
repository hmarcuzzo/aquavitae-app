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
from src.modules.domain.item.dto.item.create_item_dto import CreateItemDto
from src.modules.domain.item.dto.item.item_dto import ItemDto
from src.modules.domain.item.dto.item.item_query_dto import FindAllItemQueryDto, OrderByItemQueryDto
from src.modules.domain.item.dto.item.update_item_dto import UpdateItemDto
from src.modules.domain.item.entities.item_entity import Item
from src.modules.domain.item.services.item_service import ItemService
from src.modules.infrastructure.database import get_db

item_router = APIRouter(tags=["Item"], prefix="/item")

item_service = ItemService()


@item_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=ItemDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_item(
    request: CreateItemDto, database: Session = Depends(get_db)
) -> Optional[ItemDto]:
    return await item_service.create_item(request, database)


@item_router.get(
    "/get",
    response_model=PaginationResponseDto[ItemDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_item_paginated(
    pagination: FindManyOptions = Depends(
        GetPagination(Item, ItemDto, FindAllItemQueryDto, OrderByItemQueryDto)
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[ItemDto]]:
    return await item_service.get_all_item_paginated(pagination, database)


@item_router.get(
    "/get/{id}",
    response_model=ItemDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_item_by_id(id: UUID, database: Session = Depends(get_db)) -> Optional[ItemDto]:
    return await item_service.find_one_item(str(id), database)


@item_router.delete(
    "/delete/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_item(id: UUID, database: Session = Depends(get_db)) -> Optional[UpdateResult]:
    return await item_service.delete_item(str(id), database)


@item_router.patch(
    "/update/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_item(
    request: UpdateItemDto, id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await item_service.update_item(str(id), request, database)
