from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.constants.enum.user_role import UserRole
from src.core.decorators.http_decorator import Auth
from src.modules.domain.item.dto.item.create_item_dto import CreateItemDto
from src.modules.domain.item.dto.item.item_dto import ItemDto
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
